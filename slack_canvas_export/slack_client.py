"""Slack API client for fetching canvas data using files.info endpoint."""

import requests
import json
from typing import Dict, Any, Optional


class SlackAPIClient:
    """Client for interacting with Slack API to fetch canvas data via files.info."""

    def __init__(self, bot_token: str):
        """Initialize the Slack API client.

        Args:
            bot_token: Slack bot token for authentication
        """
        self.bot_token = bot_token
        self.base_url = "https://slack.com/api"
        self.headers = {
            "Authorization": f"Bearer {bot_token}",
            "Content-Type": "application/json",
        }

    def get_canvas_info(self, canvas_id: str) -> Optional[Dict[str, Any]]:
        """Get canvas information from Slack API using files.info.

        Args:
            canvas_id: The ID of the canvas to fetch (file ID)

        Returns:
            Canvas file data as a dictionary, or None if not found

        Raises:
            requests.RequestException: If the API request fails
            ValueError: If the response is invalid
        """
        url = f"{self.base_url}/files.info"
        params = {"file": canvas_id}

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()

        data = response.json()

        if not data.get("ok"):
            error_msg = data.get("error", "Unknown error")
            if error_msg == "file_not_found":
                raise ValueError(f"Canvas with ID {canvas_id} not found")
            elif error_msg == "invalid_auth":
                raise ValueError("Invalid bot token provided")
            else:
                raise ValueError(f"Slack API error: {error_msg}")

        return data.get("file")

    def get_canvas_content(self, canvas_id: str) -> Optional[str]:
        """Get the content of a canvas from the document_content field.

        Args:
            canvas_id: The ID of the canvas to fetch content for

        Returns:
            Canvas content as markdown string, or None if not found
        """
        # Get the canvas info first, which includes document_content
        canvas_info = self.get_canvas_info(canvas_id)
        
        if not canvas_info:
            return None
            
        # Extract document_content from the file object
        document_content = canvas_info.get("document_content", {})
        
        # Check if it's markdown type and extract content
        if document_content.get("type") == "markdown":
            return document_content.get("markdown", "")
        
        # If document_content is not present or not markdown, return None
        # Could potentially use download URLs here in the future if needed
        return None
