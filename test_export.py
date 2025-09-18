#!/usr/bin/env python3
"""
Test script to demonstrate the canvas exporter functionality with mock data.
"""

import sys
import json
from datetime import datetime
from pathlib import Path

# Add the package to Python path
sys.path.insert(0, str(Path(__file__).parent))

from slack_canvas_export.exporter import CanvasExporter


def create_mock_canvas_data():
    """Create mock canvas data for testing."""
    return {
        "id": "F09G8G3GB6V",
        "title": "Project Planning Canvas",
        "date_create": int(datetime(2024, 1, 15, 10, 30).timestamp()),
        "date_update": int(datetime(2024, 1, 20, 14, 45).timestamp()),
        "owner": {"id": "U1234567890", "name": "john.doe", "real_name": "John Doe"},
    }


def create_mock_markdown_content():
    """Create mock markdown content."""
    return """# Team Goals for Q1 2024

## Objectives
- Increase user engagement by 25%
- Launch new feature set
- Improve customer satisfaction

## Action Items
- [ ] Conduct user research
- [x] Design mockups
- [ ] Development sprint planning

## Notes
This is a **bold** statement with some *emphasis*.

```python
def hello_world():
    print("Hello, World!")
```

[Link to documentation](https://example.com/docs)
"""


def create_mock_json_content():
    """Create mock JSON content to test conversion."""
    return json.dumps(
        {
            "type": "canvas",
            "version": "1.0",
            "content": {
                "blocks": [
                    {"type": "header", "text": "Welcome to our Canvas"},
                    {
                        "type": "text",
                        "content": "This is some example content in JSON format",
                    },
                ]
            },
        },
        indent=2,
    )


def test_markdown_export():
    """Test exporting a canvas with markdown content."""
    print("Testing markdown content export...")

    exporter = CanvasExporter("./test_exports")
    canvas_data = create_mock_canvas_data()
    canvas_content = create_mock_markdown_content()

    file_path = exporter.export_canvas(canvas_data, canvas_content)
    print(f"✓ Exported to: {file_path}")

    # Show the exported content
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    print("\n--- Exported Content ---")
    print(content[:500] + "..." if len(content) > 500 else content)
    print("--- End of Content ---\n")


def test_json_export():
    """Test exporting a canvas with JSON content."""
    print("Testing JSON content export...")

    exporter = CanvasExporter("./test_exports")
    canvas_data = create_mock_canvas_data()
    canvas_data["title"] = "API Response Canvas"
    canvas_data["id"] = "F09G8G3GB7W"
    canvas_content = create_mock_json_content()

    file_path = exporter.export_canvas(canvas_data, canvas_content)
    print(f"✓ Exported to: {file_path}")


def test_no_content_export():
    """Test exporting a canvas with no content."""
    print("Testing no content export...")

    exporter = CanvasExporter("./test_exports")
    canvas_data = create_mock_canvas_data()
    canvas_data["title"] = "Empty Canvas"
    canvas_data["id"] = "F09G8G3GB8X"

    file_path = exporter.export_canvas(canvas_data, None)
    print(f"✓ Exported to: {file_path}")


if __name__ == "__main__":
    print("Slack Canvas to Markdown Exporter - Test Suite")
    print("=" * 50)

    try:
        test_markdown_export()
        test_json_export()
        test_no_content_export()

        print("✓ All tests completed successfully!")
        print(
            "\nCheck the ./test_exports directory to see the generated markdown files."
        )

    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
