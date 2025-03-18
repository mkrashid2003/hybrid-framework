@echo off
REM Ensure you are in the correct project directory
cd /d %~dp0

REM Activate the virtual environment (adjust the path if necessary)
call .venv\Scripts\activate.bat

REM Verify activation by checking the Python version
python --version

REM Optionally, ensure pytest is installed (uncomment the next line if needed)
REM pip install pytest pytest-html

echo Running pytest with markers "sanity or smoke"...
pytest -v -s -m "sanity or smoke" --html=Reports/report.html Testcases/test_logint_testcase.py



