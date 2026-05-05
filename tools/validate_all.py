from __future__ import annotations

import argparse
import csv
import json
import math
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from n_algorithms.shared.verification import result_masks, verify_masks_with_solver
from database import ResultDatabase
from solver import CoveringDesignSolver

DEFAULT_BASELINE = ROOT / "n_algorithms" / "shared" / "baselines" / "coveringrepo_n_lt_26_baselines.json"
DEFAULT_OUTPUT = ROOT / "results" / "full_validation_n_7_25.csv"
DEFAULT_WORKERS = 5
FIELDNAMES = [
    "case_order",
    "case_id",
    "n",
    "k",
    "j",
    "s",
    "t",
    "baseline_blocks",
    "actual_blocks",
    "ratio_to_baseline",
    "error_pct",
    "solve_elapsed_sec",
    "verify_elapsed_sec",
    "elapsed_sec",
    "verified",
    "verify_method",
    "route_module",
    "solution_source",
    "error",
    "verify_error",
]


@dataclass(frozen=True)
class Case:
    order: int
    n: int
    k: int
    j: int
    s: int
    baseline: int | None
    t: int = 1

    @property
    def case_id(self) -> str:
        return f"L_{self.n}_{self.k}_{self.j}_{self.s}"


def load_baselines(path: Path) -> dict[tuple[int, int, int, int], int]:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    cases = payload.get("cases", [])
    baselines: dict[tuple[int, int, int, int], int] = {}
    for item in cases:
        key = (int(item["n"]), int(item["k"]), int(item["j"]), int(item["s"]))
        baselines[key] = int(item["baseline_blocks"])
    return baselines


def iter_cases(
    baselines: dict[tuple[int, int, int, int], int],
    *,
    n_min: int,
    n_max: int,
    t: int,
) -> Iterable[Case]:
    order = 0
    for n in range(n_min, n_max + 1):
        for k in range(4, min(7, n) + 1):
            for s in range(3, min(7, k) + 1):
                for j in range(s, k + 1):
                    order += 1
                    baseline = baselines.get((n, k, j, s))
                    if baseline is None and n == k:
                        baseline = 1
                    if baseline is None and k == j == s:
                        baseline = math.comb(n, k)
                    yield Case(order=order, n=n, k=k, j=j, s=s, baseline=baseline, t=t)


def parse_case_id(raw_case_id: str) -> tuple[int, int, int, int]:
    value = raw_case_id.strip()
    if not value:
        raise ValueError("empty case id")
    if value.startswith("L_"):
        parts = value.split("_")[1:]
    elif "_" in value:
        parts = value.split("_")
    else:
        if len(value) < 4 or not value.isdigit():
            raise ValueError(f"invalid compact case id: {raw_case_id}")
        parts = [value[:-3], value[-3], value[-2], value[-1]]
    if len(parts) != 4 or any(not part.isdigit() for part in parts):
        raise ValueError(f"invalid case id: {raw_case_id}")
    n, k, j, s = (int(part) for part in parts)
    if n < k or not (3 <= s <= j <= k):
        raise ValueError(f"invalid case parameters from {raw_case_id}: L({n},{k},{j},{s})")
    return n, k, j, s


def iter_selected_cases(
    baselines: dict[tuple[int, int, int, int], int],
    raw_case_ids: list[str],
    *,
    t: int,
) -> Iterable[Case]:
    all_cases = {
        (case.n, case.k, case.j, case.s): case
        for case in iter_cases(baselines, n_min=7, n_max=25, t=t)
    }
    for raw_case_id in raw_case_ids:
        key = parse_case_id(raw_case_id)
        case = all_cases.get(key)
        if case is None:
            n, k, j, s = key
            baseline = baselines.get(key)
            if baseline is None and n == k:
                baseline = 1
            if baseline is None and k == j == s:
                baseline = math.comb(n, k)
            case = Case(order=0, n=n, k=k, j=j, s=s, baseline=baseline, t=t)
        yield case


