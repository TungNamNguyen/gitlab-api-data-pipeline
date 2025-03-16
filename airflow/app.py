import sys
import argparse
import logging
from utils.logger import setup_logger
from database.models import init_db
from database.operations import ProjectRepository
from api.client import GitLabApiClient
from config import DATABASE_URI
from datetime import datetime

# Set up logging
logger = setup_logger()

def fetch_and_store_projects():
    """
    Fetch projects from GitLab API and store them in the database.
    
    Returns:
        int: Number of projects processed
    """
    try:
        logger.info("Starting GitLab API data extraction")
        
        # Initialize database
        logger.info(f"Initializing database connection to {DATABASE_URI}")
        session = init_db(DATABASE_URI)
        project_repo = ProjectRepository(session)
        
        # Initialize API client
        api_client = GitLabApiClient()
        
        # Fetch projects
        logger.info("Fetching projects from GitLab API")
        projects = api_client.get_projects()
        
        # Store projects in database
        project_count = 0
        for project_data in projects:
            try:
                # Check if project already exists
                existing_project = project_repo.get_project_by_id(project_data["id"])
                
                if existing_project:
                    # Update existing project
                    project_repo.update_project(project_data["id"], project_data)
                else:
                    # Create new project
                    project_repo.create_project(project_data)
                
                project_count += 1
            except Exception as e:
                logger.error(f"Error processing project {project_data.get('id')}: {str(e)}")
                # Continue with next project
                continue
        
        logger.info(f"Successfully processed {project_count} projects")
        return project_count
        
    except Exception as e:
        logger.exception(f"An error occurred during data extraction: {str(e)}")
        raise

def list_projects():
    """
    List all projects in the database.
    """
    try:
        # Initialize database
        session = init_db(DATABASE_URI)
        project_repo = ProjectRepository(session)
        
        # Get all projects
        projects = project_repo.get_all_projects()
        
        if not projects:
            print("No projects found in the database.")
            return
        
        # Print project information
        print(f"\n{'ID':<6} {'Name':<30} {'Visibility':<12} {'Last Activity':<20}")
        print("-" * 70)
        
        for project in projects:
            last_activity = project.last_activity_at.strftime('%Y-%m-%d %H:%M') if project.last_activity_at else "N/A"
            print(f"{project.id:<6} {project.name[:30]:<30} {project.visibility:<12} {last_activity:<20}")
        
        print(f"\nTotal: {len(projects)} projects")
        
    except Exception as e:
        logger.exception(f"Error listing projects: {str(e)}")
        print(f"Error: {str(e)}")

def show_project(project_id):
    """
    Show detailed information about a specific project.
    
    Args:
        project_id (int): Project ID
    """
    try:
        # Initialize database
        session = init_db(DATABASE_URI)
        project_repo = ProjectRepository(session)
        
        # Get project
        project = project_repo.get_project_by_id(project_id)
        
        if not project:
            print(f"Project with ID {project_id} not found.")
            return
        
        # Print project details
        print("\nProject Details:")
        print(f"{'ID:':<20} {project.id}")
        print(f"{'Name:':<20} {project.name}")
        print(f"{'Description:':<20} {project.description or 'N/A'}")
        print(f"{'Full Path:':<20} {project.path_with_namespace}")
        print(f"{'Web URL:':<20} {project.web_url}")
        print(f"{'Visibility:':<20} {project.visibility}")
        print(f"{'Created At:':<20} {project.created_at}")
        print(f"{'Last Activity:':<20} {project.last_activity_at}")
        print(f"{'Archived:':<20} {project.archived}")
        
        # Print namespace information
        if project.namespaces:
            namespace = project.namespaces[0]
            print("\nNamespace:")
            print(f"{'ID:':<20} {namespace.id}")
            print(f"{'Name:':<20} {namespace.name}")
            print(f"{'Kind:':<20} {namespace.kind}")
            print(f"{'Full Path:':<20} {namespace.full_path}")
        
    except Exception as e:
        logger.exception(f"Error showing project {project_id}: {str(e)}")
        print(f"Error: {str(e)}")

