"""Clean modern GUI using pure tkinter (no CustomTkinter)."""

from __future__ import annotations

import math
import queue
import random
import threading
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from typing import Callable, Optional

from app_core import format_result_filename, format_t_detail
from database import ResultDatabase, SavedResult
from solver import CoveringDesignSolver, SolverProgress, SolverResult, elements_to_mask

DEFAULT_TIME_BUDGET_SEC = 120.0
UI_FONT = "Helvetica"
MONO_FONT = "Menlo"

class CleanModernApp:
    """Modern application using pure tkinter with clean design."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Optimal Samples Selection System")
        self.root.geometry("1080x820")
        self.root.minsize(920, 700)
        
        self.colors = {
            'bg': '#f7f7f5',
            'card_bg': '#ffffff',
            'panel': '#fbfbfa',
            'field_bg': '#f4f4f2',
            'primary': '#202123',
            'primary_hover': '#343541',
            'secondary': '#10a37f',
            'secondary_hover': '#0e8f70',
            'danger': '#d92d20',
            'danger_hover': '#b42318',
            'warning': '#b7791f',
            'warning_hover': '#9a6619',
            'neutral': '#eeeeeb',
            'neutral_hover': '#dededb',
            'text': '#202123',
            'text_light': '#6b7280',
            'text_subtle': '#9ca3af',
            'border': '#dededb',
            'border_strong': '#c9c9c5',
            'selection': '#e8f5ee',
        }
        
        self.root.configure(bg=self.colors['bg'])
        self.root.option_add("*Font", f"{UI_FONT} 12")
        self._configure_ttk_style()
        self._mousewheel_handlers: dict[str, Callable[[int], str | None]] = {}
        self._setup_mousewheel_dispatcher()
        self._main_layout_wide: bool | None = None
        self._main_layout_refresh_job: str | None = None

        self.db = ResultDatabase()
        self._q: queue.Queue[SolverProgress | SolverResult | str] = queue.Queue()
        self._thread: Optional[threading.Thread] = None
        self._cancel_flag = False
        self._time_budget_sec = DEFAULT_TIME_BUDGET_SEC
        self._run_started_at: float | None = None
        self._stop_reason = "idle"
        self._deadline_stop_requested = False

        self._current_result: Optional[SolverResult] = None
        self._current_samples: list[int] = []
        self._params: dict[str, int] = {}

        self._build_main_frame()
        self._build_db_frame()
        self.root.bind("<Configure>", self._on_root_configure, add="+")
        self._show_main()

        self.root.after(120, self._poll_queue)

    def run(self) -> None:
        self.root.mainloop()
    
    def _on_window_resize(self, event) -> None:
        """Handle window resize to adjust layout responsively."""
        if event.widget != self.root:
            return
        self._schedule_main_layout_refresh()
    
    def _update_layout(self) -> None:
        """Update the layout based on window width."""
        # Forget current packing
        self._main_left_col.pack_forget()
        self._main_right_col.pack_forget()
        
        if self._is_wide_layout:
            # Wide layout: two columns side by side (results on the right)
            self._main_left_col.pack(side="left", fill="both", expand=False)
            self._main_right_col.pack(side="left", fill="both", expand=True, padx=(10, 0))
        else:
            # Narrow layout: single column stacked (results below)
            self._main_left_col.pack(fill="x")
            self._main_right_col.pack(fill="both", expand=True)

    # ==================================================================
    # Screen switching
    # ==================================================================

    def _show_main(self) -> None:
        self._db_frame.pack_forget()
        self._main_frame.pack(fill="both", expand=True)

    def _show_db(self) -> None:
        self._main_frame.pack_forget()
        self._db_frame.pack(fill="both", expand=True)
        self._refresh_db_list()

    def _setup_mousewheel_dispatcher(self) -> None:
        self.root.bind_all("<MouseWheel>", self._dispatch_mousewheel, add="+")
        self.root.bind_all("<Button-4>", self._dispatch_mousewheel_linux_up, add="+")
        self.root.bind_all("<Button-5>", self._dispatch_mousewheel_linux_down, add="+")

    def _register_mousewheel_handler(
        self,
        widget: tk.Widget,
        handler: Callable[[int], str | None],
    ) -> None:
        self._mousewheel_handlers[str(widget)] = handler

    def _resolve_mousewheel_handler(
        self,
        widget: tk.Widget | None,
    ) -> Callable[[int], str | None] | None:
        current = widget
        while current is not None:
            handler = self._mousewheel_handlers.get(str(current))
            if handler is not None:
                return handler
            current = getattr(current, "master", None)
        return None

    def _scroll_widget_y(self, widget: tk.Widget, units: int) -> str | None:
        try:
            widget.yview_scroll(units, "units")
        except tk.TclError:
            return None
        return "break"

    def _dispatch_mousewheel(self, event) -> str | None:
        handler = self._resolve_mousewheel_handler(event.widget)
        if handler is None:
            return None
        delta = getattr(event, "delta", 0)
        if delta == 0:
            return None
        step = max(1, int(abs(delta) / 120))
        units = -step if delta > 0 else step
        return handler(units)

    def _dispatch_mousewheel_linux_up(self, event) -> str | None:
        handler = self._resolve_mousewheel_handler(event.widget)
        if handler is None:
            return None
        return handler(-1)

    def _dispatch_mousewheel_linux_down(self, event) -> str | None:
        handler = self._resolve_mousewheel_handler(event.widget)
        if handler is None:
            return None
        return handler(1)

    def _on_root_configure(self, event) -> None:
        if event.widget is not self.root:
            return
        self._schedule_main_layout_refresh()

    def _schedule_main_layout_refresh(self) -> None:
        if self._main_layout_refresh_job is not None:
            self.root.after_cancel(self._main_layout_refresh_job)
        self._main_layout_refresh_job = self.root.after(60, self._refresh_main_layout)

    def _refresh_main_layout(self) -> None:
        self._main_layout_refresh_job = None
        if not hasattr(self, "_main_columns_container"):
            return
        self._apply_main_layout(self._should_use_wide_main_layout())

    def _should_use_wide_main_layout(self) -> bool:
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        try:
            is_zoomed = str(self.root.state()) == "zoomed"
        except tk.TclError:
            is_zoomed = False
        return is_zoomed or (width >= 1500 and height >= 850)

    def _apply_main_layout(self, wide: bool) -> None:
        if self._main_layout_wide == wide:
            return
        self._main_layout_wide = wide

        self._main_left_col.pack_forget()
        self._main_right_col.pack_forget()
        self._main_canvas.pack_forget()
        self._main_scrollbar.pack_forget()

        self._main_canvas.pack(side="left", fill="both", expand=True, padx=(34, 0), pady=(8, 22))
        self._main_scrollbar.pack(side="right", fill="y", padx=(0, 34), pady=(8, 22))

        if wide:
            self._main_left_col.pack(side="left", fill="both", expand=True, padx=(0, 14))
            self._main_right_col.pack(side="left", fill="both", expand=True, padx=(14, 0))
            self._samples_lbl.config(wraplength=560)
        else:
            self._main_left_col.pack(fill="x")
            self._main_right_col.pack(fill="both", expand=True)
            self._samples_lbl.config(wraplength=850)

    def _configure_ttk_style(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Solver.Horizontal.TProgressbar",
            troughcolor=self.colors["field_bg"],
            background=self.colors["secondary"],
            bordercolor=self.colors["border"],
            lightcolor=self.colors["secondary"],
            darkcolor=self.colors["secondary"],
            thickness=8,
        )

    # ==================================================================
    # Main screen
    # ==================================================================

    def _build_main_frame(self) -> None:
        self._main_frame = tk.Frame(self.root, bg=self.colors['bg'])

        # Header
        header = tk.Frame(self._main_frame, bg=self.colors['bg'], height=88)
        header.pack(fill="x", padx=34, pady=(22, 8))
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="Optimal Samples Selection",
            font=(UI_FONT, 27, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(anchor="w", pady=(8, 0))
        
        tk.Label(
            header,
            text="A focused covering design workspace for sample sets and saved results",
            font=(UI_FONT, 12),
            bg=self.colors['bg'],
            fg=self.colors['text_light']
        ).pack(anchor="w", pady=(4, 0))

        # Scrollable container
        canvas = tk.Canvas(self._main_frame, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = tk.Scrollbar(self._main_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=self.colors['bg'])
        self._main_canvas = canvas
        self._main_scrollbar = scrollbar

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=canvas.winfo_reqwidth())
        
        def _configure_canvas(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind("<Configure>", _configure_canvas)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=(34, 0), pady=(8, 22))
        scrollbar.pack(side="right", fill="y", padx=(0, 34), pady=(8, 22))

        self._register_mousewheel_handler(
            canvas,
            lambda units: self._scroll_widget_y(canvas, units),
        )
        self._register_mousewheel_handler(
            scroll_frame,
            lambda units: self._scroll_widget_y(canvas, units),
        )

        self._main_columns_container = tk.Frame(scroll_frame, bg=self.colors['bg'])
        self._main_columns_container.pack(fill="both", expand=True)

        self._main_left_col = tk.Frame(self._main_columns_container, bg=self.colors['bg'])
        self._main_right_col = tk.Frame(self._main_columns_container, bg=self.colors['bg'])
        
        # Initially pack in single column (will adjust based on window size)
        self._main_left_col.pack(fill="x")
        self._main_right_col.pack(fill="both", expand=True)
        
        # Track layout mode
        self._is_wide_layout = False
        
        # Bind window resize event
        self.root.bind("<Configure>", self._on_window_resize)
        
        scroll_frame = self._main_left_col

        # Parameters Card
        params_card = self._create_card(scroll_frame, "Parameters")
        params_card.pack(fill="x", pady=(0, 14))

        params_content = tk.Frame(params_card, bg=self.colors['card_bg'])
        params_content.pack(fill="x", padx=20, pady=(8, 18))

        # First row
        row1 = tk.Frame(params_content, bg=self.colors['card_bg'])
        row1.pack(fill="x", pady=(0, 10))
        self._m = self._param_entry(row1, "Population (m)", "45", "Range: 45-54", 0)
        self._n = self._param_entry(row1, "Sample Size (n)", "8", "Range: 7-25", 1)
        self._k = self._param_entry(row1, "Group Size (k)", "6", "Range: 4-7", 2)

        # Second row
        row2 = tk.Frame(params_content, bg=self.colors['card_bg'])
        row2.pack(fill="x", pady=(0, 10))
        self._j = self._param_entry(row2, "Test Size (j)", "5", "Constraint: s≤j≤k", 0)
        self._s = self._param_entry(row2, "Threshold (s)", "5", "Range: 3-7", 1)
        self._t = self._param_entry(row2, "At least (t)", "1", "Range: 1-C(j,s) s-subsets", 2)

        # Third row
        row3 = tk.Frame(params_content, bg=self.colors['card_bg'])
        row3.pack(fill="x", pady=(0, 10))
        self._timeout = self._param_entry(row3, "Timeout (sec)", "150", "Max runtime: 30-600s", 0)

        # Sample Selection Card
        sample_card = self._create_card(scroll_frame, "Sample Selection")
        sample_card.pack(fill="x", pady=(0, 14))

        sample_content = tk.Frame(sample_card, bg=self.colors['card_bg'])
        sample_content.pack(fill="x", padx=20, pady=(8, 18))

        self._mode = tk.StringVar(value="random")
        
        mode_frame = tk.Frame(sample_content, bg=self.colors['card_bg'])
        mode_frame.pack(fill="x", pady=(0, 10))
        
        tk.Radiobutton(
            mode_frame, text="Random Selection",
            variable=self._mode, value="random",
            command=self._toggle_input,
            font=(UI_FONT, 12, "bold"),
            bg=self.colors['field_bg'],
            fg=self.colors['text'],
            selectcolor=self.colors['selection'],
            activebackground=self.colors['selection'],
            activeforeground=self.colors['text'],
            indicatoron=False,
            relief="flat",
            bd=0,
            padx=18,
            pady=9,
            highlightbackground=self.colors['border'],
            highlightthickness=1,
        ).pack(side="left", fill="x", expand=True, padx=(0, 6))
        
        tk.Radiobutton(
            mode_frame, text="Manual Input",
            variable=self._mode, value="input",
            command=self._toggle_input,
            font=(UI_FONT, 12, "bold"),
            bg=self.colors['field_bg'],
            fg=self.colors['text'],
            selectcolor=self.colors['selection'],
            activebackground=self.colors['selection'],
            activeforeground=self.colors['text'],
            indicatoron=False,
            relief="flat",
            bd=0,
            padx=18,
            pady=9,
            highlightbackground=self.colors['border'],
            highlightthickness=1,
        ).pack(side="left", fill="x", expand=True, padx=(6, 0))

        self._input_box = tk.Frame(sample_content, bg=self.colors['card_bg'])
        tk.Label(
            self._input_box,
            text="Enter sample numbers (comma-separated):",
            font=(UI_FONT, 11, "bold"),
            bg=self.colors['card_bg'],
            fg=self.colors['text']
        ).pack(anchor="w", pady=(0, 8))
        
        self._samples_entry = tk.Entry(
            self._input_box,
            font=(UI_FONT, 13),
            relief="flat",
            borderwidth=0,
            bg=self.colors['field_bg'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            highlightbackground=self.colors['border'],
            highlightcolor=self.colors['secondary'],
            highlightthickness=1,
        )
        self._samples_entry.pack(fill="x", ipady=10)

        self._samples_lbl = tk.Label(
            sample_content,
            text="",
            font=(UI_FONT, 12, "bold"),
            bg=self.colors['card_bg'],
            fg=self.colors['secondary'],
            wraplength=850,
            justify="left"
        )
        self._samples_lbl.pack(fill="x", pady=(12, 0))

        # Action Buttons - responsive layout
        btn_frame = tk.Frame(scroll_frame, bg=self.colors['bg'])
        btn_frame.pack(fill="x", pady=(0, 14))
        for col in range(4):
            btn_frame.grid_columnconfigure(col, weight=1, uniform="actions")

        self._exec_btn = self._create_button(
            btn_frame, "Execute", self._on_execute, variant="primary"
        )
        self._cancel_btn = self._create_button(
            btn_frame, "Cancel", self._on_cancel, variant="danger", state="disabled"
        )
        self._store_btn = self._create_button(
            btn_frame, "Store", self._on_store, variant="secondary", state="disabled"
        )
        self._verify_btn = self._create_button(
            btn_frame, "Verify", self._on_verify, variant="secondary", state="disabled"
        )
        self._print_btn = self._create_button(
            btn_frame, "Print Details", self._on_print, variant="neutral", state="disabled"
        )
        self._clear_btn = self._create_button(
            btn_frame, "Clear", self._on_clear, variant="neutral"
        )
        self._db_btn = self._create_button(
            btn_frame, "Database", self._show_db, variant="neutral"
        )
        for index, button in enumerate(
            [
                self._exec_btn,
                self._cancel_btn,
                self._store_btn,
                self._verify_btn,
                self._print_btn,
                self._clear_btn,
                self._db_btn,
            ]
        ):
            button.grid(row=index // 4, column=index % 4, sticky="ew", padx=4, pady=4)

        # Progress Card
        progress_card = self._create_card(scroll_frame, "Progress")
        progress_card.pack(fill="x", pady=(0, 14))

        progress_content = tk.Frame(progress_card, bg=self.colors['card_bg'])
        progress_content.pack(fill="x", padx=20, pady=(8, 18))

        self._prog_var = tk.StringVar(value="Ready to execute")
        tk.Label(
            progress_content,
            textvariable=self._prog_var,
            font=(UI_FONT, 12, "bold"),
            bg=self.colors['card_bg'],
            fg=self.colors['text']
        ).pack(fill="x", pady=(0, 12))
        
        self._prog_bar = ttk.Progressbar(
            progress_content,
            mode="determinate",
            length=300,
            style="Solver.Horizontal.TProgressbar",
        )
        self._prog_bar.pack(fill="x")
        self._prog_bar["value"] = 0

        # Results Card - add to right column for wide layout
        results_frame = self._main_right_col
        results_card = self._create_card(results_frame, "Results")
        results_card.pack(fill="both", expand=True)

        results_content = tk.Frame(results_card, bg=self.colors['card_bg'])
        results_content.pack(fill="both", expand=True, padx=20, pady=(8, 18))

        self._result_text = scrolledtext.ScrolledText(
            results_content,
            height=15,
            font=(MONO_FONT, 12),
            bg=self.colors['panel'],
            fg=self.colors['text'],
            relief="flat",
            borderwidth=0,
            wrap="none",
            insertbackground=self.colors['text'],
            selectbackground=self.colors['selection'],
            highlightbackground=self.colors['border'],
            highlightcolor=self.colors['secondary'],
            highlightthickness=1,
        )
        self._result_text.pack(fill="both", expand=True)
        self._register_mousewheel_handler(
            self._result_text,
            lambda units: self._scroll_widget_y(self._result_text, units),
        )

        self._file_lbl = tk.StringVar()
        tk.Label(
            results_content,
            textvariable=self._file_lbl,
            font=(UI_FONT, 12, "bold"),
            bg=self.colors['card_bg'],
            fg=self.colors['secondary']
        ).pack(pady=(10, 0))

        self.root.after(0, self._refresh_main_layout)

    def _create_card(self, parent, title: str) -> tk.Frame:
        """Create a modern card-style frame."""
        card = tk.Frame(
            parent, 
            bg=self.colors['card_bg'],
            relief="flat",
            borderwidth=1,
            highlightbackground=self.colors['border'],
            highlightthickness=1
        )
        
        header = tk.Frame(card, bg=self.colors['card_bg'], height=44)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text=title,
            bg=self.colors['card_bg'],
            fg=self.colors['text'],
            font=(UI_FONT, 13, "bold")
        ).pack(side="left", padx=20, pady=(12, 8), anchor="w")
        
        return card

    def _param_entry(self, parent, label: str, default: str, hint: str, col: int) -> tk.StringVar:
        """Create a modern parameter entry."""
        container = tk.Frame(parent, bg=self.colors['card_bg'])
        container.grid(row=0, column=col, padx=8, sticky="ew")
        parent.grid_columnconfigure(col, weight=1)
        
        tk.Label(
            container,
            text=label,
            font=(UI_FONT, 12, "bold"),
            bg=self.colors['card_bg'],
            fg=self.colors['text'],
            anchor="w"
        ).pack(anchor="w")
        
        tk.Label(
            container,
            text=hint,
            font=(UI_FONT, 10),
            bg=self.colors['card_bg'],
            fg=self.colors['text_light'],
            anchor="w"
        ).pack(anchor="w", pady=(2, 8))
        
        var = tk.StringVar(value=default)
        entry = tk.Entry(
            container,
            textvariable=var,
            font=(UI_FONT, 15, "bold"),
            relief="flat",
            borderwidth=0,
            justify="center",
            bg=self.colors['field_bg'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            highlightbackground=self.colors['border'],
            highlightcolor=self.colors['secondary'],
            highlightthickness=1,
        )
        entry.pack(fill="x", ipady=10)
        
        return var

    def _button_colors(self, _variant: str) -> tuple[str, str, str]:
        return self.colors['neutral'], self.colors['text'], self.colors['neutral_hover']

    def _create_button(
        self,
        parent,
        text: str,
        command,
        width: int = 0,
        height: int = 1,
        state: str = "normal",
        variant: str = "neutral",
    ) -> tk.Button:
        """Create a modern styled button."""
        background, foreground, hover = self._button_colors(variant)
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=background,
            fg=foreground,
            activebackground=hover,
            activeforeground=foreground,
            disabledforeground=self.colors['text_subtle'],
            font=(UI_FONT, 11, "bold"),
            relief="flat",
            borderwidth=0,
            width=width,
            height=height,
            cursor="hand2",
            state=state,
            padx=15,
            pady=9,
            highlightbackground=self.colors['border'],
            highlightthickness=1,
        )
        
        # Hover effect
        def on_enter(e):
            if btn['state'] != 'disabled':
                btn['bg'] = hover
        
        def on_leave(e):
            btn['bg'] = background
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn

    def _show_custom_dialog(self, title: str, message: str, icon_type: str = "success") -> None:
        """Show a beautiful custom dialog."""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("500x280")
        dialog.resizable(False, False)
        dialog.configure(bg=self.colors['card_bg'])
        
        # Center the dialog
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Icon and color based on type
        if icon_type == "success":
            color = self.colors['secondary']
            variant = "secondary"
        else:
            color = self.colors['danger']
            variant = "danger"
        
        shell = tk.Frame(dialog, bg=self.colors['card_bg'])
        shell.pack(fill="both", expand=True, padx=24, pady=22)
        
        tk.Frame(shell, bg=color, width=4).pack(side="left", fill="y", padx=(0, 18))

        main = tk.Frame(shell, bg=self.colors['card_bg'])
        main.pack(side="left", fill="both", expand=True)

        tk.Label(
            main,
            text=title,
            font=(UI_FONT, 18, "bold"),
            bg=self.colors['card_bg'],
            fg=self.colors['text']
        ).pack(anchor="w")
        
        # Message content
        content = tk.Frame(main, bg=self.colors['card_bg'])
        content.pack(fill="both", expand=True, pady=(14, 18))
        
        tk.Label(
            content,
            text=message,
            font=(UI_FONT, 12),
            bg=self.colors['card_bg'],
            fg=self.colors['text'],
            justify="left",
            wraplength=420
        ).pack(anchor="w")
        
        # Button
        btn_frame = tk.Frame(main, bg=self.colors['card_bg'])
        btn_frame.pack(fill="x")
        ok_btn = self._create_button(btn_frame, "OK", dialog.destroy, variant=variant, width=12)
        ok_btn.pack(side="right")
        
        # Center dialog on screen
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        dialog.wait_window()

    def _show_confirm_dialog(self, title: str, message: str) -> bool:
        """Show a beautiful confirmation dialog with Yes/No buttons."""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("500x260")
        dialog.resizable(False, False)
        dialog.configure(bg=self.colors['card_bg'])
        
        # Center the dialog
        dialog.transient(self.root)
        dialog.grab_set()
        
        result = [False]  # Use list to store result
        
        shell = tk.Frame(dialog, bg=self.colors['card_bg'])
        shell.pack(fill="both", expand=True, padx=24, pady=22)

        tk.Frame(shell, bg=self.colors['danger'], width=4).pack(side="left", fill="y", padx=(0, 18))

        main = tk.Frame(shell, bg=self.colors['card_bg'])
        main.pack(side="left", fill="both", expand=True)

        tk.Label(
            main,
            text=title,
            font=(UI_FONT, 18, "bold"),
            bg=self.colors['card_bg'],
            fg=self.colors['text']
        ).pack(anchor="w")
        
        # Message content
        content = tk.Frame(main, bg=self.colors['card_bg'])
        content.pack(fill="both", expand=True, pady=(14, 18))
        
        tk.Label(
            content,
            text=message,
            font=(UI_FONT, 12),
            bg=self.colors['card_bg'],
            fg=self.colors['text'],
            justify="left",
            wraplength=420
        ).pack(anchor="w")
        
        # Buttons
        btn_frame = tk.Frame(main, bg=self.colors['card_bg'])
        btn_frame.pack(fill="x")
        
        def on_yes():
            result[0] = True
            dialog.destroy()
        
        def on_no():
            result[0] = False
            dialog.destroy()
        
        # No button
        no_btn = self._create_button(btn_frame, "Cancel", on_no, variant="neutral", width=12)
        no_btn.pack(side="right", padx=(10, 0))
        
        # Yes button
        yes_btn = self._create_button(btn_frame, "Confirm Delete", on_yes, variant="danger", width=14)
        yes_btn.pack(side="right")
        
        # Center dialog on screen
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        dialog.wait_window()
        return result[0]

    def _darken_color(self, hex_color: str) -> str:
        """Darken a hex color by 10%."""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = max(0, int(r * 0.9))
        g = max(0, int(g * 0.9))
        b = max(0, int(b * 0.9))
        return f'#{r:02x}{g:02x}{b:02x}'

    def _toggle_input(self) -> None:
        if self._mode.get() == "input":
            self._input_box.pack(fill="x", pady=(10, 0))
        else:
            self._input_box.pack_forget()

    # --- Actions ---

    def _on_execute(self) -> None:
        try:
            p = self._read_params()
        except ValueError as exc:
            self._show_custom_dialog(
                "Invalid Parameters",
                f"Parameter validation failed:\n\n{str(exc)}\n\nPlease check your input and try again.",
                "error"
            )
            return

        samples = self._select_samples(p)
        if samples is None:
            return

        self._current_samples = samples
        self._params = p
        self._samples_lbl.config(text=f"Selected samples: {samples}")

        # Update time budget from user input
        self._time_budget_sec = p["timeout"]
        
        self._cancel_flag = False
        self._deadline_stop_requested = False
        self._stop_reason = "running"
        self._run_started_at = time.time()
        self._exec_btn.config(state="disabled")
        self._store_btn.config(state="disabled")
        self._verify_btn.config(state="disabled")
        self._print_btn.config(state="disabled")
        self._cancel_btn.config(state="normal")
        self._result_text.delete("1.0", "end")
        self._prog_bar["value"] = 0
        self._prog_var.set(
            f"Running with {self._time_budget_sec:.0f}s time budget..."
        )

        self._thread = threading.Thread(target=self._run_solver, daemon=True)
        self._thread.start()

    def _on_store(self) -> None:
        if not self._current_result or not self._current_samples:
            return
        p = self._params
        samples = self._current_samples
        real_groups = [
            [samples[g] for g in grp]
            for grp in self._current_result.groups
        ]
        fn = self.db.save(
            p["m"], p["n"], p["k"], p["j"], p["s"],
            samples,
            real_groups,
            self._current_result.elapsed,
            self._current_result.first_legal_elapsed,
            t=p["t"],
        )
        self._file_lbl.set(f"Stored: {fn}")
        
        # Build message with solution found time if available
        time_info = f"Total Time: {self._current_result.elapsed:.2f}s"
        if self._current_result.first_legal_elapsed is not None:
            time_info += f"\nSolution Found: {self._current_result.first_legal_elapsed:.2f}s"
        
        self._show_custom_dialog(
            "Saved Successfully",
            f"✓ Result saved to database!\n\n"
            f"Filename: {fn}\n"
            f"{time_info}\n\n"
            f"You can view it in the Database Browser.",
            "success"
        )

    def _on_print(self) -> None:
        """Print full detailed group information."""
        if not self._current_result:
            return
        
        result = self._current_result
        p = self._params
        run_count = self._get_run_count(p["m"], p["n"], p["k"], p["j"], p["s"], p["t"])
        current_run = run_count + 1

        # Show detailed information WITHOUT verification status
        lines = [
            "═" * 70,
            "  DETAILED SOLUTION",
            "═" * 70,
            "",
            (
                f"  Parameters: m={p['m']}, n={p['n']}, k={p['k']}, "
                f"j={p['j']}, s={p['s']}, {format_t_detail(p['t'])}"
            ),
            f"  Run Number: {self._ordinal(current_run)}",
            f"  Groups Found: {result.num_groups}",
            f"  Time Elapsed: {result.elapsed:.2f}s",
            "",
            f"  Selected Samples: {self._current_samples}",
            "",
            "═" * 70,
            "  GROUP DETAILS",
            "═" * 70,
            ""
        ]
        
        samples = self._current_samples
        for i, grp in enumerate(result.groups, 1):
            nums = [samples[g] for g in grp]
            lines.append(f"  Group {i:3d}: {', '.join(map(str, nums))}")
        
        lines.append("")
        lines.append("═" * 70)
        
        # Add verification hint if not verified yet
        if not result.verified:
            lines.append("")
            lines.append("  Note: Click 'Verify' button to check solution validity")
            lines.append("")
        
        self._result_text.delete("1.0", "end")
        self._result_text.insert("1.0", "\n".join(lines))

    def _on_verify(self) -> None:
        """Verify the current solution and refresh display."""
        if not self._current_result:
            return
        
        p = self._params
        current = self._current_result
        
        from n_algorithms.shared.verification import verify_masks_with_solver

        t = p.get("t", 1)
        verification = verify_masks_with_solver(
            n=p["n"],
            k=p["k"],
            j=p["j"],
            s=p["s"],
            t=t,
            masks=self._result_masks(current),
        )
        is_verified = verification.verified
        
        # Update the result
        self._current_result = SolverResult(
            groups=self._current_result.groups,
            num_groups=self._current_result.num_groups,
            elapsed=self._current_result.elapsed,
            verified=is_verified,
            first_legal_elapsed=self._current_result.first_legal_elapsed,
            groups_complete=self._current_result.groups_complete,
            group_masks=self._current_result.group_masks,
        )
        
        # Get run number
        run_count = self._get_run_count(p["m"], p["n"], p["k"], p["j"], p["s"], t)
        current_run = run_count + 1
        
        # Auto-refresh display with verification result
        if is_verified:
            lines = [
                "",
                "  " + "=" * 35,
                "",
                "            SOLUTION VERIFIED SUCCESSFULLY",
                "",
                "  " + "=" * 35,
                "",
                "",
                "  Summary:",
                "  " + "─" * 66,
                f"    Groups Found      : {self._current_result.num_groups}",
                f"    Time Elapsed      : {self._current_result.elapsed:.2f}s",
                f"    Run Number        : {self._ordinal(current_run)}",
                f"    Verification      : PASSED - All targets covered",
                "  " + "─" * 66,
                "",
                "",
                "  Next Steps:",
                "",
                "    1. Solution is valid and ready to use",
                "    2. Click 'Print Details' to see all groups",
                "    3. Click 'Store' to save to database",
                "",
                "",
            ]
            self._show_custom_dialog(
                "Verification Success",
                "✓ Solution verified successfully!\n\n"
                "All targets are properly covered.\n"
                "The solution is valid and ready to use.",
                "success"
            )
            self._prog_var.set(f"Verified: {self._current_result.num_groups} groups (valid solution)")
        else:
            lines = [
                "",
                "  " + "=" * 35,
                "",
                "            VERIFICATION FAILED",
                "",
                "  " + "=" * 35,
                "",
                "",
                "  Summary:",
                "  " + "─" * 66,
                f"    Groups Found      : {self._current_result.num_groups}",
                f"    Time Elapsed      : {self._current_result.elapsed:.2f}s",
                f"    Run Number        : {self._ordinal(current_run)}",
                f"    Verification      : FAILED - Some targets not covered",
                "  " + "─" * 66,
                "",
                "",
                "  Warning:",
                "",
                "    The solution does not cover all required targets.",
                "    This may indicate an algorithm issue.",
                "",
                "",
            ]
            self._show_custom_dialog(
                "Verification Failed",
                "✗ Verification failed!\n\n"
                "Some targets are not properly covered.\n"
                "The solution may be incomplete.",
                "error"
            )
            self._prog_var.set(f"Verification failed: {self._current_result.num_groups} groups")
        
        # Refresh display
        self._result_text.delete("1.0", "end")
        self._result_text.insert("1.0", "\n".join(lines))
        
        # Update file label with verification status
        filename = format_result_filename(
            m=p["m"],
            n=p["n"],
            k=p["k"],
            j=p["j"],
            s=p["s"],
            t=t,
            run_number=current_run,
            num_groups=self._current_result.num_groups,
        )
        status = "Verified" if is_verified else "Failed"
        self._file_lbl.set(f"{status} {filename}")

    def _on_clear(self) -> None:
        self._result_text.delete("1.0", "end")
        self._prog_var.set("Ready to execute")
        self._prog_bar["value"] = 0
        self._file_lbl.set("")
        self._current_result = None
        self._store_btn.config(state="disabled")
        self._verify_btn.config(state="disabled")
        self._print_btn.config(state="disabled")

    def _on_cancel(self) -> None:
        self._cancel_flag = True
        if self._stop_reason == "running":
            self._stop_reason = "manual_cancel"
        self._cancel_btn.config(state="disabled")

    def _should_cancel_solver(self, started_at: float) -> bool:
        if self._cancel_flag:
            return True
        if (time.time() - started_at) >= self._time_budget_sec:
            self._deadline_stop_requested = True
            if self._stop_reason == "running":
                self._stop_reason = "deadline"
            return True
        return False

    def _result_reason_text(self) -> str:
        if self._stop_reason == "deadline":
            return (
                f"Time budget reached ({self._time_budget_sec:.0f}s); "
                "returned current best-so-far solution"
            )
        if self._stop_reason == "manual_cancel":
            return "Stopped by user; returned current best-so-far solution"
        return "Completed normal solve flow"

    def _result_masks(self, result: SolverResult):
        if result.group_masks is not None:
            return result.group_masks
        return [elements_to_mask(grp) for grp in result.groups]

    # --- Parameter reading ---

    def _read_params(self) -> dict[str, int]:
        def _int(var: tk.StringVar, name: str) -> int:
            try:
                return int(var.get())
            except ValueError:
                raise ValueError(f"{name} must be an integer") from None

        m = _int(self._m, "m")
        n = _int(self._n, "n")
        k = _int(self._k, "k")
        j = _int(self._j, "j")
        s = _int(self._s, "s")
        t = _int(self._t, "t")
        timeout = _int(self._timeout, "timeout")

        if not 45 <= m <= 54:
            raise ValueError("m must be between 45 and 54")
        if not 7 <= n <= 25:
            raise ValueError("n must be between 7 and 25")
        if not 4 <= k <= 7:
            raise ValueError("k must be between 4 and 7")
        if not 3 <= s <= 7:
            raise ValueError("s must be between 3 and 7")
        if not s <= j <= k:
            raise ValueError(f"Need s({s}) ≤ j({j}) ≤ k({k})")
        if n > m:
            raise ValueError(f"n({n}) cannot exceed m({m})")
        
        # Validate t parameter
        from math import comb
        max_t = comb(j, s)
        if not 1 <= t <= max_t:
            raise ValueError(f"t must be between 1 and C({j},{s})={max_t}")
        
        if not 30 <= timeout <= 600:
            raise ValueError("Timeout must be between 30 and 600 seconds")
        
        return {"m": m, "n": n, "k": k, "j": j, "s": s, "t": t, "timeout": timeout}

    def _select_samples(self, p: dict[str, int]) -> list[int] | None:
        m, n = p["m"], p["n"]
        if self._mode.get() == "random":
            return sorted(random.sample(range(1, m + 1), n))

        raw = self._samples_entry.get().strip()
        if not raw:
            self._show_custom_dialog(
                "Input Required",
                "Please enter sample numbers.\n\nYou need to provide comma-separated numbers.",
                "error"
            )
            return None
        try:
            nums = [int(x.strip()) for x in raw.split(",")]
        except ValueError:
            self._show_custom_dialog(
                "Invalid Input",
                "All values must be integers.\n\nPlease check your input format.",
                "error"
            )
            return None
        if len(nums) != n:
            self._show_custom_dialog(
                "Wrong Count",
                f"Expected {n} numbers, but got {len(nums)}.\n\nPlease provide exactly {n} sample numbers.",
                "error"
            )
            return None
        if len(set(nums)) != n:
            self._show_custom_dialog(
                "Duplicate Values",
                "Duplicate values found.\n\nEach sample number must be unique.",
                "error"
            )
            return None
        if any(x < 1 or x > m for x in nums):
            self._show_custom_dialog(
                "Out of Range",
                f"All values must be in range 1 to {m}.\n\nPlease check your sample numbers.",
                "error"
            )
            return None
        return sorted(nums)

    # --- Solver thread ---

    def _run_solver(self) -> None:
        p = self._params
        try:
            started_at = self._run_started_at or time.time()
            solver = CoveringDesignSolver(
                n=p["n"], k=p["k"], j=p["j"], s=p["s"], t=p["t"],
                progress_cb=lambda prog: self._q.put(prog),
                cancel_fn=lambda _t0=started_at: self._should_cancel_solver(_t0),
                num_attempts=5,
                time_budget_sec=self._time_budget_sec,
                skip_final_verify=True,  # Skip verification for faster GUI response
            )
            result = solver.solve()
            if self._stop_reason == "running":
                self._stop_reason = "completed"
            self._q.put(result)
        except Exception as exc:
            self._q.put(f"Error: {exc}")

    def _poll_queue(self) -> None:
        try:
            while True:
                item = self._q.get_nowait()
                if isinstance(item, SolverProgress):
                    self._prog_var.set(f"[{item.elapsed:.1f}s] {item.message}")
                    if item.total > 0:
                        pct = (item.total - item.remaining) / item.total * 100
                        self._prog_bar["value"] = pct
                elif isinstance(item, SolverResult):
                    self._on_result(item)
                elif isinstance(item, str):
                    self._prog_var.set(item)
                    self._exec_btn.config(state="normal")
                    self._cancel_btn.config(state="disabled")
        except queue.Empty:
            pass
        self.root.after(120, self._poll_queue)

    def _on_result(self, result: SolverResult) -> None:
        self._current_result = result
        self._exec_btn.config(state="normal")
        self._cancel_btn.config(state="disabled")
        self._store_btn.config(state="normal")
        self._verify_btn.config(state="normal")
        self._print_btn.config(state="normal")

        # Get run number
        p = self._params
        run_count = self._get_run_count(p["m"], p["n"], p["k"], p["j"], p["s"], p["t"])
        current_run = run_count + 1

        self._render_result_summary(result, current_run)

    def _render_result_summary(self, result: SolverResult, current_run: int) -> None:
        p = self._params
        first_legal = (
            f"{result.first_legal_elapsed:.2f}s"
            if result.first_legal_elapsed is not None
            else "---"
        )
        reason_text = self._result_reason_text()
        
        lines = [
            "",
            "  " + "=" * 35,
            "",
            "            SOLUTION GENERATED",
            "",
            "  " + "=" * 35,
            "",
            "",
            "  Summary:",
            "  " + "-" * 66,
            f"    Groups Found      : {result.num_groups}",
            f"    Cover Count       : {format_t_detail(p['t'])}",
            f"    Time Elapsed      : {result.elapsed:.2f}s",
            f"    First Legal       : {first_legal}",
            f"    Run Number        : {self._ordinal(current_run)}",
            f"    Return Mode       : {reason_text}",
            f"    Verification      : {'Passed' if result.verified else 'Pending'}",
            "  " + "-" * 66,
            "",
            "",
            "  Next Steps:",
            "",
            "    1. Click 'Print Details' to view all groups",
            "    2. Click 'Verify' to validate the solution",
            "    3. Click 'Store' to save to database",
            "",
            "",
        ]
        self._result_text.delete("1.0", "end")
        self._result_text.insert("1.0", "\n".join(lines))

        filename = format_result_filename(
            m=p["m"],
            n=p["n"],
            k=p["k"],
            j=p["j"],
            s=p["s"],
            t=p["t"],
            run_number=current_run,
            num_groups=result.num_groups,
        )
        self._file_lbl.set(f"Result: {filename}")

        if self._stop_reason == "deadline":
            self._prog_var.set(
                f"Time budget reached ({self._time_budget_sec:.0f}s): "
                f"returned {result.num_groups} groups in {result.elapsed:.2f}s"
            )
        elif self._stop_reason == "manual_cancel":
            self._prog_var.set(
                f"Stopped by user: returned {result.num_groups} groups "
                f"in {result.elapsed:.2f}s"
            )
        else:
            self._prog_var.set(
                f"Generated: {result.num_groups} groups in {result.elapsed:.2f}s "
                f"(Run #{current_run})"
            )
        self._prog_bar["value"] = 100

    def _ordinal(self, n: int) -> str:
        """Convert number to ordinal string (1st, 2nd, 3rd, etc.)."""
        if 10 <= n % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
        return f"{n}{suffix}"

    def _get_run_count(self, m: int, n: int, k: int, j: int, s: int, t: int = 1) -> int:
        """Get the number of previous runs with the same parameters."""
        try:
            return self.db.count_by_params(m, n, k, j, s, t)
        except Exception:
            return 0

    # ==================================================================
    # DB Browser screen
    # ==================================================================

    def _build_db_frame(self) -> None:
        self._db_frame = tk.Frame(self.root, bg=self.colors['bg'])

        # Header
        header = tk.Frame(self._db_frame, bg=self.colors['bg'], height=88)
        header.pack(fill="x", padx=34, pady=(22, 8))
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="Database Browser",
            font=(UI_FONT, 27, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(anchor="w", pady=(8, 0))
        
        tk.Label(
            header,
            text="View and manage saved results",
            font=(UI_FONT, 12),
            bg=self.colors['bg'],
            fg=self.colors['text_light']
        ).pack(anchor="w", pady=(4, 0))

        # Scrollable container
        canvas = tk.Canvas(self._db_frame, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = tk.Scrollbar(self._db_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=self.colors['bg'])

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=canvas.winfo_reqwidth())
        
        def _configure_canvas(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind("<Configure>", _configure_canvas)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=(34, 0), pady=(8, 22))
        scrollbar.pack(side="right", fill="y", padx=(0, 34), pady=(8, 22))

        self._register_mousewheel_handler(
            canvas,
            lambda units: self._scroll_widget_y(canvas, units),
        )
        self._register_mousewheel_handler(
            scroll_frame,
            lambda units: self._scroll_widget_y(canvas, units),
        )

        # Action Buttons
        btn_frame = tk.Frame(scroll_frame, bg=self.colors['bg'])
        btn_frame.pack(fill="x", pady=(0, 14))
        for col in range(3):
            btn_frame.grid_columnconfigure(col, weight=1, uniform="db-actions")

        db_buttons = [
            self._create_button(btn_frame, "Display", self._db_display, variant="primary"),
            self._create_button(btn_frame, "Delete", self._db_delete, variant="danger"),
            self._create_button(btn_frame, "Back", self._show_main, variant="neutral"),
        ]
        for index, button in enumerate(db_buttons):
            button.grid(row=0, column=index, sticky="ew", padx=4, pady=4)

        # Saved Results Card
        list_card = self._create_card(scroll_frame, "Saved Results")
        list_card.pack(fill="x", pady=(0, 14))

        list_content = tk.Frame(list_card, bg=self.colors['card_bg'])
        list_content.pack(fill="x", padx=20, pady=(8, 18))

        list_frame = tk.Frame(
            list_content,
            bg=self.colors['panel'],
            relief="flat",
            borderwidth=0,
            highlightbackground=self.colors['border'],
            highlightthickness=1,
        )
        list_frame.pack(fill="x")

        scrollbar_list = tk.Scrollbar(list_frame, orient="vertical")
        scrollbar_list.pack(side="right", fill="y")

        self._db_list = tk.Listbox(
            list_frame,
            height=10,
            selectmode=tk.SINGLE,
            font=(MONO_FONT, 13, "bold"),
            bg=self.colors['panel'],
            fg=self.colors['text'],
            selectbackground=self.colors['selection'],
            selectforeground=self.colors['text'],
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            yscrollcommand=scrollbar_list.set
        )
        scrollbar_list.config(command=self._db_list.yview)
        self._db_list.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self._register_mousewheel_handler(
            self._db_list,
            lambda units: self._scroll_widget_y(self._db_list, units),
        )

        self._db_ids: list[int] = []

        # Detail View Card
        detail_card = self._create_card(scroll_frame, "Group Details")
        detail_card.pack(fill="both", expand=True)

        detail_content = tk.Frame(detail_card, bg=self.colors['card_bg'])
        detail_content.pack(fill="both", expand=True, padx=20, pady=(8, 18))

        self._db_text = scrolledtext.ScrolledText(
            detail_content,
            height=18,
            font=(MONO_FONT, 12),
            bg=self.colors['panel'],
            fg=self.colors['text'],
            relief="flat",
            borderwidth=0,
            wrap="none",
            insertbackground=self.colors['text'],
            selectbackground=self.colors['selection'],
            highlightbackground=self.colors['border'],
            highlightcolor=self.colors['secondary'],
            highlightthickness=1,
        )
        self._db_text.pack(fill="both", expand=True)
        self._register_mousewheel_handler(
            self._db_text,
            lambda units: self._scroll_widget_y(self._db_text, units),
        )

    def _refresh_db_list(self) -> None:
        self._db_list.delete(0, tk.END)
        self._db_ids.clear()
        for r in self.db.list_all():
            self._db_list.insert(tk.END, r.filename)
            self._db_ids.append(r.id)

    def _selected_db_id(self) -> int | None:
        sel = self._db_list.curselection()
        if not sel:
            self._show_custom_dialog(
                "No Selection",
                "Please select a result first.\n\nClick on a result in the list to select it.",
                "error"
            )
            return None
        return self._db_ids[sel[0]]

    def _db_display(self) -> None:
        rid = self._selected_db_id()
        if rid is None:
            return
        r = self.db.load(rid)
        if r is None:
            return

        lines = [
            "═" * 70,
            "  SAVED RESULT DETAILS",
            "═" * 70,
            "",
            f"  File: {r.filename}",
            f"  Created: {r.created_at}",
            f"  Total Algorithm Time: {r.elapsed_time:.2f}s",
        ]
        
        # Add solution found time if available
        if r.solution_found_time is not None:
            lines.append(f"  Solution Found Time: {r.solution_found_time:.2f}s")
        
        lines.extend([
            "",
            "  Parameters:",
            f"    • Population (m): {r.m}",
            f"    • Sample Size (n): {r.n}",
            f"    • Group Size (k): {r.k}",
            f"    • Test Size (j): {r.j}",
            f"    • Threshold (s): {r.s}",
            f"    • Cover Count (t): {format_t_detail(r.t)}",
            "",
            "  Selected Samples:",
            f"    {r.samples}",
            "",
            "═" * 70,
            f"  GROUPS ({r.num_groups} total)",
            "═" * 70,
            "",
        ])
        
        for i, grp in enumerate(r.groups, 1):
            lines.append(f"  Group {i:3d}: {', '.join(map(str, grp))}")
        
        lines.append("")
        lines.append("═" * 70)

        self._db_text.config(state="normal")
        self._db_text.delete("1.0", "end")
        self._db_text.insert("1.0", "\n".join(lines))
        self._db_text.config(state="disabled")

    def _db_delete(self) -> None:
        rid = self._selected_db_id()
        if rid is None:
            return
        if self._show_confirm_dialog(
            "Confirm Delete", 
            "Are you sure you want to delete this result?\n\nThis action cannot be undone."
        ):
            self.db.delete(rid)
            self._refresh_db_list()
            self._db_text.config(state="normal")
            self._db_text.delete("1.0", "end")
            self._db_text.config(state="disabled")


if __name__ == "__main__":
    app = CleanModernApp()
    app.run()
