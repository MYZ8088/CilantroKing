"""SQLite storage for Optimal Samples Selection results."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class SavedResult:
    id: int
    m: int
    n: int
    k: int
    j: int
    s: int
    run_number: int
    num_groups: int
    samples: list[int]
    groups: list[list[int]]
    filename: str
    created_at: str
    elapsed_time: float
    solution_found_time: float | None


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

    # --- write --------------------------------------------------------

    def save(
        self,
        m: int, n: int, k: int, j: int, s: int,
        samples: list[int],
        groups: list[list[int]],
        elapsed_time: float = 0.0,
        solution_found_time: float | None = None,
    ) -> str:
        run = self._next_run(m, n, k, j, s)
        num_groups = len(groups)
        filename = f"{m}-{n}-{k}-{j}-{s}-{run}-{num_groups}"
        with sqlite3.connect(self._path) as conn:
            conn.execute(
                "INSERT INTO results "
                "(m,n,k,j,s,run_number,num_groups,samples,groups_data,filename,elapsed_time,solution_found_time) "
                "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (m, n, k, j, s, run, num_groups,
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

    def _next_run(self, m: int, n: int, k: int, j: int, s: int) -> int:
        with sqlite3.connect(self._path) as conn:
            row = conn.execute(
                "SELECT COALESCE(MAX(run_number),0)+1 FROM results "
                "WHERE m=? AND n=? AND k=? AND j=? AND s=?",
                (m, n, k, j, s),
            ).fetchone()
        return row[0] if row else 1

    @staticmethod
    def _to_obj(row: sqlite3.Row) -> SavedResult:
        return SavedResult(
            id=row["id"],
            m=row["m"], n=row["n"], k=row["k"],
            j=row["j"], s=row["s"],
            run_number=row["run_number"],
            num_groups=row["num_groups"],
            samples=json.loads(row["samples"]),
            groups=json.loads(row["groups_data"]),
            filename=row["filename"],
            created_at=row["created_at"],
            elapsed_time=row["elapsed_time"],
            solution_found_time=row["solution_found_time"],
        )
