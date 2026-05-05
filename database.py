"""SQLite storage for Optimal Samples Selection results."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from typing import Optional

from app_core import format_result_filename


@dataclass(frozen=True)
class SavedResult:
    id: int
    m: int
    n: int
    k: int
    j: int
    s: int
    t: int
    run_number: int
    num_groups: int
    samples: list[int]
    groups: list[list[int]]
    filename: str
    created_at: str
    elapsed_time: float
    solution_found_time: float | None


@dataclass(frozen=True)
class SavedResultSummary:
    id: int
    filename: str
    created_at: str
    num_groups: int


class ResultDatabase:
    """CRUD operations for covering design results."""

    def __init__(self, db_path: str = "results.db") -> None:
        self._path = db_path
        self._init()

    def _init(self) -> None:
        with sqlite3.connect(self._path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    m           INTEGER NOT NULL,
                    n           INTEGER NOT NULL,
                    k           INTEGER NOT NULL,
                    j           INTEGER NOT NULL,
                    s           INTEGER NOT NULL,
                    t           INTEGER NOT NULL DEFAULT 1,
                    run_number  INTEGER NOT NULL,
                    num_groups  INTEGER NOT NULL,
                    samples     TEXT    NOT NULL,
                    groups_data TEXT    NOT NULL,
                    filename    TEXT    NOT NULL,
                    elapsed_time REAL   NOT NULL DEFAULT 0.0,
                    solution_found_time REAL DEFAULT NULL,
                    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            columns = {
                row[1] for row in conn.execute("PRAGMA table_info(results)").fetchall()
            }
            if "t" not in columns:
                conn.execute(
                    "ALTER TABLE results ADD COLUMN t INTEGER NOT NULL DEFAULT 1"
                )
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_results_params
                ON results (m, n, k, j, s)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_results_params_with_t
                ON results (m, n, k, j, s, t)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_results_created_at
                ON results (created_at DESC)
            """)

    # --- write --------------------------------------------------------

    def save(
        self,
        m: int, n: int, k: int, j: int, s: int,
        samples: list[int],
        groups: list[list[int]],
        elapsed_time: float = 0.0,
        solution_found_time: float | None = None,
        *,
        t: int = 1,
    ) -> str:
        run = self._next_run(m, n, k, j, s, t)
        num_groups = len(groups)
        filename = format_result_filename(
            m=m,
            n=n,
            k=k,
            j=j,
            s=s,
            t=t,
            run_number=run,
            num_groups=num_groups,
        )
        with sqlite3.connect(self._path) as conn:
            conn.execute(
                "INSERT INTO results "
                "(m,n,k,j,s,t,run_number,num_groups,samples,groups_data,filename,elapsed_time,solution_found_time) "
                "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (m, n, k, j, s, t, run, num_groups,
                 json.dumps(samples), json.dumps(groups), filename, elapsed_time, solution_found_time),
            )
        return filename

    # --- read ---------------------------------------------------------

    def list_all(self) -> list[SavedResult]:
        with sqlite3.connect(self._path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM results ORDER BY created_at DESC"
            ).fetchall()
        return [self._to_obj(r) for r in rows]

    def list_summaries(self) -> list[SavedResultSummary]:
        with sqlite3.connect(self._path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT id, filename, created_at, num_groups "
                "FROM results ORDER BY created_at DESC"
            ).fetchall()
        return [
            SavedResultSummary(
                id=row["id"],
                filename=row["filename"],
                created_at=row["created_at"],
                num_groups=row["num_groups"],
            )
            for row in rows
        ]

    def load(self, result_id: int) -> Optional[SavedResult]:
        with sqlite3.connect(self._path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM results WHERE id=?", (result_id,)
            ).fetchone()
        return self._to_obj(row) if row else None

    # --- delete -------------------------------------------------------

    def delete(self, result_id: int) -> None:
        with sqlite3.connect(self._path) as conn:
            conn.execute("DELETE FROM results WHERE id=?", (result_id,))

    # --- helpers ------------------------------------------------------

    def _next_run(self, m: int, n: int, k: int, j: int, s: int, t: int = 1) -> int:
        with sqlite3.connect(self._path) as conn:
            row = conn.execute(
                "SELECT COALESCE(MAX(run_number),0)+1 FROM results "
                "WHERE m=? AND n=? AND k=? AND j=? AND s=? AND t=?",
                (m, n, k, j, s, t),
            ).fetchone()
        return row[0] if row else 1

    def count_by_params(self, m: int, n: int, k: int, j: int, s: int, t: int = 1) -> int:
        with sqlite3.connect(self._path) as conn:
            row = conn.execute(
                "SELECT COUNT(*) FROM results "
                "WHERE m=? AND n=? AND k=? AND j=? AND s=? AND t=?",
                (m, n, k, j, s, t),
            ).fetchone()
        return int(row[0]) if row else 0

    @staticmethod
    def _to_obj(row: sqlite3.Row) -> SavedResult:
        return SavedResult(
            id=row["id"],
            m=row["m"], n=row["n"], k=row["k"],
            j=row["j"], s=row["s"],
            t=row["t"],
            run_number=row["run_number"],
            num_groups=row["num_groups"],
            samples=json.loads(row["samples"]),
            groups=json.loads(row["groups_data"]),
            filename=row["filename"],
            created_at=row["created_at"],
            elapsed_time=row["elapsed_time"],
            solution_found_time=row["solution_found_time"],
        )
