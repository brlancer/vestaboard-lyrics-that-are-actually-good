# 🎵 Vestaboard Daily Lyrics

A Python automation script that sends a beautifully formatted song lyric to your Vestaboard display every day. The script uses Vestaboard's VBML (Vestaboard Markup Language) service to center and format lyrics for optimal display on the 6×22 character grid.

## ✨ Features

- **Daily Automation**: Runs automatically every day at 9:00 AM PST via GitHub Actions
- **VBML Formatting**: Uses Vestaboard's compose endpoint to center and align lyrics perfectly
- **Random Selection**: Picks a different lyric from a curated collection each day
- **Error Handling**: Comprehensive error handling with detailed logging
- **Manual Trigger**: Can be triggered manually from GitHub Actions UI for testing
- **Zero Infrastructure**: Runs entirely on GitHub Actions - no servers needed

## 📋 Prerequisites

- A [Vestaboard](https://www.vestaboard.com/) display
- Vestaboard Read/Write API Key ([get one here](https://www.vestaboard.com/))
- GitHub account (for automated daily runs)
- Python 3.11+ (for local testing)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/vestaboard-lyrics-that-are-actually-good.git
cd vestaboard-lyrics-that-are-actually-good
```

### 2. Set Up GitHub Secret

1. Navigate to your repository on GitHub
2. Go to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Create a secret with:
   - **Name**: `VESTABOARD_API_KEY`
   - **Value**: Your Vestaboard Read/Write API key

### 3. Enable GitHub Actions

Push your code to GitHub. The workflow will automatically:
- Run every day at 9:00 AM PST
- Or be triggered manually from the **Actions** tab

## 🏠 Local Development

### Installation

```bash
# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running Locally

```bash
# Set your API key as an environment variable
export VESTABOARD_API_KEY="your-api-key-here"

# Run the script
python main.py
```

### Expected Output

```
============================================================
Selected lyric: The Beatles - "All you need is love"
============================================================

Formatting lyric with VBML: The Beatles - "All you need is love"
Successfully formatted lyric. Response length: 6 rows
Sending message to Vestaboard...
Successfully sent message to Vestaboard!

✓ Daily lyric successfully sent to Vestaboard!
```

## 🎨 Customization

### Adding More Lyrics

Edit the `SONG_LYRICS` list in [main.py](main.py):

```python
SONG_LYRICS = [
    'Artist Name - "Your lyric here"',
    'Another Artist - "Another great lyric"',
    # Add as many as you like!
]
```

**Tips for Lyrics:**
- Keep them concise (Vestaboard is 6 rows × 22 columns)
- The VBML formatter will handle wrapping and centering
- Include artist attribution for context
- Test locally to see how they look

### Changing the Schedule

Edit [.github/workflows/daily_lyric.yml](.github/workflows/daily_lyric.yml):

```yaml
schedule:
  # Cron format: minute hour day month day-of-week
  - cron: '0 17 * * *'  # 9:00 AM PST (17:00 UTC)
```

**Common Schedules:**
- `'0 17 * * *'` - 9:00 AM PST daily
- `'0 14 * * *'` - 6:00 AM PST daily
- `'0 1 * * 1'` - 5:00 PM PST every Monday
- `'0 */4 * * *'` - Every 4 hours

Use [crontab.guru](https://crontab.guru/) to generate cron expressions.

### Customizing VBML Formatting

Edit the `format_lyric_with_vbml()` function in [main.py](main.py):

```python
payload = {
    "components": [
        {
            "style": {
                "justify": "center",  # Options: left, center, right
                "align": "center"     # Options: top, center, bottom
            },
            "template": lyric
        }
    ]
}
```

## 🔧 How It Works

### Architecture

```
┌─────────────────────┐
│   GitHub Actions    │
│   (Daily at 9 AM)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     main.py         │
│  1. Select lyric    │
│  2. Format via VBML │
│  3. Send to board   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Vestaboard API    │
│   - VBML Compose    │
│   - Read/Write      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Your Vestaboard!   │
└─────────────────────┘
```

### API Flow

1. **VBML Compose** (`https://vbml.vestaboard.com/compose`)
   - Sends lyric text with formatting preferences
   - Returns a 6×22 array of character codes
   - Character codes represent Vestaboard's internal character set

2. **Vestaboard Read/Write** (`https://rw.vestaboard.com/`)
   - Receives the character code array
   - Updates your Vestaboard display
   - Confirms successful update

## 📖 API Reference

### Authentication

All requests require the Read/Write API key:

```
Header: X-Vestaboard-Read-Write-Key
Value: your-api-key-here
```

### VBML Compose Endpoint

**URL**: `https://vbml.vestaboard.com/compose`  
**Method**: POST  
**Content-Type**: application/json

**Request Body**:
```json
{
  "components": [
    {
      "style": {
        "justify": "center",
        "align": "center"
      },
      "template": "Your text here"
    }
  ]
}
```

**Response**: Array of 6 arrays (rows), each containing 22 integers (character codes)

### Vestaboard Read/Write Endpoint

**URL**: `https://rw.vestaboard.com/`  
**Method**: POST  
**Content-Type**: application/json

**Request Body**: Character code array from VBML compose, or:
```json
{"text": "Simple text message"}
```

## 🐛 Troubleshooting

### Script Fails with "VESTABOARD_API_KEY environment variable not set"

**Solution**: Ensure you've set the GitHub Secret or local environment variable:
```bash
export VESTABOARD_API_KEY="your-key-here"
```

### "Error formatting lyric with VBML"

**Possible Causes**:
- Invalid API key
- Network connectivity issues
- Lyric text contains unsupported characters

**Solution**: Check the error logs in GitHub Actions or terminal output for specific details.

### "Error sending message to Vestaboard"

**Possible Causes**:
- API key lacks write permissions
- Vestaboard is offline or disconnected

**Solution**: 
1. Verify your API key has Read/Write permissions
2. Check your Vestaboard's network connection
3. Test with a simple message locally

### Workflow Not Running at Expected Time

**Note**: GitHub Actions uses UTC time. PST is UTC-8, so:
- 9:00 AM PST = 17:00 UTC
- During Daylight Saving Time (PDT), adjust accordingly

### Testing Without Waiting for Schedule

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Select **Daily Vestaboard Lyric** workflow
4. Click **Run workflow** button
5. Select branch and click **Run workflow**

## 📁 Project Structure

```
vestaboard-lyrics-that-are-actually-good/
├── .github/
│   └── workflows/
│       └── daily_lyric.yml    # GitHub Actions workflow
├── main.py                     # Main Python script
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🔐 Security Best Practices

- ✅ **Never commit API keys** to the repository
- ✅ **Use GitHub Secrets** for sensitive credentials
- ✅ **Rotate API keys** periodically
- ✅ **Review workflow logs** for any exposed credentials (they should be masked)

## 🤝 Contributing

Want to improve this project? Contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Ideas for Contributions

- [ ] Add support for external lyric sources (APIs, CSV files)
- [ ] Implement lyric history to avoid repeats
- [ ] Add configuration file for easier customization
- [ ] Support for multiple Vestaboards
- [ ] Quote of the day mode
- [ ] Weather integration
- [ ] Special messages for holidays

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [Vestaboard](https://www.vestaboard.com/) for their amazing display and API
- All the incredible artists whose lyrics bring joy to our days

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/vestaboard-lyrics-that-are-actually-good/issues)
- **Vestaboard API Docs**: [Vestaboard Developers](https://docs.vestaboard.com/)
- **GitHub Actions Docs**: [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

Made with ❤️ for Vestaboard enthusiasts
