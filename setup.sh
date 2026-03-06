#!/bin/bash

# ==============================================================================
# ARCH LINUX AUTOMATION SETUP FOR CYBERCHALLENGE (V4 - YAY & AUR INTEGRATION)
# ------------------------------------------------------------------------------
# IDEMPOTENT SCRIPT: Safe to run multiple times.
# STRICT MODE: The script will abort immediately if any command fails.
# ==============================================================================

# Define Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# --- LOGGING SETUP ---
LOG_FILE="setup_error.log"
> "$LOG_FILE"
exec > >(tee -a "$LOG_FILE") 2>&1

trap 'echo -e "\n${RED}[!] CRITICAL ERROR: Automation aborted. Something broke! Check the log file: ${LOG_FILE}${NC}\n"' ERR

set -e

echo "---  STARTING AUTOMATION: IDEMPOTENT SETUP ---"

# 1. System Update
echo "---  Step 1: Updating System... ---"
sudo pacman -Syu --noconfirm

# 1.5. Core Documentation
echo "---  Step 1.5: Installing Core Documentation (man pages)... ---"
sudo pacman -S --needed --noconfirm man-db man-pages

# --- BASE SYSTEM & DEV ---
echo "[*] Installing Base & Dev tools..."
sudo pacman -S --needed --noconfirm git base-devel code python python-pip fastfetch virtualbox-guest-utils docker-compose cmake curl

# --- STEP 1.75: INSTALL YAY (AUR HELPER) ---
# Added this step to manage AUR packages more efficiently during CTFs.
# yay-bin is preferred to avoid long compilation times.
echo "---  Step 1.75: Installing yay (AUR Helper)... ---"
if ! command -v yay &> /dev/null; then
    echo "[*] yay not found. Proceeding with manual installation from AUR..."
    ORIGINAL_DIR=$(pwd)
    BUILD_DIR=$(mktemp -d)
    
    cd "$BUILD_DIR"
    git clone https://aur.archlinux.org/yay-bin.git
    cd yay-bin
    makepkg -si --noconfirm
    
    cd "$ORIGINAL_DIR"
    rm -rf "$BUILD_DIR"
    echo -e "${GREEN}    yay installed successfully.${NC}"
else
    echo -e "${GREEN}    yay is already present. Skipping manual build.${NC}"
fi

# 2. BlackArch Repository Setup
echo "---  Step 2: Configuring BlackArch Repository... ---"
if ! grep -q "\[blackarch\]" /etc/pacman.conf; then
    echo "    Downloading and executing BlackArch strap.sh..."
    curl -O https://blackarch.org/strap.sh
    chmod +x strap.sh
    sudo ./strap.sh
    sudo pacman -Syu --noconfirm
    rm strap.sh
    echo -e "${GREEN}    BlackArch repository configured successfully.${NC}"
else
    echo -e "${GREEN}    BlackArch repository is already configured. Skipping.${NC}"
fi

# 3. Install Tools by CyberChallenge Macro-Categories
echo "---  Step 3: Installing Tools by CTF Categories... ---"

# --- WEB SECURITY ---
# Splitting between pacman (official/blackarch) and yay (AUR)
echo "[*] Installing Web Security tools (Official & BlackArch)..."
sudo pacman -S --needed --noconfirm sqlmap seclists jq burpsuite 

# --- AUR TOOLS (ffuf & pup) ---
# Using yay for tools that often fail or are missing in standard repos.
echo "[*] Installing AUR-specific tools via yay..."
yay -S --needed --noconfirm ffuf-bin pup-bin

# --- NETWORK SECURITY ---
echo "[*] Installing Network Security tools..."
sudo pacman -S --needed --noconfirm nmap wireshark-qt tcpdump bind openbsd-netcat

# --- CRYPTOGRAPHY ---
echo "[*] Installing Cryptography tools..."
sudo pacman -S --needed --noconfirm john hashcat

# --- SOFTWARE SECURITY (Pwn & Reverse Engineering) ---
echo "[*] Installing Software Security tools..."
sudo pacman -S --needed --noconfirm gdb strace ltrace radare2 binwalk

# --- HARDWARE SECURITY ---
echo "[*] Installing Hardware Security tools..."
sudo pacman -S --needed --noconfirm minicom flashrom

# Setup Wireshark permissions
echo "---  Configuring Wireshark Permissions... ---"
sudo usermod -aG wireshark $USER

# --- Man page color configuration ---
MAN_COLORS="
# Man colors configuration
export LESS_TERMCAP_mb=$'\e[1;31m'
export LESS_TERMCAP_md=$'\e[1;36m'
export LESS_TERMCAP_me=$'\e[0m'
export LESS_TERMCAP_se=$'\e[0m'
export LESS_TERMCAP_so=$'\e[01;44;33m'
export LESS_TERMCAP_ue=$'\e[0m'
export LESS_TERMCAP_us=$'\e[1;32m'"

if ! grep -q "LESS_TERMCAP_mb" ~/.bashrc; then
    echo "$MAN_COLORS" >> ~/.bashrc
    echo "Man page colors configured."
fi

# --- Virtual Environment Setup for Python CTF Tools ---
echo "---  Step 4: Setting up Python Virtual Environment... ---"
if [ ! -d "venv" ]; then
    python -m venv venv
    echo -e "${GREEN}Virtual environment created.${NC}"
fi

echo "---  Installing Python tools in venv... ---"
./venv/bin/pip install --upgrade pip
./venv/bin/pip install exrex rstr requests scapy pwntools pycryptodome arjun dirsearch beautifulsoup4

# 5. Global Git Configuration
echo "---  Step 5: Configuring Global Git Settings... ---"
git config --global credential.helper store

# 6. Clean Cache
echo "---  Step 6: Cleaning Package Cache... ---"
sudo pacman -Sc --noconfirm

rm -f "$LOG_FILE"

# 7. Final Success Message
echo ""
echo "----------------------------------------------------------------"
echo -e "${GREEN}  ACCESS GRANTED. SYSTEM READY.${NC}"
echo -e "${GREEN}  ALL TOOLS INSTALLED SUCCESSFULLY.${NC}"
echo -e "${GREEN}  GLHF (Good Luck Have Fun) & HAPPY HACKING! 💀${NC}"
echo "----------------------------------------------------------------"

fastfetch

echo ""
echo " PYTHON VENV REMINDER:"
echo "To use your tools (like pwntools, arjun, bs4), run: source venv/bin/activate"