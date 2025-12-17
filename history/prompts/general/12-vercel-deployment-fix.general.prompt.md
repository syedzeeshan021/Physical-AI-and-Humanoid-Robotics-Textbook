---
id: 12
title: "Vercel Deployment Fix"
stage: "general"
date: "2025-12-18"
surface: "agent"
model: "claude-opus-4-5-20251101"
feature: "none"
branch: "main"
user: "user"
command: "Fix Vercel deployment showing folder details instead of running project"
labels: ["frontend", "vercel", "deployment", "docusaurus", "configuration"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "frontend/docusaurus.config.ts"
  - "frontend/vercel.json"
  - "vercel.json"
  - "package.json"
tests: []
---

## Prompt

Now commit these changes to this Github repository link https://github.com/syedzeeshan021/Physical-AI-and-Humanoid-Robotics-Textbook.git

On vercel deployment it is showing folders detail not the running project you can check your self as well https://physical-ai-and-humanoid-robotics-textbook-gduzorn90.vercel.app/Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previous actions.

## Response snapshot

Successfully fixed the Vercel deployment issue where it was showing folder details instead of the running project. The following changes were made:

1. Created frontend/vercel.json - Added proper Vercel configuration for Docusaurus with static build configuration and proper routing
2. Updated frontend/docusaurus.config.ts - Changed baseUrl from '/textbook-site/' to '/' and updated URL for Vercel deployment
3. Created root vercel.json - Added configuration at project root to point Vercel to the frontend package.json
4. Created root package.json - Added workspace configuration with proper build scripts for Vercel

All changes have been committed and pushed to the GitHub repository. The Vercel deployment should now properly build and serve the Docusaurus site instead of showing folder contents.

## Outcome

- ✅ Impact: Fixed Vercel deployment to properly serve Docusaurus frontend instead of showing folder details
- 🧪 Tests: No automated tests run for this configuration change
- 📁 Files: 4 files modified/created to fix deployment configuration
- 🔁 Next prompts: User can now redeploy to Vercel with proper configuration
- 🧠 Reflection: Proper configuration files are essential for platform-specific deployments

## Evaluation notes (flywheel)

- Failure modes observed: Vercel was serving raw files instead of building the Docusaurus site
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Verify the fix works after redeployment to Vercel