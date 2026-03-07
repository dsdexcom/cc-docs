# Claude Code Changelog

> **Source**: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
> 
> This is the official Claude Code release changelog, automatically fetched from the Claude Code repository. For documentation, see other topics via `/docs`.

---

# Changelog

## 2.1.71

- Added `/loop` command to run a prompt or slash command on a recurring interval (e.g. `/loop 5m check the deploy`)
- Added cron scheduling tools for recurring prompts within a session
- Added `voice:pushToTalk` keybinding to make the voice activation key rebindable in `keybindings.json` (default: space) — modifier+letter combos like `meta+k` have zero typing interference
- Added `fmt`, `comm`, `cmp`, `numfmt`, `expr`, `test`, `printf`, `getconf`, `seq`, `tsort`, and `pr` to the bash auto-approval allowlist
- Fixed stdin freeze in long-running sessions where keystrokes stop being processed but the process stays alive
- Fixed a 5–8 second startup freeze for users with voice mode enabled, caused by CoreAudio initialization blocking the main thread after system wake
- Fixed startup UI freeze when many claude.ai proxy connectors refresh an expired OAuth token simultaneously
- Fixed forked conversations (`/fork`) sharing the same plan file, which caused plan edits in one fork to overwrite the other
- Fixed the Read tool putting oversized images into context when image processing failed, breaking subsequent turns in long image-heavy sessions
- Fixed false-positive permission prompts for compound bash commands containing heredoc commit messages
- Fixed plugin installations being lost when running multiple Claude Code instances
- Fixed claude.ai connectors failing to reconnect after OAuth token refresh
- Fixed claude.ai MCP connector startup notifications appearing for every org-configured connector instead of only previously connected ones
- Fixed background agent completion notifications missing the output file path, which made it difficult for parent agents to recover agent results after context compaction
- Fixed duplicate output in Bash tool error messages when commands exit with non-zero status
- Fixed Chrome extension auto-detection getting permanently stuck on "not installed" after running on a machine without local Chrome
- Fixed `/plugin marketplace update` failing with merge conflicts when the marketplace is pinned to a branch/tag ref
- Fixed `/plugin marketplace add owner/repo@ref` incorrectly parsing `@` — previously only `#` worked as a ref separator, causing undiagnosable errors with `strictKnownMarketplaces`
- Fixed duplicate entries in `/permissions` Workspace tab when the same directory is added with and without a trailing slash
- Fixed `--print` hanging forever when team agents are configured — the exit loop no longer waits on long-lived `in_process_teammate` tasks
- Fixed "❯ Tool loaded." appearing in the REPL after every `ToolSearch` call
- Fixed prompting for `cd <cwd> && git ...` on Windows when the model uses a mingw-style path
- Improved startup time by deferring native image processor loading to first use
- Improved bridge session reconnection to complete within seconds after laptop wake from sleep, instead of waiting up to 10 minutes
- Improved `/plugin uninstall` to disable project-scoped plugins in `.claude/settings.local.json` instead of modifying `.claude/settings.json`, so changes don't affect teammates
- Improved plugin-provided MCP server deduplication — servers that duplicate a manually-configured server (same command/URL) are now skipped, preventing duplicate connections and tool sets. Suppressions are shown in the `/plugin` menu.
- Updated `/debug` to toggle debug logging on mid-session, since debug logs are no longer written by default
- Removed startup notification noise for unauthenticated org-registered claude.ai connectors

## 2.1.70

