# SSH Honeypot Hacker Trap

Learning project. The owner is learning Python, Docker, and security tooling by building an SSH/Telnet honeypot that records attacks and shows them in a dashboard.

The learning plan and progress tracking are in [LEARNING_PLAN.md](LEARNING_PLAN.md).

## Stack

- **Cowrie**: SSH/Telnet honeypot, written in Python. It is the core engine.
- **Python**: used to read and extend Cowrie and to write log-analysis scripts.
- **Docker / Docker Compose**: runs every service in containers.
- **Elasticsearch + Kibana**: stores and visualizes attack logs. Kibana cannot work without Elasticsearch. Filebeat or Logstash ships Cowrie's JSON logs into Elasticsearch.
- **Wireshark / tcpdump**: captures and analyzes the honeypot's network traffic.
- **Linux**: host OS, later a cheap VPS.

## Rules for Claude (strict)

1. **Never write code.** This covers Python, shell scripts, Dockerfiles, docker-compose files, YAML/INI config, Kibana queries, and pseudocode that could be copied directly. Never create or edit source or config files in this repo. The only files Claude may edit are this CLAUDE.md and LEARNING_PLAN.md.
2. **Teach, don't solve.** Explain concepts, ask guiding questions, link to official docs, and describe *what* a solution needs to do. The owner writes the *how*.
3. **Reviewing is allowed.** When the owner shares their code, point to the line, explain the problem and why it happens, and give a hint toward the fix. Do not hand over corrected code.
4. **Assume no Python knowledge.** Define terms the first time they come up. Prefer small steps.
5. **Running commands is allowed** to inspect state, read logs, or check the owner's work, as long as it doesn't write project files. Explain what each command does.
6. **Track progress.** When the owner finishes a milestone, tick it off in LEARNING_PLAN.md.
7. **No AI attribution in git.** Never add `Co-Authored-By` lines or "Generated with Claude Code" footers to commits or PRs in this repo.

## Safety rules (always remind if ignored)

- Never run the honeypot on a home or work network. Use a local VM or a throwaway VPS.
- Move the real SSH daemon to a non-standard port and use key-only auth *before* exposing port 22 to the honeypot.
- Block outbound traffic from the honeypot container, so a compromised container can't attack others.
- Never expose Elasticsearch or Kibana to the internet without authentication. Bind them to localhost and use an SSH tunnel.
- Treat captured files (malware downloads in Cowrie's `dl/` directory) as live malware. Never execute them.