def run_case(case: Case, time_limit: float, attempts: int, verify: bool) -> dict[str, object]:
    started_at = time.time()
    error = ""
    verify_error = ""
    route_module = ""
    solution_source = ""
    verify_method = ""
    solve_elapsed = 0.0
    verify_elapsed = 0.0
    num_groups: int | None = None
    verified = False
    try:
        solve_started_at = time.time()
        solver = CoveringDesignSolver(
            n=case.n,
            k=case.k,
            j=case.j,
            s=case.s,
            t=case.t,
            num_attempts=attempts,
            time_budget_sec=time_limit,
            skip_final_verify=True,
        )
        result = solver.solve()
        solve_elapsed = time.time() - solve_started_at
        masks = result_masks(result)
        groups = result.preview_groups(None)
        route_module = getattr(result, "route_module", "")
        solution_source = getattr(result, "solution_source", "")
        num_groups = int(result.num_groups)
        if verify:
            try:
                verification = verify_masks_with_solver(
                    n=case.n,
                    k=case.k,
                    j=case.j,
                    s=case.s,
                    t=case.t,
                    masks=masks,
                )
                verified = verification.verified
                verify_method = verification.method
                verify_elapsed = verification.elapsed_sec
            except Exception as exc:
                verify_error = str(exc)
        else:
            verified = bool(result.verified)
    except Exception as exc:
        error = str(exc)
    elapsed = time.time() - started_at
    error_pct = ""
    ratio = ""
    if case.baseline and num_groups is not None:
        ratio_value = num_groups / case.baseline
        ratio = round(ratio_value, 6)
        error_pct = round((ratio_value - 1.0) * 100.0, 6)
    return {
        "case_order": case.order,
        "case_id": case.case_id,
        "n": case.n,
        "k": case.k,
        "j": case.j,
        "s": case.s,
        "t": case.t,
        "baseline_blocks": case.baseline if case.baseline is not None else "",
        "actual_blocks": num_groups if num_groups is not None else "",
        "ratio_to_baseline": ratio,
        "error_pct": error_pct,
        "solve_elapsed_sec": round(solve_elapsed, 6),
        "verify_elapsed_sec": round(verify_elapsed, 6),
        "elapsed_sec": round(elapsed, 6),
        "verified": verified,
        "verify_method": verify_method,
        "route_module": route_module,
        "solution_source": solution_source,
        "error": error,
        "verify_error": verify_error,
        "_groups": groups if not error else [],
        "_first_legal_elapsed": getattr(result, "first_legal_elapsed", None) if not error else None,
    }


def failed_row(case: Case, error: str) -> dict[str, object]:
    return {
        "case_order": case.order,
        "case_id": case.case_id,
        "n": case.n,
        "k": case.k,
        "j": case.j,
        "s": case.s,
        "t": case.t,
        "baseline_blocks": case.baseline if case.baseline is not None else "",
        "actual_blocks": "",
        "ratio_to_baseline": "",
        "error_pct": "",
        "solve_elapsed_sec": 0.0,
        "verify_elapsed_sec": 0.0,
        "elapsed_sec": 0.0,
        "verified": False,
        "verify_method": "",
        "route_module": "",
        "solution_source": "",
        "error": error,
        "verify_error": "",
    }


def default_per_n_dir(output: Path) -> Path:
    return output.with_name(f"{output.stem}_by_n")


class CsvOutputs:
    def __init__(self, output: Path, per_n_dir: Path) -> None:
        self._output = output
        self._per_n_dir = per_n_dir
        self._summary_handle = None
        self._summary_writer = None
        self._per_n_handles: dict[int, object] = {}
        self._per_n_writers: dict[int, csv.DictWriter] = {}

    def __enter__(self) -> "CsvOutputs":
        self._output.parent.mkdir(parents=True, exist_ok=True)
        self._per_n_dir.mkdir(parents=True, exist_ok=True)
        for path in self._per_n_dir.glob("n[0-9][0-9].csv"):
            path.unlink()
        self._summary_handle = self._output.open("w", newline="", encoding="utf-8")
        self._summary_writer = csv.DictWriter(self._summary_handle, fieldnames=FIELDNAMES)
        self._summary_writer.writeheader()
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        for handle in self._per_n_handles.values():
            handle.close()
        if self._summary_handle is not None:
            self._summary_handle.close()

    def write_row(self, row: dict[str, object]) -> None:
        if self._summary_writer is None or self._summary_handle is None:
            raise RuntimeError("CSV outputs are not open")
        csv_row = {field: row.get(field, "") for field in FIELDNAMES}
        self._summary_writer.writerow(csv_row)
        self._summary_handle.flush()
        n = int(row["n"])
        writer, handle = self._writer_for_n(n)
        writer.writerow(csv_row)
        handle.flush()

    def _writer_for_n(self, n: int) -> tuple[csv.DictWriter, object]:
        writer = self._per_n_writers.get(n)
        if writer is not None:
            return writer, self._per_n_handles[n]
        path = self._per_n_dir / f"n{n:02d}.csv"
        handle = path.open("w", newline="", encoding="utf-8")
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        self._per_n_handles[n] = handle
        self._per_n_writers[n] = writer
        return writer, handle


