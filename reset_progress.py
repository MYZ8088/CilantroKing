"""Reset batch run progress to start from beginning."""

import os

PROGRESS_FILE = "batch_progress.json"

def main():
    if not os.path.exists(PROGRESS_FILE):
        print(f"✓ No progress file found. Batch run will start fresh.")
        return
    
    print(f"Found progress file: {PROGRESS_FILE}")
    
    response = input(f"\nDelete progress file and restart from beginning? (yes/no): ")
    
    if response.lower() != 'yes':
        print("Cancelled. Progress file kept.")
        return
    
    try:
        os.remove(PROGRESS_FILE)
        print(f"✓ Progress file deleted. Next batch run will start from beginning.")
    except Exception as e:
        print(f"✗ Error: {e}")


if __name__ == "__main__":
    main()
