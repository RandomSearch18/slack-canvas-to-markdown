"""Command line interface for Slack Canvas to Markdown exporter."""

import click
import os
import sys
from pathlib import Path

from .slack_client import SlackAPIClient
from .exporter import CanvasExporter


@click.command()
@click.argument("canvas_id", type=str)
@click.option(
    "--token",
    "-t",
    type=str,
    help="Slack bot token (can also be set via SLACK_BOT_TOKEN environment variable)",
    envvar="SLACK_BOT_TOKEN",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    default="./exported_canvases",
    help="Output directory for exported markdown files (default: ./exported_canvases)",
)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def export_canvas(canvas_id: str, token: str, output: str, verbose: bool):
    """Export a Slack canvas to markdown format.

    CANVAS_ID is the Slack canvas ID (e.g., F09G8G3GB6V)

    Example:
        slack-canvas-export F09G8G3GB6V --token xoxb-your-bot-token
    """
    if verbose:
        click.echo(f"Starting export for canvas ID: {canvas_id}")

    # Validate token
    if not token:
        click.echo(
            "Error: Slack bot token is required. Use --token option or set SLACK_BOT_TOKEN environment variable."
        )
        sys.exit(1)

    # Validate canvas ID format (basic check)
    if not canvas_id or len(canvas_id) < 5:
        click.echo("Error: Invalid canvas ID format. Expected format like F09G8G3GB6V")
        sys.exit(1)

    try:
        # Initialize clients
        if verbose:
            click.echo("Initializing Slack API client...")
        slack_client = SlackAPIClient(token)
        exporter = CanvasExporter(output)

        # Fetch canvas information
        if verbose:
            click.echo(f"Fetching canvas information for {canvas_id}...")
        canvas_data = slack_client.get_canvas_info(canvas_id)

        if not canvas_data:
            click.echo(f"Error: Canvas {canvas_id} not found or not accessible.")
            sys.exit(1)

        # Fetch canvas content
        if verbose:
            click.echo("Fetching canvas content...")
        try:
            canvas_content = slack_client.get_canvas_content(canvas_id)
        except Exception as e:
            if verbose:
                click.echo(f"Warning: Could not fetch canvas content: {e}")
                click.echo("Proceeding with metadata only...")
            canvas_content = None

        # Export to markdown
        if verbose:
            click.echo("Converting to markdown and saving...")
        file_path = exporter.export_canvas(canvas_data, canvas_content)

        click.echo(f"✓ Canvas exported successfully to: {file_path}")

        # Display some information about the exported canvas
        title = canvas_data.get("title", "Untitled")
        click.echo(f"  Title: {title}")
        click.echo(f"  Canvas ID: {canvas_id}")
        click.echo(f"  File size: {Path(file_path).stat().st_size} bytes")

    except ValueError as e:
        click.echo(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        if verbose:
            click.echo(f"Unexpected error: {e}")
            import traceback

            traceback.print_exc()
        else:
            click.echo(f"Error: {e}")
        sys.exit(1)


@click.command()
@click.option(
    "--token", "-t", type=str, help="Slack bot token to test", envvar="SLACK_BOT_TOKEN"
)
def test_auth(token: str):
    """Test Slack bot token authentication."""
    if not token:
        click.echo(
            "Error: Slack bot token is required. Use --token option or set SLACK_BOT_TOKEN environment variable."
        )
        sys.exit(1)

    try:
        import requests

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        response = requests.get("https://slack.com/api/auth.test", headers=headers)
        response.raise_for_status()

        data = response.json()

        if data.get("ok"):
            click.echo("✓ Authentication successful!")
            click.echo(f"  Bot User ID: {data.get('user_id')}")
            click.echo(f"  Team: {data.get('team')}")
        else:
            click.echo(f"✗ Authentication failed: {data.get('error')}")
            sys.exit(1)

    except Exception as e:
        click.echo(f"Error testing authentication: {e}")
        sys.exit(1)


@click.group()
def main():
    """Slack Canvas to Markdown Exporter

    A tool to export Slack canvases to markdown files for backup purposes.
    """
    pass


main.add_command(export_canvas, name="export")
main.add_command(test_auth, name="test-auth")


if __name__ == "__main__":
    main()
