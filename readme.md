# llocaly

A streamlit-based interface for interacting with local AI models through Ollama.

![image](https://github.com/user-attachments/assets/185f1a64-5cb9-40a6-ad59-72cca3cb55fd)



## 🚀 Features

- 🤖 Query locally installed Ollama models
- 📝 Chat with multiple models simultaneously
- 💾 Enable or disable memory retention per model
- 🔄 Start new chat sessions anytime
- 📱 Connect from other devices using QR code
- 💻 Works completely offline


## 📋 Prerequisites

- Python 3.8+
- Ollama installed and running on your system
- Good GPU (optional, models run with CPU too)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/PhidLarkson/llocaly.git
cd llocaly
```

### Windows

1. Double-click `start.bat`
2. A browser window will automatically open with the LLocaly interface

### Linux/macOS

1. Make the start script executable:
   ```bash
   chmod +x start.sh
   ```
2. Double-click `start.sh` or run it from the terminal:
   ```bash
   ./start.sh
   ```

## How to Use

1. Select models from the sidebar
2. Send messages in the chat input at the bottom
3. View responses from each model in separate tabs
4. Toggle memory for individual models as needed
5. Start a new chat session with the "New Chat Session" button
6. Connect from other devices on the same network using the QR code


## 🤝 Contributing

We welcome contributions! llocaly is open for improvements, particularly in these areas:

### Priority Areas for Contribution

1. **Memory Management**
   - Add RAG 
   - Add file query feature

2. **Model Integration**
   - Expand support for different model formats
   - Improve model loading and tab switching

### How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/<your_new_feature>`)
3. Commit your changes (`git commit -m 'Add some <your_new_feature>'`)
4. Push to the branch (`git push origin feature/<your_new_feature>`)
5. Open a Pull Request


## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🙏 Acknowledgments

- [Ollama](https://ollama.com/) for local model serving
- [Streamlit](https://streamlit.io/) for the web interface
- Future contributors and supporters of the project

## 🔮 Future Plans

- Advanced prompt templates
- Custom model configuration
- Performance optimization tools
- Framework variety

## ⚠️ Known Limitations

- Limited to models available through Ollama


## 📞 Support

For support, please open an issue in the GitHub repository.
