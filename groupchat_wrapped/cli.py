"""CLI interface for Group Chat Wrapped."""

import click
from pathlib import Path
import sys
import json
from datetime import datetime

from .parser import load_conversation, decode_facebook_encoding
from .analyzer import analyze_conversation
from .generator import generate_html


def find_inbox_folder(export_path: Path) -> Path | None:
    """Find the inbox folder in Facebook export."""
    # Direct inbox folder
    if export_path.name == "inbox" and export_path.is_dir():
        return export_path
    
    # Check common paths
    possible_paths = [
        export_path / "messages" / "inbox",
        export_path / "your_facebook_activity" / "messages" / "inbox",
        export_path / "inbox",
    ]
    
    for path in possible_paths:
        if path.exists() and path.is_dir():
            return path
    
    # Search recursively for inbox folder
    for path in export_path.rglob("inbox"):
        if path.is_dir() and (path / ".." ).resolve().name == "messages":
            return path
    
    return None


def get_chat_info(chat_folder: Path) -> dict | None:
    """Get basic info about a chat from its folder."""
    message_files = sorted(chat_folder.glob("message_*.json"))
    if not message_files:
        return None
    
    try:
        # Load first file for metadata
        with open(message_files[0], 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        title = decode_facebook_encoding(data.get("title", chat_folder.name))
        participants = [
            decode_facebook_encoding(p.get("name", "Unknown"))
            for p in data.get("participants", [])
        ]
        
        # Get total message count and last message time
        total_messages = 0
        last_timestamp = 0
        
        for msg_file in message_files:
            with open(msg_file, 'r', encoding='utf-8') as f:
                file_data = json.load(f)
            messages = file_data.get("messages", [])
            total_messages += len(messages)
            
            for msg in messages:
                ts = msg.get("timestamp_ms", 0)
                if ts > last_timestamp:
                    last_timestamp = ts
        
        last_date = datetime.fromtimestamp(last_timestamp / 1000) if last_timestamp else None
        
        return {
            "path": chat_folder,
            "title": title,
            "participants": participants,
            "participant_count": len(participants),
            "message_count": total_messages,
            "last_message": last_date,
            "last_timestamp": last_timestamp,
        }
    except Exception as e:
        return None


def discover_chats(inbox_path: Path) -> list[dict]:
    """Discover all chats in the inbox folder."""
    chats = []
    
    for item in inbox_path.iterdir():
        if item.is_dir():
            info = get_chat_info(item)
            if info and info["message_count"] > 0:
                chats.append(info)
    
    # Sort by last message timestamp (most recent first)
    chats.sort(key=lambda x: x["last_timestamp"], reverse=True)
    
    return chats


@click.command()
@click.argument('input_path', type=click.Path(exists=True, path_type=Path))
@click.option(
    '-o', '--output',
    type=click.Path(path_type=Path),
    default=None,
    help='Output HTML file path. Default: output/<chat_name>_wrapped.html'
)
@click.option(
    '--open/--no-open',
    default=True,
    help='Open the generated HTML in browser'
)
@click.option(
    '-c', '--chat',
    type=int,
    default=None,
    help='Chat number to select (skip interactive selection)'
)
def main(input_path: Path, output: Path | None, open: bool, chat: int | None):
    """
    Generate a "Group Chat Wrapped" from a Facebook Messenger export.
    
    INPUT_PATH: Path to the Facebook export folder (will auto-discover chats).
    
    Examples:
    
        groupchat-wrapped /path/to/facebook-export/
        
        groupchat-wrapped /path/to/facebook-export/ -c 1
        
        groupchat-wrapped /path/to/facebook-export/ -o output/wrapped.html
    """
    click.echo(click.style("🎉 Group Chat Wrapped Generator", fg='magenta', bold=True))
    click.echo()
    
    # Check if input is a direct chat folder (has message_*.json files)
    if list(input_path.glob("message_*.json")):
        # Direct chat folder provided
        chat_path = input_path
        click.echo(f"📂 Loading conversation from: {input_path}")
    else:
        # Try to find inbox folder and list chats
        inbox_path = find_inbox_folder(input_path)
        
        if not inbox_path:
            click.echo(click.style("❌ Could not find inbox folder in the export.", fg='red'))
            click.echo("   Make sure you provided the path to the Facebook export folder.")
            click.echo("   Expected structure: export/messages/inbox/")
            sys.exit(1)
        
        click.echo(f"📂 Found inbox folder: {inbox_path}")
        click.echo("🔍 Discovering chats...")
        click.echo()
        
        chats = discover_chats(inbox_path)
        
        if not chats:
            click.echo(click.style("❌ No chats found in the inbox folder.", fg='red'))
            sys.exit(1)
        
        # Display chat list
        click.echo(click.style(f"📋 Found {len(chats)} chats:", fg='cyan'))
        click.echo()
        
        for i, chat_info in enumerate(chats, 1):
            last_msg = chat_info["last_message"].strftime("%d.%m.%Y") if chat_info["last_message"] else "N/A"
            participants_str = f"{chat_info['participant_count']} participants" if chat_info['participant_count'] > 2 else ""
            
            # Highlight group chats
            if chat_info['participant_count'] > 2:
                title_style = click.style(f"{chat_info['title']}", fg='yellow', bold=True)
                badge = click.style(" [GROUP]", fg='green')
            else:
                title_style = chat_info['title']
                badge = ""
            
            click.echo(f"  {click.style(f'{i:3d}', fg='cyan')}. {title_style}{badge}")
            click.echo(f"       💬 {chat_info['message_count']:,} messages | 📅 Last: {last_msg} | 👥 {chat_info['participant_count']}")
            click.echo()
        
        # Get user selection
        if chat is not None:
            selection = chat
        else:
            click.echo()
            selection = click.prompt(
                click.style("🎯 Select a chat number", fg='magenta'),
                type=int,
                default=1
            )
        
        if selection < 1 or selection > len(chats):
            click.echo(click.style(f"❌ Invalid selection. Please choose 1-{len(chats)}", fg='red'))
            sys.exit(1)
        
        selected_chat = chats[selection - 1]
        chat_path = selected_chat["path"]
        
        click.echo()
        click.echo(f"✅ Selected: {click.style(selected_chat['title'], fg='green', bold=True)}")
        click.echo()
    
    # Load conversation
    click.echo(f"📂 Loading conversation...")
    try:
        conversation = load_conversation(chat_path)
    except Exception as e:
        click.echo(click.style(f"❌ Error loading conversation: {e}", fg='red'))
        sys.exit(1)
    
    click.echo(click.style(f"✅ Loaded: {conversation.title}", fg='green'))
    click.echo(f"   📨 Messages: {len(conversation.messages):,}")
    click.echo(f"   👥 Participants: {len(conversation.participants)}")
    click.echo()
    
    # Analyze
    click.echo("🔍 Analyzing conversation...")
    result = analyze_conversation(conversation)
    click.echo(click.style(f"✅ Found {len(result.categories)} categories!", fg='green'))
    click.echo()
    
    # Generate HTML
    if output is None:
        # Create safe filename from chat title
        safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in conversation.title)
        safe_title = safe_title.replace(' ', '_')[:50]
        output = Path("output") / f"{safe_title}_wrapped.html"
        output.parent.mkdir(parents=True, exist_ok=True)
    
    click.echo(f"🎨 Generating HTML: {output}")
    generate_html(result, output)
    click.echo(click.style(f"✅ Generated: {output.absolute()}", fg='green'))
    click.echo()
    
    # Print summary of categories
    click.echo(click.style("📊 Categories generated:", fg='cyan'))
    for cat in result.categories:
        winner_info = cat.winner if cat.winner else "Multiple winners"
        click.echo(f"   {cat.icon} {cat.title}: {winner_info}")
    
    click.echo()
    click.echo(click.style("🎉 Done! Enjoy your Group Chat Wrapped!", fg='magenta', bold=True))
    
    # Open in browser
    if open:
        import webbrowser
        webbrowser.open(f"file://{output.absolute()}")


if __name__ == '__main__':
    main()
