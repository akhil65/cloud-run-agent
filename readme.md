# AI Agent on Cloud Run

This project is a foundational framework for a task-oriented AI agent, built with Python and Flask, containerized with Docker, and deployed as a serverless application on Google Cloud Run.

---

## Project Overview

The application functions as a web service that can receive a high-level goal, break it down into a multi-step plan, and track its progress toward completion. This serves as a backend for an autonomous agent capable of executing complex workflows.

The core components of the agent framework are:

* **Web Service:** An API built with Flask to receive goals and report status via HTTP requests.
* **Planning Engine:** A function (`create_plan`) that simulates the agent's intelligence by creating a step-by-step plan from a given goal.
* **State Machine:** A simple in-memory tracker (`current_step_index`) that serves as the agent's memory, allowing it to know its current position in the plan.
* **Tool-Using Capability:** A placeholder function (`use_tool_for_step`) that represents the agent's ability to take real-world actions to complete a step.

---

## Technology Stack

* **Language:** Python 3.9+
* **Framework:** Flask
* **Containerization:** Docker
* **Cloud Platform:** Google Cloud Run, Artifact Registry
* **CLI Tools:** `gcloud`, `docker`
* **Testing:** `requests` (Python library)

---

## Local Development Setup

### Prerequisites

* Python 3.9+ and pip installed.
* Docker Desktop installed and running.

### Instructions

1.  Clone the repository (or create the project files locally).
2.  Navigate to the project directory:
    ```bash
    cd /path/to/your/project
    ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Run the application (available at `http://127.0.0.1:8080`):

   ```bash
   python app.py
   ```

---

## Docker Usage

### Building the Image

To ensure compatibility with Cloud Run (which uses `amd64` architecture):

```bash
docker build --platform=linux/amd64 -t my-agent .
```

### Running the Container Locally

Run the container and map your local port `8080` to the container's port `8080`:

```bash
docker run -p 8080:8080 my-agent
```

---

## Deployment to Google Cloud Run

### 1. Google Cloud Setup

1. Create a Google Cloud account and a new project.
2. Install and initialize the gcloud CLI.
3. Log in and set your project:

   ```bash
   gcloud auth login
   gcloud config set project [YOUR_PROJECT_ID]
   ```

### 2. Enable APIs and Create Repository

```bash
# Enable required services
gcloud services enable run.googleapis.com artifactregistry.googleapis.com

# Create a repository in Artifact Registry
gcloud artifacts repositories create my-agent-repo \
  --repository-format=docker \
  --location=us-central1
```

### 3. Authenticate Docker

Configure Docker to use your gcloud credentials:

```bash
gcloud auth configure-docker us-central1-docker.pkg.dev
```

### 4. Tag and Push the Image

```bash
# Define your image URI
IMAGE_URI="us-central1-docker.pkg.dev/[YOUR_PROJECT_ID]/my-agent-repo/my-agent"

# Tag the image
docker tag my-agent $IMAGE_URI

# Push the image
docker push $IMAGE_URI
```

### 5. Deploy to Cloud Run

```bash
gcloud run deploy my-agent-service \
  --image=$IMAGE_URI \
  --platform=managed \
  --region=us-central1 \
  --allow-unauthenticated
```

---

## Verification and Testing

### 1. Manual End-to-End Testing

* **Check Status:** Visit the Cloud Run service URL. It should return:

  ```
  Agent is ready for a goal.
  ```

* **Test Workflow:**
  Use an API client (Postman or curl) to:

  * `POST` a goal to `/`
  * `POST` to `/next-step` repeatedly until completion.

### 2. Automated API Testing

Run the test script after updating the service URL:

```bash
python test_agent.py
```

### 3. Health Checks and Log Inspection

* **Logs:**
  Cloud Console → Cloud Run → *Logs* tab
  Look for `Container started` and your app's `print()` logs.

* **Metrics:**
  Cloud Console → Cloud Run → *Metrics* tab
  Review Request Count, Latency, and CPU/Memory graphs.

---

## Security Improvements

### Input Validation

The final `app.py` adds robust input validation to prevent crashes and misuse.

**Before (Vulnerable):**

```python
def handle_goal():
    data = request.get_json()
    goal_from_client = data['goal']  # Trusts input completely
    # ...
```

**After (Secure):**

```python
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
```

### Secure Error Handling

Generic error messages are returned to users; detailed errors are logged internally.

**Before (Vulnerable):**

```python
except Exception as e:
    # Leaks internal error details to the user
    return f"Error processing request: {e}", 500
```

**After (Secure):**

```python
except Exception as e:
    logging.error(f"An internal error occurred: {e}", exc_info=True)

    error_response = {
        "error_code": "E500",
        "message": "An internal server error occurred."
    }
    return jsonify(error_response), 500
```

---
