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
- [x] I can write a script that reads a file line by line and parses JSON
- [x] I understand dicts well enough to pull out nested values
- [x] I can read a short class definition and say what it does

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
- [x] I can capture traffic with `tcpdump` and open it in Wireshark
- [x] I can explain why I can see Telnet passwords but not SSH passwords

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
- [x] I can explain image vs. container vs. volume
- [x] I can start and stop a multi-service setup with `docker compose up` / `down`

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
- [x] I can log in to my own honeypot and find my session in the logs
- [x] I can explain the main event types (`cowrie.login.success`, `cowrie.command.input`, ...)

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
- [x] My script prints a useful attack summary from `cowrie.json`

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
- [x] My own test logins show up in Kibana within a minute
- [x] I have a dashboard with at least 4 panels

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
- [x] Real attacks appear in Kibana (usually within minutes)
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
| 2026-10-06 | 1 | Lesson 4 (files, with, encoding, json, JSON Lines) done. Bonus: imports between files, `if __name__ == "__main__"`, __pycache__ ignored, type hints. Comprehensions understood. Next: lesson 5 (nested data). |
| 2026-10-06 | 1 | Lesson 5 (nested data) done: chained access, safe .get chains, references vs. .copy() vs. copy.deepcopy, any() + generator expressions, group_by_session (dict of lists). Learned real Cowrie session event order. Next: lesson 6 (modules, imports, pip). |
| 2026-10-06 | 1 | Lesson 6 (modules, sys.path, __name__, namespace packages, pip, supply-chain checks, requirements.txt with == pins, requests + ip-api.com GeoIP) done. Learned: HTTP 200 != success, no fake defaults (Null Island), translate external schemas at the boundary. Skipped: urllib bonus. Next: lesson 7 (exceptions). |
| 2026-10-07 | 1 | Lesson 7 (exceptions) done: try/except/else/finally, hierarchy (BaseException vs Exception, bare except blocks Ctrl+C), raise across function boundaries, enumerate line numbers, read → validate pipeline, repr() + truncation against ANSI escape injection (danger is after json.loads). Open: ESC test line in test log not switched to a valid event. Next: lesson 8 (classes). |
| 2026-10-08 | 1 | Lesson 8 (classes) done: __init__, self, methods vs attributes (bound method bug), __repr__ vs __str__, @classmethod from_dict, inheritance + super(), polymorphism, @dataclass (generated __init__/__repr__/__eq__). Read Cowrie Command_whoami (HoneyPotCommand, call(), self.write, commands dict registry). All Phase 1 checkboxes done; stdlib helpers (Counter, datetime, argparse) not covered yet. |
| 2026-10-12 | 1 | Lesson 9 (stdlib helpers) in progress: A (synthetic log generator) ✅, B (set) ✅, C (Counter, raw counting + cleanup only at output, tuple pairs, nested unpacking) ✅, D steps 1–2 (fromisoformat, aware UTC, min/max, strftime, divmod) ✅, D step 3c (session_durations dict) ✅. Switched machines here, see Handover. |
| 2026-10-13 | 1 | New machine set up: venv from Homebrew `python3.14` (Homebrew's versioned formula has no unversioned `python3` in `bin`; system `/usr/bin/python3` is 3.9 and breaks nested-quote f-strings). D step 3d ✅: `min`/`max` with keyword-only `key=` (positional 2nd arg = compare args themselves), `min(dict)` compares keys alphabetically ("runs ≠ correct"), `.get` vs `[]`/`__getitem__` typing, `timedelta` has no `strftime` → `format_duration` helper. D step 3e ✅: `sum` `start` must be the neutral element (`dt.timedelta()`), not the min (counted twice); function accidentally read the `__main__` global instead of its (typo'd) parameter; `str.join` is called on the separator; return-type hints (`->`, not enforced at runtime). D step 4 ✅: `.hour` attribute + `Counter`; all-24-hours trap (missing `Counter` key, `range` exclusive end); nested f-string field for dynamic width; `"#" * n` bar; sum-of-counts `assert` as permanent sanity check, not a one-off print. Phase 1 part D fully done; only part E (argparse) left in lesson 9. |
| 2026-10-15 | 1 | Lesson 9 part E ✅: `ArgumentParser`, positional `logPath` + `-t`/`--top` (`type=int`) + `-g`/`--generate` (`action='store_true'`); argparse's own validation and non-zero exit on bad/missing args; `--generate` flag closes the old "test data regenerates every run" issue. Found/fixed a real bug: `logPath` was parsed but `read_events` still read the old hardcoded path, so a bad path silently fell back to the default file instead of failing. Added an empty-log guard, first placed after step 3 (unreachable — step 2 already crashes earlier on empty data) then correctly moved right after `read_events`. **Lesson 9 and Phase 1 complete.** Starting Phase 2 (networking + Wireshark). |
| 2026-10-15 | 2 | Phase 2 (networking + Wireshark) done. Installed Wireshark, verified `ChmodBPF`/`access_bpf` group membership for non-root packet capture. Used throwaway `docker run` containers (no compose file — doesn't belong in this repo) for both exercises: `linuxserver/openssh-server` and `wistic/telnetd`. Debugged a real auth failure (1Password SSH agent offered every stored key before password auth, hit the server's `MaxAuthTries`) by adding an `ssh_config` host alias with `IdentityAgent none`, placed above the catch-all `Host *` block (first-match-wins order). Found and fixed two capture mistakes: missed the TCP handshake by starting Wireshark after connecting (fixed by starting `tcpdump` first, which removes the GUI click-then-switch-windows race) and Wireshark not labeling SSH traffic on port 2222 (needs `Decode As` → SSH, since the dissector is only attached to port 22 by default). Verified the capture with `tshark` (bundled in the Wireshark app) rather than reading raw pcap bytes. Found SYN/SYN-ACK/ACK, the plaintext version banner, labeled key-exchange packets, and the exact point each side's traffic switches to `Encrypted packet` (each side calls `New Keys` independently, not simultaneously). Telnet capture via `Follow TCP Stream` showed the password in plain text; explained the doubled characters as Telnet's remote-echo behavior (every keystroke is two packets: the key, then the server's echo of it). |
| 2026-10-15 | 3 | Phase 3 (Docker) done. Exercise 1: `nginx` via `docker run -p 8900:80`, confirmed port mapping only applies from the host side (`curl localhost:80` works *inside* the container regardless of the published host port). Exercise 2: wrote `docker-compose.yml` (`backend`/`proxy`, two `nginx` services) and `proxy/nginx.conf` (own files, not written by Claude per CLAUDE.md rule 1). Debugged two real nginx config errors from the actual `nginx -t`/container log output: missing `;` after `proxy_pass`, then missing `http://` scheme on it. Hit a confusing `docker logs` red herring — the container was being reused (same ID, same `Created` timestamp) across `docker compose up -d` re-runs since only the bind-mounted file changed, not the compose file itself, so `docker logs` showed every prior crash's history; `nginx -t` + a live `curl` were the authoritative "is it broken now" checks instead. Confirmed service-name-as-hostname networking (`proxy_pass http://backend;` resolves via Compose's built-in DNS, no IP/manual network needed). Covered bind mount vs. named volume (own file you author and edit live, vs. container-generated data you just want to survive `docker rm`) and the stop-vs-remove distinction (a stopped container keeps its data even without a volume; only removal destroys it). **Phase 3 complete.** |
| 2026-10-16 | 1 | Phase 4 (Cowrie) done. Ran `cowrie/cowrie` via Docker on port 2222; the image ships no shell at all (`sh`/`ls`/`which` all missing), so exploration and `playlog` replay went through the container's own `python3` + `os.walk` instead of `docker exec ... sh`. Found a session's `wget http://example.com` triggered a real `cowrie.session.file_download` — Cowrie actually fetches and saves the real bytes by SHA-256, concretely explaining CLAUDE.md's "never execute downloads/" rule rather than just reciting it. Hit the standard `Host key verification failed` again (3rd different SSH server on `localhost:2222` this week) — same `ssh-keygen -R`/`ssh-exercise` alias fix as phase 2. Pulled `cowrie.cfg.dist`/`userdb.example` out via `docker cp`, edited `hostname` and `userdb.txt` (owner wrote both). Debugged two real bugs from actual container logs: a bind-mounted empty host dir *replaces*, not merges, the image's pre-existing `var/lib/cowrie/tty`+`downloads` subdirs, so sessions crashed with `FileNotFoundError` until those subdirs were `mkdir -p`'d on the host first; and a `*:x:*` catch-all already present in the stock `userdb.example`, sitting *before* the owner's own `paul`/`wpadmin` rules, silently accepted every login regardless of the new rules (first-match-wins applies to the whole file, not just lines you add — same principle as lesson 9's dict ordering bugs, just hitting it in an inherited config file this time). Confirmed fix: `paul`/`password` now fails, `paul`/anything-else succeeds, fake hostname `wordpress` shows in the prompt. `cowrie/logs/` and `cowrie/downloads/` gitignored as generated runtime data; only `cowrie/etc/cowrie.cfg` and `cowrie/etc/userdb.txt` are real config, kept. **Phase 4 complete.** |
| 2026-10-16 | 2 | Phase 5 (log analysis) done, against the real `cowrie.json` (73+ entries) instead of synthetic test data. Extracted a new top-level `honeypot/` package (`logs.py`, `sanitize.py`, `export.py`) from lesson 7's `read_events`/`cleanup_text`, scoped to only what the script needs now rather than reorganizing all 9 lessons upfront; lessons 1–9 stay frozen as the graded historical record. Confirmed real cowrie.json field names match the lesson-9 synthetic generator exactly, so no new parsing logic was needed, just new `eventid`-prefix filtering (`cowrie.login.`, `cowrie.command.input`). Covered `argparse` gaps lesson 9 didn't hit: a positional with `default=` is still required unless `nargs='?'` is also set; `nargs='?'` + `const=` on an optional flag (`--csv` with no value vs. omitted vs. given a value); typing `parse_args()`'s result via an `argparse.Namespace` subclass with class-level annotations (confirmed via pyright `reveal_type` that it types correctly-spelled fields precisely, but — correcting my own earlier claim — does **not** catch a typo'd attribute name, which still only surfaces as a runtime `AttributeError`, because `Namespace` falls back to `Any` for unknown attributes even on subclasses). Debugged a `--top` value silently ignored on two of four metrics (missing argument at the call site) and a function named `get_top_...` that didn't actually cap anything. `csv.writer`: built one combined summary file (category/value/count) instead of four separate exports, after catching that calling the export function multiple times in `'w'` mode would've silently overwritten all but the last metric. Caught and fixed a real CSV/formula-injection risk (OWASP-documented) by routing exported values through `cleanup_text` before writing — a spreadsheet opening a field starting with `=`/`+`/`-`/`@` can execute it as a formula. Also fixed a `Path(file).mkdir()` bug that created the CSV's target path as a directory instead of a file (needed `.parent.mkdir()`). **Phase 5 complete.** |
| 2026-10-19 | 1 | Phase 6 (Elasticsearch/Kibana) done, debugged almost entirely from real cluster state rather than guessed config. Elasticsearch 8.x+ security/TLS defaults made a plain `curl` fail silently (`Empty reply from server`, actually a TLS handshake mismatch plus real auth); used `discovery.type=single-node`/`xpack.security.enabled=false` for this localhost-only dev setup. Found a genuine Filebeat/Cowrie field-name collision: Cowrie's own `input` field (command text) collided with Filebeat's own reserved `input.type` metadata, silently losing Cowrie's data at JSON-decode time — not fixable with a later `processors: rename` step (too late in the pipeline), fixed properly by nesting all of Cowrie's fields under a `cowrie.*` prefix (`parsers: - ndjson: target: 'cowrie'`) instead of `keys_under_root`. Each schema change needed a full wipe (`DELETE _data_stream/...` + recreate the filebeat container to reset its position registry) since Elasticsearch field types can't change retroactively and Compose doesn't recreate containers just because a bind-mounted file changed. Built an Elasticsearch `geoip` ingest pipeline for the map panel; discovered local Docker traffic uses a private IP with no geographic data, so injected a handful of clearly-marked demo documents (real public IPs) to prove the panel works, verified against the pipeline via `_ingest/pipeline/.../_simulate` before touching any real data. Introducing a competing index template to fix `cowrie.geoip.location`'s mapping (needed, since nesting under `cowrie.*` also sidestepped Filebeat's own `geoip.location` → `geo_point` convention) had a side effect I under-anticipated: a higher-priority template doesn't merge with a lower one, it fully replaces it — so our own `cowrie.*` fields silently lost Filebeat's keyword-only dynamic mapping too, breaking two already-working dashboard panels (fixed by using `.keyword` suffixes consistently from then on, the pragmatic fix over reworking the template with `composed_of`). Diagnosed a "no data showing" dead end down to a leftover dashboard-level filter pill from map-testing, left filtering out everything real. Separately found the actual `cowrie.json` log file had lost all history from the 16th — gone from the source file itself during the multi-day gap, unrelated to anything done today. Exported the dashboard (`kibana/dashboard-export.ndjson`) and the ingest pipeline + index template (`elasticsearch/*.json`) for reproducibility, same reasoning as the Phase 3 compose files. **Phase 6 complete.** |
| 2026-10-19 | 7 | Phase 7 started. Oracle Cloud Free Tier ARM instance (A1.Flex, Ubuntu 26.04) running. ELK and Cowrie will run on the same VPS. The VCN had no internet gateway or default route, so `ssh` timed out (silently dropped, not refused). Fixed with an internet gateway plus a `0.0.0.0/0` route. Read-only inspection of sshd (socket-activated, password auth already off) and of Oracle's default iptables (REJECT at the end of INPUT). Checkpoint before moving sshd, see Handover. |
| 2026-10-23 | 7 | Step 2 done: admin sshd moved to a high port, key-only. Opened it in all three layers (VCN security list for own IP `/32`, iptables inserted before the REJECT and persisted, `ssh.socket` via `daemon-reload` + socket restart), then tested with both ports active before removing 22. Traps hit: the image has no editor; `sshd -T` without `sudo` fails; the ssh alias pointed `IdentityFile` at the `.pub` file. Port 22 is now free for Cowrie. Next: step 3 (firewall). |
| 2026-10-23 | 7 | Step 3 done: security list opens 22 + 23 to the world, admin port only from own IP. Telnet decided yes. Learned that Docker-published ports go through `FORWARD`, not `INPUT`, so the host INPUT REJECT doesn't protect them, and `127.0.0.1:` bindings in Compose are the real protection for Elasticsearch/Kibana. `rpcbind` stopped + disabled (stop vs. disable), checked TCP and UDP listeners separately. Next: step 4 (Docker + Cowrie on the VPS). |
| 2026-10-26 | 7 | **Honeypot live.** Docker on the VPS, Cowrie on 22/23 in its own network, ELK on a separate network, Kibana only through an SSH tunnel. The first Telnet botnets (e.g. Odesa, `admin/admin`, `enable`/`linuxshell`/`system`) arrived within minutes, with 4431 documents after about an hour. Debugged: `.env` not read (bind on `127.0.0.1`), Filebeat config owner, UID 999 on `cowrie/downloads` (SSH dead, Telnet alive), honeypot host key in `known_hosts`, `*_millis` fields in the exports, a typo'd template name, and the tunnel accidentally landing on the local Kibana. Done-when 1 ✅. Open: outbound restriction, IP isolation test on the VPS, tcpdump, nmap. |

