"""Slack API client for fetching canvas data."""

import requests
import json
from typing import Dict, Any, Optional


class SlackAPIClient:
    """Client for interacting with Slack API to fetch canvas data."""
    
    def __init__(self, bot_token: str):
        """Initialize the Slack API client.
        
        Args:
            bot_token: Slack bot token for authentication
        """
        self.bot_token = bot_token
        self.base_url = "https://slack.com/api"
        self.headers = {
            "Authorization": f"Bearer {bot_token}",
            "Content-Type": "application/json"
        }
    
    def get_canvas_info(self, canvas_id: str) -> Optional[Dict[str, Any]]:
        """Get canvas information from Slack API.
        
        Args:
            canvas_id: The ID of the canvas to fetch
            
        Returns:
            Canvas data as a dictionary, or None if not found
            
        Raises:
            requests.RequestException: If the API request fails
            ValueError: If the response is invalid
        """
        url = f"{self.base_url}/canvases.info"
        params = {"canvas_id": canvas_id}
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get("ok"):
            error_msg = data.get("error", "Unknown error")
            if error_msg == "canvas_not_found":
                raise ValueError(f"Canvas with ID {canvas_id} not found")
            elif error_msg == "invalid_auth":
                raise ValueError("Invalid bot token provided")
            else:
                raise ValueError(f"Slack API error: {error_msg}")
        
        return data.get("canvas")
    
    def get_canvas_content(self, canvas_id: str) -> Optional[str]:
        """Get the content of a canvas.
        
        Args:
            canvas_id: The ID of the canvas to fetch content for
            
        Returns:
            Canvas content as a string, or None if not found
        """
        url = f"{self.base_url}/canvases.content.get"
        params = {"canvas_id": canvas_id}
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get("ok"):
            error_msg = data.get("error", "Unknown error")
            if error_msg == "canvas_not_found":
                raise ValueError(f"Canvas with ID {canvas_id} not found")
            elif error_msg == "invalid_auth":
                raise ValueError("Invalid bot token provided")
            else:
                raise ValueError(f"Slack API error: {error_msg}")
        
        # Canvas content might be in different formats depending on Slack's implementation
        content = data.get("content", {})
        
        # If it's already markdown, return it directly
        if isinstance(content, str):
            return content
        
        # If it's structured data, we might need to convert it
        # For now, return JSON representation if it's not a string
        return json.dumps(content, indent=2)