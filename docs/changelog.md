# Claude Code Changelog

> **Source**: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
> 
> This is the official Claude Code release changelog, automatically fetched from the Claude Code repository. For documentation, see other topics via `/docs`.

---

# Changelog

## 2.1.51

- Added `claude remote-control` subcommand for external builds, enabling local environment serving for all users.
- Updated plugin marketplace default git timeout from 30s to 120s and added `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS` to configure.
- Added support for custom npm registries and specific version pinning when installing plugins from npm sources
- BashTool now skips login shell (`-l` flag) by default when a shell snapshot is available, improving command execution performance. Previously this required setting `CLAUDE_BASH_NO_LOGIN=true`.
- Fixed a security issue where `statusLine` and `fileSuggestion` hook commands could execute without workspace trust acceptance in interactive mode.
- Tool results larger than 50K characters are now persisted to disk (previously 100K). This reduces context window usage and improves conversation longevity.
- Fixed a bug where duplicate `control_response` messages (e.g. from WebSocket reconnects) could cause API 400 errors by pushing duplicate assistant messages into the conversation.
- Added `CLAUDE_CODE_ACCOUNT_UUID`, `CLAUDE_CODE_USER_EMAIL`, and `CLAUDE_CODE_ORGANIZATION_UUID` environment variables for SDK callers to provide account info synchronously, eliminating a race condition where early telemetry events lacked account metadata.
- Fixed slash command autocomplete crashing when a plugin's SKILL.md description is a YAML array or other non-string type
- The `/model` picker now shows human-readable labels (e.g., "Sonnet 4.5") instead of raw model IDs for pinned model versions, with an upgrade hint when a newer version is available.

## 2.1.50

- Added support for `startupTimeout` configuration for LSP servers
- Added `WorktreeCreate` and `WorktreeRemove` hook events, enabling custom VCS setup and teardown when agent worktree isolation creates or removes worktrees.
- Fixed a bug where resumed sessions could be invisible when the working directory involved symlinks, because the session storage path was resolved at different times during startup. Also fixed session data loss on SSH disconnect by flushing session data before hooks and analytics in the graceful shutdown sequence.
- Linux: Fixed native modules not loading on systems with glibc older than 2.30 (e.g., RHEL 8)
- Fixed memory leak in agent teams where completed teammate tasks were never garbage collected from session state
- Fixed `CLAUDE_CODE_SIMPLE` to fully strip down skills, session memory, custom agents, and CLAUDE.md token counting
- Fixed `/mcp reconnect` freezing the CLI when given a server name that doesn't exist
- Fixed memory leak where completed task state objects were never removed from AppState
- Added support for `isolation: worktree` in agent definitions, allowing agents to declaratively run in isolated git worktrees.
- `CLAUDE_CODE_SIMPLE` mode now also disables MCP tools, attachments, hooks, and CLAUDE.md file loading for a fully minimal experience.
- Fixed bug where MCP tools were not discovered when tool search is enabled and a prompt is passed in as a launch argument
- Improved memory usage during long sessions by clearing internal caches after compaction
- Added `claude agents` CLI command to list all configured agents
- Improved memory usage during long sessions by clearing large tool results after they have been processed
- Fixed a memory leak where LSP diagnostic data was never cleaned up after delivery, causing unbounded memory growth in long sessions
- Fixed a memory leak where completed task output was not freed from memory, reducing memory usage in long sessions with many tasks
- Improved startup performance for headless mode (`-p` flag) by deferring Yoga WASM and UI component imports
- Fixed prompt suggestion cache regression that reduced cache hit rates
- Fixed unbounded memory growth in long sessions by capping file history snapshots
- Added `CLAUDE_CODE_DISABLE_1M_CONTEXT` environment variable to disable 1M context window support
- Opus 4.6 (fast mode) now includes the full 1M context window
- VSCode: Added `/extra-usage` command support in VS Code sessions
- Fixed memory leak where TaskOutput retained recent lines after cleanup
- Fixed memory leak in CircularBuffer where cleared items were retained in the backing array
- Fixed memory leak in shell command execution where ChildProcess and AbortController references were retained after cleanup

