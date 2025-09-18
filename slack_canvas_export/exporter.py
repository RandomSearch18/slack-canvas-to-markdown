"""Canvas exporter for converting and saving canvas data to markdown files."""

import os
import json
import re
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path


class CanvasExporter:
    """Handles exporting canvas data to markdown files."""

    def __init__(self, output_dir: str = "./exported_canvases"):
        """Initialize the canvas exporter.

        Args:
            output_dir: Directory to save exported markdown files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for filesystem compatibility.

        Args:
            filename: Original filename

        Returns:
            Sanitized filename safe for filesystem
        """
        # Remove or replace invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', "_", filename)
        # Replace multiple underscores with single one
        filename = re.sub(r"_{2,}", "_", filename)
        # Remove leading/trailing underscores and spaces
        filename = filename.strip("_ ")
        # Ensure it's not empty
        if not filename:
            filename = "untitled"
        return filename

    def convert_to_markdown(
        self, canvas_data: Dict[str, Any], canvas_content: Optional[str]
    ) -> str:
        """Convert canvas data to markdown format.

        Args:
            canvas_data: Canvas metadata and information
            canvas_content: Canvas content (may already be markdown)

        Returns:
            Markdown formatted string
        """
        markdown_lines = []

        # Add title from canvas metadata
        title = canvas_data.get("title", "Untitled Canvas")
        markdown_lines.append(f"# {title}\n")

        # Add metadata section
        markdown_lines.append("## Canvas Information\n")

        # Add creation/modification dates if available
        if "date_create" in canvas_data:
            create_date = datetime.fromtimestamp(canvas_data["date_create"]).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            markdown_lines.append(f"**Created:** {create_date}\n")

        if "date_update" in canvas_data:
            update_date = datetime.fromtimestamp(canvas_data["date_update"]).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            markdown_lines.append(f"**Updated:** {update_date}\n")

        # Add canvas ID for reference
        canvas_id = canvas_data.get("id", "Unknown")
        markdown_lines.append(f"**Canvas ID:** {canvas_id}\n")

        # Add owner information if available
        if "owner" in canvas_data:
            owner = canvas_data["owner"]
            if isinstance(owner, dict):
                owner_name = owner.get("name", owner.get("real_name", "Unknown"))
                markdown_lines.append(f"**Owner:** {owner_name}\n")

        markdown_lines.append("\n---\n")
        markdown_lines.append("## Canvas Content\n")

        # Add the actual canvas content
        if canvas_content:
            # Check if content looks like markdown already
            if self._is_likely_markdown(canvas_content):
                markdown_lines.append(canvas_content)
            else:
                # If it's JSON or other structured data, format it appropriately
                try:
                    # Try to parse as JSON and format nicely
                    parsed_json = json.loads(canvas_content)
                    markdown_lines.append("```json\n")
                    markdown_lines.append(json.dumps(parsed_json, indent=2))
                    markdown_lines.append("\n```\n")
                except json.JSONDecodeError:
                    # If it's not JSON, just add as preformatted text
                    markdown_lines.append("```\n")
                    markdown_lines.append(canvas_content)
                    markdown_lines.append("\n```\n")
        else:
            markdown_lines.append("*No content available*\n")

        return "\n".join(markdown_lines)

    def _is_likely_markdown(self, content: str) -> bool:
        """Check if content appears to be markdown formatted.

        Args:
            content: Content to check

        Returns:
            True if content appears to be markdown
        """
        # Simple heuristics to detect markdown
        markdown_indicators = [
            r"^#{1,6}\s+",  # Headers
            r"\*\*.*\*\*",  # Bold
            r"\*.*\*",  # Italic
            r"^\* ",  # Bullet points
            r"^\d+\. ",  # Numbered lists
            r"`.*`",  # Inline code
            r"```",  # Code blocks
            r"^\> ",  # Blockquotes
            r"\[.*\]\(.*\)",  # Links
        ]

        content_lines = content.split("\n")
        markdown_matches = 0

        for line in content_lines[:20]:  # Check first 20 lines
            for pattern in markdown_indicators:
                if re.search(pattern, line, re.MULTILINE):
                    markdown_matches += 1
                    break

        # If more than 20% of lines have markdown indicators, assume it's markdown
        return markdown_matches > len(content_lines) * 0.2

    def export_canvas(
        self, canvas_data: Dict[str, Any], canvas_content: Optional[str]
    ) -> str:
        """Export canvas to a markdown file.

        Args:
            canvas_data: Canvas metadata and information
            canvas_content: Canvas content

        Returns:
            Path to the exported file
        """
        # Generate filename from title and canvas ID
        title = canvas_data.get("title", "untitled")
        canvas_id = canvas_data.get("id", "unknown")

        safe_title = self.sanitize_filename(title)
        filename = f"{safe_title}_{canvas_id}.md"

        # Convert to markdown
        markdown_content = self.convert_to_markdown(canvas_data, canvas_content)

        # Write to file
        file_path = self.output_dir / filename

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        return str(file_path)
