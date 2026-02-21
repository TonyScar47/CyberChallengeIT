#!/bin/bash

# ==============================================================================
# ARCH LINUX AUTOMATION SETUP FOR CYBERCHALLENGE
# ------------------------------------------------------------------------------
# IDEMPOTENT SCRIPT: Safe to run multiple times.
# STRICT MODE: The script will abort immediately if any command fails.
# ==============================================================================

# Stop script on error (Safety First!)
set -e

# Define Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "---  STARTING AUTOMATION: IDEMPOTENT SETUP ---"

# 1. System Update
echo "---  Step 1: Updating System (Safe Update)... ---"
sudo pacman -Syu --noconfirm

# 2. Install Essential Tools
echo "---  Step 2: Installing Essential Tools... ---"

# Tools list (One by one for clarity)
sudo pacman -S --needed --noconfirm git
sudo pacman -S --needed --noconfirm base-devel
sudo pacman -S --needed --noconfirm code
sudo pacman -S --needed --noconfirm python
sudo pacman -S --needed --noconfirm python-pip
sudo pacman -S --needed --noconfirm nmap
sudo pacman -S --needed --noconfirm fastfetch
sudo pacman -S --needed --noconfirm virtualbox-guest-utils
sudo pacman -S --needed --noconfirm openbsd-netcat
sudo pacman -S --needed --noconfirm bind

sudo pacman -S --needed --noconfirm docker-compose

# Python System Packages:
sudo pacman -S --needed --noconfirm python-requests

# --- NEW: Virtual Environment Setup for CTF Tools ---
echo "---  Setting up Python Virtual Environment... ---"
if [ ! -d "venv" ]; then
    python -m venv venv
    echo -e "${GREEN}Virtual environment created.${NC}"
fi

# Install exrex inside the venv (Avoids PEP 668 errors on Arch)
echo "---  Installing exrex in venv... ---"
./venv/bin/pip install --upgrade pip
./venv/bin/pip install exrex
./venv/bin/pip install rstr requests
# ----------------------------------------------------

# 3. Global Git Configuration
echo "---  Step 3: Configuring Global Git Settings... ---"
git config --global credential.helper store

# 4. Clean Cache
echo "---  Step 4: Cleaning Package Cache... ---"
sudo pacman -Sc --noconfirm

# 5. Final Success Message
echo ""
echo "----------------------------------------------------------------"
echo -e "${GREEN}  ACCESS GRANTED. SYSTEM READY.${NC}"
echo -e "${GREEN}  ALL TOOLS INSTALLED SUCCESSFULLY.${NC}"
echo -e "${GREEN}  GLHF (Good Luck Have Fun) & HAPPY HACKING! 💀${NC}"
echo "----------------------------------------------------------------"

# Show System Info
fastfetch

echo ""
echo " VS CODE GIT REMINDER:"
echo "If sync fails: 'git pull origin main --rebase' then 'git push origin main'"
echo ""
echo " PYTHON VENV REMINDER:"
echo "To use your tools, run: source venv/bin/activate"
echo "then run: deactivate"
