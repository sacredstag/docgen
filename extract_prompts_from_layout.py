import os
import argparse

PROMPT_DIR = "prompts"

os.makedirs(PROMPT_DIR, exist_ok=True)

SECTION_TAGS = {
    "header": "<ac:layout-section ac:type=\"single\">",
    "overview": "<h1>Overview</h1>",
    "key_terms": "<ac:parameter ac:name=\"title\">Key Terms &amp; Definitions</ac:parameter>",
    "diagnostics": "<h1>Order of Operations</h1>",
    "footer": "<h1>Frequently Asked Questions</h1>"
}

SECTION_WRAPPERS = {
    "overview": lambda: (
        "<!-- DO NOT change the heading. Only replace the paragraph below it. -->\n"
        "<ac:rich-text-body>\n"
        "<h1>Overview</h1>\n"
        "<p>[INSERT OVERVIEW PARAGRAPH HERE]</p>\n"
        "</ac:rich-text-body>"
    ),
    "key_terms": lambda: (
        "<!-- Only replace or expand the definitions within the panel structure. Keep the layout intact. -->\n"
    ),
    "diagnostics": lambda: (
        "<!-- Only replace diagnostic steps and CLI commands. Do not alter layout tags. -->\n"
    ),
    "footer": lambda: (
        "<!-- Replace FAQ content only. Maintain structure and macro layout. -->\n"
    )
}

def extract_sections(text):
    sections = {}
    last_index = 0
    ordered_keys = list(SECTION_TAGS.keys())

    for i, key in enumerate(ordered_keys):
        tag = SECTION_TAGS[key]
        idx = text.find(tag)
        if idx == -1:
            print(f"⚠️ Tag for {key} not found. Skipping.")
            continue

        next_idx = text.find(SECTION_TAGS[ordered_keys[i + 1]], idx) if i + 1 < len(ordered_keys) else len(text)
        section_content = text[idx:next_idx].strip()

        if key in SECTION_WRAPPERS:
            wrapper = SECTION_WRAPPERS[key]()
            section_content = wrapper if key == "overview" else wrapper + section_content

        sections[key] = section_content
        last_index = next_idx

    return sections

def write_prompts(sections):
    for name, content in sections.items():
        with open(os.path.join(PROMPT_DIR, f"{name}.txt"), "w") as f:
            f.write(content)
        print(f"✅ Wrote: prompts/{name}.txt")

def run(source_path):
    with open(source_path, "r") as f:
        raw = f.read()

    sections = extract_sections(raw)
    write_prompts(sections)
    print("\n✅ Extraction complete. Prompts ready.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, help="Path to Confluence XML-like enriched doc")
    args = parser.parse_args()
    run(args.source)
