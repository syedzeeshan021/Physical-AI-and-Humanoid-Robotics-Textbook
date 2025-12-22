# Claude Code Slash Commands Setup and Maintenance Guide

## Issue Description

The Speckit Plus slash commands (like `/sp.specify`, `/sp.plan`, `/sp.tasks`, etc.) were not appearing or working in Claude Code interface. This was happening because the commands were present in the `.claude/commands/` directory but were not included in the permissions list in the settings file.

## Root Cause

Claude Code requires explicit permission for each slash command to be available. Even though the command files exist in `.claude/commands/`, they won't work unless they're explicitly added to the permissions list in the settings file.

## Solution Applied

Updated `.claude/settings.local.json` to include all Speckit Plus commands in the `permissions.allow` array:

```json
{
  "permissions": {
    "allow": [
      "Bash(mkdir -p \"specs/textbook-generation\")",
      "Bash(npm start)",
      "SlashCommand(/sp.adr)",
      "SlashCommand(/sp.analyze)",
      "SlashCommand(/sp.checklist)",
      "SlashCommand(/sp.clarify)",
      "SlashCommand(/sp.constitution)",
      "SlashCommand(/sp.git.commit_pr)",
      "SlashCommand(/sp.implement)",
      "SlashCommand(/sp.phr)",
      "SlashCommand(/sp.plan)",
      "SlashCommand(/sp.specify)",
      "SlashCommand(/sp.tasks)",
      "Bash(powershell -ExecutionPolicy Bypass -File .specify/scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks)",
      "Bash(dir)",
      "Bash($env:SPECIFY_FEATURE=\"001-urdu-translation-button\")",
      "Bash(powershell -Command \"$env:SPECIFY_FEATURE=''001-urdu-translation-button''; . ''.specify/scripts/powershell/check-prerequisites.ps1'' -Json -RequireTasks -IncludeTasks\")",
      "Bash(powershell -ExecutionPolicy Bypass -File ../../../.specify/scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks:*)",
      "Bash(powershell -ExecutionPolicy Bypass -File \"E:\\\\GIAIC Q4 AGENTIC AI\\\\PIAHR\\\\.specify\\\\scripts\\\\powershell\\\\check-prerequisites.ps1\" -Json -RequireTasks -IncludeTasks)",
      "Bash(powershell -ExecutionPolicy Bypass -File \"E:\\\\GIAIC Q4 AGENTIC AI\\\\PIAHR\\\\.specify\\\\scripts\\\\powershell\\\\check-prerequisites.ps1\" -Json)",
      "Bash(find backend -name \"*.py\" -exec grep -l \"create_all\\\\|alembic\\\\|migration\" {} ;)",
      "Bash(python -c \"\nimport asyncio\nfrom backend.src.core.database import init_db\nasyncio.run\\(init_db\\(\\)\\)\nprint\\(''Database initialized successfully''\\)\n\")",
      "Bash(python -c \"\nimport asyncio\nimport sys\nimport os\nsys.path.append\\(os.path.dirname\\(os.path.abspath\\(__file__\\)\\)\\)\n\nfrom src.core.database import init_db\nfrom src.core.config import settings\n\nasync def run_init\\(\\):\n    print\\(''Database URL:'', settings.DATABASE_URL\\)\n    await init_db\\(\\)\n    print\\(''Database initialized successfully''\\)\n\nasyncio.run\\(run_init\\(\\)\\)\n\")",
      "Bash(python init_db.py)",
      "Bash(python add_missing_columns.py)",
      "Bash(python -m uvicorn src.main:app --reload)",
      "Bash(npm run start)",
      "Bash(npm run)",
      "Bash(npm run dev)",
      "Bash(timeout 5 ping -n 1 127.0.0.)",
      "Bash(curl -s -o nul -w \"%{http_code}\" http://127.0.0.1:8000/health)"
    ],
    "deny": [],
    "ask": []
  }
}
```

## Commands Available

All Speckit Plus commands are now available:

- `/sp.adr` - Create Architecture Decision Records
- `/sp.analyze` - Analyze the codebase or requirements
- `/sp.checklist` - Generate checklists
- `/sp.clarify` - Clarify specifications
- `/sp.constitution` - Work with project constitution
- `/sp.git.commit_pr` - Handle git commit and PR workflows
- `/sp.implement` - Implementation workflow
- `/sp.phr` - Create Prompt History Records
- `/sp.plan` - Create architectural plans
- `/sp.specify` - Create feature specifications
- `/sp.tasks` - Generate implementation tasks

## Maintenance Instructions

If you encounter the slash commands not working again:

1. Check that the command files exist in `.claude/commands/`
2. Verify that the command is included in the `permissions.allow` array in `.claude/settings.local.json`
3. If a new command was added to the commands directory, make sure to add it to the permissions as well

## Troubleshooting

If commands still don't work after this fix:

1. Restart Claude Code completely
2. Verify the command files have proper YAML frontmatter
3. Check that the `.claude/config.json` has the correct configuration:

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

This solution should permanently fix the slash commands issue. The commands will now be available in the Claude Code interface.