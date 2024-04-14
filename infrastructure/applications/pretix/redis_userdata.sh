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

mkdir /redis-data

sudo echo "UUID=6dbc6ff5-7b78-47fe-85af-4ab6fa4473cc /redis-data xfs defaults,nofail 0 2" >> /etc/fstab
sudo mount -a

sudo su
sudo dd if=/dev/zero of=/swapfile bs=128M count=32
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
sudo echo "/swapfile swap swap defaults 0 0" >> /etc/fstab
