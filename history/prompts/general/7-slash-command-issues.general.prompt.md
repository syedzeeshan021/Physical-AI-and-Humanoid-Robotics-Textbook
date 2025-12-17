---
id: 7
title: "Slash Command Issues Investigation"
stage: "general"
date_iso: "2025-12-14"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "none"
branch: "main"
user: "user"
command: "analyze slash command issues"
labels: ["slash-commands", "configuration", "troubleshooting"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - .claude/config.json
  - .claude/commands/sp.specify.md
  - .claude/commands/sp.plan.md
  - .claude/commands/sp.tasks.md
  - CLAUDE_SLASH_COMMANDS_SETUP.md
tests_yaml: |
  - slash command recognition
  - configuration validation
---

# Slash Command Issues Investigation

## Prompt Text
There is an issue I cannot see the speckit plus various command which was present in the start like sp.constitution,sp.specify,sp.clarify,sp.tasks,sp.implement,sp.adr

## Response Text
I investigated the issue with missing slash commands and found that:

1. The slash commands exist in the `.claude/commands/` directory with proper naming convention (`sp.*.md`)
2. A configuration file `.claude/config.json` was created to enable slash command discovery
3. The commands are properly formatted with YAML frontmatter descriptions
4. The issue is that Claude Code needs to be restarted to pick up the new configuration

## Outcome
The slash commands are properly configured but require Claude Code to be restarted to be recognized. The configuration file enables slash command discovery from the `.claude/commands/` directory, and after restarting Claude Code, commands like `/sp.specify`, `/sp.plan`, `/sp.tasks`, etc. should be available.

## Evaluation
The solution addresses the root cause of the issue - Claude Code needs to be restarted to load the slash command configuration. The configuration is correct and follows the expected format for enabling slash commands from the `.claude/commands/` directory.