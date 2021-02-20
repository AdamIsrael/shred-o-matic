#!/usr/bin/env python3
import datetime
import os
import time

from slack import WebClient

# Delete files older than this number of days
DAYS = 90
CHANNELS=None

# Initialize a Web API client
client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

def main():

    ts_to = int(time.time()) - DAYS * 24 * 60 * 60
    channels = getChannels()

    print("Checking for old files...")
    response = client.files_list(channels=CHANNELS, ts_to=ts_to)

    # Walk backwards through the files, deleting by page
    # Hoping this will work around the issue of files_list returning 0 files
    # when there are clearly still files to delete.
    for page in range(response['paging']['pages'], 1, -1):
        # Get the next page of results
        print("Getting page {}".format(page))
        response = client.files_list(page=page, channels=CHANNELS, ts_to=ts_to)

        if response['ok'] is True:
            fc = len(response['files'])
            if fc == 0:
                print("No files to delete")
            else:
                print("Attempting to delete {} files...".format(fc))
                for file in response['files']:
                    id = file['id']
                    ts = time.ctime(file['created'])

                    # Attempt to suss out the channel name
                    channel = file['channels'][0]
                    cname = 'unknown'
                    if channel in channels:
                        cname = channels[channel]

                    if deleteFile(id):
                        print("Deleted file {} from #{} - ({})".format(id, cname, ts))

                # Sleep for a bit, to avoid rate limiting
                time.sleep(15)
        else:
            if response['error'] == 'ratelimited':
                time.sleep(30)
            else:
                print(response)
                break
    print("Done!")

def deleteFile(id : int):
    """Delete one file."""

    response = client.files_delete(file=id)

    return response['ok']


def getChannels():
    """Get a list of channels

    Get a dictionary of all channels on the server, keyed by id so that we can
    translate that into the friendly name.
    """
    channels = {}
    response = client.conversations_list()
    if response['ok']:
        for channel in response['channels']:
            id = channel['id']
            channels[id] = channel['name']

    return channels

if __name__ == "__main__":
    main()
