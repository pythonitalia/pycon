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

chmod +x /usr/local/bin/claimspace.sh
echo "0 0 * * * root /usr/local/bin/claimspace.sh" > /etc/cron.d/claimspace

# Run pretix cron
cat << "EOF" > /usr/local/bin/pretixcron.sh
#!/bin/bash
docker exec `docker ps --no-trunc -q --filter="name=.*pretix.*" | head -n 1` pretix cron
exit 0
EOF

chmod +x /usr/local/bin/pretixcron.sh
echo "15,45 * * * * /usr/local/bin/pretixcron.sh" > /etc/cron.d/pretixcron

sudo mkdir -p /var/pretix/data/media
sudo chown -R 15371:15371 /var/pretix/data/media
