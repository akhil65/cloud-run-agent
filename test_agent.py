import requests
import time

# --- CONFIGURATION ---
# Replace this with in-scope actual Cloud Run Service URL
BASE_URL = "https://my-agent-service-28429081679.us-central1.run.app/"
# ---------------------

def run_test():
    """Runs a full end-to-end test of the agent service."""
    
    print(f"--- Starting test for service at {BASE_URL} ---")
    
    # Step 1: Send a goal to the root URL
    try:
        print("\nStep 1: Sending goal...")
        goal_payload = {"goal": "Automated test"}
        response = requests.post(BASE_URL + '/', json=goal_payload)
        
        # Check if the request was successful
        response.raise_for_status() 
        
        print(f"  - SUCCESS: Server responded with: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"  - FAILED: Could not send goal. Error: {e}")
        return

    # Step 2: Advance the plan until it's complete
    print("\nStep 2: Advancing plan...")
    for i in range(5): # We try up to 5 times to be safe
        time.sleep(1) # Pause for a second between requests
        try:
            response = requests.post(BASE_URL + '/next-step')
            response.raise_for_status()

            print(f"  - SUCCESS: Server responded with: {response.text}")
            
            # Check if the plan is complete
            if "Plan complete" in response.text:
                print("\n--- TEST COMPLETE: Agent finished its plan. ---")
                return
        except requests.exceptions.RequestException as e:
            print(f"  - FAILED: Could not advance step. Error: {e}")
            return
            
    print("\n--- TEST FAILED: Agent did not complete its plan in time. ---")


# Run the main test function
if __name__ == "__main__":
    run_test()