- Fixed API 400 errors when using `ANTHROPIC_BASE_URL` with a third-party gateway — tool search now correctly detects proxy endpoints and disables `tool_reference` blocks
- Fixed `API Error: 400 This model does not support the effort parameter` when using custom Bedrock inference profiles or other model identifiers not matching standard Claude naming patterns
- Fixed empty model responses immediately after `ToolSearch` — the server renders tool schemas with system-prompt-style tags at the prompt tail, which could confuse models into stopping early
- Fixed prompt-cache bust when an MCP server with `instructions` connects after the first turn
- Fixed Enter inserting a newline instead of submitting when typing over a slow SSH connection
- Fixed clipboard corrupting non-ASCII text (CJK, emoji) on Windows/WSL by using PowerShell `Set-Clipboard`
- Fixed extra VS Code windows opening at startup on Windows when running from the VS Code integrated terminal
- Fixed voice mode failing on Windows native binary with "native audio module could not be loaded"
- Fixed push-to-talk not activating on session start when `voiceEnabled: true` was set in settings
- Fixed markdown links containing `#NNN` references incorrectly pointing to the current repository instead of the linked URL
- Fixed repeated "Model updated to Opus 4.6" notification when a project's `.claude/settings.json` has a legacy Opus model string pinned
- Fixed plugins showing as inaccurately installed in `/plugin`
- Fixed plugins showing "not found in marketplace" errors on fresh startup by auto-refreshing after marketplace installation
- Fixed `/security-review` command failing with `unknown option merge-base` on older git versions
- Fixed `/color` command having no way to reset back to the default color — `/color default`, `/color gray`, `/color reset`, and `/color none` now restore the default
- Fixed a performance regression in the `AskUserQuestion` preview dialog that re-ran markdown rendering on every keystroke in the notes input
- Fixed feature flags read during early startup never refreshing their disk cache, causing stale values to persist across sessions
- Fixed `permissions.defaultMode` settings values other than `acceptEdits` or `plan` being applied in Claude Code Remote environments — they are now ignored
- Fixed skill listing being re-injected on every `--resume` (~600 tokens saved per resume)
- Fixed teleport marker not rendering in VS Code teleported sessions
- Improved error message when microphone captures silence to distinguish from "no speech detected"
- Improved compaction to preserve images in the summarizer request, allowing prompt cache reuse for faster and cheaper compaction
- Improved `/rename` to work while Claude is processing, instead of being silently queued
- Reduced prompt input re-renders during turns by ~74%
- Reduced startup memory by ~426KB for users without custom CA certificates
- Reduced Remote Control `/poll` rate to once per 10 minutes while connected (was 1–2s), cutting server load ~300×. Reconnection is unaffected — transport loss immediately wakes fast polling.
- [VSCode] Added spark icon in VS Code activity bar that lists all Claude Code sessions, with sessions opening as full editors
- [VSCode] Added full markdown document view for plans in VS Code, with support for adding comments to provide feedback
- [VSCode] Added native MCP server management dialog — use `/mcp` in the chat panel to enable/disable servers, reconnect, and manage OAuth authentication without switching to the terminal

## 2.1.69

