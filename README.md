# 🛡️ VERITAS — File Integrity Checker

> **VERITAS** is a lightweight and stylish File Integrity Monitoring (FIM) tool that helps you detect unauthorized file changes using SHA-256 hashing.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)
![Type](https://img.shields.io/badge/Project-File%20Integrity%20Checker-orange?style=flat)
![Hashing](https://img.shields.io/badge/Hashing-SHA--256-purple?style=flat)
![CLI](https://img.shields.io/badge/Interface-Command%20Line-lightgrey?style=flat)
![Status](https://img.shields.io/badge/Status-Active%20Development-brightgreen?style=flat)

<img width="695" height="279" alt="banner" src="https://github.com/user-attachments/assets/242e32f2-d8d2-4c62-9d81-016218b742c0" />



---
## Features

- **SHA-256 Cryptographic Hashing**  
  Generates secure file fingerprints to detect unauthorized modifications.

- **Baseline Initialization**  
  Create an initial integrity snapshot for a single file or an entire directory.

- **Integrity Change Detection**  
  Identifies important file state changes, including:
  - Unmodified files  
  - Modified files  
  - Missing or deleted files  

- **Baseline Updating**  
  Allows intentional changes to be synchronized safely into the stored baseline.

- **JSON-Based Storage**  
  Hash records are stored locally in a simple and readable `file_hashes.json` database.

- **Clean CLI Reporting**  
  Provides structured, color-coded terminal output for quick visibility.

- **Recursive Directory Scanning**  
  Automatically monitors all files inside nested subdirectories.

## Preview

```text
[ INFO ] Checking integrity...
[ OK ] Unmodified: ./src/app.py
[ ALERT ] Modified: ./config/settings.json
[ ERROR ] MISSING: ./logs/data.log
```

---

## How It Works

VERITAS operates in 3 main phases:

### 1. Initialize Baseline (`init`)
Creates a trusted “truth database” of file hashes.

### 2. Integrity Scan (`check`)
Recomputes hashes and compares them against the baseline.

### 3. Update Baseline (`update`)
Synchronizes hashes after legitimate edits.

All hashes are stored in:

```bash
file_hashes.json
```

---

## Installation

Clone the project:

```bash
git clone https://github.com/yourusername/veritas.git
cd veritas
```

Make sure you have Python 3 installed:

```bash
python3 --version
```

---

## Usage

Run the script with:

```bash
python3 veritas.py <command> [path]
```

---

## Commands

| Command   | Description |
|----------|-------------|
| `init`   | Create baseline hashes for a file or directory |
| `check`  | Scan monitored files and detect changes |
| `update` | Update baseline hashes after intentional changes |

---

## Examples

### Initialize a directory baseline

```bash
python3 veritas.py init ./src
```

### Check file integrity

```bash
python3 veritas.py check
```

### Update baseline for one file

```bash
python3 veritas.py update ./src/main.py
```

### Update baseline for an entire folder

```bash
python3 veritas.py update ./src
```

---

## 📌 Output Summary

After every scan, VERITAS prints a report:

```text
========================================
SCAN COMPLETED
========================================
Total Scanned: 12
✔ OK:        10
✖ Modified:   1
⚠ Missing:    1
========================================
```

## 🔗 Project URL

https://github.com/whoosh09/Veritas
