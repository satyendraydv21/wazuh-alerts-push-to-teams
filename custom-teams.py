# note if you are using custom-teams.py then you should ingnore custom-teams-optionalscript.py ***Anyway this scipt is tested so it's working correctly*
#----------custom-teams.py---------
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
#Start copy from here 
 
#!/usr/bin/env python3

import sys
import requests
import json

# Read configuration
alert_file = sys.argv[1]
user = sys.argv[2].split(":")[0]
hook_url = sys.argv[3]

# Read alert file
with open(alert_file) as f:
    alert_json = json.loads(f.read())

# Extract alert level
alert_level = alert_json["rule"]["level"]

# Choose color based on severity (Teams uses hex in cards)
if alert_level < 5:
    color = "00FF00"  # green
elif 5 <= alert_level <= 7:
    color = "FFFF00"  # yellow
else:
    color = "FF0000"  # red

# Agent name
if "agentless" in alert_json:
    agent_name = "agentless"
else:
    agent_name = alert_json["agent"]["name"]

# Prepare the Teams message card payload
payload = {
    "@type": "MessageCard",
    "@context": "http://schema.org/extensions",
    "summary": f"Wazuh Alert - Rule {alert_json['rule']['id']}",
    "themeColor": color,
    "title": f"Wazuh Alert - Rule {alert_json['rule']['id']}",
    "sections": [{
        "activityTitle": "🚨 **Alert Triggered**",
        "facts": [
            {"name": "Agent", "value": agent_name},
            {"name": "Description", "value": alert_json["rule"]["description"]},
            {"name": "Level", "value": str(alert_level)},
        ],
        "markdown": True
    }]
}

# Send the POST request
response = requests.post(hook_url, data=json.dumps(payload), headers={"Content-Type": "application/json"})

# Optional: print response for debugging
if response.status_code != 200:
    print(f"[!] Error sending to Teams: {response.status_code} - {response.text}")
