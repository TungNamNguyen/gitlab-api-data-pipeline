import requests
import logging
import json
from config import GITLAB_API_URL, GITLAB_PRIVATE_TOKEN

logger = logging.getLogger('gitlab_api.client')

class GitLabApiClient:
    """Client for interacting with the GitLab API."""
    
    def __init__(self, api_url=GITLAB_API_URL, private_token=GITLAB_PRIVATE_TOKEN):
        """
        Initialize GitLab API client.
        
        Args:
            api_url (str): GitLab API URL
            private_token (str): GitLab private token
        """
        self.api_url = api_url
        self.private_token = private_token
        self.headers = {
            "Private-Token": private_token,
            "Accept": "application/json"
        }
        
        # Validate configuration
        if not self.api_url or not self.private_token:
            logger.error("GitLab API URL or Private Token not configured")
            raise ValueError("GitLab API URL or Private Token not configured")
    
    def get_projects(self, params=None):
        """
        Get projects from the GitLab API.
        
        Args:
            params (dict, optional): Query parameters for the API request
            
        Returns:
            list: List of project dictionaries
            
        Raises:
            requests.RequestException: If API request fails
        """
        try:
            url = f"{self.api_url}/projects"
            logger.info(f"Fetching projects from {url}")
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()  # Raise exception for non-2xx responses
            
            projects = response.json()
            logger.info(f"Retrieved {len(projects)} projects from GitLab API")
            
            # Log sample data (for debugging)
            if projects:
                logger.debug(f"Sample project data: {json.dumps(projects[0], indent=2)}")
                
            return projects
            
        except requests.RequestException as e:
            logger.error(f"Error fetching projects from GitLab API: {str(e)}")
            # Re-raise exception after logging
            raise
    
    def get_project(self, project_id):
        """
        Get a specific project by ID.
        
        Args:
            project_id (int): Project ID
            
        Returns:
            dict: Project data
            
        Raises:
            requests.RequestException: If API request fails
        """
        try:
            url = f"{self.api_url}/projects/{project_id}"
            logger.info(f"Fetching project {project_id} from {url}")
            
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            project = response.json()
            logger.info(f"Retrieved project {project_id} from GitLab API")
            
            return project
            
        except requests.RequestException as e:
            logger.error(f"Error fetching project {project_id} from GitLab API: {str(e)}")
            raise