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

### 💡 Troubleshooting Git in VS Code

If you encounter issues syncing from VS Code, follow these steps:

1. Click the **three dots** in the VS Code sidebar (Source Control) or open the **Terminal** from the top menu.
2. In the VS Code terminal, run the following commands:

```bash
git pull origin main --rebase
git push origin main

git config --global user.name "YourName"
git config --global user.email "YourEmail@email.com"

```

If the script is already present on your VM and you want to apply updates (such as a new command you've added), simply navigate to the directory (cd [...]), grant execution permission (chmod [...]), and run the .sh file

```bash
cd CyberChallenge-Tools
chmod +x setup.sh
./setup.sh
```

---

*Developed with ❤️ by **BadBoyEn***
