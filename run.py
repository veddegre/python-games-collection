#!/usr/bin/env python3
"""
run.py — entry point for the Games Collection.
Works on Windows, macOS, and Linux.
"""
import os
import sys
import subprocess

# Suppress pygame startup message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# Tell Python not to write .pyc / __pycache__ folders
# This keeps the game folder clean — no compiled bytecode clutter
sys.dont_write_bytecode = True
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

script_dir = os.path.dirname(os.path.abspath(__file__))
menu_path  = os.path.join(script_dir, 'menu.py')

if not os.path.exists(menu_path):
    print("Error: menu.py not found. Make sure you're running from the game folder.")
    sys.exit(1)

subprocess.run([sys.executable, '-B', menu_path])
