import yaml

with open("scenarios/greenlake_subscription_validation.yaml", "r") as f:
    data = yaml.safe_load(f)

print("Parsed YAML:")
print(data)

print("\nParsed 'steps' field:")
for i, s in enumerate(data.get("steps", []), 1):
    print(f"Step {i}: {type(s)} - {s}")
