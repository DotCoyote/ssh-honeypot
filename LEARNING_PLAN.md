# Learning Plan: SSH Honeypot Hacker Trap

Each phase ends with a "done when" checklist. Tick the boxes as you go. Do the phases in order, because each one builds on the last.

---

## Phase 0: Linux and terminal basics (≈ 3–5 days)

**Goal:** be comfortable at the shell, because everything else happens there.

Learn:
- Navigation and files: `ls`, `cd`, `cat`, `less`, `grep`, `find`, pipes (`|`), redirection (`>`)
- Permissions and users: `chmod`, `chown`, `sudo`
- Processes and ports: `ps`, `kill`, `ss -tlnp`
- Services: `systemctl`, `journalctl`
- How SSH works: keys vs. passwords, `~/.ssh/authorized_keys`, `/etc/ssh/sshd_config`

Exercises:
- Create an SSH key pair and log in to a local VM with the key only.
- Find out which process is listening on port 22.

Done when:
- [x] I can explain what a port is and which program owns port 22
- [x] I can log in to a machine with an SSH key and no password
- [x] I can search a log file for a word with `grep`

Resources: [The Linux Command Line (free book)](https://linuxcommand.org/tlcl.php), `man <command>`

---

## Phase 1: Python fundamentals (≈ 2–3 weeks)

**Goal:** enough Python to read Cowrie's source code and write small log-analysis scripts.

Learn, in this order:
1. Running Python, the REPL, and virtual environments (`python -m venv`)
2. Variables, types, strings, f-strings
3. Lists, dicts, loops, `if`
4. Functions
5. Reading and writing files, the `with` statement
6. The `json` module. **This is the key one, because Cowrie logs one JSON object per line.**
7. Modules and imports, `pip`
8. Exceptions (`try`/`except`)
9. Classes, at a basic level (Cowrie plugins are classes)
10. Stdlib helpers: `collections.Counter`, `datetime`, `argparse`

Exercises (you write all of them):
- Script that counts the words in a text file
- Script that reads a JSON file and prints one field
- Script that reads a file with one JSON object per line and counts how often each value of a field appears

Done when:
- [ ] I can write a script that reads a file line by line and parses JSON
- [ ] I understand dicts well enough to pull out nested values
- [ ] I can read a short class definition and say what it does

Resources: [Official Python Tutorial](https://docs.python.org/3/tutorial/), [Automate the Boring Stuff (free)](https://automatetheboringstuff.com/)

---

## Phase 2: Networking and Wireshark (≈ 1 week)

**Goal:** see what an SSH attack looks like on the wire.

Learn:
- The TCP handshake (SYN, SYN-ACK, ACK), IP addresses, ports
- Why SSH traffic is encrypted, and what you *can* still see (handshake, key exchange, timing, packet sizes)
- Telnet is plaintext, so you can read passwords in Wireshark
- `tcpdump` to capture on a headless server, then open the `.pcap` file in Wireshark on your desktop
- Wireshark display filters (`tcp.port == 22`, `ip.addr == ...`)

Exercises:
- Capture your own SSH login and identify the handshake and key exchange packets.
- Capture a Telnet session to a local test server and find the password in the plaintext.

Done when:
- [ ] I can capture traffic with `tcpdump` and open it in Wireshark
- [ ] I can explain why I can see Telnet passwords but not SSH passwords

Resources: [Wireshark User's Guide](https://www.wireshark.org/docs/wsug_html_chunked/)

---

## Phase 3: Docker (≈ 1 week)

**Goal:** run and connect containers.

Learn:
- Images vs. containers, `docker run`, `docker ps`, `docker logs`, `docker exec`
- Port mapping (`-p host:container`)
- Volumes, which keep data after a container is deleted
- Docker networks
- Docker Compose: describing several services in one file

Exercises:
- Run an `nginx` container and reach it from your browser.
- Write a compose file (you write it) with two services that talk to each other.

Done when:
- [ ] I can explain image vs. container vs. volume
- [ ] I can start and stop a multi-service setup with `docker compose up` / `down`

Resources: [Docker Get Started](https://docs.docker.com/get-started/)

---

## Phase 4: Cowrie (≈ 1 week)

**Goal:** a working honeypot on your local machine or VM.

Learn:
- What Cowrie emulates: a fake shell, a fake filesystem, and recorded sessions
- Cowrie config (`cowrie.cfg`): hostname, ports, `userdb` (which passwords are "accepted")
- Log output: `cowrie.json`, TTY session recordings, downloaded files
- Running Cowrie with the official Docker image `cowrie/cowrie`

Exercises:
- Run Cowrie in Docker on port 2222 and SSH into it yourself.
- Type commands, then find your session in `cowrie.json`.
- Replay a recorded session with `playlog`.
- Change the fake hostname and the accepted credentials.

Done when:
- [ ] I can log in to my own honeypot and find my session in the logs
- [ ] I can explain the main event types (`cowrie.login.success`, `cowrie.command.input`, ...)

Resources: [Cowrie docs](https://cowrie.readthedocs.io/), [Cowrie GitHub](https://github.com/cowrie/cowrie)

---

## Phase 5: Log analysis in Python (≈ 1 week)

**Goal:** turn your Phase 1 skills on real Cowrie logs.

Build these yourself:
- Top 10 usernames and passwords tried
- Top 10 commands run after login
- Number of attempts per source IP
- Bonus: export a summary as CSV (`csv` module)

Done when:
- [ ] My script prints a useful attack summary from `cowrie.json`

---

## Phase 6: Elasticsearch and Kibana (≈ 1–2 weeks)

**Goal:** an attack dashboard.

Learn:
- The ELK pipeline: Cowrie JSON log → **Filebeat** (ships the logs) → **Elasticsearch** (stores and indexes them) → **Kibana** (visualizes them)
- Indices, documents, and fields
- Kibana: data views, Discover, KQL queries, visualizations, dashboards
- GeoIP enrichment, to map attacker IPs to countries
- Elasticsearch needs a lot of RAM (plan for at least 4 GB on the host)

Exercises:
- Add Elasticsearch, Kibana, and Filebeat to your compose file next to Cowrie.
- Build a dashboard: logins over time, top passwords, top commands, and a world map of source IPs.

Done when:
- [ ] My own test logins show up in Kibana within a minute
- [ ] I have a dashboard with at least 4 panels

Resources: [Elastic docs](https://www.elastic.co/docs), Cowrie docs → "Output plugins"

---

## Phase 7: Go live safely (≈ 3–5 days)

**Goal:** catch real attackers. Read the safety rules in CLAUDE.md first.

Steps to research and do yourself:
- Rent a small throwaway VPS (≥ 4 GB RAM if ELK runs there too)
- Move the real `sshd` to another port, use key-only auth, and test it **before** logging out
- Firewall: allow honeypot ports 22/23 from the internet, and admin SSH only from your IP
- Map public port 22 to Cowrie's port
- Restrict outbound traffic from the Cowrie container
- Keep Kibana bound to localhost and reach it through an SSH tunnel
- Run a `tcpdump` capture for one hour and analyze it in Wireshark

Done when:
- [ ] Real attacks appear in Kibana (usually within minutes)
- [ ] Kibana and Elasticsearch are not reachable from the internet (check with `nmap` from another machine)

---

## Phase 8: Extend (open-ended)

Ideas, roughly from easiest to hardest:
- Add fake files to Cowrie's filesystem so attackers find "juicy" data
- Write a Python script that looks up downloaded malware hashes on VirusTotal (API)
- Send alerts to Telegram or Discord on a successful honeypot login
- Write your own Cowrie output plugin (real Python classes, using Cowrie's plugin API)
- Write a minimal SSH honeypot of your own with `paramiko`, to understand what Cowrie does under the hood

---

## Progress log

| Date | Phase | Notes |
|------|-------|-------|
| 2026-10-04 | 0 | Lesson 1 (navigation) done. Host has no SSH server installed. Decision: local VM (VirtualBox, already installed) for Phases 0–6, VPS maybe for Phase 7. |
| 2026-10-04 | 0 | VM "SSH Honeypot Ubuntu" running (Ubuntu Server, 8 GB, 2 CPU). NAT 10.0.2.15 + host-only 192.168.56.101 (host = 192.168.56.1). Reachable from laptop. No sshd installed yet. |
| 2026-10-04 | 0 | Lesson 2 (permissions) done. VM user: vboxuser. Learned: pipes, less, grep. To revisit: owner vs. group column, hash vs. encryption. |
| 2026-10-05 | 0 | Lesson 2 extras: setuid, symlinks. Lesson 3 (processes, ports, services, journalctl) done. Next: lesson 4 (sshd + key login). |
| 2026-10-05 | 0 | Lesson 4 A–C done: openssh-server in VM, key login works via 1Password key `honeypot-lab` (Host alias `honeypot-lab` with IdentitiesOnly, ssh-copy-id -f). Next: part D (disable password auth). |
| 2026-10-05 | 0 | ✅ Phase 0 complete. Password auth disabled in VM (`PasswordAuthentication no`), verified with `-o PubkeyAuthentication=no` → `Permission denied (publickey)`. Next: Phase 1 (Python). |
| 2026-10-05 | 1 | Decision: write code on laptop (Python 3.14, VS Code), repo will become public on GitHub. VM pulls code via git later. |
| 2026-10-05 | 1 | Lesson 0: git repo, .venv, hello.py, first commit done. Fixed: .gitignore, .claude/ state untracked, commit amended with GitHub noreply email, force-pushed to DotCoyote/ssh-honeypot. Next: lesson 1 (variables, types, strings). |
| 2026-10-05 | 1 | Lessons 1 + 2 done (types, f-strings, conversions, TypeError/ValueError; lists, dicts, for/if, .get() default, counting with a dict). Open nits: unneeded parens in if, .get() vs [] for required keys, src_port vs dst_port. Next: lesson 3 (functions). |
| 2026-10-05 | 1 | Lesson 3 (functions) done: def, return vs print, defaults, docstrings, scope, None. Skipped: min_length=10 call, dst_port in test data, explaining the list comprehension in filter_events (revisit when it comes up). Next: lesson 4 (files, with, json). |
