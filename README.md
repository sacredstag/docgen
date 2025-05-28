# 📘 Confluence DocGen POC

A powerful GPT-powered toolchain that generates and enriches structured Confluence documentation using SME prompts, YAML scenarios, and CLI-driven pipelines.

---

## 🎯 Purpose

Automate the transformation of raw technical troubleshooting notes into complete, validated Confluence View Storage Format articles — ready for publishing with macros, panels, anchors, CLI blocks, and documentation best practices.

---

## 🏗️ Project Structure

```
.
├── main.py                      ← CLI entry point for all phases
├── docgen.sh                    ← Interactive SME-driven generator
├── inject_scenario.py           ← Converts scenario YAML + raw text → input_1.txt
├── validate_output.py           ← Checks for macro/anchor compliance
├── repair_output.py             ← Cleans up missing/invalid macro XML
├── doc_generation_guide_HCorp.md← System prompt used across all GPT calls
├── scenarios/                   ← Modular YAML definitions for known workflows
│   └── *.yaml
├── output_*.txt                 ← Timestamped generated docs
├── input_1.txt                  ← Dynamic prompt for phase 2/enrich
├── enrich_source.txt            ← Pointer to base doc (enrich pipeline)
├── .env                         ← API key (OPENAI_API_KEY)
└── README.md                    ← You're reading this
```

---

## 🔁 Supported Phases

| Phase      | Purpose                                                      |
|------------|--------------------------------------------------------------|
| `1`        | Build doc layout skeleton with anchors and macro blocks      |
| `2`        | Fill layout with technical procedures, CLI, warnings         |
| `enrich`   | Review + enhance an existing doc without overwriting content |
| `auto`     | Run: enrich → repair → validate in one seamless pipeline     |

---

## 🚀 Workflow Options

### Option A: Manual Pipeline

```bash
python main.py --phase 1
python main.py --phase 2
python repair_output.py
python validate_output.py
```

### Option B: Scenario-Based Automation

```bash
python inject_scenario.py --scenario pvc_mount_failure --source kube_pvc_issue_notes.txt
python main.py --phase auto
```

Or run the helper pipeline script:

```bash
python pipeline.py --scenario pvc_mount_failure --source kube_pvc_issue_notes.txt
```

This generates input, runs GPT, repairs macro output, and validates structure.

---

## 💬 SME-Driven Prompting (`docgen.sh`)

```bash
./docgen.sh
```

Prompts for:
- Title, platform, audience
- Issue summary
- Troubleshooting goals
- CLI expectations
- Risk notes
- Desired depth: basic → expert

Then auto-runs the full pipeline.

---

## 🔧 inject_scenario.py

```bash
python inject_scenario.py --scenario <name> --source <source.txt>
```

Merges:
- `scenarios/<name>.yaml`: Describes platform, commands, known steps
- `source.txt`: SME raw input

→ Outputs formatted `input_1.txt` with structured instructions for GPT.

---

## 🔍 Validation (`validate_output.py`)

Ensures all required elements are present:
- `<ac:layout>`
- `panel`, `expand`, `noformat`, `anchor` macros
- Placeholder and FAQ resolution

---

## 🧰 Repair Script (`repair_output.py`)

Cleans output by:
- Fixing nesting issues
- Auto-wrapping CLI with proper macros
- Inserting missing FAQ/anchors/macros
- Filling empty tags with default content

---

## 📄 Scenario YAML (Example)

```yaml
title: Subscription Validation Failure in HPE GreenLake
audience: L3 GreenLake Support Engineers
system: HPE Alletra Storage MP + GreenLake Console
detail: expert

steps:
  - title: Verify Network Connectivity
    cmd: ping cloud.hpe.com
    desc: Check if the array has outbound connectivity to the GreenLake Console endpoints.

  - title: Manually Trigger Sync
    cmd: initiate-subscription-validation
    desc: Use CLI to manually validate subscription registration.
```

---

## 🧠 Prompt Strategy

All GPT calls use `doc_generation_guide_HCorp.md` as a system prompt, enforcing:

- Macro compliance
- SME content preservation
- Anchored, panel-based layouting
- Contextual syntax-aware CLI insertions
- Output in Confluence Storage Format **only**

---

## 📂 Output Files

- `output.txt`: Latest output
- `output_<phase>_<timestamp>.txt`: Versioned backup
- `output_repaired.txt`: Cleaned and macro-fixed
- `input_1.txt`: Current GPT input

---

## ✅ Requirements

- Python 3.11+
- `openai`, `pyyaml`, `dotenv`, `httpx`
- `.env` file with: `OPENAI_API_KEY`

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🛣️ Future Plans

- Upload directly to Confluence
- Support alternate platforms (Salesforce, ServiceNow KBs)
- Case ingestion → KB suggestion engine
- Doc drift detection over time
- Flag stale documentation automatically

---

## 🔒 Security

- All SME content remains local
- Only GPT prompts and context sent via secure OpenAI API
- API keys managed via `.env`, never hardcoded

---

