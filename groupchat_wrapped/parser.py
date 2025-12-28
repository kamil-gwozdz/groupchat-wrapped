"""Parser for Facebook Messenger export JSON files."""

import json
from pathlib import Path
from typing import Any
from dataclasses import dataclass
from datetime import datetime
import os


@dataclass
class Message:
    """Represents a single message in the chat."""
    sender: str
    content: str
    timestamp: datetime
    message_type: str  # text, photo, video, audio, gif, sticker, share, name_change, photo_change
    reactions: list[dict]
    
    
@dataclass  
class Conversation:
    """Represents a full conversation/group chat."""
    title: str
    participants: list[str]
    messages: list[Message]
    

def decode_facebook_encoding(text: str) -> str:
    """Decode Facebook's weird encoding (UTF-8 stored as Latin-1)."""
    if text is None:
        return ""
    try:
        return text.encode('latin-1').decode('utf-8')
    except (UnicodeDecodeError, UnicodeEncodeError):
        return text


def parse_message(msg_data: dict) -> Message | None:
    """Parse a single message from JSON data."""
    sender = decode_facebook_encoding(msg_data.get("sender_name", "Unknown"))
    timestamp = datetime.fromtimestamp(msg_data.get("timestamp_ms", 0) / 1000)
    
    # Determine message type and content
    content = ""
    msg_type = "text"
    
    if "content" in msg_data:
        content = decode_facebook_encoding(msg_data["content"])
        lower_content = content.lower()
        
        # Check for group name changes
        if any(phrase in lower_content for phrase in [
            'named the group', 'changed the group name',
            'nazwał grupę', 'nadał grupie nazwę', 'zmienił nazwę grupy',
            'zmienił(-a) nazwę grupy', 'nadał(-a) grupie nazwę'
        ]):
            msg_type = "name_change"
        # Check for group photo changes
        elif any(phrase in lower_content for phrase in [
            'changed the group photo', 'set the group photo',
            'removed the group photo', 'zmienił zdjęcie grupy',
            'ustawił zdjęcie grupy', 'usunął zdjęcie grupy',
            'zmienił(-a) zdjęcie grupy'
        ]):
            msg_type = "photo_change"
        else:
            msg_type = "text"
    elif "photos" in msg_data:
        msg_type = "photo"
        content = f"[{len(msg_data['photos'])} zdjęć]"
    elif "videos" in msg_data:
        msg_type = "video"
        content = "[wideo]"
    elif "audio_files" in msg_data:
        msg_type = "audio"
        content = "[audio]"
    elif "gifs" in msg_data:
        msg_type = "gif"
        content = "[GIF]"
    elif "sticker" in msg_data:
        msg_type = "sticker"
        content = "[naklejka]"
    elif "share" in msg_data:
        msg_type = "share"
        share = msg_data["share"]
        content = decode_facebook_encoding(share.get("link", "[udostępnienie]"))
    elif "call_duration" in msg_data:
        msg_type = "call"
        content = f"[rozmowa: {msg_data['call_duration']}s]"
    else:
        # Skip system messages or messages without meaningful content
        return None
    
    reactions = msg_data.get("reactions", [])
    
    return Message(
        sender=sender,
        content=content,
        timestamp=timestamp,
        message_type=msg_type,
        reactions=reactions
    )


def load_conversation(path: Path) -> Conversation:
    """Load a conversation from a Facebook export directory or file."""
    messages: list[Message] = []
    title = "Conversation"
    participants: list[str] = []
    
    # Handle both single file and directory with multiple message_X.json files
    if path.is_file():
        files = [path]
    else:
        # Look for message_*.json files in the directory
        files = sorted(path.glob("message_*.json"))
        if not files:
            # Maybe it's in a subdirectory
            for subdir in path.iterdir():
                if subdir.is_dir():
                    files = sorted(subdir.glob("message_*.json"))
                    if files:
                        break
    
    if not files:
        raise ValueError(f"No message files found in {path}")
    
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Get metadata from first file
        if not participants:
            title = decode_facebook_encoding(data.get("title", "Conversation"))
            participants = [
                decode_facebook_encoding(p.get("name", "Unknown"))
                for p in data.get("participants", [])
            ]
        
        # Parse messages
        for msg_data in data.get("messages", []):
            msg = parse_message(msg_data)
            if msg:
                messages.append(msg)
    
    # Sort messages by timestamp (oldest first)
    messages.sort(key=lambda m: m.timestamp)
    
    return Conversation(
        title=title,
        participants=participants,
        messages=messages
    )
