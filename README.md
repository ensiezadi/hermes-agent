<p align="center">
  <img src="assets/banner.png" alt="Hermes Agent" width="100%">
</p>

# Hermes Agent ☤

<p align="center">
  <a href="https://hermes-agent.nousresearch.com/docs/"><img src="https://img.shields.io/badge/Docs-hermes--agent.nousresearch.com-FFD700?style=for-the-badge" alt="Documentation"></a>
  <a href="https://discord.gg/NousResearch"><img src="https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord"></a>
  <a href="https://github.com/NousResearch/hermes-agent/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License: MIT"></a>
  <a href="https://nousresearch.com"><img src="https://img.shields.io/badge/Built%20by-Nous%20Research-blueviolet?style=for-the-badge" alt="Built by Nous Research"></a>
  <a href="README.zh-CN.md"><img src="https://img.shields.io/badge/Lang-中文-red?style=for-the-badge" alt="中文"></a>
</p>

**The self-improving AI agent built by [Nous Research](https://nousresearch.com).** It is the only intelligent agent with a built-in learning loop—creating skills from experience, improving them during use, proactively persisting knowledge, searching past conversations, and gradually building a deep understanding of you across sessions. It can run on a $5 VPS, on a GPU cluster, or using Serverless infrastructure at almost zero cost. It is not tied to your laptop—you can talk to it on Telegram while it works on a cloud VM.

Supports any model—[Nous Portal](https://portal.nousresearch.com), [OpenRouter](https://openrouter.ai) (200+ models), [NVIDIA NIM](https://build.nvidia.com) (Nemotron), [Xiaomi MiMo](https://platform.xiaomimimo.com), [z.ai/GLM](https://z.ai), [Kimi/Moonshot](https://platform.moonshot.ai), [MiniMax](https://www.minimax.io), [Hugging Face](https://huggingface.co), OpenAI, or custom endpoints. Use `hermes model` to switch—no code changes, no lock-in.

<table>
<tr><td><b>True Terminal UI</b></td><td>Full TUI with multi-line editing, slash command auto-completion, conversation history, interrupt redirection, and streaming tool outputs.</td></tr>
<tr><td><b>Wherever you are</b></td><td>Telegram, Discord, Slack, WhatsApp, Signal, and CLI—all running from a single gateway process. Voice memo transcription and cross-platform conversation continuity.</td></tr>
<tr><td><b>Closed-Loop Learning</b></td><td>The agent manages memory and periodically reminds itself. Auto-creates skills after complex tasks. Skills self-improve in use. FTS5 session search paired with LLM summarization for cross-session recall. <a href="https://github.com/plastic-labs/honcho">Honcho</a> dialectic user modeling. Compatible with the <a href="https://agentskills.io">agentskills.io</a> open standard.</td></tr>
<tr><td><b>Scheduled Automation</b></td><td>Built-in cron scheduler, supporting delivery to any platform. Daily reports, nightly backups, weekly audits—all described in natural language and running unattended.</td></tr>
<tr><td><b>Delegation & Parallelism</b></td><td>Spawn isolated subagents to handle parallel workflows. Write Python scripts to call tools via RPC, compressing multi-step pipelines into zero-context-overhead turns.</td></tr>
<tr><td><b>Run Anywhere</b></td><td>Six terminal backends—Local, Docker, SSH, Daytona, Singularity, and Modal. Daytona and Modal offer Serverless persistence—the agent environment sleeps when idle, wakes on demand, with near zero cost during idle time. Runs on a $5 VPS or a GPU cluster.</td></tr>
<tr><td><b>Research Ready</b></td><td>Batch trajectory generation and trajectory compression—for training next-generation tool-calling models.</td></tr>
</table>

---

## Quick Install

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

Supports Linux, macOS, WSL2, and Android (Termux). The installer automatically handles platform-specific configuration.

> **Android / Termux:** For tested manual installation paths, please refer to the [Termux Guide](https://hermes-agent.nousresearch.com/docs/getting-started/termux). On Termux, Hermes installs a curated `.[termux]` extra, because the full `.[all]` extra pulls in Android-incompatible voice dependencies.
>
> **Windows:** Native Windows is not supported. Please install [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) and run the command above.

After installation:

```bash
source ~/.bashrc    # Reload shell (or: source ~/.zshrc)
hermes              # Start chatting!
```

---

## Quick Start

```bash
hermes              # Interactive CLI — start a conversation
hermes model        # Select LLM provider and model
hermes tools        # Configure enabled tools
hermes config set   # Set a single configuration item
hermes gateway      # Start the messaging gateway (Telegram, Discord, etc.)
hermes setup        # Run the full setup wizard (configure everything at once)
hermes claw migrate # Migrate from OpenClaw (if coming from OpenClaw)
hermes update       # Update to the latest version
hermes doctor       # Diagnose issues
```

📖 **[Full Documentation →](https://hermes-agent.nousresearch.com/docs/)**

## CLI vs Messaging Platforms Quick Reference

Hermes has two entry points: launch the terminal UI with `hermes`, or run the gateway to chat with it from Telegram, Discord, Slack, WhatsApp, Signal, or Email. Once in a conversation, many slash commands are shared across both interfaces.

| Action                  | CLI                                           | Messaging Platforms                                                      |
| ----------------------- | --------------------------------------------- | ------------------------------------------------------------------------ |
| Start a conversation    | `hermes`                                      | Run `hermes gateway setup` + `hermes gateway start`, then message the bot|
| Start a new conversation| `/new` or `/reset`                            | `/new` or `/reset`                                                       |
| Change model            | `/model [provider:model]`                     | `/model [provider:model]`                                                |
| Set personality         | `/personality [name]`                         | `/personality [name]`                                                    |
| Retry or undo last turn | `/retry`, `/undo`                             | `/retry`, `/undo`                                                        |
| Compress context / usage| `/compress`, `/usage`, `/insights [--days N]` | `/compress`, `/usage`, `/insights [days]`                                |
| Browse skills           | `/skills` or `/<skill-name>`                  | `/skills` or `/<skill-name>`                                             |
| Interrupt current work  | `Ctrl+C` or send a new message                | `/stop` or send a new message                                            |
| Platform-specific status| `/platforms`                                  | `/status`, `/sethome`                                                    |

For the full list of commands, please see the [CLI Guide](https://hermes-agent.nousresearch.com/docs/user-guide/cli) and the [Messaging Gateway Guide](https://hermes-agent.nousresearch.com/docs/user-guide/messaging).

---

## Documentation

All documentation is located at **[hermes-agent.nousresearch.com/docs](https://hermes-agent.nousresearch.com/docs/)**:

| Section                                                                                    | Content                                                    |
| ------------------------------------------------------------------------------------------ | ---------------------------------------------------------- |
| [Quickstart](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart)        | Install → Setup → Start your first conversation in 2 mins  |
| [CLI Usage](https://hermes-agent.nousresearch.com/docs/user-guide/cli)                     | Commands, shortcuts, personalities, sessions               |
| [Configuration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration)       | Config files, providers, models, all options               |
| [Messaging Gateway](https://hermes-agent.nousresearch.com/docs/user-guide/messaging)       | Telegram, Discord, Slack, WhatsApp, Signal, Home Assistant |
| [Security](https://hermes-agent.nousresearch.com/docs/user-guide/security)                 | Command approval, DM pairing, container isolation          |
| [Tools & Toolsets](https://hermes-agent.nousresearch.com/docs/user-guide/features/tools)   | 40+ tools, toolset system, terminal backends               |
| [Skill System](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)      | Procedural memory, skills hub, creating skills             |
| [Memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory)            | Persistent memory, user profiles, best practices           |
| [MCP Integration](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp)      | Connect any MCP server (e.g. MiniMax Token Plan) to expand |
| [Image Generation](https://hermes-agent.nousresearch.com/docs/user-guide/features/image)   | Native integration with MiniMax and FAL.ai                 |
| [Cron Scheduling](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron)     | Scheduled tasks and platform delivery                      |
| [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)| Project context that influences every conversation         |
| [Architecture](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture)    | Project structure, agent loop, key classes                 |
| [Contributing](https://hermes-agent.nousresearch.com/docs/developer-guide/contributing)    | Dev setup, PR process, coding style                        |
| [CLI Reference](https://hermes-agent.nousresearch.com/docs/reference/cli-commands)         | All commands and flags                                     |
| [Environment Variables](https://hermes-agent.nousresearch.com/docs/reference/environment-variables)| Full environment variable reference                  |

---

## Migrating from OpenClaw

If you are coming from OpenClaw, Hermes can automatically import your settings, memories, skills, and API keys.

**During first install:** The setup wizard (`hermes setup`) will automatically detect `~/.openclaw` and offer migration options before configuration begins.

**Anytime after install:**

```bash
hermes claw migrate              # Interactive migration (full preset)
hermes claw migrate --dry-run    # Preview what will be migrated
hermes claw migrate --preset user-data   # Only migrate user data, no keys
hermes claw migrate --overwrite  # Overwrite existing conflicts
```

What is imported:

- **SOUL.md** — Personality profile
- **Memories** — MEMORY.md and USER.md entries
- **Skills** — User-created skills → `~/.hermes/skills/openclaw-imports/`
- **Command Whitelist** — Approval mode
- **Messaging Settings** — Platform config, allowed users, working directory
- **API Keys** — Whitelisted keys (Telegram, OpenRouter, OpenAI, Anthropic, ElevenLabs)
- **TTS Assets** — Workspace audio files
- **Workspace Instructions** — AGENTS.md (using `--workspace-target`)

Use `hermes claw migrate --help` to see all options, or use the `openclaw-migration` skill for interactive agent-guided migration (including a dry-run preview).

---

## Contributing

Contributions are welcome! Please refer to the [Contributing Guide](https://hermes-agent.nousresearch.com/docs/developer-guide/contributing) for development setup, coding style, and the PR process.

Contributor quick start—clone and use `setup-hermes.sh`:

```bash
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent
./setup-hermes.sh     # Installs uv, creates venv, installs .[all], symlinks ~/.local/bin/hermes
./hermes              # Auto-detects venv, no need to source first
```

Manual install (equivalent to above):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv venv --python 3.11
source venv/bin/activate
uv pip install -e ".[all,dev]"
python -m pytest tests/ -q
```

---

## Community

- 💬 [Discord](https://discord.gg/NousResearch)
- 📚 [Skills Hub](https://agentskills.io)
- 🐛 [Issue Tracker](https://github.com/NousResearch/hermes-agent/issues)
- 💡 [Discussions](https://github.com/NousResearch/hermes-agent/discussions)
- 🔌 [HermesClaw](https://github.com/AaronWong1999/hermesclaw) — Community WeChat bridge: Run Hermes Agent and OpenClaw on the same WeChat account.

---

## License

MIT — see [LICENSE](LICENSE) for details.

Built by [Nous Research](https://nousresearch.com).
