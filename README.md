# slack-canvas-to-markdown

Rescues Slack canvases from Salesforce by exporting them as markdown files

## Description

This tool allows you to export Slack canvases to markdown files for backup purposes, especially useful when migrating away from Slack. It uses the Slack API to fetch canvas data and converts it to markdown format for easy reading and archiving.

## Features

- Export individual Slack canvases by ID
- Automatic conversion to markdown format
- Preserves canvas metadata (title, creation date, owner, etc.)
- Command-line interface for easy automation
- Support for batch processing (can be scripted)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/RandomSearch18/slack-canvas-to-markdown.git
cd slack-canvas-to-markdown
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Install as a package:
```bash
pip install -e .
```

## Usage

### Basic Usage

Export a single canvas using the direct script:

```bash
python export_canvas.py export F09G8G3GB6V --token xoxb-your-bot-token
```

### Using Environment Variable

Set your bot token as an environment variable:

```bash
export SLACK_BOT_TOKEN="xoxb-your-bot-token"
python export_canvas.py export F09G8G3GB6V
```

### Command Options

- `--token, -t`: Slack bot token (required, can be set via SLACK_BOT_TOKEN env var)
- `--output, -o`: Output directory for markdown files (default: ./exported_canvases)
- `--verbose, -v`: Enable verbose output for debugging

### Examples

```bash
# Basic export
python export_canvas.py export F09G8G3GB6V --token xoxb-2210535565-9525419665143-qnlqbJQvFi8t7ksm3m6vW8X3

# Export to specific directory with verbose output
python export_canvas.py export F09G8G3GB6V --token xoxb-your-token --output ./my_backups --verbose

# Test authentication
python export_canvas.py test-auth --token xoxb-your-token
```

## Getting a Slack Bot Token

1. Go to [Slack API Apps](https://api.slack.com/apps)
2. Create a new app or select an existing one
3. Go to "OAuth & Permissions" in the sidebar
4. Add the following bot token scopes:
   - `canvases:read` - To read canvas content
   - `files:read` - To read file information
5. Install the app to your workspace
6. Copy the "Bot User OAuth Token" (starts with `xoxb-`)

## Output Format

Exported markdown files include:
- Canvas title as main header
- Metadata section with creation/update dates, owner, and canvas ID
- Original canvas content (converted to markdown if needed)

## Troubleshooting

### Common Issues

1. **"Invalid bot token"**: Make sure your bot token is correct and has the required scopes
2. **"Canvas not found"**: Verify the canvas ID and ensure the bot has access to it
3. **Permission errors**: Ensure the bot is added to the workspace and has appropriate permissions

### Testing Authentication

Use the test command to verify your bot token:

```bash
python export_canvas.py test-auth --token your-token
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.
