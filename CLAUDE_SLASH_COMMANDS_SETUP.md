# Claude Code Slash Commands Setup Guide

## Issue Description
Claude Code was not recognizing slash commands that were properly created in the `.claude/commands/` directory. The command files existed with the correct naming convention (`sp.*.md`) and proper structure, but Claude Code wasn't loading them automatically.

## Root Cause
The issue was that Claude Code requires explicit configuration to recognize and load slash commands from the `.claude/commands/` directory. Without a proper configuration file, Claude Code doesn't know to look for and register these commands.

## Solution Implemented
A configuration file was created at `.claude/config.json` with the following settings:

```json
{
  "commands": {
    "directory": ".claude/commands",
    "pattern": "sp.*.md",
    "enabled": true
  },
  "features": {
    "slash_commands": true,
    "auto_reload": true
  }
}
```

## Configuration Details
- `commands.directory`: Specifies where Claude Code should look for command files
- `commands.pattern`: Defines the file naming pattern for command files (sp.*.md matches all your slash command files)
- `commands.enabled`: Enables the command loading functionality
- `features.slash_commands`: Enables slash command support in Claude Code
- `features.auto_reload`: Allows commands to be reloaded without restarting Claude Code

## Verification
After creating the configuration file, Claude Code should now recognize and load all slash commands from the `.claude/commands/` directory. The commands should be available and functional when you use them in Claude Code.

## Available Commands
All commands in the format `/sp.*` should now work:
- `/sp.specify` - Create or update feature specifications
- `/sp.plan` - Execute implementation planning workflow
- `/sp.tasks` - Generate testable tasks from planning artifacts
- `/sp.implement` - Execute implementation workflow
- `/sp.adr` - Create Architecture Decision Records
- `/sp.phr` - Create Prompt History Records
- And all other `sp.*` commands

## Troubleshooting
If commands are still not recognized:
1. Verify the config file exists at `.claude/config.json`
2. Check that the command files follow the `sp.*.md` naming pattern
3. Ensure the command files have proper YAML frontmatter with descriptions
4. Restart Claude Code to ensure the configuration is loaded