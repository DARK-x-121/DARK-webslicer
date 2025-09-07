# 🌑 DARK WEBSLICER v2.0 — NO NAME PRIME Edition
> **By Amit @ DARK** • Non-root Website Recon & Vulnerability Scanner for Termux

![By Amit @ DARK](https://img.shields.io/badge/By-Amit%20@%20DARK-purple?style=for-the-badge)
![Python 3.x](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge)
![Termux](https://img.shields.io/badge/Termux-Non--Rooted-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-Educational-red?style=for-the-badge)

DARK WebSlicer v2.0 is a **fast, non-root** vulnerability scanner for **authorized security testing**.  
It targets common web issues (Reflected **XSS**, **Open Redirects**, error-based **SQLi**) and adds speed with **async I/O**, basic **CSRF** heuristics, and **directory discovery**—all wrapped in a clean, hacker-style UI.

> ⚠️ **Use only on systems you own or have written permission to test.**  
> This project is for **education & defensive security**.

---

## ✨ Features

- ⚡ **Async scanning (aiohttp)** for high speed
- 🧪 **XSS / SQLi (error-based) / Open Redirect** checks
- 🛡️ **CSRF missing** (basic heuristic) detection
- 🗂️ **Directory discovery** (`/admin`, `/backup`, etc.)
- 🧠 **Smart payload set** with easy customization
- 📄 **JSON reports** (timestamped and ready to share)
- 🎛️ **Simple interactive CLI** (Termux friendly, non-root)

---

## 🧭 Quick Start (Termux / Linux)

```bash
# 1) System prep
pkg update && pkg upgrade -y || sudo apt update && sudo apt -y upgrade

# 2) Install Python & Git (Termux shown)
pkg install -y python git

# 3) Clone this repo
git clone https://github.com/DARK-x-121/DARK-WebSlicer.git
cd DARK-WebSlicer

# 4) Install Python deps
pip install aiohttp requests colorama tqdm prettytable

# 5) Run
python dark_webslicer_v2.py
