#!/bin/bash

# Script to create an Architecture Decision Record (ADR)
# Usage: ./create-adr.sh "<title>"

set -e  # Exit on any error

# Get title from command line argument
TITLE="$1"

if [[ -z "$TITLE" ]]; then
    echo "Error: Title is required" >&2
    echo "Usage: $0 \"<title>\"" >&2
    exit 1
fi

# Create history/adr directory if it doesn't exist
mkdir -p "history/adr"

# Find the next available ADR ID
ID=1
for file in history/adr/ADR-*; do
    if [[ -f "$file" ]]; then
        file_id=$(basename "$file" | cut -d'-' -f2 | cut -d'.' -f1)
        if [[ "$file_id" =~ ^[0-9]+$ ]] && [[ "$file_id" -ge "$ID" ]]; then
            ID=$((file_id + 1))
        fi
    fi
done

# Generate filename with zero-padded ID
PADDED_ID=$(printf "%04d" $ID)
FILENAME="history/adr/ADR-${PADDED_ID}-${TITLE// /-}.md"

# Create the ADR file from template
cat > "$FILENAME" << 'EOF'
# ADR-{{ID}}: {{TITLE}}

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Proposed | Accepted | Superseded | Rejected
- **Date:** {{DATE_ISO}}
- **Feature:** {{FEATURE_NAME}}
- **Context:** {{CONTEXT}}

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

{{DECISION}}

<!-- For technology stacks, list all components:
     - Framework: Next.js 14 (App Router)
     - Styling: Tailwind CSS v3
     - Deployment: Vercel
     - State Management: React Context (start simple)
-->

## Consequences

### Positive

{{POSITIVE_CONSEQUENCES}}

<!-- Example: Integrated tooling, excellent DX, fast deploys, strong TypeScript support -->

### Negative

{{NEGATIVE_CONSEQUENCES}}

<!-- Example: Vendor lock-in to Vercel, framework coupling, learning curve -->

## Alternatives Considered

{{ALTERNATIVES}}

<!-- Group alternatives by cluster:
     Alternative Stack A: Remix + styled-components + Cloudflare
     Alternative Stack B: Vite + vanilla CSS + AWS Amplify
     Why rejected: Less integrated, more setup complexity
-->

## References

- Feature Spec: {{SPEC_LINK}}
- Implementation Plan: {{PLAN_LINK}}
- Related ADRs: {{RELATED_ADRS}}
- Evaluator Evidence: {{EVAL_NOTES_LINK}} <!-- link to eval notes/PHR showing graders and outcomes -->
EOF

# Get current date
DATE_ISO=$(date -I)

# Replace placeholders in the file - use different approach for cross-platform compatibility
TEMP_FILE=$(mktemp)
sed "s/{{ID}}/$ID/g; s/{{TITLE}}/$TITLE/g; s/{{DATE_ISO}}/$DATE_ISO/g" "$FILENAME" > "$TEMP_FILE"
mv "$TEMP_FILE" "$FILENAME"

echo "ADR-${PADDED_ID} created: $FILENAME"