---

## Handover (current state, 2026-10-19)

Read this first when resuming on a new machine or in a new session.

### Where we are

**Phase 7 (go live safely): the honeypot is live and collecting real attacks.** Open: steps 5 and 7, the IP-level isolation test on the VPS, and the final `nmap` check (done-when 2). Phases 0–6 are complete and committed.

The VPS public IP and the admin SSH port are deliberately **not** written here, because this repo is public. They live in the owner's `~/.ssh/config` alias `Oracle-SSH-Honeypot`.

| Step | Status |
|------|--------|
| 1. Rent VPS | ✅ Oracle Cloud Free Tier, `VM.Standard.A1.Flex` (ARM/aarch64), Ubuntu **26.04 LTS**, user `ubuntu`, key-only login works |
| 2. Move sshd, key-only auth | ✅ admin sshd on a high port only (own drop-in in `sshd_config.d/`), key-only, alias has `Port` set. Opened in all 3 layers: VCN security list (own IP `/32`), iptables (inserted before the REJECT and persisted in `rules.v4`), `ssh.socket` (reloaded via `daemon-reload`) |
| 3. Firewall (honeypot ports open, admin SSH only from own IP) | ✅ security list: 22 + 23 from `0.0.0.0/0`, admin port from own `/32` only. No INPUT rule for 23 needed (Docker-published ports go through `FORWARD`, not `INPUT`). `rpcbind` (111 TCP/UDP) stopped and disabled. Remaining listeners: only the admin sshd publicly, the rest on localhost/private interface (resolver 53, DHCP 68, chrony 323) |
| 4. Map public 22 → Cowrie | ✅ 22 → 2222 (SSH) and 23 → 2223 (Telnet), bind address via `COWRIE_PUBLIC_IP` (default `127.0.0.1`, `0.0.0.0` only in the VPS `.env`). Cowrie on its own `cowrie-net`, ELK on `elk-net` |
| 5. Restrict Cowrie container's outbound traffic | ⬜ |
| 6. Kibana on localhost + SSH tunnel | ✅ `ssh -L <local port>:localhost:5601 -N -o ExitOnForwardFailure=yes` through the admin alias. Dashboard imported, real attacks visible |
| 7. One-hour `tcpdump` capture → Wireshark | ⬜ |

