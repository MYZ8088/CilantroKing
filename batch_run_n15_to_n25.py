"""Advanced batch run for n=15 to 25, k=6 with progress tracking and resume capability."""

import json
import math
import time
from datetime import datetime
from pathlib import Path
from itertools import product
from database import ResultDatabase
from n_algorithms.shared.solver_core import CoveringDesignSolver


PROGRESS_FILE = "batch_progress_n15_to_n25.json"


def generate_all_cases():
    """Generate all valid cases for n=15 to 25, k=6, with all valid t values."""
    cases = []
    
    m = 45  # Fixed population size
    
    for n in range(15, 26):  # n = 15 to 25
        k = 6
        
        if n < k:
            continue
        
        for s in range(3, 8):  # s = 3 to 7
            for j in range(s, k + 1):  # j from s to k
                # Test t=1 (always valid)
                cases.append({
                    'm': m,
                    'n': n,
                    'k': k,
                    'j': j,
                    's': s,
                    't': 1,
                    'case_id': f"{m}-{n}-{k}-{j}-{s} (at least 1)",
                })
                
                # Test t=4 (only if C(j,s) >= 4)
                if math.comb(j, s) >= 4:
                    cases.append({
                        'm': m,
                        'n': n,
                        'k': k,
                        'j': j,
                        's': s,
                        't': 4,
                        'case_id': f"{m}-{n}-{k}-{j}-{s} (at least 4)",
                    })
    
    return cases


def load_progress():
    """Load progress from file."""
    if Path(PROGRESS_FILE).exists():
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {'completed': [], 'failed': [], 'start_time': None}


def save_progress(progress):
    """Save progress to file."""
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)


def is_case_completed(case, progress):
    """Check if case is already completed."""
    case_id = case['case_id']
    return case_id in progress['completed'] or case_id in progress['failed']


def run_case(case, db, time_budget=120.0):
    """Run a single case and store in database."""
    m, n, k, j, s, t = case['m'], case['n'], case['k'], case['j'], case['s'], case['t']
    case_id = case['case_id']
    
    try:
        # Create solver with 120s time budget
        start_time = time.time()
        solver = CoveringDesignSolver(
            n=n, k=k, j=j, s=s, t=t,
            time_budget_sec=120.0,  # Fixed 120s time budget
        )
        
        # Solve
        result = solver.solve()
        elapsed = time.time() - start_time
        
        if result.num_groups == 0:
            return False, f"No solution found", elapsed
        
        # Generate samples
        samples = list(range(m - n + 1, m + 1))
        
        # Convert groups
        groups_with_samples = []
        for group in result.groups:
            group_samples = [samples[idx] for idx in group]
            groups_with_samples.append(group_samples)
        
        # Store in database with t parameter
        filename = db.save(
            m=m, n=n, k=k, j=j, s=s,
            samples=samples,
            groups=groups_with_samples,
            elapsed_time=elapsed,
            solution_found_time=result.first_legal_elapsed,
            t=t,  # Now properly stored in database
        )
        
        t_info = f" (t={t})" if t > 1 else ""
        return True, f"{result.num_groups} groups{t_info}, stored as {filename}", elapsed
        
    except Exception as e:
        return False, f"Error: {str(e)}", 0.0


def print_progress_bar(current, total, bar_length=40):
    """Print a progress bar."""
    percent = current / total
    filled = int(bar_length * percent)
    bar = '█' * filled + '░' * (bar_length - filled)
    print(f"\r  Progress: [{bar}] {current}/{total} ({percent*100:.1f}%)", end='', flush=True)


def main():
    """Main batch run function."""
    print("="*70)
    print("ADVANCED BATCH RUN: n=15 to 25, k=6")
    print("="*70)
    
    # Initialize database
    db = ResultDatabase("results.db")
    
    # Generate all cases
    cases = generate_all_cases()
    
    # Load progress
    progress = load_progress()
    
    # Filter out completed cases
    remaining_cases = [c for c in cases if not is_case_completed(c, progress)]
    completed_count = len(cases) - len(remaining_cases)
    
    print(f"\nTotal cases: {len(cases)}")
    print(f"Already completed: {completed_count}")
    print(f"Remaining: {len(remaining_cases)}")
    
    if len(remaining_cases) == 0:
        print("\n✓ All cases already completed!")
        return
    
    # Show summary by n
    print("\nRemaining cases by n:")
    for n in range(15, 26):
        n_cases = [c for c in remaining_cases if c['n'] == n]
        if n_cases:
            print(f"  n={n}: {len(n_cases)} cases")
    
    # Ask for confirmation
    response = input("\nProceed with batch run? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled.")
        return
    
    # Initialize progress tracking
    if progress['start_time'] is None:
        progress['start_time'] = datetime.now().isoformat()
        save_progress(progress)
    
    # Run remaining cases
    print("\n" + "="*70)
    print("RUNNING BATCH")
    print("="*70)
    
    batch_start = time.time()
    
    for idx, case in enumerate(remaining_cases, 1):
        case_id = case['case_id']
        m, n, k, j, s, t = case['m'], case['n'], case['k'], case['j'], case['s'], case['t']
        
        # Print header
        print(f"\n[{completed_count + idx}/{len(cases)}] {case_id} (m={m}, t={t})")
        
        # Run case
        case_start = time.time()
        success, message, elapsed = run_case(case, db, time_budget=120.0)
        
        # Update progress
        if success:
            progress['completed'].append(case_id)
            status = "✓"
        else:
            progress['failed'].append(case_id)
            status = "✗"
        
        save_progress(progress)
        
        # Print result
        print(f"  {status} {message} ({elapsed:.2f}s)")
        
        # Print overall progress
        print_progress_bar(completed_count + idx, len(cases))
    
    print()  # New line after progress bar
    
    batch_time = time.time() - batch_start
    
    # Final summary
    print("\n" + "="*70)
    print("BATCH RUN COMPLETE")
    print("="*70)
    print(f"Total cases: {len(cases)}")
    print(f"Completed: {len(progress['completed'])}")
    print(f"Failed: {len(progress['failed'])}")
    print(f"Batch time: {batch_time:.2f}s ({batch_time/60:.1f} minutes)")
    if len(remaining_cases) > 0:
        print(f"Average time per case: {batch_time/len(remaining_cases):.2f}s")
    print("="*70)
    
    # Show failed cases if any
    if progress['failed']:
        print("\nFailed cases:")
        for case_id in progress['failed']:
            print(f"  - {case_id}")
    
    # Database summary
    all_results = db.list_all()
    print(f"\nDatabase now contains {len(all_results)} results")
    
    # Clean up progress file if all done
    if len(progress['completed']) + len(progress['failed']) == len(cases):
        print("\n✓ All cases processed. Progress file can be deleted.")


if __name__ == "__main__":
    main()
