# 🎵 Vestaboard Daily Lyrics

Send a random song lyric to your Vestaboard display every day using GitHub Actions.

## Setup

### 1. Get Your API Key
Get a Vestaboard Read/Write API key from [vestaboard.com](https://www.vestaboard.com/)

### 2. Set Up Google Sheets (Optional)

If you want to manage lyrics in a Google Sheet instead of editing code:

1. **Create a Google Cloud Service Account**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable Google Sheets API
   - Create a Service Account and download the JSON credentials file

2. **Create a Google Sheet**:
   - Create a new Google Sheet
   - Add a tab named `lyrics`
   - Add a column header `formatted` in the first row
   - Add your lyrics in rows below the header
   - Share the sheet with the service account email (found in the credentials JSON)

3. **Get the Sheet ID**:
   - The Sheet ID is in the URL: `https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit`

### 3. Add GitHub Secrets

For Google Sheets integration in GitHub Actions:

1. Go to your repo **Settings** → **Secrets and variables** → **Actions**
2. Add these secrets:
   - `VESTABOARD_API_KEY` - Your Vestaboard API key
   - `GOOGLE_SHEET_ID` - Your Google Sheet ID
   - `GOOGLE_CREDENTIALS` - Paste the entire contents of your service account JSON file

For the workflow to work, you'll need to update `.github/workflows/daily_lyric.yml` to write the credentials to a file.

### 4. Done!
The workflow runs daily at 9 AM PST. Manually trigger it from the **Actions** tab to test.

## Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Set your API key
export VESTABOARD_API_KEY="your-key-here"

# Optional: Set up Google Sheets
export GOOGLE_SHEET_ID="your-sheet-id"
export GOOGLE_CREDENTIALS_FILE="/path/to/credentials.json"

# Run
python main.py
```

**Note**: If Google Sheets environment variables are not set, the app will use the hardcoded lyrics as a fallback.

## Customize

**Manage lyrics in Google Sheets**: Follow setup instructions above to use a Google Sheet instead of hardcoded lyrics

**Add more hardcoded lyrics**: Edit the `SONG_LYRICS` list in `main.py` (used as fallback)

**Change schedule**: Edit the cron expression in `.github/workflows/daily_lyric.yml`
- Current: `'0 17 * * *'` (9 AM PST / 5 PM UTC)
- Use [crontab.guru](https://crontab.guru/) to customize

**Adjust formatting**: Modify the `style` object in `format_lyric_with_vbml()` in `main.py`

## Security

✅ API keys are stored securely in GitHub Secrets
✅ Never hardcoded in the codebase
✅ Automatically masked in workflow logs

**Note**: GitHub Secrets is the recommended approach for sensitive credentials in GitHub Actions. The secret is encrypted and only exposed to the workflow at runtime as an environment variable.

## How It Works

1. GitHub Actions triggers daily (or manually)
2. Script picks a random lyric
3. Formats it via Vestaboard's VBML API
4. Sends to your board via Read/Write API

## Troubleshooting

**"VESTABOARD_API_KEY not set"**: Add the GitHub Secret or set the environment variable locally

**Format/send errors**: Check API key permissions and Vestaboard connectivity in Action logs