Decisions made:
- **ELK runs on the same VPS as Cowrie** (24 GB RAM is plenty). Trade-off accepted: a container escape would land on the same host as the log data. Mitigation still to do: put Cowrie on its own Docker network, with no route to Elasticsearch/Kibana.
- Images must be **arm64**. Check every image before pulling it on the VPS.

Debugged so far:
- Instance creation: the public subnet can't be created from the instance form. Fixed with **Networking → VCN Wizard → "VCN with Internet Connectivity"**.
- `ssh` timed out (packets dropped, not refused): the VCN had **no internet gateway** and the route table was empty. Fixed with an internet gateway plus route rule `0.0.0.0/0 → Internet Gateway`. Trap: Target Type "Private IP" is wrong, because that's for routing through another instance.

State found on the VPS (read-only checks, nothing changed yet):
- `sshd -T`: `port 22`, `passwordauthentication no`, `pubkeyauthentication yes`, `permitrootlogin prohibit-password` (could tighten to `no`).
- sshd is **socket-activated**: `ssh.socket` listens on `0.0.0.0:22` and `[::]:22`. Changing `Port` in the config alone plus `restart ssh` won't move it. Research `sshd-socket-generator`: something needs a reload before the socket restarts.
- Host firewall `/etc/iptables/rules.v4` (Oracle image default): INPUT allows only ESTABLISHED, ICMP, `lo`, and TCP 22, then **`-j REJECT`**. A new ACCEPT rule must be inserted *before* that REJECT (appending puts it after, so it never matches). It must also be persisted for reboots (`netfilter-persistent`). Check `rules.v6` too.

