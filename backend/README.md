# Autonomous Recruitment Platform Backend

An advanced FastAPI-based backend system that serves as an API and agent manager for deploying and managing a fleet of autonomous AI recruitment agents built with Fetch.ai's uagents library. The platform automates candidate sourcing, outreach, and communication using AgentMail integration with PostgreSQL for data persistence.

## Project Structure

```
/autonomous-recruitment-backend
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application instance
│   ├── database.py                # SQLAlchemy configuration
│   ├── models/
│   │   ├── __init__.py
│   │   ├── agent_model.py         # Agent ORM models
│   │   └── job_model.py           # Job and candidate ORM models
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── agent_schema.py        # Pydantic validation schemas
│   ├── services/
│   │   ├── __init__.py
│   │   └── agent_service.py       # Business logic layer
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── agent_controller.py    # Request handling layer
│   └── routes/
│       ├── __init__.py
│       └── agent_routes.py        # FastAPI API endpoints
├── agents/
│   ├── __init__.py
│   ├── README.md                  # Agent documentation guidelines
│   └── sourcing_agent.py          # Fetch.ai autonomous agent
├── .env                           # Environment variables (empty)
├── .gitignore                     # Git ignore rules
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## File and Function Descriptions

| File | Function/Class | Description |
| :--- | :--- | :--- |
| `app/main.py` | `create_app()` | Initializes and returns the main FastAPI application instance. |
| `app/main.py` | `lifespan()` | Application lifespan manager for startup and shutdown events. |
| `app/main.py` | `root()` | Root endpoint to verify the application is running. |
| `app/main.py` | `health_check()` | Health check endpoint for monitoring and load balancers. |
| `app/database.py` | `get_db()` | A FastAPI dependency that provides a database session for each request. |
| `app/database.py` | `init_db()` | Initialize the database by creating all tables. |
| `app/models/agent_model.py` | `Agent` | SQLAlchemy model representing an autonomous recruitment agent. |
| `app/models/agent_model.py` | `AgentActivity` | SQLAlchemy model for tracking agent activities and logs. |
| `app/models/job_model.py` | `Job` | SQLAlchemy model representing a job posting for recruitment. |
| `app/models/job_model.py` | `Candidate` | SQLAlchemy model for storing candidate information discovered by agents. |
| `app/schemas/agent_schema.py` | `AgentCreate` | Pydantic schema for creating a new agent. |
| `app/schemas/agent_schema.py` | `AgentUpdate` | Pydantic schema for updating an existing agent. |
| `app/schemas/agent_schema.py` | `AgentResponse` | Pydantic schema for agent response data. |
| `app/schemas/agent_schema.py` | `AgentDeployRequest` | Pydantic schema for agent deployment requests. |
| `app/schemas/agent_schema.py` | `AgentStatusResponse` | Pydantic schema for agent status check responses. |
| `app/services/agent_service.py` | `AgentService` | Service class for managing autonomous recruitment agents. |
| `app/services/agent_service.py` | `deploy_new_agent()` | Deploy a new autonomous recruitment agent for a specific job. |
| `app/services/agent_service.py` | `get_agent_status()` | Get the current status and activity summary of an agent. |
| `app/services/agent_service.py` | `stop_agent()` | Stop a running agent and update its status. |
| `app/services/agent_service.py` | `list_agents()` | List all agents with pagination. |
| `app/controllers/agent_controller.py` | `AgentController` | Controller class for managing agent-related HTTP requests. |
| `app/controllers/agent_controller.py` | `create_agent()` | Create and deploy a new autonomous recruitment agent. |
| `app/controllers/agent_controller.py` | `get_agent_status()` | Get the current status and activity summary of a specific agent. |
| `app/controllers/agent_controller.py` | `list_agents()` | List all agents with pagination support. |
| `app/controllers/agent_controller.py` | `stop_agent()` | Stop a running agent. |
| `app/routes/agent_routes.py` | `deploy_agent()` | POST endpoint to deploy a new autonomous recruitment agent. |
| `app/routes/agent_routes.py` | `create_agent()` | POST endpoint to create a new agent with full configuration options. |
| `app/routes/agent_routes.py` | `get_agent_status()` | GET endpoint to retrieve agent status and activity metrics. |
| `app/routes/agent_routes.py` | `list_agents()` | GET endpoint to list all agents with pagination support. |
| `app/routes/agent_routes.py` | `update_agent()` | PUT endpoint to update an existing agent's configuration. |
| `app/routes/agent_routes.py` | `stop_agent()` | DELETE endpoint to stop a running agent. |
| `app/routes/agent_routes.py` | `get_agent_activities()` | GET endpoint to retrieve agent activity logs. |
| `app/routes/agent_routes.py` | `get_agent_candidates()` | GET endpoint to retrieve candidates discovered by an agent. |
| `agents/sourcing_agent.py` | `Agent` | Fetch.ai agent instance for autonomous candidate sourcing. |
| `agents/sourcing_agent.py` | `startup_event()` | Event handler for agent startup and initialization. |
| `agents/sourcing_agent.py` | `periodic_sourcing_task()` | Periodic task for candidate sourcing that runs every hour. |
| `agents/sourcing_agent.py` | `handle_sourcing_request()` | Handle sourcing requests from the backend API. |
| `agents/sourcing_agent.py` | `search_for_candidates()` | Search for candidates matching the job requirements. |
| `agents/sourcing_agent.py` | `send_outreach_emails()` | Send outreach emails to discovered candidates using AgentMail. |
| `agents/sourcing_agent.py` | `log_agent_activity()` | Log agent activity to the database. |
| `agents/sourcing_agent.py` | `shutdown_event()` | Event handler for agent shutdown and cleanup. |

## Technology Stack

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Agent Framework**: Fetch.ai uagents
- **Agent Communication**: AgentMail
- **Server**: Uvicorn
- **Environment Management**: python-dotenv

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Redis (for Celery tasks)
- Fetch.ai testnet access

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd autonomous-recruitment-backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Set up the database:
```bash
# Create PostgreSQL database
createdb recruitment_db

