from __future__ import annotations

import argparse
import csv
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.validate_all import (
    DEFAULT_BASELINE,
    FIELDNAMES,
    Case,
    failed_row,
    iter_selected_cases,
    load_baselines,
    run_case,
)

RUN_FIELDNAMES = ["run_index", "input_case_id", *FIELDNAMES]
TRIMMED_FIELDNAMES = [
    "run_index",
    "case_order",
    "case_id",
    "baseline_blocks",
    "actual_blocks",
    "ratio_to_baseline",
    "solve_elapsed_sec",
    "verify_elapsed_sec",
    "elapsed_sec",
    "verified",
]
TIME_FIELDNAMES = [
    "run_index",
    "case_order",
    "case_id",
    "solve_elapsed_sec",
    "verify_elapsed_sec",
    "elapsed_sec",
]


@dataclass(frozen=True)
class RunTask:
    run_index: int
    input_case_id: str
    case: Case


def build_tasks(raw_case_ids: list[str], *, repeat: int, baseline_path: Path, t: int) -> list[RunTask]:
    baselines = load_baselines(baseline_path)
    selected_cases = tuple(zip(raw_case_ids, iter_selected_cases(baselines, raw_case_ids, t=t)))
    return [
        RunTask(run_index=run_index, input_case_id=raw_case_id, case=case)
        for run_index in range(1, repeat + 1)
        for raw_case_id, case in selected_cases
    ]


def add_run_metadata(task: RunTask, row: dict[str, object]) -> dict[str, object]:
    output_row = {"run_index": task.run_index, "input_case_id": task.input_case_id, **row}
    return {field: output_row.get(field, "") for field in RUN_FIELDNAMES}


def failed_run_row(task: RunTask, error: str) -> dict[str, object]:
    return add_run_metadata(task, failed_row(task.case, error))


def int_value(value: object) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def row_sort_key(row: dict[str, object]) -> tuple[int, int, str]:
    return (int_value(row.get("case_order")), int_value(row.get("run_index")), str(row.get("case_id", "")))


def print_status(row: dict[str, object]) -> None:
    status = "ok" if row["verified"] and not row["error"] and not row["verify_error"] else "check"
    print(
        f"run={row['run_index']} {row['case_id']} {status}: "
        f"baseline={row['baseline_blocks']} actual={row['actual_blocks']} "
        f"ratio={row['ratio_to_baseline']} total={row['elapsed_sec']}s"
    )


def run_tasks(tasks: list[RunTask], *, time_limit: float, attempts: int, workers: int, verify: bool) -> list[dict[str, object]]:
    if workers == 1:
        rows = []
        for task in tasks:
            try:
                row = add_run_metadata(task, run_case(task.case, time_limit, attempts, verify))
            except Exception as exc:
                row = failed_run_row(task, str(exc))
            rows.append(row)
            print_status(row)
        return rows

    rows: list[dict[str, object]] = []
    completed_tasks: set[RunTask] = set()
    try:
        with ProcessPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(run_case, task.case, time_limit, attempts, verify): task
                for task in tasks
            }
            for future in as_completed(futures):
                task = futures[future]
                try:
                    row = add_run_metadata(task, future.result())
                except Exception as exc:
                    row = failed_run_row(task, str(exc))
                rows.append(row)
                completed_tasks.add(task)
                print_status(row)
    except Exception as exc:
        for task in tasks:
            if task not in completed_tasks:
                row = failed_run_row(task, str(exc))
                rows.append(row)
                print_status(row)
    return rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def write_outputs(rows: list[dict[str, object]], *, output: Path, per_n_dir: Path | None) -> None:
    sorted_rows = sorted(rows, key=row_sort_key)
    write_csv(output, RUN_FIELDNAMES, sorted_rows)
    write_csv(output.with_name(f"{output.stem}_sorted_trimmed.csv"), TRIMMED_FIELDNAMES, sorted_rows)
    write_csv(output.with_name(f"{output.stem}_sorted_time.csv"), TIME_FIELDNAMES, sorted_rows)

    target_per_n_dir = per_n_dir or output.with_name(f"{output.stem}_by_n")
    grouped_rows: dict[int, list[dict[str, object]]] = {}
    for row in sorted_rows:
        grouped_rows.setdefault(int(row["n"]), []).append(row)
    for n, n_rows in grouped_rows.items():
        write_csv(target_per_n_dir / f"n{n:02d}.csv", RUN_FIELDNAMES, n_rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rerun selected covering-design cases, optionally repeated")
    parser.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--per-n-dir", type=Path)
    parser.add_argument("--time-limit", type=float, default=120.0)
    parser.add_argument("--attempts", type=int, default=5)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument("--no-verify", action="store_true")
    parser.add_argument("--t", type=int, default=1)
    parser.add_argument("--case-ids", nargs="+", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.workers < 1:
        raise ValueError("--workers must be at least 1")
    if args.repeat < 1:
        raise ValueError("--repeat must be at least 1")

    tasks = build_tasks(args.case_ids, repeat=args.repeat, baseline_path=args.baseline, t=args.t)
    print(f"Running {len(tasks)} selected tasks with {args.workers} workers")
    rows = run_tasks(
        tasks,
        time_limit=args.time_limit,
        attempts=args.attempts,
        workers=args.workers,
        verify=not args.no_verify,
    )
    write_outputs(rows, output=args.output, per_n_dir=args.per_n_dir)
    print(f"Saved {args.output}")
    print(f"Saved {args.output.with_name(f'{args.output.stem}_sorted_trimmed.csv')}")
    print(f"Saved {args.output.with_name(f'{args.output.stem}_sorted_time.csv')}")
    print(f"Saved {args.per_n_dir or args.output.with_name(f'{args.output.stem}_by_n')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())