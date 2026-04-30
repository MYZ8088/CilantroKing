# Phone-Style Desktop App

Run the app-shaped desktop prototype:

```bash
python phone_app.py
```

This opens a phone-sized window with the two PDF screens:

- `S1`: parameter input, random/manual sample selection, selected values, generated groups, execute/cancel/verify/store/clear/print/next.
- `S2`: DB resource list, display/delete, selected result details, back/print.

The app calls `CoveringDesignSolver` through [solver.py](solver.py) and uses [database.py](database.py) for saved results. The algorithm modules under [n_algorithms](n_algorithms) are not changed.