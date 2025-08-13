
from flask import Flask, request
# Make sure it's importing from our new script
from automation_script import run_automation, DEFAULT_CLAIM_DATA

app = Flask(__name__)

@app.route('/run-job', methods=['POST'])
def run_job_endpoint():
    zapier_data = request.json or {}
    print(f"Received data from Zapier: {zapier_data}")

    # Start with defaults and override with Zapier's data
    final_claim_data = DEFAULT_CLAIM_DATA.copy()
    final_claim_data.update(zapier_data)

    run_automation(final_claim_data)

    # Immediately respond to Zapier
    return {"status": "success", "message": "Automation job started."}, 200
