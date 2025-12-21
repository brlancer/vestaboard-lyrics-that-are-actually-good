#!/usr/bin/env python3
"""
Daily Song Lyric Sender for Vestaboard
Sends a random song lyric to a Vestaboard display using VBML formatting.
"""

import os
import sys
import random
import requests
import gspread
from google.oauth2.service_account import Credentials
from typing import Optional


# Hardcoded list of 10 song lyrics (fallback if Google Sheets fails)
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


def fetch_lyrics_from_google_sheets() -> Optional[list]:
    """
    Fetch lyrics from Google Sheets using service account authentication.
    
    Returns:
        List of lyrics if successful, None if error occurs
    """
    try:
        # Get configuration from environment variables
        sheet_id = os.environ.get("GOOGLE_SHEET_ID")
        creds_file = os.environ.get("GOOGLE_CREDENTIALS_FILE")
        
        if not sheet_id or not creds_file:
            print("Google Sheets not configured (GOOGLE_SHEET_ID or GOOGLE_CREDENTIALS_FILE missing)")
            return None
        
        # Set up authentication
        scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        creds = Credentials.from_service_account_file(creds_file, scopes=scopes)
        client = gspread.authorize(creds)
        
        # Open the sheet and get the "lyrics" tab
        sheet = client.open_by_key(sheet_id)
        worksheet = sheet.worksheet("lyrics")
        
        # Get all values from the worksheet
        all_values = worksheet.get_all_values()
        
        if not all_values:
            print("No data found in Google Sheet")
            return None
        
        # Find the "formatted" column
        headers = all_values[0]
        try:
            formatted_col_index = headers.index("formatted")
        except ValueError:
            print("'formatted' column not found in sheet")
            return None
        
        # Extract all lyrics from the "formatted" column (skip header row)
        lyrics = [row[formatted_col_index] for row in all_values[1:] if len(row) > formatted_col_index and row[formatted_col_index].strip()]
        
        if not lyrics:
            print("No lyrics found in 'formatted' column")
            return None
        
        print(f"Successfully fetched {len(lyrics)} lyrics from Google Sheets")
        return lyrics
        
    except Exception as e:
        print(f"Error fetching lyrics from Google Sheets: {e}", file=sys.stderr)
        return None


def get_random_lyric(lyrics: list = None) -> str:
    """Select and return a random song lyric from the list."""
    if lyrics is None:
        lyrics = SONG_LYRICS
    return random.choice(lyrics)


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
                    "align": "left"
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
    
    # Try to fetch lyrics from Google Sheets
    lyrics = fetch_lyrics_from_google_sheets()
    
    if lyrics:
        print(f"Using lyrics from Google Sheets ({len(lyrics)} available)")
    else:
        print(f"Using fallback hardcoded lyrics ({len(SONG_LYRICS)} available)")
        lyrics = SONG_LYRICS
    
    # Step 1: Select a random lyric
    lyric = get_random_lyric(lyrics)
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
