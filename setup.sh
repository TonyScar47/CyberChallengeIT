#!/bin/bash

# ==============================================================================
# ARCH LINUX AUTOMATION SETUP FOR CYBERCHALLENGE (V5 - HARDENED SETUP)
# ------------------------------------------------------------------------------
# IDEMPOTENT SCRIPT: Safe to run multiple times.
# STRICT MODE: Script aborts immediately if any command fails.
# NETWORK CONNECTIVITY CHECK.
# ==============================================================================

# Define Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# --- LOGGING SETUP ---
LOG_FILE="setup_error.log"
> "$LOG_FILE"
exec > >(tee -a "$LOG_FILE") 2>&1

trap 'echo -e "\n${RED}[!] CRITICAL ERROR: Automation aborted. Check log file: ${LOG_FILE}${NC}\n"' ERR

set -euo pipefail

echo "--- STARTING AUTOMATION: IDEMPOTENT SETUP ---"

# ------------------------------------------------------------------------------
# NETWORK CHECK
# ------------------------------------------------------------------------------
echo "--- Checking Internet connectivity... ---"
if ! ping -c 1 archlinux.org &> /dev/null; then
    echo -e "${RED}[!] No Internet connection detected. Aborting.${NC}"
    exit 1
fi
echo -e "${GREEN}Network OK.${NC}"

# ------------------------------------------------------------------------------
# ROOT / SUDO MANAGEMENT
# ------------------------------------------------------------------------------
echo "--- Checking sudo privileges... ---"

if [ "$EUID" -eq 0 ]; then
    echo -e "${RED}[!] Do not run this script as root. Run as normal user.${NC}"
    exit 1
fi

echo "[*] Requesting sudo password once..."
sudo -v

# keep sudo alive
while true; do sudo -n true; sleep 60; kill -0 "$$" || exit; done 2>/dev/null &

# ------------------------------------------------------------------------------
# KEYRING UPDATE (CRITICAL FOR ARCH)
# ------------------------------------------------------------------------------
echo "--- Step 0: Updating Arch keyring... ---"
sudo pacman -Sy --noconfirm archlinux-keyring

# ------------------------------------------------------------------------------
# SYSTEM UPDATE
# ------------------------------------------------------------------------------
echo "--- Step 1: Updating System... ---"
sudo pacman -Su --noconfirm

# ------------------------------------------------------------------------------
# CORE DOCUMENTATION
# ------------------------------------------------------------------------------
echo "--- Step 1.5: Installing Core Documentation (man pages)... ---"
sudo pacman -S --needed --noconfirm man-db man-pages

# ------------------------------------------------------------------------------
# BASE SYSTEM & DEV
# ------------------------------------------------------------------------------
echo "[*] Installing Base & Dev tools..."
sudo pacman -S --needed --noconfirm \
git base-devel code python python-pip fastfetch \
virtualbox-guest-utils docker docker-compose \
cmake curl tmux zip unzip

# ------------------------------------------------------------------------------
# DOCKER FULL SETUP
# ------------------------------------------------------------------------------
echo "--- Configuring Docker... ---"

sudo systemctl enable docker.service
sudo systemctl start docker.service

if ! groups $USER | grep &>/dev/null docker; then
    sudo usermod -aG docker $USER
    echo "User added to docker group (logout required)."
fi

# ------------------------------------------------------------------------------
# INSTALL YAY (ROBUST VERSION)
# ------------------------------------------------------------------------------
echo "--- Step 1.75: Installing yay (AUR Helper)... ---"

if ! command -v yay &> /dev/null; then
    echo "[*] yay not found. Installing from AUR..."

    ORIGINAL_DIR=$(pwd)
    BUILD_DIR=$(mktemp -d)

    git clone https://aur.archlinux.org/yay-bin.git "$BUILD_DIR/yay-bin"
    cd "$BUILD_DIR/yay-bin"

    makepkg -si --noconfirm

    cd "$ORIGINAL_DIR"
    rm -rf "$BUILD_DIR"

    echo -e "${GREEN}yay installed successfully.${NC}"
