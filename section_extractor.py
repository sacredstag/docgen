import os
import re
import argparse

SOURCE_FILE = "kube_openshift_order_ops_PVC.txt"
CHUNKS_DIR = "chunks"
SECTION_PATTERN = re.compile(r"<ac:structured-macro ac:name=\"section\".*?<ac:rich-text-body>(.*?)</ac:rich-text-body>.*?</ac:structured-macro>", re.DOTALL)

os.makedirs(CHUNKS_DIR, exist_ok=True)

def extract_sections(path):
    with open(path, "r") as f:
        raw = f.read()

    matches = SECTION_PATTERN.findall(raw)

    count = 0
    for i, match in enumerate(matches):
        # Skip first (overview) and last (FAQ/panels)
        if i == 0 or i == len(matches) - 1:
            continue

        out_path = os.path.join(CHUNKS_DIR, f"section_{count + 1}.txt")
        with open(out_path, "w") as out:
            out.write(match.strip())
        print(f"✅ Extracted: section_{count + 1}.txt")
        count += 1

    print(f"\n🧾 Extracted {count} dynamic section(s).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=SOURCE_FILE, help="Path to structured enriched file")
    args = parser.parse_args()
    extract_sections(args.source)
