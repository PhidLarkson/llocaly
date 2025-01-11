import streamlit as st
import subprocess
import platform
import time
from datetime import datetime
import json
import psutil
from langchain_community.llms import Ollama
from collections import deque
import GPUtil

# Constants
TECH_GRAY = "#1E1E1E"
ACCENT_GRAY = "#2D2D2D"
TEXT_COLOR = "#E0E0E0"
ACCENT_COLOR = "#4A4A4A"
HIGHLIGHT_COLOR = "#646464"
MAX_HISTORY_POINTS = 50

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'metrics' not in st.session_state:
    st.session_state.metrics = {
        'response_times': deque(maxlen=MAX_HISTORY_POINTS),
        'token_rates': deque(maxlen=MAX_HISTORY_POINTS),
        'timestamps': deque(maxlen=MAX_HISTORY_POINTS)
    }

def apply_modern_theme():
    st.markdown(f"""
        <style>
        /* Main theme */
        .stApp {{
            background-color: {TECH_GRAY};
            color: {TEXT_COLOR};
        }}
        
        /* Headers */
        h1, h2, h3 {{
            color: {TEXT_COLOR} !important;
            font-family: 'Inter', sans-serif;
            font-weight: 600;
        }}
        
        /* Buttons */
        .stButton>button {{
            background-color: {ACCENT_GRAY};
            color: {TEXT_COLOR};
            border: 1px solid {HIGHLIGHT_COLOR};
            border-radius: 8px;
            font-family: 'Inter', sans-serif;
            transition: all 0.3s ease;
        }}
        .stButton>button:hover {{
            border-color: {TEXT_COLOR};
            transform: translateY(-2px);
        }}
        
        /* Chat messages */
        .stChatMessage {{
            # background-color: {ACCENT_GRAY};
            padding: 15px;
            margin: 10px 0;
            # box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        /* Inputs */
        .stTextInput>div>div>input {{
            background-color: {ACCENT_GRAY};
            color: {TEXT_COLOR};
            border: 1px solid {HIGHLIGHT_COLOR};
            border-radius: 8px;
        }}
        
        /* Metrics */
        .stMetric {{
            background-color: {ACCENT_GRAY};
            border: 1px solid {HIGHLIGHT_COLOR};
            border-radius: 8px;
            padding: 15px;
        }}
        
        /* Expander */
        .streamlit-expanderHeader {{
            background-color: {ACCENT_GRAY};
            border: 1px solid {HIGHLIGHT_COLOR};
            border-radius: 8px;
        }}
        </style>
    """, unsafe_allow_html=True)

def get_system_info():
    try:
        memory = psutil.virtual_memory()
        
        info = {
            'system': {
                'os': f"{platform.system()} {platform.release()}",
                'architecture': platform.machine(),
                'hostname': platform.node()
            },
            'hardware': {
                'cpu_cores': psutil.cpu_count(logical=False),
                'threads': psutil.cpu_count(logical=True),
                'memory': {
                    'total': f"{memory.total / (1024**3):.1f} GB",
                    'available': f"{memory.available / (1024**3):.1f} GB",
                    'usage': f"{memory.percent}%"
                }
            }
        }
        return info
    except Exception as e:
        return {'error': str(e)}

def get_available_models():
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            models = []
            for line in result.stdout.strip().split('\n')[1:]:
                parts = line.split()
                if parts:
                    models.append({'name': parts[0]})
            return models
        return []
    except Exception as e:
        st.error(f"Model detection error: {str(e)}")
        return []

