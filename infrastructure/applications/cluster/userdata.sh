#!/bin/bash
set -x

# change 2
echo "ECS_CLUSTER=${ecs_cluster}" > /etc/ecs/ecs.config
echo "ECS_INSTANCE_ATTRIBUTES={\"role\": \"${role}\"}" >> /etc/ecs/ecs.config

sudo su
sudo dd if=/dev/zero of=/swapfile bs=${swap_size} count=32
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
sudo echo "/swapfile swap swap defaults 0 0" >> /etc/fstab
