#!/bin/bash
set -x

# Config ECS agent
echo "ECS_CLUSTER=${ecs_cluster}" > /etc/ecs/ecs.config

# Reclaim unused Docker disk space
cat << "EOF" > /usr/local/bin/claimspace.sh
#!/bin/bash
# Run fstrim on the host OS periodically to reclaim the unused container data blocks
docker ps -q | xargs docker inspect --format='{{ .State.Pid }}' | xargs -IZ sudo fstrim /proc/Z/root/
exit $?
EOF

# Run pretix cron
cat << "EOF" > /usr/local/bin/pretixcron.sh
#!/bin/bash
docker exec `docker ps --no-trunc -q --filter="name=.*pretix.*" | head -n 1` pretix cron
exit 0
EOF

chmod +x /usr/local/bin/claimspace.sh
chmod +x /usr/local/bin/pretixcron.sh

cat << "EOF" > /etc/systemd/system/claimspace.service
[Unit]
Description=Run fstrim on Docker containers

[Service]
Type=oneshot
ExecStart=/usr/local/bin/claimspace.sh

[Install]
WantedBy=multi-user.target
EOF

cat << "EOF" > /etc/systemd/system/pretixcron.service
[Unit]
Description=Run Pretix cron job

[Service]
Type=oneshot
ExecStart=/usr/local/bin/pretixcron.sh

[Install]
WantedBy=multi-user.target
EOF

cat << "EOF" > /etc/systemd/system/claimspace.timer
[Unit]
Description=Run fstrim on Docker containers daily

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
EOF

cat << "EOF" > /etc/systemd/system/pretixcron.timer
[Unit]
Description=Run Pretix cron job

[Timer]
OnCalendar=*:15,45
Persistent=true

[Install]
WantedBy=timers.target
EOF

systemctl daemon-reload

systemctl enable --now claimspace.timer
systemctl enable --now pretixcron.timer

dd if=/dev/zero of=/swapfile bs=128M count=32
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo "/swapfile swap swap defaults 0 0" >> /etc/fstab