def main():
    st.set_page_config(
        page_title="llocaly",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    apply_modern_theme()

    # Sidebar
    with st.sidebar:
        
        # Model Selection
        st.subheader("Model Configuration")
        available_models = get_available_models()
        if available_models:
            model_names = [m['name'] for m in available_models]
            selected_model = st.selectbox("Select Model", model_names)
        else:
            st.error("No models detected")
            selected_model = None
        
        # Technical Settings
        with st.expander("Advanced Settings", expanded=True):
            temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
            context_length = st.select_slider(
                "Context Length",
                options=[1024, 2048, 4096, 8192],
                value=2048
            )

        # System Information
        with st.expander("System Status", expanded=True):
            sys_info = get_system_info()
            # print(sys_info)
            
            st.markdown("**System Details**")
            st.code(json.dumps(sys_info['system'], indent=2), language='json')
            
            # st.markdown("**Systems**")
            # cols = st.columns(4)
            # cols[0].metric("CPU Cores", sys_info['hardware']['cpu_cores'])
            # cols[1].metric("Threads", sys_info['hardware']['threads'])
            # cols[2].metric("Total RAM", sys_info['hardware']['memory']['total'])
            # cols[3].metric("Available", sys_info['hardware']['memory']['available'])

            st.markdown("**Hardware**")
            cols = st.columns(2)
            cols[0].metric("CPU Cores", sys_info['hardware']['cpu_cores'])
            cols[1].metric("Threads", sys_info['hardware']['threads'])
            
            st.markdown("**Memory**")
            cols = st.columns(2)
            cols[0].metric("Total RAM", sys_info['hardware']['memory']['total'])
            cols[1].metric("Available", sys_info['hardware']['memory']['available'])
            # GPU Information
            st.markdown("**GPU Status**")
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    for gpu in gpus:
                        st.markdown(f"**{gpu.name}**")
                        cols = st.columns(2)
                        cols[0].metric("GPU Load", f"{gpu.load * 100:.1f}%")
                        cols[1].metric("Memory Used", f"{gpu.memoryUsed} MB")
                        cols = st.columns(2)
                        cols[0].metric("Memory Total", f"{gpu.memoryTotal} MB")
                        cols[1].metric("Temperature", f"{gpu.temperature} °C")
                else:
                    st.markdown("No GPU detected")
            except Exception as e:
                st.error(f"GPU detection error: {str(e)}")


        # Performance Metrics
        if st.session_state.metrics['response_times']:
            with st.expander("Performance", expanded=True):
                avg_time = sum(st.session_state.metrics['response_times']) / len(st.session_state.metrics['response_times'])
                st.metric("Avg Response Time", f"{avg_time:.2f}s")
                
                if st.session_state.metrics['token_rates']:
                    avg_rate = sum(st.session_state.metrics['token_rates']) / len(st.session_state.metrics['token_rates'])
                    st.metric("Avg Tokens/sec", f"{avg_rate:.1f}")

    # Main Chat Interface    
    # Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "metadata" in message:
                with st.expander("Details"):
                    st.code(json.dumps(message["metadata"], indent=2), language='json')

    # Chat Input
    if prompt := st.chat_input("Enter your message..."):
        if not selected_model:
            st.error("Please select a model first")
            return

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            model = Ollama(model=selected_model, temperature=temperature)

            with st.chat_message("assistant"):
                with st.spinner("Generating response..."):
                    start_time = time.time()
                    response = model(prompt)
                    end_time = time.time()
                    
                    generation_time = end_time - start_time
                    token_count = len(response.split())
                    token_rate = token_count / generation_time

                    st.session_state.metrics['response_times'].append(generation_time)
                    st.session_state.metrics['token_rates'].append(token_rate)
                    st.session_state.metrics['timestamps'].append(datetime.now().isoformat())

                    metadata = {
                        "timestamp": datetime.now().isoformat(),
                        "metrics": {
                            "generation_time": f"{generation_time:.2f}s",
                            "token_count": token_count,
                            "token_rate": f"{token_rate:.1f} tokens/sec"
                        },
                        "settings": {
                            "model": selected_model,
                            "temperature": temperature,
                            "context_length": context_length
                        }
                    }

                    st.markdown(response)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response,
                        "metadata": metadata
                    })

        except Exception as e:
            st.error(f"Error: {str(e)}")

    # Control Buttons
    cols = st.columns(2)
    if cols[0].button("Clear Chat x2"):
        st.session_state.messages = []
        st.session_state.metrics = {
            'response_times': deque(maxlen=MAX_HISTORY_POINTS),
            'token_rates': deque(maxlen=MAX_HISTORY_POINTS),
            'timestamps': deque(maxlen=MAX_HISTORY_POINTS)
        }
        
    if cols[1].button("Export Log"):
        export_data = {
            "messages": st.session_state.messages,
            "metrics": {
                "response_times": list(st.session_state.metrics['response_times']),
                "token_rates": list(st.session_state.metrics['token_rates']),
                "timestamps": list(st.session_state.metrics['timestamps'])
            },
            "system_info": get_system_info(),
            "export_timestamp": datetime.now().isoformat()
        }
        
        st.download_button(
            "Download",
            data=json.dumps(export_data, indent=2),
            file_name=f"chat_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

if __name__ == "__main__":
    main()