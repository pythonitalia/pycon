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

## NAT

sudo yum install iptables-services -y
sudo systemctl enable iptables
sudo systemctl start iptables

sudo touch /etc/sysctl.d/custom-ip-forwarding.conf
sudo chmod 666 /etc/sysctl.d/custom-ip-forwarding.conf
sudo echo "net.ipv4.ip_forward=1" >> /etc/sysctl.d/custom-ip-forwarding.conf
sudo sysctl -p /etc/sysctl.d/custom-ip-forwarding.conf

sudo /sbin/iptables -I INPUT 4 -i docker0 -j ACCEPT

sudo /sbin/iptables -t nat -A POSTROUTING -o ens5 -j MASQUERADE
sudo /sbin/iptables -F FORWARD
sudo service iptables save

## Tailscale

sudo yum install yum-utils -y
sudo yum-config-manager -y --add-repo https://pkgs.tailscale.com/stable/amazon-linux/2/tailscale.repo
sudo yum install tailscale -y
sudo systemctl enable --now tailscaled
sudo tailscale up --ssh --authkey ${tailscale_auth_key} --advertise-tags=tag:main-server --hostname main-server

## Redis

mkdir /redis-data


## Mount volumes

sudo echo "UUID=0240a196-f4eb-4a34-8218-75af80d479f6 /var/pretix xfs defaults,nofail 0 2" >> /etc/fstab
sudo echo "UUID=6dbc6ff5-7b78-47fe-85af-4ab6fa4473cc /redis-data xfs defaults,nofail 0 2" >> /etc/fstab
sudo mount -a