def update_project(project_id):
    """
    Update a project in the database.
    
    Args:
        project_id (int): Project ID
    """
    try:
        # Initialize database
        session = init_db(DATABASE_URI)
        project_repo = ProjectRepository(session)
        
        # Get project first to confirm it exists
        project = project_repo.get_project_by_id(project_id)
        
        if not project:
            print(f"Project with ID {project_id} not found.")
            return
        
        print("Current project details:")
        print(f"{'ID:':<20} {project.id}")
        print(f"{'Name:':<20} {project.name}")
        print(f"{'Description:':<20} {project.description or 'N/A'}")
        print(f"{'Full Path:':<20} {project.path_with_namespace}")
        print(f"{'Web URL:':<20} {project.web_url}")
        print(f"{'Visibility:':<20} {project.visibility}")
        
        # Get new project data from user input
        new_name = input("Enter new name (leave empty to keep current): ")
        new_description = input("Enter new description (leave empty to keep current): ")
        new_visibility = input("Enter new visibility (leave empty to keep current): ")
        
        # Update project fields if provided
        if new_name:
            project.name = new_name
        if new_description:
            project.description = new_description
        if new_visibility:
            project.visibility = new_visibility
        
        # Update project in database
        project_repo.update_project(project_id, {
            "name": project.name,
            "description": project.description,
            "visibility": project.visibility
        })
        
        print(f"Project '{project.id}' has been updated successfully.")
        
    except Exception as e:
        logger.exception(f"Error updating project {project_id}: {str(e)}")
        print(f"Error: {str(e)}")

def delete_project(project_id):
    """
    Delete a project from the database.
    
    Args:
        project_id (int): Project ID
    """
    try:
        # Initialize database
        session = init_db(DATABASE_URI)
        project_repo = ProjectRepository(session)
        
        # Get project first to confirm it exists
        project = project_repo.get_project_by_id(project_id)
        
        if not project:
            print(f"Project with ID {project_id} not found.")
            return
        
        # Confirm deletion
        confirm = input(f"Are you sure you want to delete project '{project.name}' (ID: {project_id})? [y/N]: ")
        
        if confirm.lower() == 'y':
            # Delete project
            project_repo.delete_project(project_id)
            print(f"Project '{project.name}' (ID: {project_id}) has been successfully deleted.")
        else:
            print("Deletion canceled.")
        
    except Exception as e:
        logger.exception(f"Error deleting project {project_id}: {str(e)}")
        print(f"Error: {str(e)}")

def main():
    """
    Main function to parse arguments and execute commands.
    
    Returns:
        int: Exit code
    """
    parser = argparse.ArgumentParser(description='GitLab API Data Extraction Tool')
    
    # Define subcommands
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # 'fetch' command
    fetch_parser = subparsers.add_parser('fetch', help='Fetch projects from GitLab API')
    
    # 'list' command
    list_parser = subparsers.add_parser('list', help='List all projects in the database')
    
    # 'show' command
    show_parser = subparsers.add_parser('show', help='Show details of a specific project')
    show_parser.add_argument('id', type=int, help='Project ID')
    
    # 'update' command
    update_parser = subparsers.add_parser('update', help='Update a project in the database')
    update_parser.add_argument('id', type=int, help='Project ID')
    
    # 'delete' command
    delete_parser = subparsers.add_parser('delete', help='Delete a project from the database')
    delete_parser.add_argument('id', type=int, help='Project ID')
    
    args = parser.parse_args()
    
    # Execute appropriate command
    try:
        if args.command == 'fetch' or args.command is None:
            # Default to fetch if no command is provided
            count = fetch_and_store_projects()
            print(f"Successfully processed {count} projects.")
            return 0
        elif args.command == 'list':
            list_projects()
            return 0
        elif args.command == 'show':
            show_project(args.id)
            return 0
        elif args.command == 'update':
            update_project(args.id)
            return 0
        elif args.command == 'delete':
            delete_project(args.id)
            return 0
        else:
            parser.print_help()
            return 1
    except Exception as e:
        logger.exception(f"Unhandled error in main function: {str(e)}")
        print(f"An error occurred: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())