def save_row_to_db(row: dict[str, object], db: ResultDatabase) -> str:
    if row.get("error") or row.get("verify_error"):
        return ""

    groups = row.get("_groups")
    if not isinstance(groups, list) or not groups:
        return ""

    n = int(row["n"])
    samples = list(range(1, n + 1))
    stored_groups = [
        [int(element) + 1 for element in group]
        for group in groups
    ]
    first_legal_elapsed = row.get("_first_legal_elapsed")
    return db.save(
        n,
        n,
        int(row["k"]),
        int(row["j"]),
        int(row["s"]),
        samples,
        stored_groups,
        float(row["solve_elapsed_sec"]),
        float(first_legal_elapsed) if first_legal_elapsed is not None else None,
        t=int(row["t"]),
    )


def write_and_report_row(
    *,
    index: int,
    total: int,
    row: dict[str, object],
    outputs: CsvOutputs,
    db: ResultDatabase | None,
) -> None:
    stored_filename = save_row_to_db(row, db) if db is not None else ""
    outputs.write_row(row)
    status = (
        "ok"
        if row["verified"] and not row["error"] and not row["verify_error"]
        else "check"
    )
    print(
        f"[{index}/{total}] {row['case_id']} {status}: "
        f"baseline={row['baseline_blocks']} actual={row['actual_blocks']} "
        f"error%={row['error_pct']} solve={row['solve_elapsed_sec']}s "
        f"verify={row['verify_elapsed_sec']}s total={row['elapsed_sec']}s "
        f"db={stored_filename or '-'}"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate all n=7..25 covering-design cases")
    parser.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--per-n-dir", type=Path)
    parser.add_argument("--time-limit", type=float, default=120.0)
    parser.add_argument("--attempts", type=int, default=5)
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS)
    parser.add_argument("--no-verify", action="store_true")
    parser.add_argument("--n-min", type=int, default=7)
    parser.add_argument("--n-max", type=int, default=25)
    parser.add_argument("--t", type=int, default=1)
    parser.add_argument("--db-path", type=Path)
    parser.add_argument("--case-ids", nargs="*")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.workers < 1:
        raise ValueError("--workers must be at least 1")
    if args.n_min > args.n_max:
        raise ValueError("--n-min must be <= --n-max")
    baselines = load_baselines(args.baseline)
    if args.case_ids:
        cases = list(iter_selected_cases(baselines, args.case_ids, t=args.t))
    else:
        cases = list(iter_cases(baselines, n_min=args.n_min, n_max=args.n_max, t=args.t))
    per_n_dir = args.per_n_dir or default_per_n_dir(args.output)
    print(
        f"Running {len(cases)} cases with {args.workers} workers; "
        f"n={args.n_min}..{args.n_max}; verify={not args.no_verify}"
    )
    print(f"Aggregate CSV: {args.output}")
    print(f"Per-n CSV dir: {per_n_dir}")
    db = None
    if args.db_path is not None:
        args.db_path.parent.mkdir(parents=True, exist_ok=True)
        db = ResultDatabase(str(args.db_path))
        print(f"Result DB: {args.db_path}")
    with CsvOutputs(args.output, per_n_dir) as outputs:
        if args.workers == 1:
            for index, case in enumerate(cases, 1):
                try:
                    row = run_case(case, args.time_limit, args.attempts, not args.no_verify)
                except Exception as exc:
                    row = failed_row(case, str(exc))
                write_and_report_row(
                    index=index,
                    total=len(cases),
                    row=row,
                    outputs=outputs,
                    db=db,
                )
        else:
            with ProcessPoolExecutor(max_workers=args.workers) as executor:
                futures = {
                    executor.submit(run_case, case, args.time_limit, args.attempts, not args.no_verify): case
                    for case in cases
                }
                for index, future in enumerate(as_completed(futures), 1):
                    case = futures[future]
                    try:
                        row = future.result()
                    except Exception as exc:
                        row = failed_row(case, str(exc))
                    write_and_report_row(
                        index=index,
                        total=len(cases),
                        row=row,
                        outputs=outputs,
                        db=db,
                    )
    print(f"Saved validation CSV: {args.output}")
    print(f"Saved per-n CSV files: {per_n_dir}")
    if args.db_path is not None:
        print(f"Saved result DB: {args.db_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
