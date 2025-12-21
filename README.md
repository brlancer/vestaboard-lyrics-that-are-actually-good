# 🎵 Vestaboard Daily Lyrics

Send a random song lyric to your Vestaboard display every day using GitHub Actions.

## Setup

### 1. Get Your API Key
Get a Vestaboard Read/Write API key from [vestaboard.com](https://www.vestaboard.com/)

### 2. Add GitHub Secret
1. Go to your repo **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `VESTABOARD_API_KEY`
4. Value: Your API key

### 3. Done!
The workflow runs daily at 9 AM PST. Manually trigger it from the **Actions** tab to test.

## Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Set your API key
export VESTABOARD_API_KEY="your-key-here"

# Run
python main.py
```

## Customize

**Add more lyrics**: Edit the `SONG_LYRICS` list in `main.py`

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
