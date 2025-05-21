# 📘 Confluence DocGen POC – System Overview

## 🧭 Purpose

This system automates the transformation of SME-authored technical notes into fully formatted Confluence documentation using OpenAI's GPT API. It enriches SME content with command context, error interpretation, procedural structure, and macros – converting raw notes into review-ready docs.

## 🧱 System Architecture

### Main Phases:
1. **Scenario Injection** – Converts YAML + SME input into structured GPT prompt.
2. **Doc Generation** (`main.py`)
   - `--phase 1`: Optional layout only
   - `--phase 2`: Optional SME injection into layout
   - `--phase auto`: Full enrichment + validation + repair
3. **Repair & Validation**
   - Fixes missing/malformed macros
   - Validates anchor/macros/panels

## 📂 Key Files

| File | Role |
|------|------|
| `docgen.sh` | Interactive SME prompt wizard |
| `main.py` | Core orchestrator script |
| `repair_output.py` | Repairs Confluence XML macros |
| `validate_output.py` | Validates final output |
| `inject_scenario.py` | Converts scenario YAML + SME into GPT prompt |
| `scenarios/*.yaml` | Structured scenario data |
| `input_1.txt` | Final GPT user input |
| `output.txt` | Final Confluence XML |
| `output_repaired.txt` | Fixed version |

## 🧩 Flow

1. SME provides rough notes (`*.txt`)
2. Writer authors a YAML scenario (`*.yaml`)
3. Run:

```bash
python inject_scenario.py --scenario scenario_name --source notes.txt
python main.py --phase auto
```

4. Result: validated `output.txt` with full macro formatting.

## 🛡️ Features

- View Storage Format output
- Expand + noformat for CLI
- Panel macros
- Anchor macros
- FAQ scaffolding
- Repairs + validation pass built-in

## 🚀 Future Expansion

- Confluence API integration
- Slack trigger bot
- Multi-section auto injection
- LLM chain for review notes

---

**Owner:** Bryan Cope  
**Construct Partner:** Bob – Anchor Construct