Learned in step 2 (2026-10-23):
- A single `Port` line disables the default 22. To listen on both during the switch, you need two `Port` lines.
- The minimal Oracle image has no editor, so `nano` had to be installed.
- `sshd -T` and `ss -p` need `sudo`. Without it they fail (`no hostkeys available`) or show an empty Process column.
- The ssh alias first pointed `IdentityFile` at the `.pub` file. That only works with an agent that holds the private key. Oracle's generated key isn't in 1Password, so it has to point at the private key file (`chmod 600`).
- `nc` result meanings: timeout = a firewall drops the packets, refused = they arrive but nothing listens, succeeded = something listens. Used to check each layer separately.

Learned in step 3 (2026-10-23):
- Decision: **Telnet too** (port 23, many IoT botnets). It must be enabled in `cowrie.cfg` (off by default).
- Docker publishes ports via DNAT, so the traffic runs through `FORWARD` (Docker inserts its rules there before Oracle's REJECT), not `INPUT`. Consequence: a port published as plain `-p 9200:9200` is reachable from the internet **despite** INPUT REJECT. The `127.0.0.1:` bindings for Elasticsearch/Kibana are the real protection, so check them before the first `up` on the VPS.
- `systemctl stop` only ends the current run; `disable` removes the autostart. Without `mask`, another package can still pull rpcbind in as a dependency, and the final `nmap` check would catch that.
- `ss -tlnp` shows TCP only; UDP needs `ss -ulnp`.
- From macOS, `nc` can't tell a TCP reset from an ICMP reject (both show "refused"). The iptables packet counters (`-L -v`) show which rule really matched.

Learned in steps 4 + 6 (2026-10-26):
- Docker from Ubuntu's packages (`docker.io` + Compose plugin). The `docker` group is root-equivalent, so keep using `sudo docker`. Never run `netfilter-persistent save` after Docker is installed (it would freeze Docker's chains into `rules.v4`).
- **Isolation only proven at the name level:** from Cowrie, `elasticsearch` doesn't resolve (`gaierror`), but locally (Docker Desktop) a connection **by IP** across networks worked. **On the VPS (2026-10-27) the IP test times out** (Cowrie → `172.18.0.2:9200`, the IP confirmed by the DNAT rule), so on real Linux Docker separates the networks at the IP level too. The commit `5e0a90f` statement holds on the VPS; the local leak was Docker Desktop-specific.
- `host_binding_ipv4` as a network option was ignored on Docker Desktop. An explicit IP in the port entry works. On macOS, Docker Desktop binds privileged ports (<1024) as `*:22`, but filters in software (checked from the LAN IP).
- On real Linux, UIDs matter for bind mounts: Cowrie runs as `999:999`. `cowrie/downloads` **itself** (= `var/lib/cowrie`) also has to belong to 999, or the SSH host key can't be written. Then Telnet runs but SSH doesn't (refused from inside the container, while the DNAT counters still count).
- Filebeat on Linux only accepts a config owned by root with no group/other write. Downside: `git pull` as `ubuntu` can't overwrite `filebeat.yml` any more.
- Exports from `GET` contain system-managed fields (`created_date_millis`) that `PUT` rejects. Fixed in the repo (`8116546`). Load the pipeline and template **before** Filebeat's first start, and test with `_simulate` (the GeoLite2 DB downloads itself).
- Honeypot SSH test via a separate `ssh_config` alias with `StrictHostKeyChecking no` + `UserKnownHostsFile /dev/null` + no agent/pubkey. **Never** in the admin alias.
- The first tunnel attempt silently failed: the local Kibana held `5601`, so the browser showed the empty local Kibana. Check with `lsof` which process holds the port. `ExitOnForwardFailure=yes` makes ssh fail loudly instead.

