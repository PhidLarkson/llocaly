@echo off
echo starting LLocaly...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo python is not installed! please install python 3.8 or higher.
    pause
    exit /b 1
)

pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo pip is not installed! please install pip.
    pause
    exit /b 1
)

ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ollama is not installed! please install ollama from https://ollama.ai/
    pause
    exit /b 1
)

if not exist .venv (
    echo creating virtual environment...
    python -m venv .venv
)

echo activating virtual environment...
call .venv\Scripts\activate

echo installing dependencies...
pip install -r requirements.txt

echo starting LLocaly application...
python -m streamlit run app/main.py --server.headless true --browser.serverAddress "localhost"

pause