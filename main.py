#!/usr/bin/env python3
"""
Daily Song Lyric Sender for Vestaboard
Sends a random song lyric to a Vestaboard display using VBML formatting.
"""

import os
import sys
import random
import requests
from typing import Optional


# Hardcoded list of 10 song lyrics
SONG_LYRICS = [
    'The Beatles - "All you need is love"',
    'Bob Dylan - "The answer is blowin\' in the wind"',
    'Queen - "Is this the real life? Is this just fantasy?"',
    'John Lennon - "Imagine all the people living life in peace"',
    'Simon & Garfunkel - "Hello darkness, my old friend"',
    'David Bowie - "We can be heroes, just for one day"',
    'Louis Armstrong - "What a wonderful world"',
    'Bill Withers - "Lean on me, when you\'re not strong"',
    'Bob Marley - "Don\'t worry about a thing"',
    'Stevie Wonder - "I just called to say I love you"',
]

# API Configuration
VBML_COMPOSE_URL = "https://vbml.vestaboard.com/compose"
VESTABOARD_RW_URL = "https://rw.vestaboard.com/"


def get_random_lyric() -> str:
    """Select and return a random song lyric from the list."""
    return random.choice(SONG_LYRICS)


def format_lyric_with_vbml(lyric: str, api_key: str) -> Optional[list]:
    """
    Format the lyric using Vestaboard's VBML compose service.
    
    Args:
        lyric: The song lyric text to format
        api_key: Vestaboard API key for authentication
    
    Returns:
        Array of character codes if successful, None if error occurs
    """
    headers = {
        "X-Vestaboard-Read-Write-Key": api_key,
        "Content-Type": "application/json"
    }
    
    payload = {
        "components": [
            {
                "style": {
                    "justify": "center",
                    "align": "center"
                },
                "template": lyric
            }
        ]
    }
    
    try:
        print(f"Formatting lyric with VBML: {lyric}")
        response = requests.post(VBML_COMPOSE_URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        
        character_codes = response.json()
        print(f"Successfully formatted lyric. Response length: {len(character_codes)} rows")
        return character_codes
        
    except requests.exceptions.RequestException as e:
        print(f"Error formatting lyric with VBML: {e}", file=sys.stderr)
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}", file=sys.stderr)
        return None


def send_to_vestaboard(character_codes: list, api_key: str) -> bool:
    """
    Send the formatted message to the Vestaboard.
    
    Args:
        character_codes: Array of character codes from VBML compose
        api_key: Vestaboard API key for authentication
    
    Returns:
        True if successful, False otherwise
    """
    headers = {
        "X-Vestaboard-Read-Write-Key": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        print("Sending message to Vestaboard...")
        response = requests.post(VESTABOARD_RW_URL, json=character_codes, headers=headers, timeout=10)
        response.raise_for_status()
        
        print("Successfully sent message to Vestaboard!")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Vestaboard: {e}", file=sys.stderr)
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}", file=sys.stderr)
        return False


def main():
    """Main execution function."""
    # Get API key from environment variable
    api_key = os.environ.get("VESTABOARD_API_KEY")
    
    if not api_key:
        print("Error: VESTABOARD_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)
    
    # Step 1: Select a random lyric
    lyric = get_random_lyric()
    print(f"\n{'='*60}")
    print(f"Selected lyric: {lyric}")
    print(f"{'='*60}\n")
    
    # Step 2: Format the lyric using VBML
    character_codes = format_lyric_with_vbml(lyric, api_key)
    
    if character_codes is None:
        print("Failed to format lyric. Exiting.", file=sys.stderr)
        sys.exit(1)
    
    # Step 3: Send to Vestaboard
    success = send_to_vestaboard(character_codes, api_key)
    
    if not success:
        print("Failed to send message to Vestaboard. Exiting.", file=sys.stderr)
        sys.exit(1)
    
    print("\n✓ Daily lyric successfully sent to Vestaboard!")


if __name__ == "__main__":
    main()