**Next: step 5** (restrict Cowrie's outbound traffic), the IP isolation test on the VPS, step 7 (`tcpdump`), then the `nmap` check from outside (done-when 2). Later, watch out for Docker-published ports: they go through the `FORWARD`/`DOCKER` chains, not `INPUT`, so the host's INPUT rules don't cover them.

### Older open items (low priority)

- `lesson9.py` cleanup nits (dict comprehension, repeated `min`/`max`/`strftime`, debug prints, missing docstrings). Lessons 1–9 are frozen as the historical record, so these are optional.
- Lesson 7: ESC test line in `test_log_lesson7.json` never switched to a valid success event (protection verified separately, works).
- Lesson 3: `format_event` prints attacker fields without `cleanup_text`.

### How the owner likes to work (teaching style)

- Strict CLAUDE.md rules: never write code/config; review with line numbers + hints; owner writes everything.
- When the owner says **"guide me" / "explain further"**: give a detailed step-by-step guide (sub-steps, tables, what to look up, expected output, plausibility check) — still no code.
- When the owner says **"done" / "check again"**: read the file, **run it**, verify output (incl. plausibility), then review: ✅ what's right first, then numbered issues with line refs, then small nits.
- When the owner says **"next" / "let's continue"**: accept skipped items, note them in the log, move on.
- Recurring principles taught so far (reuse when reviewing): `[]` for required keys / fail loudly; no fake defaults (Null Island); translate at boundaries; clean attacker data only at output (`cleanup_text` = `repr` + truncation); labels must say exactly what's printed; reuse existing helpers instead of rewriting; keep `try` small.
- Commits: owner uses `/make-commit`; split logically (infra vs. lesson); no scope (no ticket on `main`); **no Co-Authored-By** (CLAUDE.md rule 7).

### Environment on the old machine (not in the repo)

- VirtualBox VM "SSH Honeypot Ubuntu" (Ubuntu Server, 8 GB/2 CPU), NAT + host-only `192.168.56.101`, user `vboxuser`, sshd with password auth disabled, key-only login.
- SSH: 1Password agent key `honeypot-lab`, `~/.ssh/config` alias `honeypot-lab` (IdentitiesOnly, IdentityFile = public key file).
- The VM is only needed again from Phase 2/4 on. On a new machine, Python lessons only need: clone repo → `python3 -m venv .venv` → activate → `pip install -r requirements.txt`. Lesson 6 needs internet (ip-api.com).
