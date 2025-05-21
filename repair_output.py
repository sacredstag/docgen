import re

def read_file(path="output.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(content, path="output_repaired.txt"):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def inject_layout(xml):
    if "<ac:layout" in xml:
        return xml
    return f"<ac:layout>\n<ac:layout-section ac:type=\"single\">\n<ac:layout-cell>\n{xml}\n</ac:layout-cell>\n</ac:layout-section>\n</ac:layout>"

def insert_anchor(xml, anchor_id):
    if f"<ac:parameter ac:name=\"\">{anchor_id}</ac:parameter>" in xml:
        return xml
    anchor_block = f"""
<ac:structured-macro ac:name="anchor">
  <ac:parameter ac:name="">{anchor_id}</ac:parameter>
</ac:structured-macro>
"""
    return anchor_block + xml

def insert_faq_section(xml):
    if "<h2>Frequently Asked Questions</h2>" in xml:
        return xml
    faq_block = """
<ac:structured-macro ac:name="anchor">
  <ac:parameter ac:name="">faq</ac:parameter>
</ac:structured-macro>
<ac:structured-macro ac:name="panel">
  <ac:parameter ac:name="bgColor">#7630EA</ac:parameter>
  <ac:rich-text-body>
    <h2>Frequently Asked Questions</h2>
    <p>[To be added]</p>
  </ac:rich-text-body>
</ac:structured-macro>
"""
    if "</ac:layout>" in xml:
        return xml.replace("</ac:layout>", faq_block + "\n</ac:layout>")
    return xml + faq_block

def insert_missing_macros(xml):
    additions = ""
    if 'ac:name="expand"' not in xml:
        additions += """
<ac:structured-macro ac:name="expand">
  <ac:parameter ac:name="title">Click to view additional information</ac:parameter>
  <ac:rich-text-body>
    <ac:structured-macro ac:name="noformat">
      <ac:plain-text-body><![CDATA[echo "Replace this with actual CLI command"]]></ac:plain-text-body>
    </ac:structured-macro>
  </ac:rich-text-body>
</ac:structured-macro>
"""
    if 'ac:name="info"' not in xml:
        additions += """
<ac:structured-macro ac:name="info">
  <ac:rich-text-body>
    <p><strong>Note:</strong> Double-check SAN zoning configuration before continuing.</p>
  </ac:rich-text-body>
</ac:structured-macro>
"""
    if additions:
        if "</ac:layout>" in xml:
            return xml.replace("</ac:layout>", additions + "\n</ac:layout>")
        else:
            return xml + additions
    return xml

def merge_orphan_parameters(xml):
    """
    Detects improperly closed <ac:structured-macro> tags followed by <ac:parameter> lines,
    and moves the parameters up inside the last open macro.
    """
    pattern = re.compile(
        r"(</ac:structured-macro>\s*)(\s*(<ac:parameter ac:name=.*?</ac:parameter>\s*)+)",
        re.MULTILINE
    )

    def merge_macro(match):
        closing = match.group(1)
        orphaned_params = match.group(2)
        return f"{orphaned_params}{closing}"

    return pattern.sub(merge_macro, xml)

def repair_output():
    xml = read_file()
    xml = inject_layout(xml)

    for anchor in ["overview", "steps", "validation", "faq"]:
        xml = insert_anchor(xml, anchor)

    xml = insert_faq_section(xml)
    xml = insert_missing_macros(xml)
    xml = merge_orphan_parameters(xml)

    write_file(xml)
    print("✅ Repairs complete. Output saved to output_repaired.txt")

if __name__ == "__main__":
    repair_output()
