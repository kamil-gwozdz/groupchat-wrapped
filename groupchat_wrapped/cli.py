"""CLI interface for Group Chat Wrapped."""

import click
from pathlib import Path
import sys

from .parser import load_conversation
from .analyzer import analyze_conversation
from .generator import generate_html


@click.command()
@click.argument('input_path', type=click.Path(exists=True, path_type=Path))
@click.option(
    '-o', '--output',
    type=click.Path(path_type=Path),
    default=None,
    help='Output HTML file path. Default: groupchat_wrapped.html'
)
@click.option(
    '--open/--no-open',
    default=True,
    help='Open the generated HTML in browser'
)
def main(input_path: Path, output: Path | None, open: bool):
    """
    Generate a "Group Chat Wrapped" from a Facebook Messenger export.
    
    INPUT_PATH: Path to the Facebook export folder or message_1.json file.
    
    Example:
    
        groupchat-wrapped /path/to/facebook_export/messages/inbox/chatname/
    """
    click.echo(click.style("🎉 Group Chat Wrapped Generator", fg='magenta', bold=True))
    click.echo()
    
    # Parse conversation
    click.echo(f"📂 Loading conversation from: {input_path}")
    try:
        conversation = load_conversation(input_path)
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
        output = Path("groupchat_wrapped.html")
    
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
