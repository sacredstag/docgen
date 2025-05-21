import os
import argparse
import subprocess
import datetime
from openai import OpenAI
from dotenv import load_dotenv

# --- Load env vars ---
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Missing OpenAI API key in .env")

client = OpenAI(api_key=api_key)

# --- Parse CLI argument ---
parser = argparse.ArgumentParser(description="Generate or enrich Confluence documentation")
parser.add_argument(
    "--phase", choices=["1", "2", "enrich", "auto"], default="1",
    help="Select input phase: 1, 2, 'enrich', or 'auto' for full pipeline"
)
args = parser.parse_args()

# --- Load system prompt ---
with open("doc_generation_guide_HCorp.md", "r") as f:
    system_prompt = f.read()

# --- Enrich or Auto Phase (shared logic) ---
if args.phase in ["enrich", "auto"]:
    print("📈 Phase: Enrich existing documentation")

    # Load filename
    with open("enrich_source.txt", "r") as pointer:
        base_path = pointer.read().strip()

    with open(base_path, "r") as base:
        base_doc = base.read()

    # Load SME prompt
    with open("input_1.txt", "r") as p:
        review_request = p.read()

    # Build prompt
    user_prompt = (
        "You are an L3 support engineer. The document below is intended for Kubernetes/OpenShift PVC Order operations.\n"
        "You must preserve all original SME content exactly as it appears.\n"
        "Your job is to add missing diagnostics, validations, CLI syntax examples, panels, and macros — NOT to delete or restructure the input.\n"
        "Do not remove any original steps, anchors, or macro blocks. Add new content below them, or in new panels if needed.\n\n"
        "-------- Existing Document Start --------\n"
        + base_doc +
        "\n-------- End Document --------\n\n"
        "SME Enrichment Instructions:\n" + review_request
    )

# --- Standard Generation Phase ---
elif args.phase in ["1", "2"]:
    INPUT_FILE = f"input_{args.phase}.txt"
    with open(INPUT_FILE, "r") as f:
        user_prompt = f.read()

# --- GPT Call ---
response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    temperature=0.2
)

# --- Output path with timestamp ---
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f"output_{args.phase}_{timestamp}.txt"

# --- Save response ---
output = response.choices[0].message.content
with open(output_file, "w") as f:
    f.write(output)

print(f"✅ Phase {args.phase} complete. Output saved to {output_file}")

# --- Auto phase: repair and validate
if args.phase == "auto":
    print("🧰 Repairing output...")
    subprocess.run(["python", "repair_output.py"], check=True)
    os.replace("output_repaired.txt", "output.txt")

    print("🔎 Validating output...")
    subprocess.run(["python", "validate_output.py"], check=True)

    print("✅ Auto pipeline complete.")
