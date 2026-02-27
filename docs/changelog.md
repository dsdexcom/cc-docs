# Claude Code Changelog

> **Source**: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
> 
> This is the official Claude Code release changelog, automatically fetched from the Claude Code repository. For documentation, see other topics via `/docs`.

---

# Changelog

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

## 2.1.56

- VS Code: Fixed another cause of "command 'claude-vscode.editor.openLast' not found" crashes

## 2.1.55

- Fixed BashTool failing on Windows with EINVAL error

## 2.1.53

- Fixed a UI flicker where user input would briefly disappear after submission before the message rendered
- Fixed bulk agent kill (ctrl+f) to send a single aggregate notification instead of one per agent, and to properly clear the command queue
- Fixed graceful shutdown sometimes leaving stale sessions when using Remote Control by parallelizing teardown network calls
- Fixed `--worktree` sometimes being ignored on first launch
- Fixed a panic ("switch on corrupted value") on Windows
- Fixed a crash that could occur when spawning many processes on Windows
- Fixed a crash in the WebAssembly interpreter on Linux x64 & Windows x64
- Fixed a crash that sometimes occurred after 2 minutes on Windows ARM64

## 2.1.52

- VS Code: Fixed extension crash on Windows ("command 'claude-vscode.editor.openLast' not found")

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
- Managed settings can now be set via macOS plist or Windows Registry. Learn more at https://code.claude.com/docs/en/settings#settings-files

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

---

> Older versions omitted. Full changelog: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md