- Added the `/claude-api` skill for building applications with the Claude API and Anthropic SDK
- Added Ctrl+U on an empty bash prompt (`!`) to exit bash mode, matching `escape` and `backspace`
- Added numeric keypad support for selecting options in Claude's interview questions (previously only the number row above QWERTY worked)
- Added optional name argument to `/remote-control` and `claude remote-control` (`/remote-control My Project` or `--name "My Project"`) to set a custom session title visible in claude.ai/code
- Added Voice STT support for 10 new languages (20 total) — Russian, Polish, Turkish, Dutch, Ukrainian, Greek, Czech, Danish, Swedish, Norwegian
- Added effort level display (e.g., "with low effort") to the logo and spinner, making it easier to see which effort setting is active
- Added agent name display in terminal title when using `claude --agent`
- Added `sandbox.enableWeakerNetworkIsolation` setting (macOS only) to allow Go programs like `gh`, `gcloud`, and `terraform` to verify TLS certificates when using a custom MITM proxy with `httpProxyPort`
- Added `includeGitInstructions` setting (and `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` env var) to remove built-in commit and PR workflow instructions from Claude's system prompt
- Added `/reload-plugins` command to activate pending plugin changes without restarting
- Added a one-time startup prompt suggesting Claude Code Desktop on macOS and Windows (max 3 showings, dismissible)
- Added `${CLAUDE_SKILL_DIR}` variable for skills to reference their own directory in SKILL.md content
- Added `InstructionsLoaded` hook event that fires when CLAUDE.md or `.claude/rules/*.md` files are loaded into context
- Added `agent_id` (for subagents) and `agent_type` (for subagents and `--agent`) to hook events
- Added `worktree` field to status line hook commands with name, path, branch, and original repo directory when running in a `--worktree` session
- Added `pluginTrustMessage` in managed settings to append organization-specific context to the plugin trust warning shown before installation
- Added policy limit fetching (e.g., remote control restrictions) for Team plan OAuth users, not just Enterprise
- Added `pathPattern` to `strictKnownMarketplaces` for regex-matching file/directory marketplace sources alongside `hostPattern` restrictions
- Added plugin source type `git-subdir` to point to a subdirectory within a git repo
- Added `oauth.authServerMetadataUrl` config option for MCP servers to specify a custom OAuth metadata discovery URL when standard discovery fails
- Fixed a security issue where nested skill discovery could load skills from gitignored directories like `node_modules`
- Fixed trust dialog silently enabling all `.mcp.json` servers on first run. You'll now see the per-server approval dialog as expected
- Fixed `claude remote-control` crashing immediately on npm installs with "bad option: --sdk-url" (anthropics/claude-code#28334)
- Fixed `--model claude-opus-4-0` and `--model claude-opus-4-1` resolving to deprecated Opus versions instead of current
- Fixed macOS keychain corruption when using multiple OAuth MCP servers. Large OAuth metadata blobs could overflow the `security -i` stdin buffer, silently leaving stale credentials behind and causing repeated `/login` prompts.
- Fixed `.credentials.json` losing `subscriptionType` (showing "Claude API" instead of "Claude Pro"/"Claude Max") when the profile endpoint transiently fails during token refresh (anthropics/claude-code#30185)
- Fixed ghost dotfiles (`.bashrc`, `HEAD`, etc.) appearing as untracked files in the working directory after sandboxed Bash commands on Linux
- Fixed Shift+Enter printing `[27;2;13~` instead of inserting a newline in Ghostty over SSH
- Fixed stash (Ctrl+S) being cleared when submitting a message while Claude is working
- Fixed ctrl+o (transcript toggle) freezing for many seconds in long sessions with lots of file edits
- Fixed plan mode feedback input not supporting multi-line text entry (backslash+Enter and Shift+Enter now insert newlines)
- Fixed cursor not moving down into blank lines at the top of the input box
- Fixed `/stats` crash when transcript files contain entries with missing or malformed timestamps
- Fixed a brief hang after a streaming error on long sessions (the transcript was being fully rewritten to drop one line; it is now truncated in place)
- Fixed `--setting-sources user` not blocking dynamically discovered project skills
- Fixed duplicate CLAUDE.md, slash commands, agents, and rules when running from a worktree nested inside its main repo (e.g. `claude -w`)
- Fixed plugin Stop/SessionEnd/etc hooks not firing after any `/plugin` operation
- Fixed plugin hooks being silently dropped when two plugins use the same `${CLAUDE_PLUGIN_ROOT}/...` command template
- Fixed memory leak in long-running SDK/CCR sessions where conversation messages were retained unnecessarily
- Fixed API 400 errors in forked agents (autocompact, summarization) when resuming sessions that were interrupted mid-tool-batch
- Fixed "unexpected tool_use_id found in tool_result blocks" error when resuming conversations that start with an orphaned tool result
- Fixed teammates accidentally spawning nested teammates via the Agent tool's `name` parameter
- Fixed `CLAUDE_CODE_MAX_OUTPUT_TOKENS` being ignored during conversation compaction
- Fixed `/compact` summary rendering as a user bubble in SDK consumers (Claude Code Remote web UI, VSCode extension)
- Fixed voice space bar getting stuck after a failed voice activation (module loading race, cold GrowthBook)
- Fixed worktree file copy on Windows
- Fixed global `.claude` folder detection on Windows
- Fixed symlink bypass where writing new files through a symlinked parent directory could escape the working directory in `acceptEdits` mode
- Fixed sandbox prompting users to approve non-allowed domains when `allowManagedDomainsOnly` is enabled in managed settings — non-allowed domains are now blocked automatically with no bypass
- Fixed interactive tools (e.g., `AskUserQuestion`) being silently auto-allowed when listed in a skill's allowed-tools, bypassing the permission prompt and running with empty answers
- Fixed multi-GB memory spike when committing with large untracked binary files in the working tree
- Fixed Escape not interrupting a running turn when the input box has draft text. Use Up arrow to pull queued messages back for editing, or Ctrl+U to clear the input line.
- Fixed Android app crash when running local slash commands (`/voice`, `/cost`) in Remote Control sessions
- Fixed a memory leak where old message array versions accumulated in React Compiler `memoCache` over long sessions
- Fixed a memory leak where REPL render scopes accumulated over long sessions (~35MB over 1000 turns)
- Fixed memory retention in in-process teammates where the parent's full conversation history was pinned for the teammate's lifetime, preventing GC after `/clear` or auto-compact
- Fixed a memory leak in interactive mode where hook events could accumulate unboundedly during long sessions
- Fixed hang when `--mcp-config` points to a corrupted file
- Fixed slow startup when many skills/plugins are installed
- Fixed `cd <outside-dir> && <cmd>` permission prompt to surface the chained command instead of only showing "Yes, allow reading from <dir>/"
- Fixed conditional `.claude/rules/*.md` files (with `paths:` frontmatter) and nested CLAUDE.md files not loading in print mode (`claude -p`)
- Fixed `/clear` not fully clearing all session caches, reducing memory retention in long sessions
- Fixed terminal flicker caused by animated elements at the scrollback boundary
- Fixed UI frame drops on macOS when using MCP servers with OAuth (regression from 2.1.x)
- Fixed occasional frame stalls during typing caused by synchronous debug log flushes
- Fixed `TeammateIdle` and `TaskCompleted` hooks to support `{"continue": false, "stopReason": "..."}` to stop the teammate, matching `Stop` hook behavior
- Fixed `WorktreeCreate` and `WorktreeRemove` plugin hooks being silently ignored
- Fixed skill descriptions with colons (e.g., "Triggers include: X, Y, Z") failing to load from SKILL.md frontmatter
- Fixed project skills without a `description:` frontmatter field not appearing in Claude's available skills list
- Fixed `/context` showing identical token counts for all MCP tools from a server
- Fixed literal `nul` file creation on Windows when the model uses CMD-style `2>nul` redirection in Git Bash
- Fixed extra blank lines appearing below each tool call in the expanded subagent transcript view (Ctrl+O)
- Fixed Tab/arrow keys not cycling Settings tabs when `/config` search box is focused but empty
- Fixed service key OAuth sessions (CCR containers) spamming `[ERROR]` logs with 403s from profile-scoped endpoints
- Fixed inconsistent color for "Remote Control active" status indicator
- Fixed Voice waveform cursor covering the first suffix letter when dictating mid-input
- Fixed Voice input showing all 5 spaces during warmup instead of capping at ~2 (aligning with the "keep holding…" hint)
- Improved spinner performance by isolating the 50ms animation loop from the surrounding shell, reducing render and CPU overhead during turns
- Improved UI rendering performance in native binaries with React Compiler
- Improved `--worktree` startup by eliminating a git subprocess on the startup path
- Improved macOS startup by eliminating redundant settings-file reloads when managed settings resolve
- Improved macOS startup for Claude.ai enterprise/team users by skipping an unnecessary keychain lookup
- Improved MCP `-p` startup by pipelining claude.ai config fetch with local connections and using a concurrency pool instead of sequential batching
- Improved voice startup by removing imperceptible warmup pulse animations that were causing re-render stutter
- Improved MCP binary content handling: tools returning PDFs, Office documents, or audio now save decoded bytes to disk with the correct file extension instead of dumping raw base64 into the conversation context. WebFetch also saves binary responses alongside its summary.
- Improved memory usage in long sessions by stabilizing `onSubmit` across message updates
- Improved LSP tool rendering and memory context building to no longer read entire files
- Improved session upload and memory sync to avoid reading large files into memory before size/binary checks
- Improved file operation performance by avoiding reading file contents for existence checks (6 sites)
- Improved documentation to clarify that `--append-system-prompt-file` and `--system-prompt-file` work in interactive mode (the docs previously said print mode only)
- Reduced baseline memory by ~16MB by deferring Yoga WASM preloading
- Reduced memory footprint for SDK and CCR sessions using stream-json output
- Reduced memory usage when resuming large sessions (including compacted history)
- Reduced token usage on multi-agent tasks with more concise subagent final reports
- Changed Sonnet 4.5 users on Pro/Max/Team Premium to be automatically migrated to Sonnet 4.6
- Changed the `/resume` picker to show your most recent prompt instead of the first one. This also resolves some titles appearing as `(session)`.
- Changed claude.ai MCP connector failures to show a notification instead of silently disappearing from the tool list
- Changed example command suggestions to be generated deterministically instead of calling Haiku
- Changed resuming after compaction to no longer produce a preamble recap before continuing
- [SDK] Changed task creation to no longer require the `activeForm` field — the spinner falls back to the task subject
- [VSCode] Added compaction display as a collapsible "Compacted chat" card with the summary inside
- [VSCode] The permission mode picker now respects `permissions.disableBypassPermissionsMode` from your effective Claude Code settings (including managed/policy settings) — when set to `disable`, bypass permissions mode is hidden from the picker
- [VSCode] Fixed RTL text (Arabic, Hebrew, Persian) rendering reversed in the chat panel (regression in v2.1.63)

## 2.1.68

- Opus 4.6 now defaults to medium effort for Max and Team subscribers. Medium effort works well for most tasks — it's the sweet spot between speed and thoroughness. You can change this anytime with `/model`
- Re-introduced the "ultrathink" keyword to enable high effort for the next turn
- Removed Opus 4 and 4.1 from Claude Code on the first-party API — users with these models pinned are automatically moved to Opus 4.6

## 2.1.66

- Reduced spurious error logging

## 2.1.63

- Added `/simplify` and `/batch` bundled slash commands
- Fixed local slash command output like /cost appearing as user-sent messages instead of system messages in the UI
- Project configs & auto memory now shared across git worktrees of the same repository
- Added `ENABLE_CLAUDEAI_MCP_SERVERS=false` env var to opt out from making claude.ai MCP servers available
- Improved `/model` command to show the currently active model in the slash command menu
- Added HTTP hooks, which can POST JSON to a URL and receive JSON instead of running a shell command
- Fixed listener leak in bridge polling loop
- Fixed listener leak in MCP OAuth flow cleanup
- Added manual URL paste fallback during MCP OAuth authentication. If the automatic localhost redirect doesn't work, you can paste the callback URL to complete authentication.
- Fixed memory leak when navigating hooks configuration menu
- Fixed listener leak in interactive permission handler during auto-approvals
- Fixed file count cache ignoring glob ignore patterns
- Fixed memory leak in bash command prefix cache
- Fixed MCP tool/resource cache leak on server reconnect
- Fixed IDE host IP detection cache incorrectly sharing results across ports
- Fixed WebSocket listener leak on transport reconnect
- Fixed memory leak in git root detection cache that could cause unbounded growth in long-running sessions
- Fixed memory leak in JSON parsing cache that grew unbounded over long sessions
- VSCode: Fixed remote sessions not appearing in conversation history
- Fixed a race condition in the REPL bridge where new messages could arrive at the server interleaved with historical messages during the initial connection flush, causing message ordering issues.
- Fixed memory leak where long-running teammates retained all messages in AppState even after conversation compaction
- Fixed a memory leak where MCP server fetch caches were not cleared on disconnect, causing growing memory usage with servers that reconnect frequently
- Improved memory usage in long sessions with subagents by stripping heavy progress message payloads during context compaction
- Added "Always copy full response" option to the `/copy` picker. When selected, future `/copy` commands will skip the code block picker and copy the full response directly.
- VSCode: Added session rename and remove actions to the sessions list
- Fixed `/clear` not resetting cached skills, which could cause stale skill content to persist in the new conversation

## 2.1.62

- Fixed prompt suggestion cache regression that reduced cache hit rates

## 2.1.61

- Fixed concurrent writes corrupting config file on Windows

## 2.1.59

- Claude automatically saves useful context to auto-memory. Manage with /memory
- Added `/copy` command to show an interactive picker when code blocks are present, allowing selection of individual code blocks or the full response.
- Improved "always allow" prefix suggestions for compound bash commands (e.g. `cd /tmp && git fetch && git push`) to compute smarter per-subcommand prefixes instead of treating the whole command as one
- Improved ordering of short task lists
- Improved memory usage in multi-agent sessions by releasing completed subagent task state
- Fixed MCP OAuth token refresh race condition when running multiple Claude Code instances simultaneously
- Fixed shell commands not showing a clear error message when the working directory has been deleted
- Fixed config file corruption that could wipe authentication when multiple Claude Code instances ran simultaneously

## 2.1.58

- Expand Remote Control to more users

---

> Older versions omitted. Full changelog: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md