#!/bin/bash

set -e

echo "🔧 Welcome to the Documentation Generator"
echo "----------------------------------------"

# Select doc generation mode
echo ""
echo "🧭 Choose operation mode:"
echo "   1) generate – Create a new document from scratch"
echo "   2) enrich   – Review and enhance an existing Confluence doc"

select mode in "generate" "enrich"; do
  echo "📂 Selected mode: $mode"
  break
done

if [ "$mode" == "generate" ]; then
  # SME prompts
  read -p "📌 Title of the issue: " title
  read -p "🖥️ System/Platform involved: " system
  read -p "🎯 Audience (e.g. L1, L2, L3): " audience
  read -p "📖 Brief description of the issue: " description
  read -p "🧩 What should this doc help the support team do? " steps
  read -p "⚠️ Any special warnings or considerations? " warnings
  echo ""

  echo "📏 Choose the desired level of detail:"
  echo "   1) basic    – High-level steps, minimal CLI, suitable for overviews"
  echo "   2) standard – Default. Procedural steps, warnings, and core examples"
  echo "   3) detailed – Adds deeper CLI output, recovery tips, and validations"
  echo "   4) expert   – Deep dives, edge cases, expert analysis and error flows"
  echo ""

  select detail in "basic" "standard" "detailed" "expert"; do
    echo "📏 Detail level selected: $detail"
    break
  done

  # Write input_1.txt
  cat <<EOF > input_1.txt
Title: $title

Audience: $audience

System: $system

Level of Detail: $detail

Request:
$description

Support engineers need a document that includes:
- $steps

Include:
- CLI commands inside expand/noformat blocks
- A note or warning block (if needed): $warnings
- All anchor macros
- Color-coded panels for sections
- Final section titled “Frequently Asked Questions”
EOF

  # Append level-specific instructions
  case "$detail" in
    basic)
      cat <<EOB >> input_1.txt

This is a basic-level document. Please:
- Provide a high-level summary of the issue
- List core procedural steps without detailed explanation
- Keep command examples minimal
- Avoid advanced recovery or edge case discussion
- Prioritize clarity and brevity over completeness
EOB
      ;;
    standard)
      cat <<EOS >> input_1.txt

This is a standard-level document. Please:
- Include clear CLI commands using noformat blocks
- Use section anchors, color panels, and info macros
- Describe each step and why it matters
- Include a FAQ section with typical questions
- Provide a warning block if there are risks
EOS
      ;;
    detailed)
      cat <<EOD >> input_1.txt

This is a detailed-level document. Please:
- Provide CLI commands with real-world sample output
- Include diagnostic paths (e.g., logs, dmesg, multipath -ll)
- List common failure conditions and what they indicate
- Suggest recovery strategies and configuration validations
- Add a FAQ with technical depth
- Use all macro structures expected in Confluence output
EOD
      ;;
    expert)
      cat <<EOX >> input_1.txt

This is an expert-level document. Please:
- Explain both the what and the why for every step
- Reference kernel flags, edge case triggers, system interop behavior
- Include layered diagnostics and recovery logic
- Provide alternate strategies and known escalations
- Anticipate questions an L3 or SRE would ask
- Do not simplify language or skip internal mechanisms
EOX
      ;;
  esac

  echo "📝 SME input captured in input_1.txt"
  echo "----------------------------------------"

  echo "🧱 Phase 1: Building layout..."
  python main.py --phase 1

  echo "🧠 Phase 2: Injecting technical content..."
  python main.py --phase 2

  echo "🧰 Repairing structure and macros..."
  python repair_output.py
  mv output_repaired.txt output.txt

  echo "🔎 Validating final output..."
  python validate_output.py

  echo "✅ Doc generation complete. Final output ready in: output.txt"

elif [ "$mode" == "enrich" ]; then
  echo ""
  echo "📝 Enrichment Mode"
  echo "You are enhancing an existing Confluence document with technical, L3-level improvements."
  echo ""

  read -p "📄 Enter the filename of the base Confluence document (e.g. pvc_issue.txt): " basefile
  read -p "💬 What specific gaps or topics should GPT focus on improving? " focus

  echo "$basefile" > enrich_source.txt
  echo "$focus" > input_1.txt

  echo "🚀 Running enrichment pass..."
  python main.py --phase enrich

  echo "✅ Enrichment complete. Output saved to output.txt"
fi
