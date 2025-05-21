import os
import time
import re
import argparse
import subprocess
from openai import OpenAI
from dotenv import load_dotenv

# === Load API key from .env ===
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# === CLI ARGUMENT PARSING ===
parser = argparse.ArgumentParser(description="Generate chunked GPT Confluence output")
parser.add_argument("--source", required=True, help="Path to input source file for prompt extraction")
args = parser.parse_args()

# === Run prompt extraction first ===
print(f"📦 Extracting prompts from: {args.source}")
subprocess.run(["python", "extract_prompts_from_layout.py", "--source", args.source], check=True)

# === Section Configuration ===
SECTIONS = [
    {"name": "header", "prompt": "prompts/header.txt", "model": "gpt-3.5-turbo", "context_depth": 0},
    {"name": "overview", "prompt": "prompts/overview.txt", "model": "gpt-4-turbo", "context_depth": 1},
    {"name": "key_terms", "prompt": "prompts/key_terms.txt", "model": "gpt-3.5-turbo", "context_depth": 2},
    {"name": "diagnostics", "prompt": "prompts/diagnostics.txt", "model": "gpt-4-turbo", "context_depth": 2},
    {"name": "footer", "prompt": "prompts/footer.txt", "model": "gpt-3.5-turbo", "context_depth": 1},
]

OUTPUT_DIR = "chunks"
FINAL_OUTPUT = "final_output.txt"
END_MARKER = "<!-- === END OF OUTPUT === -->"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# === Utility Functions ===
def read_prompt(path):
    with open(path, "r") as f:
        return f.read()

def validate_chunk(text, section):
    reasons = []

    if section == "header":
        return True, []

    if section == "overview":
        if "<h1>Overview" not in text:
            reasons.append("Missing <h1>Overview tag")
        if "</ac:rich-text-body>" not in text:
            reasons.append("Missing </ac:rich-text-body> tag")
        return len(reasons) == 0, reasons

    open_tags = text.count("<ac:structured-macro")
    close_tags = text.count("</ac:structured-macro>")
    if open_tags != close_tags:
        reasons.append(f"Unbalanced macro tags: {open_tags} open vs {close_tags} close")

    return len(reasons) == 0, reasons

def generate_section(name, prompt, model, context):
    if name == "header":
        print(f"🛑 Skipping GPT for '{name}' — using prompt content directly.")
        return prompt

    print(f"🧠 Generating: {name} using {model}")

    if name == "overview":
        user_prompt = (
            "You are only allowed to replace the placeholder paragraph in the following block.\n"
            "Do not rename the section, do not remove the heading.\n\n" + prompt
        )
    else:
        user_prompt = context + "\n\n" + prompt

    messages = [
        {"role": "system", "content": "You are a Confluence documentation assistant. Continue the document faithfully without repetition or contradiction."},
        {"role": "user", "content": user_prompt}
    ]

    for attempt in range(2):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.2
        )
        content = response.choices[0].message.content.strip()
        valid, reasons = validate_chunk(content, name)

        if valid:
            print(f"✅ Valid section: {name}")
            return content

        print(f"⚠️ Validation failed for '{name}' (attempt {attempt + 1}):")
        for reason in reasons:
            print(f"   - {reason}")
        print("   🔎 GPT Output (trimmed):")
        print("   " + content[:300].replace("\n", " ") + "...")
        time.sleep(2)

    raise RuntimeError(f"❌ Section '{name}' failed after retries.")

# === Generation Process ===
def build():
    context_map = {}
    full_output = ""

    for i, section in enumerate(SECTIONS):
        lookback = section.get("context_depth", 0)
        context = "\n\n".join(
            context_map.get(SECTIONS[j]["name"], "")
            for j in range(max(0, i - lookback), i)
        )

        prompt = read_prompt(section["prompt"])
        output = generate_section(
            name=section["name"],
            prompt=prompt,
            model=section["model"],
            context=context
        )

        context_map[section["name"]] = output
        with open(f"{OUTPUT_DIR}/{section['name']}.txt", "w") as f:
            f.write(output)

    for name in [s["name"] for s in SECTIONS]:
        with open(f"{OUTPUT_DIR}/{name}.txt", "r") as f:
            full_output += f.read() + "\n"

    full_output += "</ac:layout>\n" + END_MARKER

    with open(FINAL_OUTPUT, "w") as f:
        f.write(full_output)

    print(f"\n✅ Full document written to: {FINAL_OUTPUT}")

# === Main Entry Point ===
if __name__ == "__main__":
    build()
