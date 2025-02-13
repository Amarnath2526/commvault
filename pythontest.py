from cvpysdk.commcell import Commcell
from cvpysdk.exception import SDKException

# Replace these variables with your Commvault and SharePoint Online details
commvault_webconsole = 'https://m036.metallic.io/commandcenter/#/serviceCatalogV2'
username = 'camarnathreddy@metallicsupportlab.com'
password = 'Deccom@2024#'
sharepoint_online_site_url = 'https://metallicsupportlab.sharepoint.com/sites/ExampleTeamSite'

try:
    # Connect to Commvault
    commcell = Commcell(commvault_webconsole, username, password)
    
    # Get the SharePoint Online client
    client = commcell.clients.get('SharePoint Online Client Name')
    
    # Get the backupset for the specific SharePoint Online site
    backupset = client.backupsets.get(sharepoint_online_site_url)
    
    # Run a backup job for the SharePoint Online site
    backup_job = backupset.backup()
    
    # Check the status of the backup job
    if backup_job:
        print(f"Backup Job ID: {backup_job.job_id}")
        print("Backup job successfully started.")
    else:
        print("Failed to start the backup job.")
    
  
        
except SDKException as e:
    print(f"An error occurred: {e}")


pause = input("Press Enter to continue...")



