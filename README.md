# 🛡️ CyberChallenge-Tools

Welcome to my personal laboratory for the **CyberChallenge.IT** competition. This repository contains my scripts, tools, and configurations used for CTFs (Capture The Flag) and cybersecurity training.

## 🛠️ Environment Setup
This repository is optimized for **Arch Linux**. I use a custom automation script to keep both my desktop and laptop environments synchronized.

### 🚀 Quick Start
To set up the environment on a new machine, simply run:
```bash
curl -s https://raw.githubusercontent.com/BadBoyEn/CyberChallenge-Tools/setup.sh | sudo bash

```
---

### 💡 Troubleshooting Ping / DNS ### 

1)ping -c 4 8.8.8.8

2)ping -c 4 google.com
->echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
->ping -c 4 google.com

---

### 💡 Troubleshooting Git in VS Code

If you encounter issues syncing from VS Code, follow these steps:

1. Click the **three dots** in the VS Code sidebar (Source Control) or open the **Terminal** from the top menu.
2. In the VS Code terminal, run the following commands:

```bash
git pull origin main --rebase
git push origin main

git config --global user.name "YourName"
git config --global user.email "YourEmail@email.com"

sudo systemctl start docker.service

```

If the script is already present on your VM and you want to apply updates (such as a new command you've added), simply navigate to the directory (cd [...]), grant execution permission (chmod [...]), and run the .sh file

```bash
cd CyberChallenge-Tools
chmod +x setup.sh
./setup.sh
```


Shortcut for gnu readline: [da tradurre]
-> Inizio comando, ctrl + a
-> fine comando, ctrl + e
-> Elimino ciò che sta post il cursore, ctrl + k
-> Elimina la prola precedente, ctrl + w
-> Pulire il terminale, digitare "clear" oppure ctrl + l
-> ctrl + r

---

*Developed with ❤️ by **BadBoyEn***
