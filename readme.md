AI Agent on Cloud Run
This project is a foundational framework for a task-oriented AI agent, built with Python and Flask, containerized with Docker, and deployed as a serverless application on Google Cloud Run.

Project Overview
The application functions as a web service that can receive a high-level goal, break it down into a multi-step plan, and track its progress toward completion. This serves as a backend for an autonomous agent capable of executing complex workflows.

The core components of the agent framework are:

Web Service: An API built with Flask to receive goals and report status via HTTP requests.

Planning Engine: A function (create_plan) that simulates the agent's intelligence by creating a step-by-step plan from a given goal.

State Machine: A simple in-memory tracker (current_step_index) that serves as the agent's memory, allowing it to know its current position in the plan.

Tool-Using Capability: A placeholder function (use_tool_for_step) that represents the agent's ability to take real-world actions to complete a step.

Technology Stack
Language: Python 3.9+

Framework: Flask

Containerization: Docker

Cloud Platform: Google Cloud Run, Artifact Registry

CLI Tools: gcloud, docker

Testing: requests (Python library)

Local Development Setup
Prerequisites
Python 3.9+ and pip installed.

Docker Desktop installed and running.

Instructions
Clone the repository (or create the project files locally).

Navigate to the project directory:

Bash

cd /path/to/your/project
Install dependencies:

Bash

pip install -r requirements.txt
Run the application:
The application will be available at http://127.0.0.1:8080.

Bash

python app.py
Docker Usage
Building the Image
To ensure compatibility with cloud services like Cloud Run (which use amd64 architecture), build the image using the --platform flag.

Bash

docker build --platform=linux/amd64 -t my-agent .
Running the Container Locally
This command runs the container and maps your local port 8080 to the container's port 8080.

Bash

docker run -p 8080:8080 my-agent
Deployment to Google Cloud Run
1. Google Cloud Setup
Create a Google Cloud account and a new project.

Install and initialize the gcloud CLI.

Log in and set your project:

Bash

gcloud auth login
gcloud config set project [YOUR_PROJECT_ID]
2. Enable APIs and Create Repository
Bash

# Enable required services
gcloud services enable run.googleapis.com artifactregistry.googleapis.com

# Create a repository in Artifact Registry
gcloud artifacts repositories create my-agent-repo \
--repository-format=docker \
--location=us-central1
3. Authenticate Docker
Configure Docker to use your gcloud credentials to authenticate with Artifact Registry.

Bash

gcloud auth configure-docker us-central1-docker.pkg.dev
4. Tag and Push the Image
Tag your local image with the full repository path and push it to the cloud.

Bash

# Define your image URI
IMAGE_URI="us-central1-docker.pkg.dev/[YOUR_PROJECT_ID]/my-agent-repo/my-agent"

# Tag the image
docker tag my-agent $IMAGE_URI

# Push the image
docker push $IMAGE_URI
5. Deploy to Cloud Run
Deploy the image from Artifact Registry to a new Cloud Run service.

Bash

gcloud run deploy my-agent-service \
--image=$IMAGE_URI \
--platform=managed \
--region=us-central1 \
--allow-unauthenticated
Verification and Testing
1. Manual End-to-End Testing
Check Status: Navigate to the public Service URL provided by Cloud Run in a browser. It should return "Agent is ready for a goal."

Test Workflow: Use an API client like Postman or curl to POST a goal to / and then POST to /next-step until the plan is complete.

2. Automated API Testing
The test_agent.py script provides an automated end-to-end test. Update the BASE_URL in the script with your service URL and run it.

Bash

python test_agent.py
3. Health Checks and Log Inspection
Navigate to your service in the Google Cloud Console > Cloud Run.

LOGS Tab: View application and system logs. Look for "Container started" messages and logs from your application's print() statements.

METRICS Tab: View performance graphs for Request Count, Latency, and resource utilization.

Security Improvements
The final app.py includes key security improvements over the initial prototype.

Input Validation
The handle_goal endpoint validates incoming JSON data to prevent crashes and basic abuse.

Before (Vulnerable):

Python

def handle_goal():
    data = request.get_json()
    goal_from_client = data['goal'] # Trusts input completely
    # ...
After (Secure):

Python

def handle_goal():
    data = request.get_json()

    if not data or 'goal' not in data:
        return jsonify({"error": "Missing 'goal' in request body."}), 400

    goal_from_client = data['goal']

    if not isinstance(goal_from_client, str):
        return jsonify({"error": "Invalid type: 'goal' must be a string."}), 400

    if len(goal_from_client) > 200:
        return jsonify({"error": "Invalid length: 'goal' cannot exceed 200 characters."}), 400
    # ...
Secure Error Handling
Generic error messages are returned to the user, while detailed exceptions are logged internally to prevent information leakage.

Before (Vulnerable):

Python

except Exception as e:
    # Leaks internal error details to the user
    return f"Error processing request: {e}", 500
After (Secure):

Python

except Exception as e:
    # Log the detailed error for developers to see internally
    logging.error(f"An internal error occurred: {e}", exc_info=True)

    # Return a generic, unhelpful message to the user
    error_response = {"error_code": "E500", "message": "An internal server error occurred."}
    return jsonify(error_response), 500