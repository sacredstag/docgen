import sys
import re

def validate(path):
    with open(path, "r") as f:
        content = f.read()

    errors = []

    if "<ac:layout" not in content or "</ac:layout>" not in content:
        errors.append("Missing <ac:layout> or </ac:layout> tag.")

    if "<!-- === END OF OUTPUT === -->" not in content:
        errors.append("Missing end marker <!-- === END OF OUTPUT === -->")

    open_macros = len(re.findall(r"<ac:structured-macro\b", content))
    close_macros = len(re.findall(r"</ac:structured-macro>", content))

    if open_macros != close_macros:
        errors.append(f"Unbalanced structured macros: {open_macros} open, {close_macros} close.")

    if errors:
        print("⛔ Validation failed:")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)
    else:
        print("✅ Validation passed: Output structure is sound.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_output.py path/to/output.txt")
        sys.exit(1)
    validate(sys.argv[1])
