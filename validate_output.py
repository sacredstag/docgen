import sys
import re
import argparse

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

<<<<<<< ours
def _print_help():
    print("Usage: python validate_output.py [path/to/output.txt]")
    print("If no path is provided, 'output.txt' is used by default.")


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] in ("-h", "--help"):
        _print_help()
        sys.exit(0)

    path = sys.argv[1] if len(sys.argv) >= 2 else "output.txt"
    validate(path)
=======
def main():
    parser = argparse.ArgumentParser(description="Validate structure of generated Confluence output")
    parser.add_argument("path", nargs="?", default="output.txt", help="Output file to validate")
    args = parser.parse_args()

    validate(args.path)


if __name__ == "__main__":
    main()
>>>>>>> theirs
