"""Phone-shaped desktop app for the Optimal Samples Selection System."""

from __future__ import annotations

import queue
import random
import threading
import time
import tkinter as tk
from dataclasses import dataclass
from tkinter import messagebox, ttk
from typing import Any

from app_core import (
    SolveRequest,
    select_samples_for_request,
    serialize_solver_result,
    validate_solve_payload,
)
from database import ResultDatabase
from n_algorithms.shared.verification import result_masks, verify_masks_with_solver
from solver import CoveringDesignSolver, SolverProgress, SolverResult


PHONE_WIDTH = 430
PHONE_HEIGHT = 860
DEFAULT_PROGRESS_FLOOR = 6.0
DEFAULT_PROGRESS_CEILING = 92.0
FONT_FAMILY = "Helvetica"
MONO_FONT = "Menlo"


@dataclass(frozen=True)
class ProgressSnapshot:
    percent: float
    message: str
    detail: str


def format_progress_snapshot(progress: SolverProgress, time_budget_sec: int) -> ProgressSnapshot:
    """Return UI progress without treating missing remaining data as done."""
    elapsed = max(0.0, float(progress.elapsed))
    phase = progress.phase.replace("_", " ").strip().title() or "Running"
    message = progress.message.strip() if progress.message else phase

    if progress.total > 0 and 0 < progress.remaining <= progress.total:
        completed = progress.total - progress.remaining
        percent = max(DEFAULT_PROGRESS_FLOOR, min(DEFAULT_PROGRESS_CEILING, completed / progress.total * 100.0))
        detail = f"{completed:,}/{progress.total:,} targets covered · {elapsed:.1f}s"
        if progress.solution_size:
            detail += f" · {progress.solution_size} groups"
        return ProgressSnapshot(percent=percent, message=message, detail=detail)

    budget = max(1, int(time_budget_sec))
    percent = max(DEFAULT_PROGRESS_FLOOR, min(DEFAULT_PROGRESS_CEILING, elapsed / budget * 90.0))
    pieces = [phase, f"{elapsed:.1f}s"]
    if progress.iteration:
        pieces.insert(1, f"iteration {progress.iteration}")
    if progress.solution_size:
        pieces.append(f"{progress.solution_size} groups")
    return ProgressSnapshot(percent=percent, message=message, detail=" · ".join(pieces))


