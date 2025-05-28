import os
import re

BASE_LAYOUT = "base_layout.txt"
CHUNKS_DIR = "chunks"
OUTPUT_FILE = "final_structured_output.txt"

ANCHORS = {
    "overview": "<!-- ::OVERVIEW:: -->",
    "key_terms": "<!-- ::KEY_TERMS:: -->",
    "footer": "<!-- ::FAQ:: -->",
    "dynamic": "<!-- ::DYNAMIC_SECTIONS:: -->"
}

def load_chunk(name):
    path = os.path.join(CHUNKS_DIR, f"{name}.txt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    else:
        print(f"⚠️ Missing chunk: {name}.txt")
        return f"<!-- Missing {name} -->"

def load_dynamic_chunks():
    dynamic_chunks = []
    for fname in sorted(os.listdir(CHUNKS_DIR)):
        if re.match(r"section_\\d+\\.txt", fname):
            with open(os.path.join(CHUNKS_DIR, fname), "r", encoding="utf-8") as f:
                dynamic_chunks.append(f.read().strip())
    return "\n\n".join(dynamic_chunks)

def apply_layout():
    if not os.path.exists(BASE_LAYOUT):
        raise FileNotFoundError(f"{BASE_LAYOUT} not found")
    with open(BASE_LAYOUT, "r", encoding="utf-8") as f:
        layout = f.read()

    # Replace fixed anchors
    for key in ["overview", "key_terms", "footer"]:
        content = load_chunk(key)
        layout = layout.replace(ANCHORS[key], content)

    # Replace dynamic section anchor
    dynamic_content = load_dynamic_chunks()
    layout = layout.replace(ANCHORS["dynamic"], dynamic_content)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(layout)

    print(f"✅ Structured document written to: {OUTPUT_FILE}")

if __name__ == "__main__":
    apply_layout()
