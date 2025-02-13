import os
import json
import time
import re
import datetime

# Function to get the UTC epoch time from a timestamp string
#def get_epoch_time(timestamp, time_format="%m/%d %H:%M:%S"):
    #return int(time.mktime(datetime.datetime.strptime(timestamp, time_format))).timestamp()

# Function to detect issue in the log files
def detect_issue(log_folder):
    issue_name = "SharePoint Restore Stuck"
    issue_description = "A large number of SharePoint files were accidentally deleted. The restore operation is critical to business operations."
    common_solution = "Authorize the Azure app to run backup or restore operations for SharePoint Online sites."
    
    issue_detected = False
    log_lines = []
    
    # Define a regex pattern to extract the timestamp
    #timestamp_pattern = re.compile(r'^\d{2}/\d{2} \d{2}:\d{2}:\d{2}')
    
    # Walk through the log folder to find and analyze the relevant log files
    for root, _, files in os.walk(log_folder):
        for file in files:
            if file.startswith("CVSPRestoreCtrl"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    for line_number, line in enumerate(f, 1):
                        if "is missing permissions for Sites APIs" in line or "is missing minimum Graph permissions required" in line or "Insufficient privileges to complete the operation" in line:
                            # Extract timestamps based on known token positions
                            tokens = line.split()
                            timestamp = tokens[2] + " " + tokens[3]
                            try:
                                #epoch_time = get_epoch_time(timestamp)
                                log_lines.append({
                                    "file": file,
                                    "lineNumber": line_number,
                                    #"timestamp": epoch_time,
                                    "line": line.strip()
                                })
                                issue_detected = True
                            except ValueError as e:
                                # Handle timestamp parsing error
                                print(f"Timestamp parsing error: {e} | Line: {line.strip()}")

    result = {
        "hasIssue": issue_detected,
        "name": issue_name,
        "description": issue_description,
        "solution": common_solution,
        "escalationEmails": [],
        "extraInfo": "",
        "logLines": log_lines
    }
    
    return result
    input("Press Enter to exit...")



# Path to the folder containing the log files
log_folder_path = (r"C:\Users\camarnathreddy\Documents\commvault\logs")

# Call the function and print the result as JSON
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        log_folder_path = sys.argv[1]
    result = detect_issue(log_folder_path)
    print(json.dumps(result, indent=2))
   



