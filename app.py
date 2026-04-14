"""Tkinter GUI for the Optimal Samples Selection System."""

from __future__ import annotations

import queue
import random
import threading
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from typing import Optional

from database import ResultDatabase, SavedResult
from solver import CoveringDesignSolver, SolverProgress, SolverResult


DEFAULT_TIME_BUDGET_SEC = 100.0


class OptimalSamplesApp:
    """Main application window with parameter input, execution, and DB browser."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("An Optimal Samples Selection System")
        self.root.geometry("860x720")
        self.root.minsize(700, 600)

        self.db = ResultDatabase()
        self._q: queue.Queue[SolverProgress | SolverResult | str] = queue.Queue()
        self._thread: Optional[threading.Thread] = None
        self._cancel_flag = False
        self._time_budget_sec = DEFAULT_TIME_BUDGET_SEC
        self._run_started_at: float | None = None
        self._stop_reason = "idle"

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
        self._main_frame.pack(fill=tk.BOTH, expand=True)

    def _show_db(self) -> None:
        self._main_frame.pack_forget()
        self._db_frame.pack(fill=tk.BOTH, expand=True)
        self._refresh_db_list()

    # ==================================================================
    # Main screen
    # ==================================================================

    def _build_main_frame(self) -> None:
        self._main_frame = ttk.Frame(self.root, padding=10)

        # --- title ---
        ttk.Label(
            self._main_frame,
            text="An Optimal Samples Selection System",
            font=("Helvetica", 16, "bold"),
        ).pack(pady=(0, 8))

        # --- parameters ---
        pf = ttk.LabelFrame(self._main_frame, text="Parameters", padding=8)
        pf.pack(fill=tk.X, pady=4)

        r1 = ttk.Frame(pf)
        r1.pack(fill=tk.X, pady=2)
        self._m = self._param_entry(r1, "m (45‑54):", "45")
        self._n = self._param_entry(r1, "n (7‑25):", "8")
        self._k = self._param_entry(r1, "k (4‑7):", "6")

        r2 = ttk.Frame(pf)
        r2.pack(fill=tk.X, pady=2)
        self._j = self._param_entry(r2, "j (s≤j≤k):", "5")
        self._s = self._param_entry(r2, "s (3‑7):", "5")

        # --- sample selection mode ---
        sf = ttk.LabelFrame(self._main_frame, text="Sample Selection", padding=8)
        sf.pack(fill=tk.X, pady=4)

        self._mode = tk.StringVar(value="random")
        ttk.Radiobutton(sf, text="Random n", variable=self._mode,
                        value="random", command=self._toggle_input).pack(side=tk.LEFT)
        ttk.Radiobutton(sf, text="Input n", variable=self._mode,
                        value="input", command=self._toggle_input).pack(side=tk.LEFT, padx=16)

        self._input_box = ttk.Frame(sf)
        ttk.Label(self._input_box, text="Enter numbers (comma-separated):").pack(anchor=tk.W)
        self._samples_entry = ttk.Entry(self._input_box, width=50)
        self._samples_entry.pack(fill=tk.X)

        self._samples_lbl = ttk.Label(sf, text="", wraplength=700)
        self._samples_lbl.pack(fill=tk.X, pady=4)

        # --- buttons ---
        bf = ttk.Frame(self._main_frame)
        bf.pack(fill=tk.X, pady=4)

        self._exec_btn = ttk.Button(bf, text="Execute", command=self._on_execute)
        self._exec_btn.pack(side=tk.LEFT, padx=4)
        self._store_btn = ttk.Button(bf, text="Store", command=self._on_store,
                                     state=tk.DISABLED)
        self._store_btn.pack(side=tk.LEFT, padx=4)
        self._print_btn = ttk.Button(bf, text="Print", command=self._on_print,
                                     state=tk.DISABLED)
        self._print_btn.pack(side=tk.LEFT, padx=4)
        self._clear_btn = ttk.Button(bf, text="Clear", command=self._on_clear)
        self._clear_btn.pack(side=tk.LEFT, padx=4)
        self._cancel_btn = ttk.Button(bf, text="Cancel", command=self._on_cancel,
                                      state=tk.DISABLED)
        self._cancel_btn.pack(side=tk.LEFT, padx=4)
        ttk.Button(bf, text="DB Browser", command=self._show_db).pack(side=tk.RIGHT, padx=4)

        # --- progress ---
        self._prog_var = tk.StringVar(value="Ready")
        ttk.Label(self._main_frame, textvariable=self._prog_var).pack(fill=tk.X)
        self._prog_bar = ttk.Progressbar(self._main_frame, mode="determinate")
        self._prog_bar.pack(fill=tk.X, pady=2)

        # --- results ---
        rf = ttk.LabelFrame(self._main_frame, text="Results", padding=4)
        rf.pack(fill=tk.BOTH, expand=True, pady=4)
        self._result_text = scrolledtext.ScrolledText(rf, height=14, width=80,
                                                      state=tk.DISABLED)
        self._result_text.pack(fill=tk.BOTH, expand=True)

        self._file_lbl = tk.StringVar()
        ttk.Label(self._main_frame, textvariable=self._file_lbl,
                  font=("Courier", 10)).pack()

    @staticmethod
    def _param_entry(parent: ttk.Frame, label: str, default: str) -> tk.StringVar:
        ttk.Label(parent, text=label).pack(side=tk.LEFT, padx=(8, 2))
        var = tk.StringVar(value=default)
        ttk.Entry(parent, textvariable=var, width=6).pack(side=tk.LEFT)
        return var

    def _toggle_input(self) -> None:
        if self._mode.get() == "input":
            self._input_box.pack(fill=tk.X, pady=4)
        else:
            self._input_box.pack_forget()

    # --- actions ------------------------------------------------------

    def _on_execute(self) -> None:
        try:
            p = self._read_params()
        except ValueError as exc:
            messagebox.showerror("Invalid parameters", str(exc))
            return

        samples = self._select_samples(p)
        if samples is None:
            return

        self._current_samples = samples
        self._params = p
        self._samples_lbl.config(text=f"Selected samples: {samples}")

        self._cancel_flag = False
        self._stop_reason = "running"
        self._run_started_at = time.time()
        self._exec_btn.config(state=tk.DISABLED)
        self._store_btn.config(state=tk.DISABLED)
        self._print_btn.config(state=tk.DISABLED)
        self._cancel_btn.config(state=tk.NORMAL)
        self._set_result_text("")
        self._prog_bar["value"] = 0
        self._prog_var.set(
            f"Running with {self._time_budget_sec:.0f}s time budget"
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
        )
        self._file_lbl.set(f"Stored: {fn}")
        messagebox.showinfo("Stored", f"Saved as {fn}")

    def _on_print(self) -> None:
        """Print the current result text to a temporary file and open system print."""
        content = self._result_text.get("1.0", tk.END).strip()
        if not content:
            return
        import tempfile, subprocess, os
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", prefix="result_", delete=False
        )
        tmp.write(content)
        tmp.close()
        try:
            subprocess.Popen(["open", tmp.name])
        except Exception as exc:
            messagebox.showerror("Print", f"Could not open file: {exc}")

    def _on_clear(self) -> None:
        self._set_result_text("")
        self._prog_var.set("Ready")
        self._prog_bar["value"] = 0
        self._file_lbl.set("")
        self._current_result = None
        self._store_btn.config(state=tk.DISABLED)
        self._print_btn.config(state=tk.DISABLED)

    def _on_cancel(self) -> None:
        self._cancel_flag = True
        if self._stop_reason == "running":
            self._stop_reason = "manual_cancel"
        self._cancel_btn.config(state=tk.DISABLED)

    def _should_cancel_solver(self, started_at: float) -> bool:
        if self._cancel_flag:
            return True
        if (time.time() - started_at) >= self._time_budget_sec:
            if self._stop_reason == "running":
                self._stop_reason = "deadline"
            return True
        return False

    def _result_reason_text(self) -> str:
        if self._stop_reason == "deadline":
            return (
                f"time budget reached ({self._time_budget_sec:.0f}s); "
                "returned best-so-far legal solution"
            )
        if self._stop_reason == "manual_cancel":
            return "stopped by user; returned best-so-far legal solution"
        return "completed normal solve flow"

    # --- parameter reading --------------------------------------------

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
            messagebox.showerror("Error", "Please enter sample numbers.")
            return None
        try:
            nums = [int(x.strip()) for x in raw.split(",")]
        except ValueError:
            messagebox.showerror("Error", "All values must be integers.")
            return None
        if len(nums) != n:
            messagebox.showerror("Error", f"Expected {n} numbers, got {len(nums)}.")
            return None
        if len(set(nums)) != n:
            messagebox.showerror("Error", "Duplicate values found.")
            return None
        if any(x < 1 or x > m for x in nums):
            messagebox.showerror("Error", f"All values must be in 1..{m}.")
            return None
        return sorted(nums)

    # --- solver thread ------------------------------------------------

    def _run_solver(self) -> None:
        p = self._params
        try:
            started_at = self._run_started_at or time.time()
            solver = CoveringDesignSolver(
                n=p["n"], k=p["k"], j=p["j"], s=p["s"],
                progress_cb=lambda prog: self._q.put(prog),
                cancel_fn=lambda _t0=started_at: self._should_cancel_solver(_t0),
                num_attempts=5,
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
                    self._prog_var.set(
                        f"[{item.elapsed:.1f}s] {item.message}"
                    )
                    if item.total > 0:
                        pct = (item.total - item.remaining) / item.total * 100
                        self._prog_bar["value"] = pct
                elif isinstance(item, SolverResult):
                    self._on_result(item)
                elif isinstance(item, str):
                    self._prog_var.set(item)
                    self._exec_btn.config(state=tk.NORMAL)
                    self._cancel_btn.config(state=tk.DISABLED)
        except queue.Empty:
            pass
        self.root.after(120, self._poll_queue)

    def _on_result(self, result: SolverResult) -> None:
        self._current_result = result
        self._exec_btn.config(state=tk.NORMAL)
        self._cancel_btn.config(state=tk.DISABLED)
        self._store_btn.config(state=tk.NORMAL)
        self._print_btn.config(state=tk.NORMAL)

        vmark = "✓" if result.verified else "✗"
        first_legal = (
            f"{result.first_legal_elapsed:.2f}s"
            if result.first_legal_elapsed is not None
            else "---"
        )
        lines = [
            f"Found {result.num_groups} groups in {result.elapsed:.2f}s "
            f"(verified: {vmark})",
            f"Return mode: {self._result_reason_text()}",
            f"First legal: {first_legal}",
            ""
        ]
        samples = self._current_samples
        for i, grp in enumerate(result.groups, 1):
            nums = [samples[g] for g in grp]
            lines.append(f"  {i:3d}. {', '.join(map(str, nums))}")
        self._set_result_text("\n".join(lines))

        p = self._params
        self._file_lbl.set(
            f"{p['m']}-{p['n']}-{p['k']}-{p['j']}-{p['s']}-*-{result.num_groups}"
        )
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
                f"Done: {result.num_groups} groups in {result.elapsed:.2f}s"
            )
        self._prog_bar["value"] = 100

    # --- result text --------------------------------------------------

    def _set_result_text(self, text: str) -> None:
        self._result_text.config(state=tk.NORMAL)
        self._result_text.delete("1.0", tk.END)
        self._result_text.insert(tk.END, text)
        self._result_text.config(state=tk.DISABLED)

    # ==================================================================
    # DB Browser screen
    # ==================================================================

    def _build_db_frame(self) -> None:
        self._db_frame = ttk.Frame(self.root, padding=10)

        ttk.Label(
            self._db_frame, text="Data Base Resources",
            font=("Helvetica", 16, "bold"),
        ).pack(pady=(0, 8))

        top = ttk.Frame(self._db_frame)
        top.pack(fill=tk.X, pady=4)

        ttk.Button(top, text="Display", command=self._db_display).pack(side=tk.LEFT, padx=4)
        ttk.Button(top, text="Delete", command=self._db_delete).pack(side=tk.LEFT, padx=4)
        ttk.Button(top, text="Back", command=self._show_main).pack(side=tk.RIGHT, padx=4)

        # file list with scrollbar
        lf = ttk.LabelFrame(self._db_frame, text="Saved Results", padding=4)
        lf.pack(fill=tk.X, pady=4)

        self._db_list = tk.Listbox(lf, height=8, selectmode=tk.SINGLE)
        sb = ttk.Scrollbar(lf, orient=tk.VERTICAL, command=self._db_list.yview)
        self._db_list.config(yscrollcommand=sb.set)
        self._db_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        self._db_ids: list[int] = []

        # detail view
        df = ttk.LabelFrame(self._db_frame, text="Groups", padding=4)
        df.pack(fill=tk.BOTH, expand=True, pady=4)
        self._db_text = scrolledtext.ScrolledText(df, height=14, width=80,
                                                  state=tk.DISABLED)
        self._db_text.pack(fill=tk.BOTH, expand=True)

    def _refresh_db_list(self) -> None:
        self._db_list.delete(0, tk.END)
        self._db_ids.clear()
        for r in self.db.list_all():
            self._db_list.insert(tk.END, r.filename)
            self._db_ids.append(r.id)

    def _selected_db_id(self) -> int | None:
        sel = self._db_list.curselection()
        if not sel:
            messagebox.showwarning("Select", "Please select a result first.")
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
            f"File: {r.filename}",
            f"Params: m={r.m}, n={r.n}, k={r.k}, j={r.j}, s={r.s}",
            f"Samples: {r.samples}",
            f"Groups ({r.num_groups}):\n",
        ]
        for i, grp in enumerate(r.groups, 1):
            lines.append(f"  {i:3d}. {', '.join(map(str, grp))}")

        self._db_text.config(state=tk.NORMAL)
        self._db_text.delete("1.0", tk.END)
        self._db_text.insert(tk.END, "\n".join(lines))
        self._db_text.config(state=tk.DISABLED)

    def _db_delete(self) -> None:
        rid = self._selected_db_id()
        if rid is None:
            return
        if messagebox.askyesno("Confirm", "Delete this result?"):
            self.db.delete(rid)
            self._refresh_db_list()
            self._db_text.config(state=tk.NORMAL)
            self._db_text.delete("1.0", tk.END)
            self._db_text.config(state=tk.DISABLED)
