"""
Database operations for the GitLab API data extraction application.

This module provides a repository class with CRUD operations for GitLab data.
"""

from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import logging
from database.models import Project, Namespace

logger = logging.getLogger('gitlab_api.database')

class ProjectRepository:
    """Repository class for database operations on Project objects."""
    
    def __init__(self, session):
        """
        Initialize the repository with a database session.
        
        Args:
            session (sqlalchemy.orm.Session): Database session
        """
        self.session = session
    
    def create_project(self, project_data):
        """
        Create a new project record in the database.
        
        Args:
            project_data (dict): Project data from GitLab API
            
        Returns:
            Project: Created project object
            
        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            # Handle datetime fields
            for date_field in ['created_at', 'last_activity_at', 'updated_at']:
                if date_field in project_data and project_data[date_field]:
                    # Handle ISO format strings
                    if isinstance(project_data[date_field], str):
                        project_data[date_field] = datetime.fromisoformat(
                            project_data[date_field].replace('Z', '+00:00')
                        )
            
            # Extract namespace data if present
            namespace_data = None
            if 'namespace' in project_data:
                namespace_data = project_data.pop('namespace')
            
            # Filter data to only include fields in our model
            valid_fields = [column.name for column in Project.__table__.columns]
            filtered_data = {k: v for k, v in project_data.items() if k in valid_fields}
            
            # Add current timestamp for last_synced
            filtered_data['last_synced'] = datetime.utcnow()
            
            # Create new project
            project = Project(**filtered_data)
            self.session.add(project)
            
            # Add namespace if it exists
            if namespace_data:
                self._add_namespace(project, namespace_data)
                
            # Commit changes
            self.session.commit()
            logger.info(f"Created project {project.id}: {project.name}")
            return project
            
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error creating project: {str(e)}")
            raise
    
    def _add_namespace(self, project, namespace_data):
        """
        Add namespace data to a project.

        Args:
            project (Project): Project object
            namespace_data (dict): Namespace data from GitLab API
        """
        try:
            # Filter namespace data
            valid_fields = [column.name for column in Namespace.__table__.columns if column.name != 'project_id']
            filtered_data = {k: v for k, v in namespace_data.items() if k in valid_fields}

            # Check if the namespace already exists
            existing_namespace = self.session.query(Namespace).filter_by(id=filtered_data["id"]).first()
            
            if not existing_namespace:
                # Create namespace object if it does not exist
                namespace = Namespace(project=project, **filtered_data)
                self.session.add(namespace)
            else:
                logger.info(f"Namespace {existing_namespace.id} already exists. Skipping creation.")

        except Exception as e:
            logger.error(f"Error adding namespace to project {project.id}: {str(e)}")
            raise
    
    def get_project_by_id(self, project_id):
        """
        Get a project by ID.
        
        Args:
            project_id (int): Project ID
            
        Returns:
            Project: Project object or None if not found
            
        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            project = self.session.query(Project).filter(Project.id == project_id).first()
            return project
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving project with ID {project_id}: {str(e)}")
            raise
    
    def update_project(self, project_id, project_data):
        """
        Update an existing project.
        
        Args:
            project_id (int): Project ID
            project_data (dict): Updated project data
            
        Returns:
            Project: Updated project object or None if not found
            
        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            project = self.get_project_by_id(project_id)
            if project:
                # Handle datetime fields
                for date_field in ['created_at', 'last_activity_at', 'updated_at']:
                    if date_field in project_data and project_data[date_field]:
                        # Handle ISO format strings
                        if isinstance(project_data[date_field], str):
                            project_data[date_field] = datetime.fromisoformat(
                                project_data[date_field].replace('Z', '+00:00')
                            )
                
                # Extract namespace data if present
                namespace_data = None
                if 'namespace' in project_data:
                    namespace_data = project_data.pop('namespace')
                
                # Filter data to only include fields in our model
                valid_fields = [column.name for column in Project.__table__.columns]
                filtered_data = {k: v for k, v in project_data.items() if k in valid_fields}
                
                # Update project fields
                for key, value in filtered_data.items():
                    setattr(project, key, value)
                
                # Update namespace if needed
                if namespace_data:
                    # Remove existing namespaces
                    for namespace in project.namespaces:
                        self.session.delete(namespace)
                    
                    # Add new namespace
                    self._add_namespace(project, namespace_data)
                
                # Update last_synced timestamp
                project.last_synced = datetime.utcnow()
                
                # Commit changes
                self.session.commit()
                logger.info(f"Updated project {project_id}")
                return project
            else:
                logger.warning(f"Project with ID {project_id} not found for update")
                return None
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating project {project_id}: {str(e)}")
            raise
    
    def delete_project(self, project_id):
        """
        Delete a project by ID.
        
        Args:
            project_id (int): Project ID
            
        Returns:
            bool: True if deleted successfully, False if project not found
            
        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            project = self.get_project_by_id(project_id)
            if project:
                self.session.delete(project)
                self.session.commit()
                logger.info(f"Deleted project {project_id}")
                return True
            else:
                logger.warning(f"Project with ID {project_id} not found for deletion")
                return False
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting project {project_id}: {str(e)}")
            raise
    
    def get_all_projects(self):
        """
        Get all projects.
        
        Returns:
            list: List of Project objects
            
        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            projects = self.session.query(Project).all()
            return projects
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving all projects: {str(e)}")
            raise
