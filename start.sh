echo "starting LLocaly..."

if ! command -v python3 &> /dev/null; then
    echo "pythoon is not installed! please install python 3.8 or higher."
    read -p "press enter to exit..."
    exit 1
fi

if ! command -v pip3 &> /dev/null; then
    echo "pip is not installed! please install pip."
    read -p "press enter to exit..."
    exit 1
fi

if ! command -v ollama &> /dev/null; then
    echo "ollama is not installed! please install ollama from https://ollama.ai/"
    read -p "press enter to exit..."
    exit 1
fi

if [ ! -d ".venv" ]; then
    echo "creating virtual environment..."
    python -m venv .venv
fi

echo "activating virtual environment..."
source .venv/bin/activate

echo "installing dependencies..."
pip install -r requirements.txt

echo "starting LLocaly application..."
python -m streamlit run main.py --server.headless true --browser.serverAddress "localhost"

read -p "press enter to exit..."