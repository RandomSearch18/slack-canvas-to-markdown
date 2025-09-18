#!/usr/bin/env python3
"""
Example usage of the Slack Canvas to Markdown exporter.
"""

import os
import sys
from pathlib import Path

# Example usage patterns for the slack-canvas-to-markdown tool


def show_basic_usage():
    """Show basic usage examples."""
    print("Slack Canvas to Markdown - Usage Examples")
    print("=" * 45)
    print()

    print("1. Basic export with token as argument:")
    print("   python export_canvas.py export F09G8G3GB6V --token xoxb-your-bot-token")
    print()

    print("2. Using environment variable for token:")
    print("   export SLACK_BOT_TOKEN='xoxb-your-bot-token'")
    print("   python export_canvas.py export F09G8G3GB6V")
    print()

    print("3. Export to specific directory with verbose output:")
    print("   python export_canvas.py export F09G8G3GB6V \\")
    print("     --token xoxb-your-token \\")
    print("     --output ./my_canvas_backups \\")
    print("     --verbose")
    print()
    
    print("4. Join a channel to access its canvases (helps with 'not_visible' errors):")
    print("   python export_canvas.py join-channel #general --token xoxb-your-token")
    print("   python export_canvas.py join-channel C1234567890 --verbose")
    print()
    
    print("5. Test your bot token authentication:")
    print("   python export_canvas.py test-auth --token xoxb-your-token")
    print()
    
    print("6. Get help for any command:")
    print("   python export_canvas.py --help")
    print("   python export_canvas.py export --help")
    print("   python export_canvas.py join-channel --help")
    print()


def show_batch_example():
    """Show how to batch export multiple canvases."""
    print("Batch Export Example:")
    print("-" * 20)
    print()

    batch_script = """#!/bin/bash
# Batch export multiple canvases
export SLACK_BOT_TOKEN="xoxb-your-bot-token"

canvas_ids=(
    "F09G8G3GB6V"
    "F09G8G3GB6W" 
    "F09G8G3GB6X"
)

for canvas_id in "${canvas_ids[@]}"; do
    echo "Exporting canvas: $canvas_id"
    python export_canvas.py export "$canvas_id" --verbose
    if [ $? -ne 0 ]; then
        echo "Failed to export canvas: $canvas_id"
    else
        echo "Successfully exported canvas: $canvas_id"
    fi
    echo "---"
done"""

    print(batch_script)
    print()


def show_troubleshooting():
    """Show common troubleshooting steps."""
    print("Troubleshooting:")
    print("-" * 15)
    print()
    print("Common issues and solutions:")
    print()
    print("• 'Invalid bot token' error:")
    print("  - Verify your token starts with 'xoxb-'")
    print("  - Check that the bot has required scopes: canvases:read, files:read")
    print("  - Ensure the bot is installed in your workspace")
    print()
    print("• 'Canvas not found' or 'not_visible' error:")
    print("  - Double-check the canvas ID format (e.g., F09G8G3GB6V)")
    print("  - Ensure the bot has access to the canvas")
    print("  - Join the channel containing the canvas using:")
    print("    python export_canvas.py join-channel #channel-name --token your-token")
    print("  - Verify the canvas exists and isn't deleted")
    print()
    print("• Permission errors:")
    print("  - Make sure the output directory is writable")
    print("  - Check that the bot has proper workspace permissions")
    print("  - Try joining the channel first if getting access errors")
    print()


if __name__ == "__main__":
    show_basic_usage()
    show_batch_example()
    show_troubleshooting()

    print("For more information, see the README.md file.")
