"""Modern GUI using CustomTkinter for the Optimal Samples Selection System."""

from __future__ import annotations

import queue
import random
import threading
import tkinter as tk
from typing import Optional

try:
    import customtkinter as ctk
except ImportError:
    print("Installing customtkinter...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter"])
    import customtkinter as ctk

from database import ResultDatabase, SavedResult
from solver import CoveringDesignSolver, SolverProgress, SolverResult


class ModernOptimalSamplesApp:
    """Modern application window with CustomTkinter."""

    def __init__(self) -> None:
        # Set appearance mode and color theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("Optimal Samples Selection System")
        self.root.geometry("1000x820")
        self.root.minsize(900, 700)

        self.db = ResultDatabase()
        self._q: queue.Queue[SolverProgress | SolverResult | str] = queue.Queue()
        self._thread: Optional[threading.Thread] = None
        self._cancel_flag = False

        self._current_result: Optional[SolverResult] = None
        self._current_samples: list[int] = []
        self._params: dict[str, int] = {}

        self._build_main_frame()
        self._build_db_frame()
        self._show_main()

        self.root.after(120, self._poll_queue)

    def run(self) -> None:
        self.root.mainloop()

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

    # ==================================================================
    # Main screen
    # ==================================================================

    def _build_main_frame(self) -> None:
        self._main_frame = ctk.CTkFrame(self.root, fg_color="transparent")

        # Header
        header = ctk.CTkFrame(self._main_frame, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(20, 10))
        
        ctk.CTkLabel(
            header,
            text="🔬 Optimal Samples Selection",
            font=ctk.CTkFont(size=32, weight="bold")
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            header,
            text="Advanced covering design solver with GPU acceleration",
            font=ctk.CTkFont(size=14),
            text_color="gray50"
        ).pack(anchor="w", pady=(5, 0))

        # Scrollable container
        scroll = ctk.CTkScrollableFrame(
            self._main_frame, 
            fg_color="transparent",
            scrollbar_button_color="gray60",
            scrollbar_button_hover_color="gray50"
        )
        scroll.pack(fill="both", expand=True, padx=30, pady=(10, 20))

        # Parameters Card
        params_card = self._create_card(scroll, "⚙️ Parameters")
        params_card.pack(fill="x", pady=(0, 15))

        params_grid = ctk.CTkFrame(params_card, fg_color="transparent")
        params_grid.pack(fill="x", padx=20, pady=15)

        # First row
        row1 = ctk.CTkFrame(params_grid, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 10))
        self._m = self._param_entry(row1, "Population (m)", "45", "Range: 45-54", 0)
        self._n = self._param_entry(row1, "Sample Size (n)", "8", "Range: 7-25", 1)
        self._k = self._param_entry(row1, "Group Size (k)", "6", "Range: 4-7", 2)

        # Second row
        row2 = ctk.CTkFrame(params_grid, fg_color="transparent")
        row2.pack(fill="x")
        self._j = self._param_entry(row2, "Test Size (j)", "5", "Constraint: s≤j≤k", 0)
        self._s = self._param_entry(row2, "Threshold (s)", "5", "Range: 3-7", 1)

        # Sample Selection Card
        sample_card = self._create_card(scroll, "📊 Sample Selection")
        sample_card.pack(fill="x", pady=(0, 15))

        sample_content = ctk.CTkFrame(sample_card, fg_color="transparent")
        sample_content.pack(fill="x", padx=20, pady=15)

        self._mode = tk.StringVar(value="random")
        
        mode_frame = ctk.CTkFrame(sample_content, fg_color="transparent")
        mode_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkRadioButton(
            mode_frame, text="🎲 Random Selection", 
            variable=self._mode, value="random",
            command=self._toggle_input,
            font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=(0, 20))
        
        ctk.CTkRadioButton(
            mode_frame, text="✏️ Manual Input",
            variable=self._mode, value="input",
            command=self._toggle_input,
            font=ctk.CTkFont(size=13)
        ).pack(side="left")

        self._input_box = ctk.CTkFrame(sample_content, fg_color="transparent")
        ctk.CTkLabel(
            self._input_box,
            text="Enter sample numbers (comma-separated):",
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w", pady=(0, 5))
        
        self._samples_entry = ctk.CTkEntry(
            self._input_box,
            placeholder_text="e.g., 1, 5, 10, 15, 20, 25, 30, 35",
            height=40,
            font=ctk.CTkFont(size=13)
        )
        self._samples_entry.pack(fill="x")

        self._samples_lbl = ctk.CTkLabel(
            sample_content,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="gray50",
            wraplength=850
        )
        self._samples_lbl.pack(fill="x", pady=(10, 0))

        # Action Buttons
        btn_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(0, 15))

        left_btns = ctk.CTkFrame(btn_frame, fg_color="transparent")
        left_btns.pack(side="left")

        self._exec_btn = ctk.CTkButton(
            left_btns, text="▶ Execute",
            command=self._on_execute,
            height=45, width=140,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10
        )
        self._exec_btn.pack(side="left", padx=(0, 10))
        
        self._cancel_btn = ctk.CTkButton(
            left_btns, text="⏹ Cancel",
            command=self._on_cancel,
            height=40, width=120,
            fg_color="#ef4444", hover_color="#dc2626",
            state="disabled",
            corner_radius=10
        )
        self._cancel_btn.pack(side="left", padx=(0, 10))

        self._store_btn = ctk.CTkButton(
            left_btns, text="💾 Store",
            command=self._on_store,
            height=40, width=120,
            fg_color="#10b981", hover_color="#059669",
            state="disabled",
            corner_radius=10
        )
        self._store_btn.pack(side="left", padx=(0, 10))
        
        self._print_btn = ctk.CTkButton(
            left_btns, text="🖨 Print",
            command=self._on_print,
            height=40, width=120,
            fg_color="#10b981", hover_color="#059669",
            state="disabled",
            corner_radius=10
        )
        self._print_btn.pack(side="left", padx=(0, 10))
        
        self._clear_btn = ctk.CTkButton(
            left_btns, text="🗑 Clear",
            command=self._on_clear,
            height=40, width=120,
            fg_color="gray40", hover_color="gray30",
            corner_radius=10
        )
        self._clear_btn.pack(side="left")

        right_btns = ctk.CTkFrame(btn_frame, fg_color="transparent")
        right_btns.pack(side="right")
        
        ctk.CTkButton(
            right_btns, text="📁 Database Browser",
            command=self._show_db,
            height=40, width=180,
            fg_color="#6366f1", hover_color="#4f46e5",
            corner_radius=10
        ).pack()

        # Progress Card
        progress_card = self._create_card(scroll, "⏱ Progress")
        progress_card.pack(fill="x", pady=(0, 15))

        progress_content = ctk.CTkFrame(progress_card, fg_color="transparent")
        progress_content.pack(fill="x", padx=20, pady=15)

        self._prog_var = tk.StringVar(value="Ready to execute")
        ctk.CTkLabel(
            progress_content,
            textvariable=self._prog_var,
            font=ctk.CTkFont(size=13),
            text_color="gray50"
        ).pack(fill="x", pady=(0, 10))
        
        self._prog_bar = ctk.CTkProgressBar(progress_content, height=12)
        self._prog_bar.pack(fill="x")
        self._prog_bar.set(0)

        # Results Card
        results_card = self._create_card(scroll, "📋 Results")
        results_card.pack(fill="both", expand=True)

        results_content = ctk.CTkFrame(results_card, fg_color="transparent")
        results_content.pack(fill="both", expand=True, padx=20, pady=15)

        self._result_text = ctk.CTkTextbox(
            results_content,
            height=300,
            font=ctk.CTkFont(family="Consolas", size=13),
            corner_radius=8,
            wrap="none"
        )
        self._result_text.pack(fill="both", expand=True)

        self._file_lbl = tk.StringVar()
        ctk.CTkLabel(
            results_content,
            textvariable=self._file_lbl,
            font=ctk.CTkFont(family="Consolas", size=12),
            text_color="gray50"
        ).pack(pady=(10, 0))

    def _create_card(self, parent, title: str) -> ctk.CTkFrame:
        """Create a modern card with shadow effect."""
        card = ctk.CTkFrame(parent, corner_radius=15, fg_color="white")
        
        header = ctk.CTkFrame(card, fg_color="transparent", height=50)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        ).pack(side="left", padx=20, pady=15)
        
        return card

    def _param_entry(self, parent, label: str, default: str, hint: str, col: int) -> tk.StringVar:
        """Create a modern parameter entry."""
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.grid(row=0, column=col, padx=10, sticky="ew")
        parent.grid_columnconfigure(col, weight=1)
        
        ctk.CTkLabel(
            container,
            text=label,
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            container,
            text=hint,
            font=ctk.CTkFont(size=11),
            text_color="gray50",
            anchor="w"
        ).pack(anchor="w", pady=(2, 5))
        
        var = tk.StringVar(value=default)
        entry = ctk.CTkEntry(
            container,
            textvariable=var,
            height=40,
            font=ctk.CTkFont(size=14),
            corner_radius=8
        )
        entry.pack(fill="x")
        
        return var

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
            self._show_error("Invalid parameters", str(exc))
            return

        samples = self._select_samples(p)
        if samples is None:
            return

        self._current_samples = samples
        self._params = p
        self._samples_lbl.configure(text=f"Selected samples: {samples}")

        self._cancel_flag = False
        self._exec_btn.configure(state="disabled")
        self._store_btn.configure(state="disabled")
        self._print_btn.configure(state="disabled")
        self._cancel_btn.configure(state="normal")
        self._result_text.delete("0.0", "end")
        self._prog_bar.set(0)

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
        )
        self._file_lbl.set(f"📄 Stored: {fn}")
        self._show_info("Stored", f"Saved as {fn}")

    def _on_print(self) -> None:
        content = self._result_text.get("0.0", "end").strip()
        if not content:
            return
        import tempfile, subprocess, os
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", prefix="result_", delete=False
        )
        tmp.write(content)
        tmp.close()
        try:
            if os.name == 'nt':
                os.startfile(tmp.name)
            else:
                subprocess.Popen(["open", tmp.name])
        except Exception as exc:
            self._show_error("Print", f"Could not open file: {exc}")

    def _on_clear(self) -> None:
        self._result_text.delete("0.0", "end")
        self._prog_var.set("Ready to execute")
        self._prog_bar.set(0)
        self._file_lbl.set("")
        self._current_result = None
        self._store_btn.configure(state="disabled")
        self._print_btn.configure(state="disabled")

    def _on_cancel(self) -> None:
        self._cancel_flag = True
        self._cancel_btn.configure(state="disabled")

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
        return {"m": m, "n": n, "k": k, "j": j, "s": s}

    def _select_samples(self, p: dict[str, int]) -> list[int] | None:
        m, n = p["m"], p["n"]
        if self._mode.get() == "random":
            return sorted(random.sample(range(1, m + 1), n))

        raw = self._samples_entry.get().strip()
        if not raw:
            self._show_error("Error", "Please enter sample numbers.")
            return None
        try:
            nums = [int(x.strip()) for x in raw.split(",")]
        except ValueError:
            self._show_error("Error", "All values must be integers.")
            return None
        if len(nums) != n:
            self._show_error("Error", f"Expected {n} numbers, got {len(nums)}.")
            return None
        if len(set(nums)) != n:
            self._show_error("Error", "Duplicate values found.")
            return None
        if any(x < 1 or x > m for x in nums):
            self._show_error("Error", f"All values must be in 1..{m}.")
            return None
        return sorted(nums)

    # --- Solver thread ---

    def _run_solver(self) -> None:
        p = self._params
        try:
            solver = CoveringDesignSolver(
                n=p["n"], k=p["k"], j=p["j"], s=p["s"],
                progress_cb=lambda prog: self._q.put(prog),
                cancel_fn=lambda: self._cancel_flag,
                num_attempts=5,
            )
            result = solver.solve()
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
                        pct = (item.total - item.remaining) / item.total
                        self._prog_bar.set(pct)
                elif isinstance(item, SolverResult):
                    self._on_result(item)
                elif isinstance(item, str):
                    self._prog_var.set(item)
                    self._exec_btn.configure(state="normal")
                    self._cancel_btn.configure(state="disabled")
        except queue.Empty:
            pass
        self.root.after(120, self._poll_queue)

    def _on_result(self, result: SolverResult) -> None:
        self._current_result = result
        self._exec_btn.configure(state="normal")
        self._cancel_btn.configure(state="disabled")
        self._store_btn.configure(state="normal")
        self._print_btn.configure(state="normal")

        vmark = "✅ VERIFIED" if result.verified else "❌ FAILED"
        lines = [
            "═" * 70,
            "  SOLUTION FOUND",
            "═" * 70,
            "",
            f"  Groups Found: {result.num_groups}",
            f"  Time Elapsed: {result.elapsed:.2f}s",
            f"  Verification: {vmark}",
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
        
        self._result_text.delete("0.0", "end")
        self._result_text.insert("0.0", "\n".join(lines))

        p = self._params
        self._file_lbl.set(
            f"📄 {p['m']}-{p['n']}-{p['k']}-{p['j']}-{p['s']}-*-{result.num_groups}"
        )
        self._prog_var.set(
            f"✅ Completed: {result.num_groups} groups in {result.elapsed:.2f}s"
        )
        self._prog_bar.set(1.0)

    # ==================================================================
    # DB Browser screen
    # ==================================================================

    def _build_db_frame(self) -> None:
        self._db_frame = ctk.CTkFrame(self.root, fg_color="transparent")

        # Header
        header = ctk.CTkFrame(self._db_frame, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(20, 10))
        
        ctk.CTkLabel(
            header,
            text="📁 Database Browser",
            font=ctk.CTkFont(size=32, weight="bold")
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            header,
            text="View and manage saved results",
            font=ctk.CTkFont(size=14),
            text_color="gray50"
        ).pack(anchor="w", pady=(5, 0))

        # Scrollable container
        scroll = ctk.CTkScrollableFrame(
            self._db_frame, 
            fg_color="transparent",
            scrollbar_button_color="gray60",
            scrollbar_button_hover_color="gray50"
        )
        scroll.pack(fill="both", expand=True, padx=30, pady=(10, 20))

        # Action Buttons
        btn_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(0, 15))

        left_btns = ctk.CTkFrame(btn_frame, fg_color="transparent")
        left_btns.pack(side="left")

        ctk.CTkButton(
            left_btns, text="👁 Display",
            command=self._db_display,
            height=40, width=140,
            corner_radius=10
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            left_btns, text="🗑 Delete",
            command=self._db_delete,
            height=40, width=140,
            fg_color="#ef4444", hover_color="#dc2626",
            corner_radius=10
        ).pack(side="left")

        right_btns = ctk.CTkFrame(btn_frame, fg_color="transparent")
        right_btns.pack(side="right")
        
        ctk.CTkButton(
            right_btns, text="← Back",
            command=self._show_main,
            height=40, width=140,
            fg_color="gray40", hover_color="gray30",
            corner_radius=10
        ).pack()

        # Saved Results Card
        list_card = self._create_card(scroll, "💾 Saved Results")
        list_card.pack(fill="x", pady=(0, 15))

        list_content = ctk.CTkFrame(list_card, fg_color="transparent")
        list_content.pack(fill="x", padx=20, pady=15)

        # Use a regular frame instead of scrollable frame to avoid artifacts
        list_frame = ctk.CTkFrame(list_content, fg_color="#fafafa", corner_radius=8)
        list_frame.pack(fill="x")

        # Add scrollbar manually
        scrollbar = ctk.CTkScrollbar(list_frame, orientation="vertical")
        scrollbar.pack(side="right", fill="y", padx=(0, 2), pady=2)

        self._db_list = tk.Listbox(
            list_frame,
            height=10,
            selectmode=tk.SINGLE,
            font=("Consolas", 16, "bold"),
            bg="#fafafa",
            fg="#1f2937",
            selectbackground="#3b82f6",
            selectforeground="white",
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        scrollbar.configure(command=self._db_list.yview)
        self._db_list.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self._db_ids: list[int] = []

        # Detail View Card
        detail_card = self._create_card(scroll, "📊 Group Details")
        detail_card.pack(fill="both", expand=True)

        detail_content = ctk.CTkFrame(detail_card, fg_color="transparent")
        detail_content.pack(fill="both", expand=True, padx=20, pady=15)

        self._db_text = ctk.CTkTextbox(
            detail_content,
            height=350,
            font=ctk.CTkFont(family="Consolas", size=14),
            corner_radius=8,
            wrap="none"
        )
        self._db_text.pack(fill="both", expand=True)

    def _refresh_db_list(self) -> None:
        self._db_list.delete(0, tk.END)
        self._db_ids.clear()
        for r in self.db.list_all():
            self._db_list.insert(tk.END, r.filename)
            self._db_ids.append(r.id)

    def _selected_db_id(self) -> int | None:
        sel = self._db_list.curselection()
        if not sel:
            self._show_warning("Select", "Please select a result first.")
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
            "",
            "  Parameters:",
            f"    • Population (m): {r.m}",
            f"    • Sample Size (n): {r.n}",
            f"    • Group Size (k): {r.k}",
            f"    • Test Size (j): {r.j}",
            f"    • Threshold (s): {r.s}",
            "",
            "  Selected Samples:",
            f"    {r.samples}",
            "",
            "═" * 70,
            f"  GROUPS ({r.num_groups} total)",
            "═" * 70,
            "",
        ]
        for i, grp in enumerate(r.groups, 1):
            lines.append(f"  Group {i:3d}: {', '.join(map(str, grp))}")
        
        lines.append("")
        lines.append("═" * 70)

        self._db_text.delete("0.0", "end")
        self._db_text.insert("0.0", "\n".join(lines))

    def _db_delete(self) -> None:
        rid = self._selected_db_id()
        if rid is None:
            return
        if self._show_confirm("Confirm", "Delete this result?"):
            self.db.delete(rid)
            self._refresh_db_list()
            self._db_text.delete("0.0", "end")

    # --- Dialogs ---

    def _show_error(self, title: str, message: str) -> None:
        import tkinter.messagebox as mb
        mb.showerror(title, message)

    def _show_info(self, title: str, message: str) -> None:
        import tkinter.messagebox as mb
        mb.showinfo(title, message)

    def _show_warning(self, title: str, message: str) -> None:
        import tkinter.messagebox as mb
        mb.showwarning(title, message)

    def _show_confirm(self, title: str, message: str) -> bool:
        import tkinter.messagebox as mb
        return mb.askyesno(title, message)


if __name__ == "__main__":
    app = ModernOptimalSamplesApp()
    app.run()
