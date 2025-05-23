import pandas as pd
import json

# The input data (as a JSON list) would typically be loaded from a file
data = [
    {"id": "start", "type": "procedure", "text": "Procedure for Start: Follow standard troubleshooting steps."},
    {"id": "start-script", "type": "script", "text": "Script for Start: Hello! Let's check the issue with your internet. Start?"},
    {"id": "start-article", "type": "article", "text": "Article for Start: This step helps users resolve start related issues."},
    {"id": "modem-lights", "type": "procedure", "text": "Procedure for Are modem lights on?: Follow standard troubleshooting steps."},
    {"id": "modem-lights-script", "type": "script", "text": "Script for Are modem lights on?: Hello! Let's check the issue with your internet. Are modem lights on??"},
    {"id": "modem-lights-article", "type": "article", "text": "Article for Are modem lights on?: This step helps users resolve are modem lights on? related issues."},
    {"id": "restart-modem", "type": "procedure", "text": "Procedure for Restart modem: Follow standard troubleshooting steps."},
    {"id": "restart-modem-script", "type": "script", "text": "Script for Restart modem: Hello! Let's check the issue with your internet. Restart modem?"},
    {"id": "restart-modem-article", "type": "article", "text": "Article for Restart modem: This step helps users resolve restart modem related issues."},
    {"id": "wifi-signal", "type": "procedure", "text": "Procedure for Ask about Wi-Fi signal: Follow standard troubleshooting steps."},
    {"id": "wifi-signal-script", "type": "script", "text": "Script for Ask about Wi-Fi signal: Hello! Let's check the issue with your internet. Ask about Wi-Fi signal?"},
    {"id": "wifi-signal-article", "type": "article", "text": "Article for Ask about Wi-Fi signal: This step helps users resolve ask about wi-fi signal related issues."},
    {"id": "check-cable", "type": "procedure", "text": "Procedure for Check cable connection: Follow standard troubleshooting steps."},
    {"id": "check-cable-script", "type": "script", "text": "Script for Check cable connection: Hello! Let's check the issue with your internet. Check cable connection?"},
    {"id": "check-cable-article", "type": "article", "text": "Article for Check cable connection: This step helps users resolve check cable connection related issues."},
    {"id": "guide-plug", "type": "procedure", "text": "Procedure for Guide user to plug/unplug: Follow standard troubleshooting steps."},
    {"id": "guide-plug-script", "type": "script", "text": "Script for Guide user to plug/unplug: Hello! Let's check the issue with your internet. Guide user to plug/unplug?"},
    {"id": "guide-plug-article", "type": "article", "text": "Article for Guide user to plug/unplug: This step helps users resolve guide user to plug/unplug related issues."},
    {"id": "escalate", "type": "procedure", "text": "Procedure for Escalate to technician: Follow standard troubleshooting steps."},
    {"id": "escalate-script", "type": "script", "text": "Script for Escalate to technician: Hello! Let's check the issue with your internet. Escalate to technician?"},
    {"id": "escalate-article", "type": "article", "text": "Article for Escalate to technician: This step helps users resolve escalate to technician related issues."},
    {"id": "close-call", "type": "procedure", "text": "Procedure for Close with confirmation: Follow standard troubleshooting steps."},
    {"id": "close-call-script", "type": "script", "text": "Script for Close with confirmation: Hello! Let's check the issue with your internet. Close with confirmation?"},
    {"id": "close-call-article", "type": "article", "text": "Article for Close with confirmation: This step helps users resolve close with confirmation related issues."},
    {"id": "callback", "type": "procedure", "text": "Procedure for Offer callback: Follow standard troubleshooting steps."},
    {"id": "callback-script", "type": "script", "text": "Script for Offer callback: Hello! Let's check the issue with your internet. Offer callback?"},
    {"id": "callback-article", "type": "article", "text": "Article for Offer callback: This step helps users resolve offer callback related issues."},
    {"id": "end", "type": "procedure", "text": "Procedure for End: Follow standard troubleshooting steps."},
    {"id": "end-script", "type": "script", "text": "Script for End: Hello! Let's check the issue with your internet. End?"},
    {"id": "end-article", "type": "article", "text": "Article for End: This step helps users resolve end related issues."}
]

# Organize data by node base name
grouped = {}
for entry in data:
    base = entry["id"].split("-")[0]
    if base not in grouped:
        grouped[base] = {"procedure": "", "script": "", "article": ""}
    grouped[base][entry["type"]] = entry["text"]

df = pd.DataFrame.from_dict(grouped, orient="index")
#print(df.to_markdown(index=False))
df.to_csv("table_datta.csv", index=False)
