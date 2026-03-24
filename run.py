#!/usr/bin/env python3
"""
run.py — entry point for the Games Collection.
Works standalone, via PyInstaller bundle, on Windows/macOS/Linux.
"""
import os
import sys
import subprocess

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
sys.dont_write_bytecode = True
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

# PyInstaller extracts files to a temp folder (_MEIPASS) at runtime.
# When running normally, just use the script's directory.
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

menu_path = os.path.join(BASE_DIR, 'menu.py')

if not os.path.exists(menu_path):
    print("Error: menu.py not found.")
    sys.exit(1)

subprocess.run([sys.executable, '-B', menu_path])
