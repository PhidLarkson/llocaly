# llocaly

A streamlit-based interface for interacting with local AI models through Ollama.

![image](https://github.com/user-attachments/assets/185f1a64-5cb9-40a6-ad59-72cca3cb55fd)



## 🚀 Features

- **Local Model Integration**: Seamless interaction with locally hosted models via Ollama
- **System Monitoring**: CPU, RAM, and GPU data
- **Performance Metrics**: Track response times and token generation rates
- **Modern Interface**: Clean, minimalist design with a professional dark theme
- **Export Capabilities**: Save your chat sessions and performance data

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

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## 🤝 Contributing

We welcome contributions! llocaly is open for improvements, particularly in these areas:

### Priority Areas for Contribution

1. **Memory Management**
   - Implement persistent conversation memory
   - Add conversation context management
   - Develop memory optimization strategies

2. **Model Integration**
   - Expand support for different model formats
   - Improve model loading and switching
   - Add model performance benchmarking

3. **UI/UX Improvements**
   - Enhanced visualization of system metrics
   - Customizable themes
   - Responsive design improvements

### How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⚙️ Configuration

The application can be configured through the sidebar interface:
- Model selection
- Temperature adjustment
- Context length settings
- System monitoring 

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🙏 Acknowledgments

- [Ollama](https://ollama.com/) for local model serving
- [Streamlit](https://streamlit.io/) for the web interface
- Future contributors and supporters of the project

## 🔮 Future Plans

- Conversation memory persistence
- Multi-model chat sessions
- Advanced prompt templates
- Custom model configuration
- Performance optimization tools
- Framework variety

## ⚠️ Known Limitations

- Currently no persistent memory between sessions
- Limited to models available through Ollama
- Single conversation context at a time

## 📞 Support

For support, please open an issue in the GitHub repository.
