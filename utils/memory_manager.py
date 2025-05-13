import json
import os
from pathlib import Path
from typing import List, Dict, Optional


class MemoryManager:
    def __init__(self, storage_dir: Path):
        """
        initialize the memory manager with a storage directory.
        
        args:
            storage_dir: dir path where chat history will be stored
        """
        self.storage_dir = storage_dir
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self) -> None:
        """ensure that the storage directory exists."""
        os.makedirs(self.storage_dir, exist_ok=True)
    
    def _get_model_dir(self, model_name: str) -> Path:
        """get the directory for a specific model."""
        model_dir = self.storage_dir / model_name
        os.makedirs(model_dir, exist_ok=True)
        return model_dir
    
    def _get_chat_file(self, model_name: str, chat_id: str) -> Path:
        """get the file path for a specific chat session."""
        model_dir = self._get_model_dir(model_name)
        return model_dir / f"{chat_id}.json"
    
    def save_messages(self, model_name: str, chat_id: str, messages: List[Dict[str, str]]) -> None:
        """
        save chat messages for a specific model and chat session.
        
        args:
            model_name: name of the model
            chat_id: identifier for the chat session
            messages: list of message dictionaries
        """
        file_path = self._get_chat_file(model_name, chat_id)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(messages, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving messages: {e}")
    
    def load_messages(self, model_name: str, chat_id: str) -> Optional[List[Dict[str, str]]]:
        """
        load chat messages for a specific model and chat session.
        
        args:
            model_name: name of the model
            chat_id: identifier for the chat session
            
        returns:
            list of message dictionaries, or None if not found
        """
        file_path = self._get_chat_file(model_name, chat_id)
        
        if not file_path.exists():
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading messages: {e}")
            return None
    
    def list_chat_sessions(self, model_name: str) -> List[str]:
        """
        list all available chat sessions for a specific model.
        
        args:
            model_name: name of the model
            
        returns:
            list of chat session IDs
        """
        model_dir = self._get_model_dir(model_name)
        
        if not model_dir.exists():
            return []
        
        chat_files = list(model_dir.glob('*.json'))
        return [file.stem for file in chat_files]
    
    def delete_chat_session(self, model_name: str, chat_id: str) -> bool:
        """
        delete a specific chat session.
        
        args:
            model_name: name of the model
            chat_id: identifier for the chat session
            
        returns:
            true if deletion was successful, false otherwise
        """
        file_path = self._get_chat_file(model_name, chat_id)
        
        if not file_path.exists():
            return False
        
        try:
            os.remove(file_path)
            return True
        except Exception as e:
            print(f"Error deleting chat session: {e}")
            return False