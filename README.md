# GitLab API Data Extractor
A command-line application that extracts GitLab project information via the GitLab API and stores it in a database.

# Features
- Connect to GitLab API using Python
- Store project data in a SQL database using -SQLAlchemy
- Perform CRUD operations on project data
- Implement proper error handling and logging
- Use OpenAPI-generated clients for API communication
- Store API credentials securely
# Requirements
- Python 3.8+
- SQLAlchemy
- Requests
- Python-dotenv
- PyJWT
- Cryptography
- Pydantic
# Installation
1. Clone this repository:
git clone <repository-url>
cd gitlab-api-project
2. Create and activate a virtual environment:
python -m venv venv
venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install dependencies:
pip install -r requirements.txt
4. Configure environment variables:
cp .env.example .env
Edit .env with your GitLab API token and other settings
# Configuration
- GITLAB_API_URL=https://gitlab.com/api/v4
- GITLAB_API_TOKEN=your_private_token
- DATABASE_URI=sqlite:///gitlab_data.db
- LOG_LEVEL=INFO
# Usage
1. Fetching Projects
python app.py fetch
2. Managing Projects
# List all projects in the database
python app.py list

# Get details for a specific project
python app.py show PROJECT_ID

# Update a project
python app.py update PROJECT_ID

# Delete a project
python app.py delete PROJECT_ID

# Help
python app.py -h

# Database Schema
The application uses SQLite with the following schema:

Projects Table
- id: Integer, Primary Key
- name: String, Not Null
- description: Text
- created_at: DateTime
- updated_at: DateTime
- web_url: String
- visibility: String
Namespaces Table
- id: Integer, Primary Key
- name: String, Not Null
- path: String, Not Null
- project_id: Integer, Foreign Key to Projects

# OpenAPI Integration
npm install @openapitools/openapi-generator-cli -g
openapi-generator-cli generate -i https://gitlab.com/gitlab-org/gitlab/-/blob/master/doc/api/openapi/openapi.yaml -g python -o ./api/generated

# Logging
The application implements comprehensive logging with:

- Configurable log levels
- File and console logging
- Log rotation with timestamps
- Structured log format

# Security Features
- API tokens stored in environment variables
- Parameterized database queries
- Input validation
- Secure error handling
- Connection pooling with validation

# Dependencies
SQLAlchemy==1.4.49 
requests==2.31.0
python-dotenv==1.0.0
urllib3==2.0.7
PyJWT==2.8.0
cryptography==41.0.5
pydantic==2.5.2