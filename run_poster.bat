@echo off
set PYTHONIOENCODING=utf-8
cd /d "d:\Dev\Antigravity\LinkedinAutoPosts"

:: Check if the virtual environment exists, otherwise use global python
if exist venv\Scripts\python.exe (
    venv\Scripts\python.exe main.py
) else (
    python main.py
)
