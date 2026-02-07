import os
import hashlib
import json
import sys

# --- Configuration & Colors ---
DB_FILE = "file_hashes.json"

# ANSI Escape Sequences for terminal colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

ST_ALERT = f"{BOLD}{RED}[ ALERT ]{RESET}"
ST_OK    = f"{BOLD}{GREEN}[ OK ]{RESET}"
ST_ERROR  = f"{BOLD}{RED}[ ERROR ]{RESET}"
ST_INFO  = f"{BOLD}{CYAN}[ INFO ]{RESET}"
ST_WARN  = f"{BOLD}{YELLOW}[ WARN ]{RESET}"


# Gradient color function for the banner
def gradient_text(text, start_color, end_color):
    """
    Applies a gradient from start_color to end_color across the text.
    Uses ANSI 256-color codes for smooth transitions.
    """
    lines = text.split('\n')
    result = []
    
    # Blue to pink gradient colors (256-color palette)
    # 33=blue, 69=light blue, 105=purple, 141=magenta, 177=pink, 213=hot pink, 219=rose
    gradient_colors = [33, 69, 75, 111, 147, 183, 219, 225, 218, 212, 206, 200, 199]
    
    for i, line in enumerate(lines):
        if line.strip():  # Only colorize non-empty lines
            color_idx = min(i, len(gradient_colors) - 1)
            color_code = gradient_colors[color_idx]
            result.append(f"\033[38;5;{color_code}m{line}{RESET}")
        else:
            result.append(line)
    
    return '\n'.join(result)

# A cool banner with gradient
BANNER_TEXT = r"""
  ██╗   ██╗███████╗██████╗ ██╗████████╗ █████╗ ███████╗
  ██║   ██║██╔════╝██╔══██╗██║╚══██╔══╝██╔══██╗██╔════╝
  ██║   ██║█████╗  ██████╔╝██║   ██║   ███████║███████╗
  ╚██╗ ██╔╝██╔══╝  ██╔══██╗██║   ██║   ██╔══██║╚════██║
   ╚████╔╝ ███████╗██║  ██║██║   ██║   ██║  ██║███████║
    ╚═══╝  ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝
     { F I L E   I N T E G R I T Y   C H E C K E R }
"""


BANNER = gradient_text(BANNER_TEXT, 33, 225)

def get_file_hash(path):
    """
    Calculates the SHA-256 hash of a file.
    Uses 4096-byte chunks to be memory-efficient for large logs.
    """
    sha256 = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception:
        return None

def load_db():
    """Loads the existing hash baseline from the JSON file."""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_db(data):
    """Saves the current hash dictionary to JSON with 4-space indentation."""
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def init_path(path):
    """
    Scans a directory or file to create the initial baseline.
    Uses os.walk to recursively find all files in sub-folders.
    """
    hashes = {}
    print(f"{ST_INFO} Initializing baseline for: {BOLD}{path}{RESET}")
    
    if os.path.isfile(path):
        hashes[path] = get_file_hash(path)
    elif os.path.isdir(path):
        for root, _, files in os.walk(path):
            for name in files:
                # Combine directory and filename into a full path
                filepath = os.path.join(root, name)
                hashes[filepath] = get_file_hash(filepath)
    else:
        print(f"{ST_ERROR} {path} is not valid.{RESET}")
        return

    save_db(hashes)
    print(f"{ST_OK} Baseline initialized for {GREEN}{BOLD}{len(hashes)}{RESET} file(s).")

def check_integrity():
    """Compares current file hashes against the 'Truth' in our JSON file.""" 
    db = load_db()

    if not db:
        print(f"{ST_WARN} No baseline found. Run 'init' first.{RESET}")
        return

    status = {
        "ok": 0,
        "modified": 0,
        "missing": 0,
        "total": len(db)
    }

    print(f"{ST_INFO} Checking integrity...{RESET}")
    
    for path, old_hash in db.items():
        if not os.path.exists(path):
            print(f"{ST_ERROR} MISSING: {path}{RESET}")
            status["missing"] += 1
            continue
        
        current_hash = get_file_hash(path)
        if current_hash == old_hash:
            print(f"{ST_OK} Unmodified: {BOLD}{path}{RESET}")
            status["ok"] += 1
        else:
            print(f"{ST_ALERT} Modified: {BOLD}{path}{RESET}")
            status["modified"] += 1

    print("\n" + "="*40)
    print(f"{BOLD}SCAN COMPLETED{RESET}")
    print("=" * 40)
    print(f"Total Scanned: {BOLD}{status['total']}{RESET}")
    print(f" {GREEN}✔ OK:{RESET}       {status['ok']}")
    print(f" {RED}✖ Modified:{RESET}   {status['modified']}")
    print(f" {YELLOW}⚠ Missing:{RESET} {status['missing']}")
    print("="*40)

def update_file(path):
    """Updates the baseline for a specific file or all files within a directory."""
    db = load_db()
    if not os.path.exists(path):
        print(f"{ST_ERROR} Path {path} not found.{RESET}")
        return

    if os.path.isfile(path):
        # Update a single file
        db[path] = get_file_hash(path)
        print(f"{ST_INFO} Hash updated successfully for file: {BOLD}{path}{RESET}")
    elif os.path.isdir(path):
        # Update all files in the directory recursively
        print(f"{ST_INFO} Updating all files in directory: {BOLD}{path}{RESET}")
        
        count = 0
        for root, _, files in os.walk(path):
            for name in files:
                filepath = os.path.join(root, name)
                db[filepath] = get_file_hash(filepath)
                count += 1
        print(f"{ST_OK} Updated {GREEN}{BOLD}{count}{RESET} file(s) inside {BOLD}{path}{RESET}")
    
    save_db(db)

def main():
    """Main Entry point: Handles CLI arguments and logic flow."""
    if len(sys.argv) < 2:
        print(BANNER)
        print(f" {BOLD}USAGE{RESET}")
        print(f"  $ python3 {sys.argv[0]} <command> [path]\n")
        
        print(f" {BOLD}COMMANDS{RESET}")
        print(f"  {CYAN}init{RESET}    <path>   Establish a new security baseline for a file or directory")
        print(f"  {CYAN}check{RESET}            Scan and verify the integrity of all monitored files")
        print(f"  {CYAN}update{RESET}  <path>   Synchronize the baseline with intentional file changes")
        
        print(f"\n {BOLD}EXAMPLES{RESET}")
        print(f"  $ python3 {sys.argv[0]} init ./src")
        print(f"  $ python3 {sys.argv[0]} check")
       
        return

    action = sys.argv[1].lower()
    
    if action == "init" and len(sys.argv) > 2:
        init_path(sys.argv[2])
    elif action == "check":
        check_integrity()
    elif action == "update" and len(sys.argv) > 2:
        update_file(sys.argv[2])
    else:
        print(f"{ST_ERROR} Invalid command or missing path.{RESET}")

if __name__ == "__main__":
    main()