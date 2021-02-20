# shred-o-matic

shred-o-matic is Python script that uses the slackclient library to delete files older than 90 days.

Disclaimer: This works for me, but I make no claims it'll work for you. At a minimum, you can use this as a minimal example of how to work with the Slack API.


## Usage

```python
virtualenv -p python3 venv
. venv/bin/activate
pip install -r requirements.txt
SLACK_BOT_TOKEN='....' python3 shred-o-matic.py
```

## Authentication

You'll need to create a [new Slack App](https://api.slack.com/apps), [install to your workspace](https://api.slack.com/apps/A01NZCK7VGC/install-on-team?) and copy the OAuth Access Token from that page, passing that in as the SLACK_BOT_TOKEN environment variable.
## Known issues

You may need to run the script several times in order for all the old files to be deleted. I found that the API lags by minutes or tens of minutes; I might delete several pages of files but the page count takes a while to update.