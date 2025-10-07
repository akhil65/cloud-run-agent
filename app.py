
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- Agent's Memory ---
agent_plan = []
current_step_index = 0
# --------------------

def create_plan(goal_text):
  """Breaks a goal down into a hardcoded list of steps."""
  print(f"--- Creating plan for goal: {goal_text} ---")
  plan = [
    "Step 1: Containerize the agent application.",
    "Step 2: Deploy the container to Cloud Run.",
    "Step 3: Configure the Cloud Run service to use a GPU.",
    "Step 4: Verify the deployment is successful."
  ]
  return plan

def use_tool_for_step(step_description):
  """Simulates the agent using a tool to complete a step."""
  print(f"--- TOOL USED: Executing '{step_description}' ---")
  return True

@app.route('/', methods=['GET', 'POST'])
def handle_goal():
  global agent_plan, current_step_index

  if request.method == 'POST':
    try:
      data = request.get_json()
      
      ## SECURE ## Step 2: Add Input Validation at the start of your logic.
      if not data or 'goal' not in data:
          return jsonify({"error": "Missing 'goal' in request body."}), 400
      
      goal_from_client = data['goal']

      if not isinstance(goal_from_client, str):
          return jsonify({"error": "Invalid type: 'goal' must be a string."}), 400
      
      if len(goal_from_client) > 200:
          return jsonify({"error": "Invalid length: 'goal' cannot exceed 200 characters."}), 400

      # --- Main Logic ---
      agent_plan = create_plan(goal_from_client)
      current_step_index = 0
      return f"Plan created. Current step is: {agent_plan[current_step_index]}"
    
    except Exception as e:
      ## SECURE ## Step 3: Implement secure error handling.
      # Log the detailed error for developers to see internally.
      logging.error(f"An internal error occurred: {e}", exc_info=True)
      
      # Return a generic, unhelpful message to the user.
      error_response = {"error_code": "E500", "message": "An internal server error occurred."}
      return jsonify(error_response), 500
  else:
    # A GET request can show the current status
    if not agent_plan:
      return "Agent is ready for a goal."
    else:
      return f"Agent is working on a plan. Current step is: {agent_plan[current_step_index]}"

# /next-step route 
@app.route('/next-step', methods=['POST'])
def advance_to_next_step():
  global current_step_index
  
  if not agent_plan:
    return jsonify({"error": "No plan has been set."}), 404
  
  current_step = agent_plan[current_step_index]
  tool_succeeded = use_tool_for_step(current_step)
  
  if tool_succeeded:
    if current_step_index < len(agent_plan) - 1:
      current_step_index += 1
      return f"Tool succeeded. New step is: {agent_plan[current_step_index]}"
    else:
      return "Plan complete! All steps have been executed."
  else:
    return jsonify({"error": f"Tool failed on step: {current_step}"}), 500

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)