else
    echo -e "${GREEN}yay already installed.${NC}"
fi

# ------------------------------------------------------------------------------
# BLACKARCH REPOSITORY
# ------------------------------------------------------------------------------
echo "--- Step 2: Configuring BlackArch Repository... ---"

if ! grep -q "\[blackarch\]" /etc/pacman.conf; then
    echo "Downloading and executing BlackArch strap.sh..."

    curl -O https://blackarch.org/strap.sh
    chmod +x strap.sh
    sudo ./strap.sh

    sudo pacman -Syu --noconfirm

    rm strap.sh

    echo -e "${GREEN}BlackArch repository configured.${NC}"
else
    echo -e "${GREEN}BlackArch repository already configured.${NC}"
fi

# ------------------------------------------------------------------------------
# CTF TOOLS INSTALLATION
# ------------------------------------------------------------------------------
echo "--- Step 3: Installing Tools by CTF Categories... ---"

# WEB SECURITY
echo "[*] Installing Web Security tools..."
sudo pacman -S --needed --noconfirm \
sqlmap seclists jq burpsuite

# AUR TOOLS
echo "[*] Installing AUR tools via yay..."
yay -S --needed --noconfirm ffuf-bin pup-bin

# NETWORK SECURITY
echo "[*] Installing Network Security tools..."
sudo pacman -S --needed --noconfirm \
nmap wireshark-qt tcpdump bind openbsd-netcat

# CRYPTOGRAPHY
echo "[*] Installing Cryptography tools..."
sudo pacman -S --needed --noconfirm john hashcat

# SOFTWARE SECURITY
echo "[*] Installing Software Security tools..."
sudo pacman -S --needed --noconfirm \
gdb strace ltrace radare2 binwalk

# HARDWARE SECURITY
echo "[*] Installing Hardware Security tools..."
sudo pacman -S --needed --noconfirm \
minicom flashrom

# ------------------------------------------------------------------------------
# WIRESHARK PERMISSIONS
# ------------------------------------------------------------------------------
echo "--- Configuring Wireshark Permissions... ---"
sudo usermod -aG wireshark $USER

# ------------------------------------------------------------------------------
# MAN PAGE COLORS
# ------------------------------------------------------------------------------
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

# ------------------------------------------------------------------------------
# PYTHON VIRTUAL ENVIRONMENT
# ------------------------------------------------------------------------------
echo "--- Step 4: Setting up Python Virtual Environment... ---"

if [ ! -d "venv" ]; then
    python -m venv venv
    echo -e "${GREEN}Virtual environment created.${NC}"
fi

echo "--- Installing Python tools in venv ---"

./venv/bin/pip install --upgrade pip
./venv/bin/pip install \
exrex rstr requests scapy pwntools \
pycryptodome arjun dirsearch beautifulsoup4

# ------------------------------------------------------------------------------
# GLOBAL GIT CONFIG
# ------------------------------------------------------------------------------
echo "--- Step 5: Configuring Global Git Settings... ---"

git config --global credential.helper store

# ------------------------------------------------------------------------------
# CLEAN CACHE
# ------------------------------------------------------------------------------
echo "--- Step 6: Cleaning Package Cache... ---"

sudo pacman -Sc --noconfirm

rm -f "$LOG_FILE"

# ------------------------------------------------------------------------------
# FINAL MESSAGE
# ------------------------------------------------------------------------------
echo ""
echo "----------------------------------------------------------------"
echo -e "${GREEN} ACCESS GRANTED. SYSTEM READY.${NC}"
echo -e "${GREEN} ALL TOOLS INSTALLED SUCCESSFULLY.${NC}"
echo -e "${GREEN} GLHF (Good Luck Have Fun) & HAPPY HACKING! 💀${NC}"
echo "----------------------------------------------------------------"

fastfetch

echo ""
echo "PYTHON VENV REMINDER:"
echo "To use your tools run:"
echo "source venv/bin/activate"
