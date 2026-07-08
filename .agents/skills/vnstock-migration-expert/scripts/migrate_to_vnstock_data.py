import os
import re
import argparse
import sys

def migrate_file(filepath: str, dry_run: bool = False) -> bool:
    """
    Migrates `vnstock` imports to `vnstock_data` in a given file.
    Works for both .py and .ipynb files (as simple content replacement).
    Returns True if modifications were made.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Regular expressions to match vnstock imports
        # Matches: import vnstock
        # Matches: from vnstock import XYZ
        # Does NOT match: from vnstock_data import XYZ
        
        # 1. replace `import vnstock` -> `import vnstock_data`
        # Using word boundaries \b to avoid matching vnstock_data, vnstock_ta, etc.
        pattern1 = r'\bimport vnstock\b'
        content_new, count1 = re.subn(pattern1, 'import vnstock_data', content)
        
        # 2. replace `from vnstock import` -> `from vnstock_data import`
        pattern2 = r'\bfrom vnstock import\b'
        content_new, count2 = re.subn(pattern2, 'from vnstock_data import', content_new)
        
        # 3. replace `from vnstock.` -> `from vnstock_data.`
        pattern3 = r'\bfrom vnstock\.'
        content_new, count3 = re.subn(pattern3, 'from vnstock_data.', content_new)

        total_replacements = count1 + count2 + count3

        if total_replacements > 0:
            if not dry_run:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content_new)
                print(f"✅ Migrated {filepath} ({total_replacements} replacements)")
            else:
                print(f"🔍 [DRY RUN] Would migrate {filepath} ({total_replacements} replacements)")
            return True
        return False
    except Exception as e:
        print(f"❌ Error processing {filepath}: {e}", file=sys.stderr)
        return False

def get_python_files(directory: str):
    """Recursively find all .py and .ipynb files in a directory."""
    files = []
    for root, _, filenames in os.walk(directory):
        # Skip virtual environments and hidden directories
        if any(ignored in root for ignored in ['.venv', 'venv', 'env', '.git', '__pycache__']):
            continue
        for filename in filenames:
            if filename.endswith('.py') or filename.endswith('.ipynb'):
                files.append(os.path.join(root, filename))
    return files

def main():
    parser = argparse.ArgumentParser(description="Migrate Python files from vnstock to vnstock_data.")
    parser.add_argument("target", help="File or directory to migrate")
    parser.add_argument("--dry-run", action="store_true", help="Print changes without modifying files")
    args = parser.parse_args()

    if not os.path.exists(args.target):
        print(f"Error: Target path '{args.target}' does not exist.")
        sys.exit(1)

    files_to_process = []
    if os.path.isfile(args.target):
        files_to_process.append(args.target)
    elif os.path.isdir(args.target):
        files_to_process.extend(get_python_files(args.target))

    if not files_to_process:
        print("No .py or .ipynb files found to process.")
        sys.exit(0)

    print(f"Found {len(files_to_process)} file(s) to inspect...")
    modified_count = 0
    
    for filepath in files_to_process:
        if migrate_file(filepath, args.dry_run):
            modified_count += 1

    if modified_count == 0:
        print("No vnstock imports found that needed migration.")
    else:
        print(f"---")
        mode = "Would modify" if args.dry_run else "Successfully modified"
        print(f"✨ {mode} {modified_count} file(s).")
        
        if not args.dry_run:
            print("\n> IMPORTANT: If you were moving from an older version of vnstock_data to v3.0.0+,")
            print("> you may also want to manually update your code to use the Unified UI ")
            print("> (e.g. from vnstock_data import Market, Reference, etc.).")
            print("> See docs/vnstock-data/01-unified-ui.md and docs/vnstock-data/migrations/v3.0.md for details.")

if __name__ == "__main__":
    main()
