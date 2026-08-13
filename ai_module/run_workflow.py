from inference_sdk import InferenceHTTPClient

# Connect to Roboflow
client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="aSqxGl8STq6PPmuMRiJ6"
)

# Ask for an image
image_path = input("Enter road image filename: ")

# Run AquaShield workflow
result = client.run_workflow(
    workspace_name="riddhi-joshi",
    workflow_id="aquashield-waterlogging-assessment-1786611030261",
    images={
        "image": image_path
    },
    use_cache=True
)

# Display result
print("\n========== AQUASHIELD WATERLOGGING ASSESSMENT ==========")

output = result[0] if isinstance(result, list) else result

print("Waterlogging Detected:", output.get("waterlogging_detected"))
print("Severity:", output.get("severity"))
print("Flood Coverage:", output.get("flood_coverage_percent"), "%")
print("Risk Score:", output.get("preliminary_risk_score"), "/100")

print("========================================================")