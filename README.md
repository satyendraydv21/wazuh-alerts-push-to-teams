# wazuh-alerts-push-to-teams
wazuh-alerts-teams integration : - 

In this episode we will cover how to push Wazuh Alerts to your Teams server! I think this integration is super useful because 99% of us probably already use teams. Why monitor a Wazuh Dashboard when you can monitor your network through Teams?

# Here is the steps to do this integration : - 

Create a Ms teams Webhook
1.	Open teams.
2.	Go to the server you want to use to monitor Wazuh.
3.	Create a text channel.
And then - 
4.	click on - three dot then click on - Manage channel
5.	Go to connector and click on edit.
6.	Select the incoming Webhook or search it.
---
7.	Click New Webhook.
8.	Name your webhook but to something like WazuhAlerts.
9.	Select the text channel for your Wazuh alerts we created a second ago.
10.	Copy the Webhook to a notepad, we will paste it in a configuration file in a minute.
---
11. Configure Wazuh's Dashboard Integration settings
Login to your Wazuh dashboard and go to the following location:
(Server Manangement / Settings)
On the top right click (edit configuration)

----
12 . We are going to paste the following code BELOW the tags <global> </global>
 <integration>
     <name>custom-teams</name>
     <hook_url>https://teams.com/api/webhooks/XXXXXXXXXXX</hook_url>
     <level>3</level>
     <alert_format>json</alert_format>
 </integration>
Then paste your teams Webhook in the <hook_url> </hook_url> tags.

---

13.	Click Save.
14.	Restart Manager.

--
15. After you login perform the following commands:
    sudo su
then go to the config section for integrations:
    cd /var/ossec/integrations
We can use the following command to see a list of files in there
    ls -l
We need to create two file here cutom-teams, custom-teams.py- run this command
    nano custom-teams and paste following script and save this.
this is github link custom-teams script is there: - wazuh-alerts-push-to-teams/README.md at main · satyendraydv21/wazuh-alerts-push-to-teams
Now we need to create custom-teams.py
    nano custom-teams.py 
this is github link custom-teams.py script is there: - wazuh-alerts-push-to-teams/custom-teams.py at main · satyendraydv21/wazuh-alerts-push-to-teams
We can then verify they are downloaded. We can also see they are white because they don't have the proper permissions yet.
    ls -l
Then we need to ensure they have the proper permissions to execute:
sudo chmod 750 /var/ossec/integrations/custom-*
sudo chown root:wazuh /var/ossec/integrations/custom-*
---
Now we can verify they are correct one more time (and that they have turned green instead of white becuase they have the right perms now.)
    ls -l

----
Now because this is a python script we need to install the proper pip: (You may get a "Running as pip as the root user..." error but its fine, do not worry about it.)
    # debian / ubuntu
    sudo apt-get install python3-pip
    pip3 install requests

---
Lastly, we need to restart Wazuhs controls:
/var/ossec/bin/wazuh-control restart

---
Verify teams Alerts
Next we can go to our Teams channel and see the service restarted with a confirmation alert:


