"""View batch run results from database."""

from database import ResultDatabase
from collections import defaultdict


def main():
    """View batch results."""
    db = ResultDatabase("results.db")
    
    # Load all results
    results = db.list_all()
    
    if not results:
        print("No results in database.")
        return
    
    print("="*70)
    print(f"DATABASE RESULTS ({len(results)} total)")
    print("="*70)
    
    # Group by n
    by_n = defaultdict(list)
    for r in results:
        by_n[r.n].append(r)
    
    # Summary by n
    print("\nSummary by n:")
    print(f"{'n':<4} {'Count':<8} {'Avg Groups':<12} {'Avg Time (s)':<15}")
    print("-"*70)
    
    for n in sorted(by_n.keys()):
        n_results = by_n[n]
        avg_groups = sum(r.num_groups for r in n_results) / len(n_results)
        avg_time = sum(r.elapsed_time for r in n_results) / len(n_results)
        print(f"{n:<4} {len(n_results):<8} {avg_groups:<12.1f} {avg_time:<15.2f}")
    
    # Detailed results
    print("\n" + "="*70)
    print("DETAILED RESULTS")
    print("="*70)
    
    for n in sorted(by_n.keys()):
        print(f"\n--- n={n} ---")
        n_results = sorted(by_n[n], key=lambda r: (r.k, r.j, r.s))
        
        for r in n_results:
            t_info = f", t={r.t}" if r.t > 1 else ""
            print(f"  L({r.n},{r.k},{r.j},{r.s}{t_info}): {r.num_groups} groups, {r.elapsed_time:.2f}s - {r.filename}")
    
    # Statistics
    print("\n" + "="*70)
    print("STATISTICS")
    print("="*70)
    
    all_groups = [r.num_groups for r in results]
    all_times = [r.elapsed_time for r in results]
    
    print(f"Total results: {len(results)}")
    print(f"Groups: min={min(all_groups)}, max={max(all_groups)}, avg={sum(all_groups)/len(all_groups):.1f}")
    print(f"Time: min={min(all_times):.2f}s, max={max(all_times):.2f}s, avg={sum(all_times)/len(all_times):.2f}s")
    
    # Find interesting cases
    print("\n" + "="*70)
    print("INTERESTING CASES")
    print("="*70)
    
    # Fastest
    fastest = min(results, key=lambda r: r.elapsed_time)
    t_info = f", t={fastest.t}" if fastest.t > 1 else ""
    print(f"Fastest: L({fastest.n},{fastest.k},{fastest.j},{fastest.s}{t_info}) - {fastest.elapsed_time:.2f}s")
    
    # Slowest
    slowest = max(results, key=lambda r: r.elapsed_time)
    t_info = f", t={slowest.t}" if slowest.t > 1 else ""
    print(f"Slowest: L({slowest.n},{slowest.k},{slowest.j},{slowest.s}{t_info}) - {slowest.elapsed_time:.2f}s")
    
    # Most groups
    most_groups = max(results, key=lambda r: r.num_groups)
    t_info = f", t={most_groups.t}" if most_groups.t > 1 else ""
    print(f"Most groups: L({most_groups.n},{most_groups.k},{most_groups.j},{most_groups.s}{t_info}) - {most_groups.num_groups} groups")
    
    # Fewest groups
    fewest_groups = min(results, key=lambda r: r.num_groups)
    t_info = f", t={fewest_groups.t}" if fewest_groups.t > 1 else ""
    print(f"Fewest groups: L({fewest_groups.n},{fewest_groups.k},{fewest_groups.j},{fewest_groups.s}{t_info}) - {fewest_groups.num_groups} groups")
    
    print("="*70)


if __name__ == "__main__":
    main()
