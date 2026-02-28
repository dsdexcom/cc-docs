# Claude Code Changelog

> **Source**: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
> 
> This is the official Claude Code release changelog, automatically fetched from the Claude Code repository. For documentation, see other topics via `/docs`.

---

# Changelog

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

---

> Older versions omitted. Full changelog: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md