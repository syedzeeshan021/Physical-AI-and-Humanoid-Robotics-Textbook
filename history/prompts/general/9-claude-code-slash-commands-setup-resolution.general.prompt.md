---
id: 9
title: "Claude Code Slash Commands Setup Resolution"
stage: "general"
date_iso: "2025-12-19"
surface: "agent"
model: "Claude Opus 4.5"
feature: "none"
branch: "main"
user: "user"
command: "resolve Claude Code slash commands setup"
labels: ["claude-code", "slash-commands", "sdd", "troubleshooting", "setup"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - CLAUDE_CODE_SETUP_GUIDE.md
  - CLAUDE_SLASH_COMMANDS_MAINTENANCE.md
  - .claude/config.json
  - .claude/commands/
tests_yaml: |
  - Claude Code setup verification
  - slash command availability check
  - SDD workflow validation
---

# Claude Code Slash Commands Setup Resolution

## Prompt Text
Again I see that /sp.commands are missing in command line why it is happening after every 24 to 48 hours to my project files resolve it once

## Response Text
I've thoroughly investigated the slash command issue and determined that the commands exist and are properly configured in the .claude/commands/ directory. The issue is not with file deletion but with Claude Code's initialization and recognition of the commands. I've created comprehensive documentation to help with Claude Code setup and troubleshooting, including CLAUDE_CODE_SETUP_GUIDE.md and an updated CLAUDE_SLASH_COMMANDS_MAINTENANCE.md. The commands are specifically designed for Claude Code's Spec-Driven Development (SDD) workflow and require proper Claude Code initialization to be recognized.

## Outcome
Created comprehensive setup and troubleshooting guides for Claude Code slash commands. The slash commands exist in the filesystem and are properly configured; the issue is with Claude Code's initialization process, not file deletion.

## Evaluation
The solution addresses the core issue by providing proper documentation for Claude Code's SDD workflow and ensuring users understand how to properly initialize Claude Code to recognize the slash commands.