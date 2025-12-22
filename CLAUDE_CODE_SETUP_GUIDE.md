# Getting Started with Claude Code and SDD in PIAHR Project

## Project Overview
This project is specifically designed for Claude Code using the Spec-Driven Development (SDD) methodology. It includes custom slash commands that follow the pattern `/sp.*` for various development workflows.

## Prerequisites
- Claude Code (not regular Claude) must be installed and enabled in your IDE
- This project directory must be opened in your IDE with Claude Code active

## Required Configuration Files
The following files are essential for Claude Code to recognize the slash commands:
- `.claude/config.json` - Enables slash command recognition
- `.claude/settings.local.json` - Defines command permissions
- `.claude/commands/` directory - Contains all `/sp.*` command files

## Available SDD Commands
All commands are in the format `/sp.*`:
- `/sp.specify` - Create feature specifications
- `/sp.plan` - Create implementation plans
- `/sp.tasks` - Generate development tasks
- `/sp.implement` - Execute implementation
- `/sp.clarify` - Clarify requirements
- `/sp.adr` - Create Architecture Decision Records
- `/sp.phr` - Create Prompt History Records
- `/sp.constitution` - Update project constitution
- `/sp.analyze` - Analyze the codebase
- `/sp.checklist` - Generate quality checklists
- `/sp.git.commit_pr` - Generate Git messages

## Setup Process
1. Open this project directory in your IDE with Claude Code enabled
2. Wait 1-2 minutes for Claude Code to index the project and command files
3. Verify Claude Code is active in your IDE (look for status indicators)
4. Test by typing `/sp.` to see if commands appear in auto-completion

## Troubleshooting
If commands don't appear:
1. Ensure Claude Code (not regular Claude) is active
2. Verify you're in the PIAHR project directory
3. Wait 1-2 minutes after opening the project for full initialization
4. Check that the `.claude/` directory and its contents exist
5. Restart your IDE if needed

## Important Notes
- This project follows SDD methodology as defined in `CLAUDE.md`
- Commands create PHRs (Prompt History Records) automatically
- The workflow is designed for specification-first development
- All slash commands are properly configured in the `.claude/commands/` directory