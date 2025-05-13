import os
import streamlit as st
from pathlib import Path
from utils.ollama_service import OllamaService
from utils.memory_manager import MemoryManager
from utils.network_utils import generate_qr_code, get_local_ip

# Set page configuration
st.set_page_config(
    page_title="LLocaly",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Initialize services
@st.cache_resource
def init_services():
    ollama_service = OllamaService()
    memory_manager = MemoryManager(Path("data/chat_history"))
    return ollama_service, memory_manager

ollama_service, memory_manager = init_services()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = {}
if "selected_models" not in st.session_state:
    st.session_state.selected_models = []
if "memory_enabled" not in st.session_state:
    st.session_state.memory_enabled = {}
if "chat_id" not in st.session_state:
    st.session_state.chat_id = "default"

# Sidebar
with st.sidebar:
    st.title("LLocaly")
    st.markdown("Local Ollama Interface")
    
    st.subheader("Available Models")
    
    # Refresh models button
    if st.button("Refresh Models"):
        ollama_service.refresh_models()
    
    # Model selection
    available_models = ollama_service.get_models()
    
    if not available_models:
        st.warning("No models found. Make sure Ollama is running.")
    else:
        selected_models = st.multiselect(
            "Select models to chat with:",
            options=available_models,
            default=st.session_state.selected_models if st.session_state.selected_models else available_models[0:1]
        )
        
        if selected_models != st.session_state.selected_models:
            st.session_state.selected_models = selected_models
            # Initialize memory enabled state for new models
            for model in selected_models:
                if model not in st.session_state.memory_enabled:
                    st.session_state.memory_enabled[model] = True
    
    # Memory toggles
    st.subheader("Memory Settings")
    
    for model in st.session_state.selected_models:
        st.session_state.memory_enabled[model] = st.checkbox(
            f"Enable memory for {model}",
            value=st.session_state.memory_enabled.get(model, True),
            key=f"memory_{model}"
        )
    
    # New chat button
    st.subheader("Chat Management")
    if st.button("New Chat Session"):
        # Generate a new chat ID
        st.session_state.chat_id = f"chat_{hash(str(len(st.session_state.messages)) + str(len(available_models)))}"
        # Clear messages
        st.session_state.messages = {model: [] for model in st.session_state.selected_models}
        st.rerun()

    # Connect via QR Code
    st.subheader("Connect via QR Code")
    local_ip = get_local_ip()
    if local_ip:
        st.markdown(f"**Local IP:** `{local_ip}:8501`")
        qr_img = generate_qr_code(f"http://{local_ip}:8501")
        st.image(qr_img, width=200)
    else:
        st.warning("Could not determine local IP address")

st.markdown("Check out https://ollama.com for more information.")

for model in st.session_state.selected_models:
    if model not in st.session_state.messages:
        # Load from memory if enabled
        if st.session_state.memory_enabled[model]:
            stored_messages = memory_manager.load_messages(model, st.session_state.chat_id)
            st.session_state.messages[model] = stored_messages if stored_messages else []
        else:
            st.session_state.messages[model] = []

model_tabs = st.tabs(st.session_state.selected_models) if st.session_state.selected_models else [st.empty()]

# model tabs
for i, model in enumerate(st.session_state.selected_models):
    with model_tabs[i]:
        st.subheader(f"{model}")
        
        message_container = st.container()
        with message_container:
            for msg in st.session_state.messages.get(model, []):
                role = "assistant" if msg["role"] == "assistant" else "user"
                with st.chat_message(role):
                    st.markdown(msg["content"])

# chat input 
if st.session_state.selected_models:
    prompt = st.chat_input("Send a message...")
    
    if prompt:
        for model in st.session_state.selected_models:
            if model not in st.session_state.messages:
                st.session_state.messages[model] = []
            
            st.session_state.messages[model].append({"role": "user", "content": prompt})
            
            # display response
            with st.spinner(f"Generating response with {model}..."):
                context = ""
                if st.session_state.memory_enabled[model]:
                    history = st.session_state.messages[model][:-1]  
                    for msg in history[-10:]:  # limit context to last 10 messages
                        context += f"{msg['role'].capitalize()}: {msg['content']}\n"
                
                response = ollama_service.generate_response(model, prompt, context)
                st.session_state.messages[model].append({"role": "assistant", "content": response})
                
                # save to memory if enabled
                if st.session_state.memory_enabled[model]:
                    memory_manager.save_messages(model, st.session_state.chat_id, st.session_state.messages[model])
        
        st.rerun()
else:
    st.warning("Please select at least one model from the sidebar to start chatting.")