class PhoneSamplesApp:
    """A desktop-run phone-style app shell matching the PDF screens."""

    def __init__(self, db_path: str = "results.db") -> None:
        self.root = tk.Tk()
        self.root.title("An Optimal Samples Selection System")
        self.root.geometry(f"{PHONE_WIDTH}x{PHONE_HEIGHT}")
        self.root.minsize(390, 720)
        self.root.configure(bg="#f4f4f2")
        self.root.option_add("*Font", f"{FONT_FAMILY} 12")

        self.colors = {
            "bg": "#f4f4f2",
            "surface": "#ffffff",
            "muted_surface": "#fafafa",
            "input_surface": "#f7f7f5",
            "selection": "#e8f5ee",
            "text": "#202123",
            "muted": "#6b7280",
            "subtle": "#9ca3af",
            "border": "#dededb",
            "primary": "#202123",
            "secondary": "#10a37f",
            "success": "#10a37f",
            "warning": "#f2c94c",
            "danger": "#d92d20",
            "neutral": "#f1f1ee",
            "neutral_text": "#202123",
            "disabled": "#c7c7c3",
        }
        self._configure_ttk_style()
        self.db = ResultDatabase(db_path)
        self.queue: queue.Queue[SolverProgress | SolverResult | str] = queue.Queue()
        self.current_request: SolveRequest | None = None
        self.current_solver_result: SolverResult | None = None
        self.current_payload: dict[str, Any] | None = None
        self.cancel_requested = False
        self.run_started_at: float | None = None
        self.stop_reason = "idle"
        self.worker: threading.Thread | None = None
        self.db_result_ids: list[int] = []

        self._build_screens()
        self._show_solve_screen()
        self.root.after(120, self._poll_queue)

    def run(self) -> None:
        self.root.mainloop()

    def _build_screens(self) -> None:
        self.container = tk.Frame(self.root, bg=self.colors["bg"])
        self.container.pack(fill="both", expand=True)
        self.solve_screen = tk.Frame(self.container, bg=self.colors["bg"])
        self.db_screen = tk.Frame(self.container, bg=self.colors["bg"])
        self._build_solve_screen()
        self._build_db_screen()

    def _build_solve_screen(self) -> None:
        self._header(self.solve_screen, "S1")
        body, canvas = self._scroll_body(self.solve_screen)

        params = self._card(body)
        params.pack(fill="x", padx=12, pady=(0, 12))
        self._label(params, "Parameters", 17, bold=True).pack(anchor="w", padx=18, pady=(18, 2))
        self._label(params, "Set the covering design inputs from the PDF.", 11, color=self.colors["muted"]).pack(anchor="w", padx=18, pady=(0, 12))
        grid = tk.Frame(params, bg=self.colors["surface"])
        grid.pack(fill="x", padx=18, pady=(0, 12))

        self.m_var = tk.StringVar(value="45")
        self.n_var = tk.StringVar(value="8")
        self.k_var = tk.StringVar(value="6")
        self.j_var = tk.StringVar(value="5")
        self.s_var = tk.StringVar(value="5")
        self.t_var = tk.StringVar(value="1")
        self.timeout_var = tk.StringVar(value="120")
        fields = [
            ("m", self.m_var, "45 <= m <= 54"),
            ("n", self.n_var, "7 <= n <= 25"),
            ("k", self.k_var, "4 <= k <= 7"),
            ("j", self.j_var, "s <= j <= k"),
            ("s", self.s_var, "3 <= s <= 7"),
            ("at least", self.t_var, "s samples"),
            ("time", self.timeout_var, "seconds"),
        ]
        for index, (label, var, hint) in enumerate(fields):
            self._entry_field(grid, label, var, hint, index)

        self.mode_var = tk.StringVar(value="random")
        mode_row = tk.Frame(params, bg=self.colors["surface"])
        mode_row.pack(fill="x", padx=18, pady=(0, 18))
        self._radio(mode_row, "Random n", "random").pack(side="left", fill="x", expand=True, padx=(0, 5))
        self._radio(mode_row, "Input n", "manual").pack(side="left", fill="x", expand=True, padx=(5, 0))

        self.manual_card = self._card(body)
        self._label(self.manual_card, "Manual samples", 15, bold=True).pack(anchor="w", padx=18, pady=(16, 8))
        self.manual_entry = tk.Text(
            self.manual_card,
            height=4,
            wrap="word",
            font=(FONT_FAMILY, 13),
            relief="flat",
            bg=self.colors["input_surface"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            padx=10,
            pady=10,
            highlightbackground=self.colors["border"],
            highlightcolor=self.colors["secondary"],
            highlightthickness=1,
        )
        self.manual_entry.pack(fill="x", padx=18, pady=(0, 16))
        self.manual_entry.insert("1.0", "1,2,3,4,5,6,7,8")

        self.values_card = self._card(body)
        self.values_card.pack(fill="x", padx=12, pady=(0, 12))
        self._label(self.values_card, "Selected samples", 15, bold=True).pack(anchor="w", padx=18, pady=(16, 4))
        self.samples_label = self._label(self.values_card, "No samples selected", 12, color=self.colors["muted"], wrap=360)
        self.samples_label.pack(anchor="w", fill="x", padx=18, pady=(0, 16))

        results = self._card(body)
        results.pack(fill="both", expand=True, padx=12, pady=(0, 16))
        head = tk.Frame(results, bg=self.colors["surface"])
        head.pack(fill="x", padx=18, pady=(16, 8))
        self._label(head, "Results", 15, bold=True).pack(side="left")
        self.status_label = self._badge(head, "Ready")
        self.status_label.pack(side="right")
        self.filename_label = self._label(results, "No DB file yet", 11, color=self.colors["muted"], wrap=360)
        self.filename_label.pack(anchor="w", fill="x", padx=18, pady=(0, 10))
        self.progress_var = tk.DoubleVar(value=0)
        self.progress = ttk.Progressbar(results, variable=self.progress_var, maximum=100, style="App.Horizontal.TProgressbar")
        self.progress.pack(fill="x", padx=18, pady=(0, 10))
        self.progress_label = self._label(results, "Ready", 12, bold=True, wrap=360)
        self.progress_label.pack(anchor="w", fill="x", padx=18, pady=(0, 2))
        self.progress_detail_label = self._label(results, "Choose inputs, then execute.", 11, color=self.colors["muted"], wrap=360)
        self.progress_detail_label.pack(anchor="w", fill="x", padx=18, pady=(0, 12))
        self.result_box = self._listbox(results, height=10)
        self.result_box.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        self.result_box.insert(tk.END, "No result generated")

        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

        actions = self._bottom_actions(self.solve_screen)
        self.execute_button = self._button(actions, "Execute", self._execute, "primary")
        self.cancel_button = self._button(actions, "Cancel", self._cancel, "danger", disabled=True)
        self.store_button = self._button(actions, "Store", self._store, "success", disabled=True)
        self.verify_button = self._button(actions, "Verify", self._verify, "warning", disabled=True)
        self.clear_button = self._button(actions, "Clear", self._clear, "neutral")
        self.print_button = self._button(actions, "Print", self._print_details, "neutral")
        self.next_button = self._button(actions, "Next", self._show_db_screen, "secondary")
        for index, button in enumerate(
            [
                self.execute_button,
                self.cancel_button,
                self.store_button,
                self.verify_button,
                self.clear_button,
                self.print_button,
                self.next_button,
            ]
        ):
            row = index // 2
            col = index % 2
            button.grid(row=row, column=col, sticky="ew", padx=4, pady=4)
        actions.grid_columnconfigure(0, weight=1)
        actions.grid_columnconfigure(1, weight=1)

    def _build_db_screen(self) -> None:
        self._header(self.db_screen, "S2")
        body, _canvas = self._scroll_body(self.db_screen)
        db_card = self._card(body)
        db_card.pack(fill="x", padx=12, pady=(0, 12))
        top = tk.Frame(db_card, bg=self.colors["surface"])
        top.pack(fill="x", padx=18, pady=(16, 8))
        self._label(top, "Database", 16, bold=True).pack(side="left")
        self.db_count_label = self._label(db_card, "Saved DB files", 11, color=self.colors["muted"])
        self.db_count_label.pack(anchor="w", padx=18, pady=(0, 10))
        self.db_list = self._listbox(db_card, height=9, font_size=11)
        self.db_list.pack(fill="x", padx=18, pady=(0, 18))

        details = self._card(body)
        details.pack(fill="both", expand=True, padx=12, pady=(0, 16))
        self._label(details, "Selected DB result", 15, bold=True).pack(anchor="w", padx=18, pady=(16, 8))
        self.db_detail_box = self._listbox(details, height=18)
        self.db_detail_box.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        actions = self._bottom_actions(self.db_screen)
        buttons = [
            self._button(actions, "Display", self._db_display, "primary"),
            self._button(actions, "Delete", self._db_delete, "danger"),
            self._button(actions, "Back", self._show_solve_screen, "secondary"),
            self._button(actions, "Print", self._print_db_details, "neutral"),
        ]
        for index, button in enumerate(buttons):
            button.grid(row=index // 2, column=index % 2, sticky="ew", padx=4, pady=4)
        actions.grid_columnconfigure(0, weight=1)
        actions.grid_columnconfigure(1, weight=1)

    def _header(self, parent: tk.Frame, mark: str) -> None:
        header = tk.Frame(parent, bg=self.colors["bg"])
        header.pack(fill="x", padx=16, pady=(18, 12))
        self._badge(header, mark, large=True).pack(side="left", padx=(0, 10))
        title_stack = tk.Frame(header, bg=self.colors["bg"])
        title_stack.pack(side="left", fill="x", expand=True)
        self._label(title_stack, "Optimal Samples", 21, bold=True, wrap=300).pack(anchor="w")
        self._label(title_stack, "Covering design solver", 11, color=self.colors["muted"], wrap=300).pack(anchor="w", pady=(1, 0))

    def _scroll_body(self, parent: tk.Frame) -> tuple[tk.Frame, tk.Canvas]:
        frame = tk.Frame(parent, bg=self.colors["bg"])
        frame.pack(fill="both", expand=True)
        canvas = tk.Canvas(frame, bg=self.colors["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        body = tk.Frame(canvas, bg=self.colors["bg"])
        window_id = canvas.create_window((0, 0), window=body, anchor="nw")
        body.bind("<Configure>", lambda _event: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda event: canvas.itemconfigure(window_id, width=event.width))
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        return body, canvas

    def _card(self, parent: tk.Widget) -> tk.Frame:
        return tk.Frame(
            parent,
            bg=self.colors["surface"],
            highlightbackground=self.colors["border"],
            highlightthickness=1,
            bd=0,
        )

    def _configure_ttk_style(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "App.Horizontal.TProgressbar",
            troughcolor=self.colors["input_surface"],
            background=self.colors["secondary"],
            bordercolor=self.colors["border"],
            lightcolor=self.colors["secondary"],
            darkcolor=self.colors["secondary"],
            thickness=10,
        )

    def _listbox(self, parent: tk.Widget, *, height: int, font_size: int = 11) -> tk.Listbox:
        return tk.Listbox(
            parent,
            height=height,
            font=(MONO_FONT, font_size),
            relief="flat",
            bd=0,
            bg=self.colors["input_surface"],
            fg=self.colors["text"],
            highlightbackground=self.colors["border"],
            highlightcolor=self.colors["secondary"],
            highlightthickness=1,
            selectbackground=self.colors["selection"],
            selectforeground=self.colors["text"],
            activestyle="none",
        )

    def _label(
        self,
        parent: tk.Widget,
        text: str,
        size: int,
        *,
        bold: bool = False,
        color: str | None = None,
        wrap: int | None = None,
    ) -> tk.Label:
        weight = "bold" if bold else "normal"
        return tk.Label(
            parent,
            text=text,
            font=(FONT_FAMILY, size, weight),
            bg=parent.cget("bg"),
            fg=color or self.colors["text"],
            justify="left",
            wraplength=wrap or 0,
        )

    def _badge(self, parent: tk.Widget, text: str, *, large: bool = False) -> tk.Label:
        return tk.Label(
            parent,
            text=text,
            font=(FONT_FAMILY, 16 if large else 11, "bold"),
            bg=self.colors["muted_surface"],
            fg=self.colors["muted"],
            padx=11,
            pady=6 if large else 5,
            highlightbackground=self.colors["border"],
            highlightthickness=1,
        )

    def _entry_field(self, parent: tk.Frame, label: str, var: tk.StringVar, hint: str, index: int) -> None:
        row = index // 2
        col = index % 2
        field = tk.Frame(parent, bg=self.colors["surface"])
        field.grid(row=row, column=col, sticky="ew", padx=5, pady=5)
        parent.grid_columnconfigure(col, weight=1)
        self._label(field, label, 12, bold=True).pack(anchor="w")
        entry = tk.Entry(
            field,
            textvariable=var,
            font=(FONT_FAMILY, 15, "bold"),
            relief="flat",
            bd=0,
            bg=self.colors["input_surface"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            highlightbackground=self.colors["border"],
            highlightcolor=self.colors["secondary"],
            highlightthickness=1,
        )
        entry.pack(fill="x", ipady=9, pady=(4, 3))
        self._label(field, hint, 10, color=self.colors["muted"]).pack(anchor="w")

    def _radio(self, parent: tk.Widget, text: str, value: str) -> tk.Radiobutton:
        return tk.Radiobutton(
            parent,
            text=text,
            value=value,
            variable=self.mode_var,
            command=self._toggle_manual,
            bg=self.colors["muted_surface"],
            fg=self.colors["text"],
            activebackground=self.colors["selection"],
            activeforeground=self.colors["text"],
            selectcolor=self.colors["selection"],
            font=(FONT_FAMILY, 12, "bold"),
            indicatoron=False,
            relief="flat",
            bd=0,
            highlightbackground=self.colors["border"],
            highlightthickness=1,
            padx=8,
            pady=10,
        )

    def _bottom_actions(self, parent: tk.Frame) -> tk.Frame:
        actions = tk.Frame(
            parent,
            bg=self.colors["surface"],
            highlightbackground=self.colors["border"],
            highlightthickness=1,
        )
        actions.pack(fill="x", padx=12, pady=(4, 12))
        return actions

    def _button(
        self,
        parent: tk.Widget,
        text: str,
        command,
        color_key: str,
        *,
        disabled: bool = False,
    ) -> tk.Button:
        fg_by_key = {
            "neutral": self.colors["neutral_text"],
            "warning": self.colors["text"],
        }
        active_by_key = {
            "primary": "#343541",
            "secondary": "#0e8f70",
            "success": "#0e8f70",
            "warning": "#eab308",
            "danger": "#b42318",
            "neutral": "#e7e7e3",
        }
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=self.colors[color_key],
            fg=fg_by_key.get(color_key, "#ffffff"),
            activebackground=active_by_key.get(color_key, self.colors[color_key]),
            activeforeground=fg_by_key.get(color_key, "#ffffff"),
            disabledforeground="#d4d4d8",
            font=(FONT_FAMILY, 13, "bold"),
            relief="flat",
            bd=0,
            padx=8,
            pady=12,
            state="disabled" if disabled else "normal",
            cursor="hand2",
            highlightbackground=self.colors["border"],
            highlightthickness=1 if color_key == "neutral" else 0,
        )

    def _toggle_manual(self) -> None:
        if self.mode_var.get() == "manual":
            self.manual_card.pack(fill="x", padx=14, pady=(0, 12), before=self.values_card)
        else:
            self.manual_card.pack_forget()

    def _show_solve_screen(self) -> None:
        self.db_screen.pack_forget()
        self.solve_screen.pack(fill="both", expand=True)

    def _show_db_screen(self) -> None:
        self.solve_screen.pack_forget()
        self.db_screen.pack(fill="both", expand=True)
        self._refresh_db_list()

    def _payload_from_form(self) -> dict[str, Any]:
        samples = self.manual_entry.get("1.0", "end").strip()
        return {
            "m": self.m_var.get(),
            "n": self.n_var.get(),
            "k": self.k_var.get(),
            "j": self.j_var.get(),
            "s": self.s_var.get(),
            "t": self.t_var.get(),
            "timeout": self.timeout_var.get(),
            "mode": self.mode_var.get(),
            "samples": samples,
        }

    def _execute(self) -> None:
        if self.worker is not None and self.worker.is_alive():
            return
        try:
            request = validate_solve_payload(self._payload_from_form())
            selected_samples = select_samples_for_request(request, random.Random())
            request = SolveRequest(
                population_size=request.population_size,
                sample_size=request.sample_size,
                group_size=request.group_size,
                test_size=request.test_size,
                threshold=request.threshold,
                cover_count=request.cover_count,
                timeout_sec=request.timeout_sec,
                selection_mode=request.selection_mode,
                selected_samples=selected_samples,
            )
        except ValueError as exc:
            messagebox.showerror("Invalid input", str(exc))
            return

        self.current_request = request
        self.current_solver_result = None
        self.current_payload = None
        self.cancel_requested = False
        self.stop_reason = "running"
        self.run_started_at = time.time()
        self.samples_label.config(text=", ".join(str(value) for value in request.selected_samples))
        self.result_box.delete(0, tk.END)
        self.result_box.insert(tk.END, "Running...")
        self.filename_label.config(text="No DB file yet")
        self.status_label.config(text="Running")
        self.progress_label.config(text="Starting solver")
        self.progress_detail_label.config(text="Preparing candidates and constraints")
        self.progress_var.set(DEFAULT_PROGRESS_FLOOR)
        self.execute_button.config(state="disabled")
        self.cancel_button.config(state="normal")
        self.store_button.config(state="disabled")
        self.verify_button.config(state="disabled")
        self.worker = threading.Thread(target=self._run_solver, daemon=True)
        self.worker.start()

    def _run_solver(self) -> None:
        request = self.current_request
        if request is None:
            return
        started_at = self.run_started_at or time.time()
        try:
            solver = CoveringDesignSolver(
                n=request.sample_size,
                k=request.group_size,
                j=request.test_size,
                s=request.threshold,
                t=request.cover_count,
                progress_cb=lambda progress: self.queue.put(progress),
                cancel_fn=lambda: self._should_cancel(started_at, request.timeout_sec),
                num_attempts=5,
                time_budget_sec=float(request.timeout_sec),
                skip_final_verify=True,
            )
            result = solver.solve()
            if self.stop_reason == "running":
                self.stop_reason = "completed"
            self.queue.put(result)
        except Exception as exc:
            self.queue.put(f"Error: {exc}")

    def _should_cancel(self, started_at: float, timeout_sec: int) -> bool:
        if self.cancel_requested:
            self.stop_reason = "manual_cancel"
            return True
        if time.time() - started_at >= timeout_sec:
            self.stop_reason = "deadline"
            return True
        return False

    def _poll_queue(self) -> None:
        try:
            while True:
                item = self.queue.get_nowait()
                if isinstance(item, SolverProgress):
                    self._on_progress(item)
                elif isinstance(item, SolverResult):
                    self._on_result(item)
                else:
                    self._on_error(item)
        except queue.Empty:
            pass
        self.root.after(120, self._poll_queue)

    def _on_progress(self, progress: SolverProgress) -> None:
        request = self.current_request
        time_budget_sec = request.timeout_sec if request is not None else 120
        snapshot = format_progress_snapshot(progress, time_budget_sec)
        self.progress_var.set(snapshot.percent)
        self.progress_label.config(text=snapshot.message)
        self.progress_detail_label.config(text=snapshot.detail)

    def _on_result(self, result: SolverResult) -> None:
        request = self.current_request
        if request is None:
            return
        self.current_solver_result = result
        run_number = self.db.count_by_params(
            request.population_size,
            request.sample_size,
            request.group_size,
            request.test_size,
            request.threshold,
        ) + 1
        self.current_payload = serialize_solver_result(
            request=request,
            solver_result=result,
            run_number=run_number,
            stop_reason=self.stop_reason,
        )
        self._render_payload(self.current_payload)
        self.status_label.config(text="Done" if self.stop_reason == "completed" else "Stopped")
        self.progress_label.config(text=f"Generated {result.num_groups} groups")
        self.progress_detail_label.config(text=f"Completed in {result.elapsed:.2f}s · verify before storing")
        self.progress_var.set(100)
        self.execute_button.config(state="normal")
        self.cancel_button.config(state="disabled")
        self.verify_button.config(state="normal")

    def _on_error(self, message: str) -> None:
        self.result_box.delete(0, tk.END)
        self.result_box.insert(tk.END, message)
        self.status_label.config(text="Failed")
        self.progress_label.config(text=message)
        self.progress_detail_label.config(text="Fix the input or try a smaller case")
        self.execute_button.config(state="normal")
        self.cancel_button.config(state="disabled")

    def _render_payload(self, payload: dict[str, Any]) -> None:
        self.filename_label.config(text=str(payload["filename"]))
        self.result_box.delete(0, tk.END)
        self.result_box.insert(tk.END, f"{payload['num_groups']} groups found")
        self.result_box.insert(tk.END, f"Verified: {'yes' if payload['verified'] else 'pending'}")
        self.result_box.insert(tk.END, "")
        for index, group in enumerate(payload["groups"], 1):
            self.result_box.insert(tk.END, f"{index:03d}: {', '.join(map(str, group))}")

    def _cancel(self) -> None:
        self.cancel_requested = True
        self.cancel_button.config(state="disabled")
        self.progress_label.config(text="Cancel requested")
        self.progress_detail_label.config(text="The solver will stop at the next safe checkpoint")

    def _verify(self) -> None:
        request = self.current_request
        solver_result = self.current_solver_result
        payload = self.current_payload
        if request is None or solver_result is None or payload is None:
            return
        outcome = verify_masks_with_solver(
            n=request.sample_size,
            k=request.group_size,
            j=request.test_size,
            s=request.threshold,
            t=request.cover_count,
            masks=result_masks(solver_result),
        )
        self.current_payload = {
            **payload,
            "verified": outcome.verified,
            "verification": {
                "method": outcome.method,
                "elapsed_sec": round(float(outcome.elapsed_sec), 6),
            },
        }
        self._render_payload(self.current_payload)
        self.store_button.config(state="normal" if outcome.verified else "disabled")
        self.verify_button.config(state="disabled" if outcome.verified else "normal")
        messagebox.showinfo("Verify", "Verification passed" if outcome.verified else "Verification failed")

    def _store(self) -> None:
        request = self.current_request
        payload = self.current_payload
        if request is None or payload is None:
            return
        if not payload.get("verified"):
            messagebox.showwarning("Store", "Verify the result successfully before storing it")
            return
        stored_filename = self.db.save(
            request.population_size,
            request.sample_size,
            request.group_size,
            request.test_size,
            request.threshold,
            list(request.selected_samples),
            payload["groups"],
            float(payload["elapsed_sec"]),
            payload["first_legal_elapsed_sec"],
        )
        self.current_payload = {**payload, "filename": stored_filename, "stored_filename": stored_filename}
        self.filename_label.config(text=stored_filename)
        self.store_button.config(state="disabled")
        messagebox.showinfo("Store", f"Stored: {stored_filename}")

    def _clear(self) -> None:
        self.current_solver_result = None
        self.current_payload = None
        self.samples_label.config(text="No samples selected")
        self.filename_label.config(text="No DB file yet")
        self.status_label.config(text="Ready")
        self.progress_label.config(text="Ready")
        self.progress_detail_label.config(text="Choose inputs, then execute.")
        self.progress_var.set(0)
        self.result_box.delete(0, tk.END)
        self.result_box.insert(tk.END, "No result generated")
        self.store_button.config(state="disabled")
        self.verify_button.config(state="disabled")

    def _print_details(self) -> None:
        if self.current_payload is None:
            messagebox.showinfo("Print", "No result to print")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append("\n".join(self.result_box.get(0, tk.END)))
        messagebox.showinfo("Print", "Result details copied to clipboard")

    def _refresh_db_list(self) -> None:
        self.db_list.delete(0, tk.END)
        self.db_result_ids.clear()
        results = self.db.list_all()
        self.db_count_label.config(text=f"{len(results)} saved DB files")
        for result in results:
            self.db_list.insert(tk.END, result.filename)
            self.db_result_ids.append(result.id)

    def _selected_db_id(self) -> int | None:
        selection = self.db_list.curselection()
        if not selection:
            messagebox.showwarning("Database", "Select a DB file first")
            return None
        return self.db_result_ids[int(selection[0])]

    def _db_display(self) -> None:
        result_id = self._selected_db_id()
        if result_id is None:
            return
        saved = self.db.load(result_id)
        if saved is None:
            messagebox.showerror("Database", "Result not found")
            return
        self.db_detail_box.delete(0, tk.END)
        self.db_detail_box.insert(tk.END, saved.filename)
        self.db_detail_box.insert(tk.END, f"Created: {saved.created_at}")
        self.db_detail_box.insert(tk.END, f"m={saved.m}, n={saved.n}, k={saved.k}, j={saved.j}, s={saved.s}")
        self.db_detail_box.insert(tk.END, f"Samples: {', '.join(map(str, saved.samples))}")
        self.db_detail_box.insert(tk.END, "")
        for index, group in enumerate(saved.groups, 1):
            self.db_detail_box.insert(tk.END, f"{index:03d}: {', '.join(map(str, group))}")

    def _db_delete(self) -> None:
        result_id = self._selected_db_id()
        if result_id is None:
            return
        if not messagebox.askyesno("Delete", "Delete selected DB file?"):
            return
        self.db.delete(result_id)
        self._refresh_db_list()
        self.db_detail_box.delete(0, tk.END)

    def _print_db_details(self) -> None:
        values = self.db_detail_box.get(0, tk.END)
        if not values:
            messagebox.showinfo("Print", "No DB result to print")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append("\n".join(values))
        messagebox.showinfo("Print", "DB details copied to clipboard")


def main() -> None:
    app = PhoneSamplesApp()
    app.run()


if __name__ == "__main__":
    main()