# Run database migrations (when implemented)
# alembic upgrade head
```

6. Start the application:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### API Documentation

Once the application is running, you can access:

- **Interactive API Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Agent Management

- `POST /api/v1/agents/deploy` - Deploy a new agent for a job
- `POST /api/v1/agents` - Create a new agent with full configuration
- `GET /api/v1/agents/{agent_id}/status` - Get agent status and metrics
- `GET /api/v1/agents` - List all agents with pagination
- `PUT /api/v1/agents/{agent_id}` - Update agent configuration
- `DELETE /api/v1/agents/{agent_id}/stop` - Stop a running agent
- `GET /api/v1/agents/{agent_id}/activities` - Get agent activity logs
- `GET /api/v1/agents/{agent_id}/candidates` - Get candidates discovered by agent

## Agent Development

See the [agents/README.md](agents/README.md) for detailed guidelines on creating and documenting autonomous agents.

## Database Schema

The application uses the following main entities:

- **Agents**: Autonomous recruitment agents with status and configuration
- **Jobs**: Job postings with requirements and details
- **Candidates**: Candidate profiles discovered by agents
- **Agent Activities**: Activity logs and communication history

## Development

### Code Style

The project uses:
- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

Run formatting and linting:
```bash
black .
isort .
flake8 .
mypy .
```

### Testing

Run tests:
```bash
pytest
```

## Deployment

### Production Considerations

1. Set `DEBUG=False` in environment variables
2. Use a production WSGI server like Gunicorn
3. Set up proper database connection pooling
4. Configure Redis for Celery task queue
5. Set up monitoring and logging
6. Use environment-specific configuration files

### Docker Deployment

Docker configuration can be added for containerized deployment.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions and support, please refer to the project documentation or contact the development team.

---

**Note**: This is a boilerplate implementation. Business logic, external API integrations, and production configurations need to be implemented based on specific requirements.
