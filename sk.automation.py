import argparse
import os
import subprocess
from datetime import datetime
from skpy import Skype

from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from slack_sdk import WebClient
from time import sleep
import argparse

# Credentials and chatID for Skype
SKYPE_CHAT_ID = os.getenv("SKYPE_CHAT_ID")
SKYPE_USERNAME = os.getenv("SKYPE_USERNAME")
SKYPE_PASSWORD = os.getenv("SKYPE_PASSWORD")
SKYPE_SEND_EVERY = int(os.getenv("SKYPE_SEND_EVERY"))

JUMIA_URL = os.getenv("JUMIA_URL")


# Slack credentials, url and channel
'''SLACK_API_TOKEN = os.getenv("SLACK_API_TOKEN")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")
SLACK_CHANNEL_ID_2 = os.getenv("SLACK_CHANNEL_ID_2")'''

# Grafana and AppDynamics details
'''GRAFANA_TOKEN = os.getenv("GRAFANA_TOKEN")
GRAFANA_DASHBOARD_URL = os.getenv("GRAFANA_DASHBOARD_URL")
CATCHPOINT_REPORT_URL = os.getenv("CATCHPOINT_REPORT_URL")'''

# Interceptor for seleniumwire driver to add auth header
def interceptor(request):
    pass
    #request.headers['Authorization'] = f"Bearer {GRAFANA_TOKEN}"


# Capture screenshots
def capture():
    # Instance headless chrome driver
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    # Get Jumia screenshot
    driver.set_window_size(1800, 3400)
    driver.request_interceptor = interceptor
    driver.get(JUMIA_URL)
    sleep(20)
    el = driver.find_element(By.TAG_NAME, 'body')
    el.send_keys("d")
    el.send_keys("E")
    sleep(20)
    el.screenshot("jumia-screenshot.png")

    # Get Catchpoint screenshot
   ''' subprocess.run(
        [
            "/usr/bin/google-chrome",
            "--virtual-time-budget=5000",
            "--no-sandbox",
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--headless",
            "--hide-scrollbars",
            "--window-size=1920,1050",
            "--screenshot=catchpoint-screenshot.png",
            CATCHPOINT_REPORT_URL,
        ]
    )'''



# Send to slack function
'''def send2slack(nowdt):
    # Instance slack and setup images to send
    slack_client = WebClient(token=SLACK_API_TOKEN)
    file_uploads = [        
        {
            "file": "grafana-screenshot.png",
            "title": "grafana-screenshot.png",
        },
        {
            "file": "catchpoint-screenshot.png",
            "title": "catchpoint-screenshot.png",
        },

    ]

    # Upload images to slack
    upload = slack_client.files_upload_v2(
        file_uploads = file_uploads,
        channel = SLACK_CHANNEL_ID,
        initial_comment = nowdt
    )

    # Upload images to slack
    upload_2 = slack_client.files_upload_v2(
        file_uploads = file_uploads,
        channel = SLACK_CHANNEL_ID_2,
        initial_comment = nowdt
    )'''

# Send to skype function
def send2skype(nowdt):
    # Login to skype
    sk = Skype(SKYPE_USERNAME, SKYPE_PASSWORD)

    # Upload screenshot to group chat
    ch = sk.chats[SKYPE_CHAT_ID]
    #msg = ch.sendMsg(nowdt)
    msg = ch.sendFile(open("jumia-screenshot.png", "rb"), "jumia-screenshot.png", image=True)    
    #msg = ch.sendFile(open("catchpoint-screenshot.png", "rb"), "catchpoint-screenshot.png", image=True)

# Get now datetime for messages and for skype sending interval evaluation
nowdt = datetime.now()

# Call capture function
print(" ** Capturing jumia screenshot")
capture()

# Send captures to slack
'''print(" ** Sending captures to Slack")
send2slack(nowdt.ctime())'''

# Determine if we need to send to skype depending on the current time and SKYPE_SEND_EVERY
print(f'SKYPE_SEND_EVERY is set to {SKYPE_SEND_EVERY}, current minute is {nowdt.minute}...')
if SKYPE_SEND_EVERY > 0:
    for i in range(int(60/SKYPE_SEND_EVERY)):
        start_minute = i*SKYPE_SEND_EVERY
        print(f'evaluating if {nowdt.minute} is >= {start_minute} and < {start_minute+5}')
        if nowdt.minute >= start_minute and nowdt.minute < start_minute+5:
            print(" ** Sending captures to Skype")
            send2skype(nowdt.ctime())
            break
