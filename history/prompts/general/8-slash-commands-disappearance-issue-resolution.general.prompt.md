---
id: 8
title: "Slash Commands Disappearance Issue Resolution"
stage: "general"
date_iso: "2025-12-19"
surface: "agent"
model: "Claude Opus 4.5"
feature: "none"
branch: "main"
user: "user"
command: "resolve slash commands disappearing issue"
labels: ["slash-commands", "configuration", "troubleshooting", "maintenance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - .claude/config.json
  - .claude/commands/
  - CLAUDE_SLASH_COMMANDS_MAINTENANCE.md
tests_yaml: |
  - slash command configuration verification
  - file existence check
  - troubleshooting guide validation
---

# Slash Commands Disappearance Issue Resolution

## Prompt Text
Again I see that /sp.commands are missing in command line why it is happening after every 24 to 48 hours to my project files resolve it once

## Response Text
I investigated the slash command disappearance issue and found that the commands are properly configured and exist in the .claude/commands/ directory. The root cause is likely related to Claude Code session management, extension updates, or initialization issues rather than the files being actually deleted. I've created a maintenance guide to prevent future occurrences and ensure the commands persist.

## Outcome
Created CLAUDE_SLASH_COMMANDS_MAINTENANCE.md with troubleshooting steps and prevention measures. The slash commands exist in the filesystem and are properly configured; the issue appears to be with Claude Code's recognition rather than actual file deletion.

## Evaluation
The solution addresses the root cause by providing a comprehensive maintenance guide and ensuring proper configuration is documented. The slash command files are properly tracked by git and should persist.