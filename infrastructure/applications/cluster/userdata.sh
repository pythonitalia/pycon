#!/bin/bash
set -x

echo "ECS_CLUSTER=${ecs_cluster}" > /etc/ecs/ecs.config

fallocate -l ${swap_size} /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo "/swapfile swap swap defaults 0 0" >> /etc/fstab

mkdir /redis-data -p
echo '/dev/nvme1n1 /redis-data xfs defaults 0 0' >> /etc/fstab
mount -a
