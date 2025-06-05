----------custom-teams.py---------
#sudo chmod 750 /var/ossec/integrations/custom-*
#sudo chown root:wazuh /var/ossec/integrations/custom-*
#Add this integration at ossec.config
"""
ossec.conf configuration structure
<integration>
<name>custom-teams</name>
<hook_url>https://teams.com/api/webhooks/XXXXXXXXXXX</hook_url>
<alert_format>json</alert_format>
</integration>
"""

 
#!/usr/bin/env python3
 
import sys
import json
import requests
import os
 
# Get arguments
alert_file = sys.argv[1]
 
# Read webhook URL from environment variable set by Wazuh
webhook_url = os.environ.get("WAZUH_INTEGRATION_WEBHOOK_URL")
if not webhook_url:
    print("Error: Missing webhook URL in environment variable")
    sys.exit(1)
 
# Read the alert file
with open(alert_file, 'r') as f:
    try:
        alert_json = json.load(f)
    except Exception as e:
        print(f"Error: Could not decode JSON alert - {e}")
        sys.exit(1)
 
# Extract alert data
rule = alert_json.get("rule", {})
agent = alert_json.get("agent", {}).get("name", "N/A")
description = rule.get("description", "No description")
rule_id = rule.get("id", "N/A")
level = rule.get("level", 0)
 
# Set color based on level
if level < 5:
    themeColor = "00FF00"  # Green
elif 5 <= level <= 7:
    themeColor = "FFFF00"  # Yellow
else:
    themeColor = "FF0000"  # Red
 
# Prepare Teams payload
teams_payload = {
    "@type": "MessageCard",
    "@context": "http://schema.org/extensions",
    "summary": "Wazuh Alert",
    "themeColor": themeColor,
    "title": f"Wazuh Alert - Rule {rule_id}",
    "sections": [
        {
            "activityTitle": f"**Agent**: {agent}",
            "text": f"**Description**: {description}\n\n**Level**: {level}"
        }
    ]
}
 
# Send to Teams
headers = {"Content-Type": "application/json"}
response = requests.post(webhook_url, headers=headers, json=teams_payload)
 
if response.status_code != 200:
    print(f"Error sending to Teams: {response.status_code} - {response.text}")
    sys.exit(1)
 
sys.exit(0)
