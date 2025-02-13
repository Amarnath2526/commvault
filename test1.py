import os
import json
import re
from datetime import datetime
import time

def find_sharepoint_restore_issue(log_folder=(r"C:\Users\camarnathreddy\Documents\commvault\logs")):
	issue_name = "SharePoint Restore"
	issue_description = "A large number of SharePoint files were accidentally deleted. This restore is critical to business operations."
	common_solution = "Need to authorize the Azure app in order to run the backup or restore of SharePoint Online sites."
	relevant_log_files = ["CVSPRestoreCtrl.log"]
	identification_string = "Please make sure the azure app has Microsoft Graph - Application - Directory.Read.All permission."

	issues_found = []
	timestamp_format = "%m/%d %H:%M:%S"

	for dirpath, dirs, files in os.walk(log_folder):
		for filename in files:
			if filename in relevant_log_files:
				filepath = os.path.join(dirpath, filename)
				with open(filepath, 'r') as log_file:
					for line_number, line in enumerate(log_file, start=1):
						if identification_string in line:
							# Extract timestamp from the log line using regex
							match = re.search(r"\d{2}/\d{2} \d{2}:\d{2}:\d{2}", line)
							if match:
								timestamp_str = match.group()
								# Convert to UTC epoch time
								timestamp = int(datetime.strptime(timestamp_str, timestamp_format).replace(year=datetime.utcnow().year).timestamp())
								issues_found.append({
									"file": filename,
									"lineNumber": line_number,
									"timestamp": timestamp,
									"line": line.strip()
								})

	has_issue = bool(issues_found)

	output = {
		"hasIssue": has_issue,
		"name": issue_name,
		"description": issue_description,
		"solution": common_solution,
		"escalationEmails": [],
		"extraInfo": "",
		"logLines": issues_found
	}

	print(json.dumps(output, indent=2))

# Example use with the provided log folder
find_sharepoint_restore_issue(",")
input("Press Enter to exit...")