## 2.1.49

- Improved MCP OAuth authentication with step-up auth support and discovery caching, reducing redundant network requests during server connections
- Added `--worktree` (`-w`) flag to start Claude in an isolated git worktree
- Subagents support `isolation: "worktree"` for working in a temporary git worktree
- Added Ctrl+F keybinding to kill background agents (two-press confirmation)
- Agent definitions support `background: true` to always run as a background task
- Plugins can ship `settings.json` for default configuration
- Fixed file-not-found errors to suggest corrected paths when the model drops the repo folder
- Fixed Ctrl+C and ESC being silently ignored when background agents are running and the main thread is idle. Pressing twice within 3 seconds now kills all background agents.
- Fixed prompt suggestion cache regression that reduced cache hit rates.
- Fixed `plugin enable` and `plugin disable` to auto-detect the correct scope when `--scope` is not specified, instead of always defaulting to user scope
- Simple mode (`CLAUDE_CODE_SIMPLE`) now includes the file edit tool in addition to the Bash tool, allowing direct file editing in simple mode.
- Permission suggestions are now populated when safety checks trigger an ask response, enabling SDK consumers to display permission options
- Sonnet 4.5 with 1M context is being removed from the Max plan in favor of our frontier Sonnet 4.6 model, which now has 1M context. Please switch in /model.
- Fixed verbose mode not updating thinking block display when toggled via `/config` — memo comparators now correctly detect verbose changes
- Fixed unbounded WASM memory growth during long sessions by periodically resetting the tree-sitter parser
- Fixed potential rendering issues caused by stale yoga layout references
- Improved performance in non-interactive mode (`-p`) by skipping unnecessary API calls during startup
- Improved performance by caching authentication failures for HTTP and SSE MCP servers, avoiding repeated connection attempts to servers requiring auth
- Fixed unbounded memory growth during long-running sessions caused by Yoga WASM linear memory never shrinking
- SDK model info now includes `supportsEffort`, `supportedEffortLevels`, and `supportsAdaptiveThinking` fields so consumers can discover model capabilities.
- Added `ConfigChange` hook event that fires when configuration files change during a session, enabling enterprise security auditing and optional blocking of settings changes.
- Improved startup performance by caching MCP auth failures to avoid redundant connection attempts
- Improved startup performance by reducing HTTP calls for analytics token counting
- Improved startup performance by batching MCP tool token counting into a single API call
- Fixed `disableAllHooks` setting to respect managed settings hierarchy — non-managed settings can no longer disable managed hooks set by policy (#26637)
- Fixed `--resume` session picker showing raw XML tags for sessions that start with commands like `/clear`. Now correctly falls through to the session ID fallback.
- Improved permission prompts for path safety and working directory blocks to show the reason for the restriction instead of a bare prompt with no context

## 2.1.47

- Fixed FileWriteTool line counting to preserve intentional trailing blank lines instead of stripping them with `trimEnd()`.
- Fixed Windows terminal rendering bugs caused by `os.EOL` (`\r\n`) in display code — line counts now show correct values instead of always showing 1 on Windows.
- Improved VS Code plan preview: auto-updates as Claude iterates, enables commenting only when the plan is ready for review, and keeps the preview open when rejecting so Claude can revise.
- Fixed a bug where bold and colored text in markdown output could shift to the wrong characters on Windows due to `\r\n` line endings.
- Fixed compaction failing when conversation contains many PDF documents by stripping document blocks alongside images before sending to the compaction API (anthropics/claude-code#26188)
- Improved memory usage in long-running sessions by releasing API stream buffers, agent context, and skill state after use
- Improved startup performance by deferring SessionStart hook execution, reducing time-to-interactive by ~500ms.
- Fixed an issue where bash tool output was silently discarded on Windows when using MSYS2 or Cygwin shells.
- Improved performance of `@` file mentions - file suggestions now appear faster by pre-warming the index on startup and using session-based caching with background refresh.
- Improved memory usage by trimming agent task message history after tasks complete
- Improved memory usage during long agent sessions by eliminating O(n²) message accumulation in progress updates
- Fixed the bash permission classifier to validate that returned match descriptions correspond to actual input rules, preventing hallucinated descriptions from incorrectly granting permissions
- Fixed user-defined agents only loading one file on NFS/FUSE filesystems that report zero inodes (anthropics/claude-code#26044)
- Fixed plugin agent skills silently failing to load when referenced by bare name instead of fully-qualified plugin name (anthropics/claude-code#25834)
- Search patterns in collapsed tool results are now displayed in quotes for clarity
- Windows: Fixed CWD tracking temp files never being cleaned up, causing them to accumulate indefinitely (anthropics/claude-code#17600)
- Use `ctrl+f` to kill all background agents instead of double-pressing ESC. Background agents now continue running when you press ESC to cancel the main thread, giving you more control over agent lifecycle.
- Fixed API 400 errors ("thinking blocks cannot be modified") that occurred in sessions with concurrent agents, caused by interleaved streaming content blocks preventing proper message merging.
- Simplified teammate navigation to use only Shift+Down (with wrapping) instead of both Shift+Up and Shift+Down.
- Fixed an issue where a single file write/edit error would abort all other parallel file write/edit operations. Independent file mutations now complete even when a sibling fails.
- Added `last_assistant_message` field to Stop and SubagentStop hook inputs, providing the final assistant response text so hooks can access it without parsing transcript files.
- Fixed custom session titles set via `/rename` being lost after resuming a conversation (anthropics/claude-code#23610)
- Fixed collapsed read/search hint text overflowing on narrow terminals by truncating from the start.
- Fixed an issue where bash commands with backslash-newline continuation lines (e.g., long commands split across multiple lines with `\`) would produce spurious empty arguments, potentially breaking command execution.
- Fixed built-in slash commands (`/help`, `/model`, `/compact`, etc.) being hidden from the autocomplete dropdown when many user skills are installed (anthropics/claude-code#22020)
- Fixed MCP servers not appearing in the MCP Management Dialog after deferred loading
- Fixed session name persisting in status bar after `/clear` command (anthropics/claude-code#26082)
- Fixed crash when a skill's `name` or `description` in SKILL.md frontmatter is a bare number (e.g., `name: 3000`) — the value is now properly coerced to a string (anthropics/claude-code#25837)
- Fixed /resume silently dropping sessions when the first message exceeds 16KB or uses array-format content (anthropics/claude-code#25721)
- Added `chat:newline` keybinding action for configurable multi-line input (anthropics/claude-code#26075)
- Added `added_dirs` to the statusline JSON `workspace` section, exposing directories added via `/add-dir` to external scripts (anthropics/claude-code#26096)
- Fixed `claude doctor` misclassifying mise and asdf-managed installations as native installs (anthropics/claude-code#26033)
- Fixed zsh heredoc failing with "read-only file system" error in sandboxed commands (anthropics/claude-code#25990)
- Fixed agent progress indicator showing inflated tool use count (anthropics/claude-code#26023)
- Fixed image pasting not working on WSL2 systems where Windows copies images as BMP format (anthropics/claude-code#25935)
- Fixed background agent results returning raw transcript data instead of the agent's final answer (anthropics/claude-code#26012)
- Fixed Warp terminal incorrectly prompting for Shift+Enter setup when it supports it natively (anthropics/claude-code#25957)
- Fixed CJK wide characters causing misaligned timestamps and layout elements in the TUI (anthropics/claude-code#26084)
- Fixed custom agent `model` field in `.claude/agents/*.md` being ignored when spawning team teammates (anthropics/claude-code#26064)
- Fixed plan mode being lost after context compaction, causing the model to switch from planning to implementation mode (anthropics/claude-code#26061)
- Fixed `alwaysThinkingEnabled: true` in settings.json not enabling thinking mode on Bedrock and Vertex providers (anthropics/claude-code#26074)
- Fixed `tool_decision` OTel telemetry event not being emitted in headless/SDK mode (anthropics/claude-code#26059)
- Fixed session name being lost after context compaction — renamed sessions now preserve their custom title through compaction (anthropics/claude-code#26121)
- Increased initial session count in resume picker from 10 to 50 for faster session discovery (anthropics/claude-code#26123)
- Windows: fixed worktree session matching when drive letter casing differs (anthropics/claude-code#26123)
- Fixed `/resume <session-id>` failing to find sessions whose first message exceeds 16KB (anthropics/claude-code#25920)
- Fixed "Always allow" on multiline bash commands creating invalid permission patterns that corrupt settings (anthropics/claude-code#25909)
- Fixed React crash (error #31) when a skill's `argument-hint` in SKILL.md frontmatter uses YAML sequence syntax (e.g., `[topic: foo | bar]`) — the value is now properly coerced to a string (anthropics/claude-code#25826)
- Fixed crash when using `/fork` on sessions that used web search — null entries in search results from transcript deserialization are now handled gracefully (anthropics/claude-code#25811)
- Fixed read-only git commands triggering FSEvents file watcher loops on macOS by adding --no-optional-locks flag (anthropics/claude-code#25750)
- Fixed custom agents and skills not being discovered when running from a git worktree — project-level `.claude/agents/` and `.claude/skills/` from the main repository are now included (anthropics/claude-code#25816)
- Fixed non-interactive subcommands like `claude doctor` and `claude plugin validate` being blocked inside nested Claude sessions (anthropics/claude-code#25803)
- Windows: Fixed the same CLAUDE.md file being loaded twice when drive letter casing differs between paths (anthropics/claude-code#25756)
- Fixed inline code spans in markdown being incorrectly parsed as bash commands (anthropics/claude-code#25792)
- Fixed teammate spinners not respecting custom spinnerVerbs from settings (anthropics/claude-code#25748)
- Fixed shell commands permanently failing after a command deletes its own working directory (anthropics/claude-code#26136)
- Fixed hooks (PreToolUse, PostToolUse) silently failing to execute on Windows by using Git Bash instead of cmd.exe (anthropics/claude-code#25981)
- Fixed LSP `findReferences` and other location-based operations returning results from gitignored files (e.g., `node_modules/`, `venv/`) (anthropics/claude-code#26051)
- Moved config backup files from home directory root to `~/.claude/backups/` to reduce home directory clutter (anthropics/claude-code#26130)
- Fixed sessions with large first prompts (>16KB) disappearing from the /resume list (anthropics/claude-code#26140)
- Fixed shell functions with double-underscore prefixes (e.g., `__git_ps1`) not being preserved across shell sessions (anthropics/claude-code#25824)
- Fixed spinner showing "0 tokens" counter before any tokens have been received (anthropics/claude-code#26105)
- VSCode: Fixed conversation messages appearing dimmed while the AskUserQuestion dialog is open (anthropics/claude-code#26078)
- Fixed background tasks failing in git worktrees due to remote URL resolution reading from worktree-specific gitdir instead of the main repository config (anthropics/claude-code#26065)
- Fixed Right Alt key leaving visible `[25~` escape sequence residue in the input field on Windows/Git Bash terminals (anthropics/claude-code#25943)
- The `/rename` command now updates the terminal tab title by default (anthropics/claude-code#25789)
- Fixed Edit tool silently corrupting Unicode curly quotes (\u201c\u201d \u2018\u2019) by replacing them with straight quotes when making edits (anthropics/claude-code#26141)
- Fixed OSC 8 hyperlinks only being clickable on the first line when link text wraps across multiple terminal lines.

## 2.1.46

- Fixed orphaned CC processes after terminal disconnect on macOS
- Added support for using claude.ai MCP connectors in Claude Code

## 2.1.45

- Added support for Claude Sonnet 4.6
- Added support for reading `enabledPlugins` and `extraKnownMarketplaces` from `--add-dir` directories
- Added `spinnerTipsOverride` setting to customize spinner tips — configure `tips` with an array of custom tip strings, and optionally set `excludeDefault: true` to show only your custom tips instead of the built-in ones
- Added `SDKRateLimitInfo` and `SDKRateLimitEvent` types to the SDK, enabling consumers to receive rate limit status updates including utilization, reset times, and overage information
- Fixed Agent Teams teammates failing on Bedrock, Vertex, and Foundry by propagating API provider environment variables to tmux-spawned processes (anthropics/claude-code#23561)
- Fixed sandbox "operation not permitted" errors when writing temporary files on macOS by using the correct per-user temp directory (anthropics/claude-code#21654)
- Fixed Task tool (backgrounded agents) crashing with a `ReferenceError` on completion (anthropics/claude-code#22087)
- Fixed autocomplete suggestions not being accepted on Enter when images are pasted in the input
- Fixed skills invoked by subagents incorrectly appearing in main session context after compaction
- Fixed excessive `.claude.json.backup` files accumulating on every startup
- Fixed plugin-provided commands, agents, and hooks not being available immediately after installation without requiring a restart
- Improved startup performance by removing eager loading of session history for stats caching
- Improved memory usage for shell commands that produce large output — RSS no longer grows unboundedly with command output size
- Improved collapsed read/search groups to show the current file or search pattern being processed beneath the summary line while active
- [VSCode] Improved permission destination choice (project/user/session) to persist across sessions

## 2.1.44

- Fixed ENAMETOOLONG errors for deeply-nested directory paths
- Fixed auth refresh errors

## 2.1.43

- Fixed AWS auth refresh hanging indefinitely by adding a 3-minute timeout
- Fixed spurious warnings for non-agent markdown files in `.claude/agents/` directory
- Fixed structured-outputs beta header being sent unconditionally on Vertex/Bedrock

## 2.1.42

- Improved startup performance by deferring Zod schema construction
- Improved prompt cache hit rates by moving date out of system prompt
- Added one-time Opus 4.6 effort callout for eligible users
- Fixed /resume showing interrupt messages as session titles
- Fixed image dimension limit errors to suggest /compact

## 2.1.41

- Added guard against launching Claude Code inside another Claude Code session
- Fixed Agent Teams using wrong model identifier for Bedrock, Vertex, and Foundry customers
- Fixed a crash when MCP tools return image content during streaming
- Fixed /resume session previews showing raw XML tags instead of readable command names
- Improved model error messages for Bedrock/Vertex/Foundry users with fallback suggestions
- Fixed plugin browse showing misleading "Space to Toggle" hint for already-installed plugins
- Fixed hook blocking errors (exit code 2) not showing stderr to the user
- Added `speed` attribute to OTel events and trace spans for fast mode visibility
- Added `claude auth login`, `claude auth status`, and `claude auth logout` CLI subcommands
- Added Windows ARM64 (win32-arm64) native binary support
- Improved `/rename` to auto-generate session name from conversation context when called without arguments
- Improved narrow terminal layout for prompt footer
- Fixed file resolution failing for @-mentions with anchor fragments (e.g., `@README.md#installation`)
- Fixed FileReadTool blocking the process on FIFOs, `/dev/stdin`, and large files
- Fixed background task notifications not being delivered in streaming Agent SDK mode
- Fixed cursor jumping to end on each keystroke in classifier rule input
- Fixed markdown link display text being dropped for raw URL
- Fixed auto-compact failure error notifications being shown to users
- Fixed permission wait time being included in subagent elapsed time display
- Fixed proactive ticks firing while in plan mode
- Fixed clear stale permission rules when settings change on disk
- Fixed hook blocking errors showing stderr content in UI

---

> Older versions omitted. Full changelog: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md