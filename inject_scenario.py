import sys
import yaml
import argparse
import os

def load_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def format_steps(steps):
    formatted = ""
    for i, step in enumerate(steps):
        if not isinstance(step, dict):
            print(f"⚠️ Skipping malformed step at index {i}: {repr(step)}")
            continue
        for title, data in step.items():
            if not isinstance(data, dict):
                print(f"⚠️ Skipping non-dict data for step '{title}': {repr(data)}")
                continue
            cmd = data.get("cmd", "[command missing]")
            desc = data.get("desc", "")
            formatted += f"""<li>
<strong>{title}</strong>
<ac:structured-macro ac:name="expand">
  <ac:parameter ac:name="title">Expand for CLI command</ac:parameter>
  <ac:rich-text-body>
    <ac:structured-macro ac:name="noformat">
      <ac:plain-text-body><![CDATA[{cmd}]]></ac:plain-text-body>
    </ac:structured-macro>
  </ac:rich-text-body>
</ac:structured-macro>
<p>{desc}</p>
</li>\n"""
    return formatted

def build_input_txt(scenario, source_txt):
    title = scenario.get("title", "[Untitled Scenario]")
    summary = scenario.get("summary", "No summary available.")
    cmds = "\n".join(f"- `{c}`" for c in scenario.get("cli_commands", []))
    errors = "\n".join(f"- {e}" for e in scenario.get("errors_to_cover", []))
    faq = scenario.get("section_tips", {}).get("faq", "")
    validation = scenario.get("section_tips", {}).get("validation", "")
    overview = scenario.get("section_tips", {}).get("overview", "")
    steps_xml = format_steps(scenario.get("steps", []))

    return f"""Title: {title}

Audience: {scenario.get('audience', 'L3')}

Platform(s): {', '.join(scenario.get('platforms', []))}

Level of Detail: expert

---

Scenario Summary:
{summary}

---

Source SME Notes:
--------
{source_txt}
--------

---

Prompt:
Write a Confluence View Storage Format article for the issue: {title}.

Include the following:

**Overview**:
{overview}

**Procedural Steps**:
<ol>
{steps_xml}</ol>

**Validation & Logs**:
{validation}

**Expected CLI Commands**:
{cmds}

**Known Errors**:
{errors}

**FAQs**:
{faq}

Format using full Confluence macros (panel, anchor, expand, noformat). Preserve all technical data from the SME text exactly. Fill in all gaps with standard known troubleshooting behavior for this scenario. Do not leave placeholders unless absolutely required.
"""

def write_individual_sections(steps):
    os.makedirs("chunks", exist_ok=True)
    count = 0
    for step in steps:
        if not isinstance(step, dict):
            continue
        for title, data in step.items():
            if not isinstance(data, dict):
                continue
            cmd = data.get("cmd", "[command missing]")
            desc = data.get("desc", "")
            xml = f"""
<ac:structured-macro ac:name="section">
  <ac:rich-text-body>
    <ac:structured-macro ac:name="column">
      <ac:parameter ac:name="width">100%</ac:parameter>
      <ac:rich-text-body>
        <h1>{title}</h1>
        <p>{desc}</p>
        <ac:structured-macro ac:name="expand">
          <ac:parameter ac:name="title">CLI Command</ac:parameter>
          <ac:rich-text-body>
            <ac:structured-macro ac:name="noformat">
              <ac:plain-text-body><![CDATA[{cmd}]]></ac:plain-text-body>
            </ac:structured-macro>
          </ac:rich-text-body>
        </ac:structured-macro>
      </ac:rich-text-body>
    </ac:structured-macro>
  </ac:rich-text-body>
</ac:structured-macro>
""".strip()
            with open(f"chunks/section_{count + 1}.txt", "w") as out:
                out.write(xml)
            print(f"🧩 Wrote: chunks/section_{count + 1}.txt")
            count += 1
    print(f"✅ Injected {count} dynamic section(s).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", required=True, help="Scenario YAML file name (without path)")
    parser.add_argument("--source", required=True, help="Path to the SME raw content text")
    args = parser.parse_args()

    scenario = load_yaml(f"scenarios/{args.scenario}.yaml")

    with open(args.source, 'r') as f:
        source_text = f.read()

    result = build_input_txt(scenario, source_text)

    with open("input_1.txt", "w") as f:
        f.write(result)

    print("✅ Scenario injection complete → input_1.txt")

    steps = scenario.get("steps", [])
    if steps:
        write_individual_sections(steps)
