#!/bin/bash

# ==============================================================================
# ARCH LINUX AUTOMATION SETUP FOR CYBERCHALLENGE
# ------------------------------------------------------------------------------
# IDEMPOTENT SCRIPT: This script is designed to be safe to run multiple times.
# It will only install missing packages and update existing ones.
# It will NOT overwrite your configurations or break existing installations.
# ==============================================================================

echo "---  STARTING AUTOMATION: IDEMPOTENT SETUP ---"

# 1. System Update
# -Syu: Synchronizes the package database and updates the system.
# --noconfirm: Skips yes/no prompts.
echo "---  Step 1: Updating System (Safe Update)... ---"
sudo pacman -Syu --noconfirm

# 2. Install Essential Tools
# We install tools one by one. If one fails, others will still try to install.
# --needed: Skips the package if it is already installed (IDEMPOTENCY).
echo "---  Step 2: Installing Essential Tools... ---"

# Version Control
sudo pacman -S --needed --noconfirm git

# Development Tools (GCC, Make, etc.)
sudo pacman -S --needed --noconfirm base-devel

# Code Editor (VS Code)
sudo pacman -S --needed --noconfirm code

# Python Language
sudo pacman -S --needed --noconfirm python

# Python Package Manager
sudo pacman -S --needed --noconfirm python-pip

# Network Scanner
sudo pacman -S --needed --noconfirm nmap

# System Info Tool (The logo!)
sudo pacman -S --needed --noconfirm fastfetch

# 3. Global Git Configuration
# Sets the credential helper so you don't have to type passwords every time.
echo "---  Step 3: Configuring Global Git Settings... ---"
git config --global credential.helper store

# 4. Clean Cache
# Removes old installation files to save space.
echo "---  Step 4: Cleaning Package Cache... ---"
sudo pacman -Sc --noconfirm

# 5. Final Check
echo "---  SETUP COMPLETE! ---"
echo "--- The VM is fully updated and ready for action. ---"

# Show System Info
fastfetch

echo ""
echo "=========================================="
echo " REMINDERS FOR VS CODE:"
echo "If you have git sync issues inside VS Code, run these in the internal terminal:"
echo "  1. git pull origin main --rebase"
echo "  2. git push origin main"
echo "=========================================="
