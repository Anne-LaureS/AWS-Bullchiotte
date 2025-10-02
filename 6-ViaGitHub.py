import os
import subprocess

# --- Configuration ---
EC2_PUBLIC_IP = "18.212.255.63"
GITHUB_REPO = "https://github.com/Anne-LaureS/AWS-Bullchiotte.git"
WEB_DIR = "/var/www/html/AWS-Bullchiotte"

# --- Installer Git et Nginx ---
subprocess.run("sudo dnf install -y git nginx", shell=True, check=True)

# --- Cloner le repo ---
if not os.path.exists(WEB_DIR):
    subprocess.run(f"sudo git clone {GITHUB_REPO} {WEB_DIR}", shell=True, check=True)
else:
    print(f"{WEB_DIR} existe déjà, mise à jour du repo...")
    subprocess.run(f"cd {WEB_DIR} && sudo git pull", shell=True, check=True)

# --- Démarrer Nginx ---
subprocess.run("sudo systemctl enable nginx", shell=True, check=True)
subprocess.run("sudo systemctl start nginx", shell=True, check=True)

print(f"Le repo est cloné dans {WEB_DIR}")
print(f"Tu peux voir ton site à l'adresse : http://{EC2_PUBLIC_IP}/AWS-Bullchiotte")
