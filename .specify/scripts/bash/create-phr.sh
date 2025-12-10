#!/bin/bash

# Script to create a Prompt History Record (PHR)
# Usage: ./create-phr.sh --title "<title>" --stage <stage> [--feature <feature>] --json

set -e  # Exit on any error

# Default values
FEATURE=""
JSON_OUTPUT=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --title)
            TITLE="$2"
            shift 2
            ;;
        --stage)
            STAGE="$2"
            shift 2
            ;;
        --feature)
            FEATURE="$2"
            shift 2
            ;;
        --json)
            JSON_OUTPUT=true
            shift
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

# Validate required parameters
if [[ -z "$TITLE" || -z "$STAGE" ]]; then
    echo "Error: Both --title and --stage are required" >&2
    exit 1
fi

# Validate stage
VALID_STAGES=("constitution" "spec" "plan" "tasks" "red" "green" "refactor" "explainer" "misc" "general")
VALID_STAGE=false
for valid_stage in "${VALID_STAGES[@]}"; do
    if [[ "$STAGE" == "$valid_stage" ]]; then
        VALID_STAGE=true
        break
    fi
done

if [[ "$VALID_STAGE" == false ]]; then
    echo "Error: Invalid stage '$STAGE'. Must be one of: ${VALID_STAGES[*]}" >&2
    exit 1
fi

# Get current branch
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")

# Get git user
USER=$(git config user.name 2>/dev/null || echo "unknown")

# Get current date - using cross-platform compatible format
DATE_ISO=$(date -u +"%Y-%m-%d")

# Generate slug from title
SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-\|-$//g')

# Get next ID by finding the highest existing ID and incrementing
ID=1
if [[ "$STAGE" == "constitution" ]]; then
    PHR_DIR="history/prompts/constitution"
elif [[ "$STAGE" == "general" ]]; then
    PHR_DIR="history/prompts/general"
elif [[ -n "$FEATURE" ]]; then
    PHR_DIR="history/prompts/$FEATURE"
else
    PHR_DIR="history/prompts/general"
fi

# Create directory if it doesn't exist
mkdir -p "$PHR_DIR"

# Find the next available ID
for file in "$PHR_DIR"/*-*."$STAGE".prompt.md; do
    if [[ -f "$file" ]]; then
        file_id=$(basename "$file" | cut -d'-' -f1)
        if [[ "$file_id" =~ ^[0-9]+$ ]] && [[ "$file_id" -ge "$ID" ]]; then
            ID=$((file_id + 1))
        fi
    fi
done

# Generate filename
if [[ -n "$FEATURE" ]]; then
    FILENAME="$PHR_DIR/${ID}-${SLUG}.$STAGE.prompt.md"
else
    if [[ "$STAGE" == "constitution" ]]; then
        FILENAME="$PHR_DIR/${ID}-${SLUG}.$STAGE.prompt.md"
    elif [[ "$STAGE" == "general" ]]; then
        FILENAME="$PHR_DIR/${ID}-${SLUG}.$STAGE.prompt.md"
    else
        FILENAME="$PHR_DIR/${ID}-${SLUG}.$STAGE.prompt.md"
    fi
fi

# Create the PHR file from template with some variables substituted
cat > "$FILENAME" << EOF
---
id: $ID
title: $TITLE
stage: $STAGE
date_iso: $DATE_ISO
surface: {{SURFACE}}
model: {{MODEL}}
feature: ${FEATURE:-{{FEATURE}}}
branch: $BRANCH
user: $USER
command: {{COMMAND}}
labels: {{LABELS}}
links:
  spec: {{LINKS_SPEC}}
  ticket: {{LINKS_TICKET}}
  adr: {{LINKS_ADR}}
  pr: {{LINKS_PR}}
files_yaml: |
  {{FILES_YAML}}
tests_yaml: |
  {{TESTS_YAML}}
---

# $TITLE

## Prompt Text

{{PROMPT_TEXT}}

## Response Text

{{RESPONSE_TEXT}}

## Outcome & Impact

{{OUTCOME_IMPACT}}

## Tests Summary

{{TESTS_SUMMARY}}

## Files Summary

{{FILES_SUMMARY}}

## Next Prompts

{{NEXT_PROMPTS}}

## Reflection Note

{{REFLECTION_NOTE}}

## Evaluation

**Failure modes observed:**
{{FAILURE_MODES_OBSERVED}}

**Next experiment to improve prompt quality:**
{{NEXT_EXPERIMENT}}
EOF

# If JSON output requested, return JSON
if [[ "$JSON_OUTPUT" == true ]]; then
    cat << EOF
{
  "id": "$ID",
  "path": "$FILENAME",
  "context": "${FEATURE:-general}",
  "stage": "$STAGE",
  "feature": "${FEATURE:-none}",
  "branch": "$BRANCH",
  "title": "$TITLE",
  "slug": "$SLUG"
}
EOF
else
    echo "PHR-$ID created: $FILENAME"
fi