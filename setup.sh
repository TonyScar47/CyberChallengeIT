#!/bin/bash

# ==============================================================================
# ARCH LINUX AUTOMATION SETUP FOR CYBERCHALLENGE
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

# 1. System Update & Mirror Optimization
echo "---  Step 1: Updating System & Optimizing Mirrors... ---"
sudo pacman -Syu --noconfirm
# Install reflector to automate the selection of the fastest/most up-to-date mirrors
sudo pacman -S --needed --noconfirm reflector
sudo reflector --latest 10 --protocol https --sort rate --save /etc/pacman.d/mirrorlist

# 1.5. Core Documentation (Guaranteed Installation)
echo "---  Step 1.5: Installing Core Documentation (man pages)... ---"
sudo pacman -S --needed --noconfirm man-db man-pages

# 2. Install Tools by CyberChallenge Macro-Categories
echo "---  Step 2: Installing Tools by CTF Categories... ---"

# --- BASE SYSTEM & DEV ---
echo "[*] Installing Base & Dev tools..."
sudo pacman -S --needed --noconfirm git base-devel code python python-pip fastfetch virtualbox-guest-utils docker-compose cmake

# --- WEB SECURITY ---
echo "[*] Installing Web Security tools (Official Repos)..."
sudo pacman -S --needed --noconfirm sqlmap seclists jq burpsuite

# --- AUR PACKAGES (ffuf) ---
echo "[*] Installing Web Security tools (AUR - ffuf)..."
if ! command -v ffuf &> /dev/null; then
    echo "    Cloning and building ffuf from AUR..."
    ORIGINAL_DIR=$(pwd)
    BUILD_DIR=$(mktemp -d)
    cd "$BUILD_DIR"
    
    git clone https://aur.archlinux.org/ffuf-bin.git
    cd ffuf-bin
    
    makepkg -si --noconfirm
    
    cd "$ORIGINAL_DIR"
    rm -rf "$BUILD_DIR"
    echo -e "${GREEN}    ffuf installed successfully.${NC}"
else
    echo -e "${GREEN}    ffuf is already installed. Skipping.${NC}"
fi

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
echo "---  Step 3: Setting up Python Virtual Environment... ---"
if [ ! -d "venv" ]; then
    python -m venv venv
    echo -e "${GREEN}Virtual environment created.${NC}"
fi

echo "---  Installing Python tools in venv... ---"
./venv/bin/pip install --upgrade pip
./venv/bin/pip install exrex rstr requests scapy pwntools pycryptodome arjun dirsearch

# 4. Global Git Configuration
echo "---  Step 4: Configuring Global Git Settings... ---"
git config --global credential.helper store

# 5. Clean Cache
echo "---  Step 5: Cleaning Package Cache... ---"
sudo pacman -Sc --noconfirm

rm -f "$LOG_FILE"

# 6. Final Success Message
echo ""
echo "----------------------------------------------------------------"
echo -e "${GREEN}  ACCESS GRANTED. SYSTEM READY.${NC}"
echo -e "${GREEN}  ALL TOOLS INSTALLED SUCCESSFULLY.${NC}"
echo -e "${GREEN}  GLHF (Good Luck Have Fun) & HAPPY HACKING! 💀${NC}"
echo "----------------------------------------------------------------"

fastfetch

echo ""
echo " PYTHON VENV REMINDER:"
echo "To use your tools (like pwntools, arjun, dirsearch), run: source venv/bin/activate"
echo "then run: deactivate"
