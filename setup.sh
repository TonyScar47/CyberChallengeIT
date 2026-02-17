#!/bin/bash

echo "--- STARTING AUTOMATION --"

#Update package repositories
sudo pacman -Sy

#Install essential programs
sudo pacman -S --noconfirm git base-devel code python python-pip nmap

#NICEEEE
echo "--- VM is up do date and ready for action! ---"