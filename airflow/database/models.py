"""
Database models for the GitLab API data extraction application.

This module defines the SQLAlchemy ORM models used to store GitLab data.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import logging

# Create base class for declarative models
Base = declarative_base()

class Project(Base):
    """SQLAlchemy model for GitLab projects."""
    
    __tablename__ = 'projects'
    
    # Primary key
    id = Column(Integer, primary_key=True)
    
    # Basic project information
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    name_with_namespace = Column(String(255))
    path = Column(String(255))
    path_with_namespace = Column(String(255))
    
    # URLs
    web_url = Column(String(512))
    ssh_url_to_repo = Column(String(512))
    http_url_to_repo = Column(String(512))
    
    # Timestamps
    created_at = Column(DateTime)
    last_activity_at = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Status and visibility
    visibility = Column(String(50))
    archived = Column(Boolean, default=False)
    empty_repo = Column(Boolean, default=False)
    
    # Features and capabilities
    issues_enabled = Column(Boolean, default=True)
    merge_requests_enabled = Column(Boolean, default=True)
    wiki_enabled = Column(Boolean, default=True)
    
    # Metadata for our application
    last_synced = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    namespaces = relationship("Namespace", back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}')>"


class Namespace(Base):
    """SQLAlchemy model for GitLab namespaces."""
    
    __tablename__ = 'namespaces'
    
    # Primary key
    id = Column(Integer, primary_key=True)
    
    # Foreign key relationship with Project
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="namespaces")
    
    # Namespace attributes
    name = Column(String(255), nullable=False)
    path = Column(String(255))
    kind = Column(String(50))
    full_path = Column(String(512))
    parent_id = Column(Integer, nullable=True)
    web_url = Column(String(512), nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Namespace(id={self.id}, name='{self.name}')>"


def init_db(db_uri):
    """
    Initialize the database, create tables if they don't exist, and return a session.
    
    Args:
        db_uri (str): Database connection URI
        
    Returns:
        sqlalchemy.orm.Session: Database session object
    """
    logger = logging.getLogger('gitlab_api.database')
    
    try:
        # Create engine with appropriate security settings
        engine = create_engine(
            db_uri, 
            echo=False,  # Set to False in production for security
            pool_pre_ping=True,  # Verify connections before use
            connect_args={"check_same_thread": False} if db_uri.startswith('sqlite') else {}
        )
        
        # Create all tables
        Base.metadata.create_all(engine)
        
        # Create session
        Session = sessionmaker(bind=engine)
        session = Session()
        
        logger.info(f"Database successfully initialized with URI: {db_uri}")
        return session
    
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise