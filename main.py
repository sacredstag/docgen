import os
import argparse
import subprocess
import datetime
from openai import OpenAI
from dotenv import load_dotenv

def load_system_prompt():
    with open("doc_generation_guide_HCorp.md", "r") as f:
        return f.read()


def build_prompt(phase: str) -> str:
    if phase in {"enrich", "auto"}:
        print("📈 Phase: Enrich existing documentation")

        if not os.path.exists("enrich_source.txt"):
            raise FileNotFoundError("enrich_source.txt not found")

        with open("enrich_source.txt", "r") as pointer:
            base_path = pointer.read().strip()
        with open(base_path, "r") as base:
            base_doc = base.read()

        with open("input_1.txt", "r") as p:
            review_request = p.read()

        return (
            "You are an L3 support engineer. The document below is intended for Kubernetes/OpenShift PVC Order operations.\n"
            "You must preserve all original SME content exactly as it appears.\n"
            "Your job is to add missing diagnostics, validations, CLI syntax examples, panels, and macros — NOT to delete or restructure the input.\n"
            "Do not remove any original steps, anchors, or macro blocks. Add new content below them, or in new panels if needed.\n\n"
            "-------- Existing Document Start --------\n"
            + base_doc +
            "\n-------- End Document --------\n\n"
            "SME Enrichment Instructions:\n" + review_request
        )

    input_file = f"input_{phase}.txt"
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Required input file '{input_file}' is missing")
    with open(input_file, "r") as f:
        return f.read()


def run_gpt(prompt: str, system_prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content


def run_pipeline(phase: str) -> str:
    system_prompt = load_system_prompt()
    prompt = build_prompt(phase)
    output = run_gpt(prompt, system_prompt)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = f"output_{phase}_{timestamp}.txt"
    with open(out_file, "w") as f:
        f.write(output)
    print(f"✅ Phase {phase} complete. Output saved to {out_file}")

    if phase == "auto":
        print("🧰 Repairing output...")
        subprocess.run(["python", "repair_output.py"], check=True)
        os.replace("output_repaired.txt", "output.txt")
        print("🔎 Validating output...")
        subprocess.run(["python", "validate_output.py"], check=True)
        print("✅ Auto pipeline complete.")

    return out_file


def main():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing OpenAI API key in .env")
    global client
    client = OpenAI(api_key=api_key)

    parser = argparse.ArgumentParser(description="Generate or enrich Confluence documentation")
    parser.add_argument("--phase", choices=["1", "2", "enrich", "auto"], default="1", help="Select pipeline phase")
    args = parser.parse_args()

    run_pipeline(args.phase)


if __name__ == "__main__":
    main()
