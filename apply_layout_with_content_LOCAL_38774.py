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
        with open(path, "r") as f:
            return f.read().strip()
    else:
        print(f"⚠️ Missing chunk: {name}.txt")
        return f"<!-- Missing {name} -->"

def load_dynamic_chunks():
    dynamic_chunks = []
    section_files = []
    for fname in os.listdir(CHUNKS_DIR):
        match = re.match(r"section_(\\d+)\\.txt", fname)
        if match:
            section_files.append((int(match.group(1)), fname))

    for _, fname in sorted(section_files):
        with open(os.path.join(CHUNKS_DIR, fname), "r") as f:
            dynamic_chunks.append(f.read().strip())

    return "\n\n".join(dynamic_chunks)

def apply_layout():
    with open(BASE_LAYOUT, "r") as f:
        layout = f.read()

    # Replace fixed anchors
    for key in ["overview", "key_terms", "footer"]:
        content = load_chunk(key)
        layout = layout.replace(ANCHORS[key], content)

    # Replace dynamic section anchor
    dynamic_content = load_dynamic_chunks()
    layout = layout.replace(ANCHORS["dynamic"], dynamic_content)

    with open(OUTPUT_FILE, "w") as f:
        f.write(layout)

    print(f"✅ Structured document written to: {OUTPUT_FILE}")

if __name__ == "__main__":
    apply_layout()
