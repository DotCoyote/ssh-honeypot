# Phase 2 setup: throwaway SSH target for Wireshark

Disposable container used to capture a real SSH handshake for the
Wireshark exercises. Not part of the honeypot stack — delete it when
the exercise is done.

## Start

```bash
docker run -d \
 --name=openssh-server \
 --hostname=openssh-server \
 -e PUID=1000 \
 -e PGID=1000 \
 -e TZ=Etc/UTC \
 -e PASSWORD_ACCESS=true \
 -e USER_PASSWORD=password \
 -e USER_NAME=linuxserver.io \
 -p 2222:2222 \
 lscr.io/linuxserver/openssh-server:latest
```

Connect: `ssh -p 2222 linuxserver.io@ssh-exercise`

## Capture

- Wireshark interface: `lo0` (loopback, not `en0` — localhost traffic
  never hits the physical NIC)
- Capture filter: `tcp port 2222`

## Teardown

docker stop openssh-server && docker rm openssh-server

Throwaway credentials — never reuse `USER_PASSWORD` value elsewhere.
