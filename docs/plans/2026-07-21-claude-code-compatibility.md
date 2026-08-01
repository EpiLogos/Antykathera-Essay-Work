# Claude Code Compatibility Implementation Plan

> For Claude: REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

Goal: Make the Return of Zero development surface and Epi-Logos submission plugin usable in Claude Code without duplicating project doctrine or relying on a nonstandard workflow runtime.

Architecture: Keep .agents/skills/ and .codex/ as the Codex-side source surfaces. Expose the same four development skills to Claude through symlinked .claude/skills/ entries, register the existing Python hook through Claude project settings, and make the plugin marketplace a valid repository-level catalog. Rewrite /mef-refract as a Claude-native orchestration instruction: the parent skill dispatches independent built-in Agent subagents for each lens and performs synthesis after the barrier.

Tech Stack: Markdown Agent Skills, Claude Code settings.json hooks, JSON marketplace manifests, Python stdlib hook handler, unittest filesystem/config tests.

---

### Task 1: Add failing Claude compatibility tests

Files:
- Create tests/test_claude_compatibility.py

Write real filesystem/config tests for the Claude skill projection, project hook registration, marketplace root/source, plugin manifest, and Claude-native MEF command. Run:

    python3 -m unittest tests.test_claude_compatibility -v

Expected result before implementation: FAIL because the .claude projection and root marketplace do not exist and the current MEF command still names the nonstandard Workflow transport.

### Task 2: Project the development skills into Claude

Files:
- Create .claude/skills/return-of-zero-orient as a symlink to ../../.agents/skills/return-of-zero-orient
- Create .claude/skills/return-of-zero-source as a symlink to ../../.agents/skills/return-of-zero-source
- Create .claude/skills/return-of-zero-write as a symlink to ../../.agents/skills/return-of-zero-write
- Create .claude/skills/return-of-zero-review as a symlink to ../../.agents/skills/return-of-zero-review

Use one shared skill body so Codex and Claude cannot silently diverge. Run the targeted projection test and expect PASS.

### Task 3: Register the existing hook handler with Claude

Files:
- Create .claude/settings.json

Register SessionStart, PreToolUse, PostToolUse, and Stop using \${CLAUDE_PROJECT_DIR}/.codex/hooks/return_zero_hook.py. Use Claude tool matchers Bash|Edit|Write and preserve existing timeouts and status messages. Run the new hook contract test plus the existing real hook tests.

### Task 4: Repair marketplace layout and documentation

Files:
- Create submission-package/.claude-plugin/marketplace.json
- Delete submission-package/epi-logos/.claude-plugin/marketplace.json
- Modify submission-package/epi-logos/README.md

Use source ./epi-logos. Tell users to add submission-package as the marketplace root, install the namespaced plugin, and use --plugin-dir for direct local testing. Validate both marketplace and plugin manifests with claude plugin validate.

### Task 5: Rewrite /mef-refract for Claude Agent subagents

Files:
- Modify submission-package/epi-logos/commands/mef-refract.md
- Delete submission-package/epi-logos/workflows/mef-refract.js

Replace Workflow-runtime instructions with explicit built-in Agent subagent dispatch. The parent session must send one fresh, blind lens prompt per lens, wait for all reports, and synthesize them itself. Preserve the lens roster, status gate, limits, topology handling, vetoes, and output contract. Remove the undocumented JS workflow artifact.

### Task 6: Run complete verification

Run:

    python3 -m unittest discover -s tests -v
    claude plugin validate submission-package/.claude-plugin/marketplace.json
    claude plugin validate submission-package/epi-logos/.claude-plugin/plugin.json
    git diff --check

Review the final diff for accidental canonical manuscript or source-house changes.
