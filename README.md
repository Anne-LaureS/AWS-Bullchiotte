# 🌩️ AWS – Déploiement d’un site statique sur EC2 avec Nginx  
![AWS](https://img.shields.io/badge/AWS-Cloud-orange?logo=amazonaws)
![EC2](https://img.shields.io/badge/EC2-Amazon_Linux_2-blue)
![S3](https://img.shields.io/badge/S3-Storage-red)
![IAM](https://img.shields.io/badge/IAM-Permissions-yellow)
![VPC](https://img.shields.io/badge/VPC-Networking-green)
![Status](https://img.shields.io/badge/Status-Fonctionnel-brightgreen)

---

## 🎯 Présentation  
Ce TP explore plusieurs briques fondamentales d’AWS à travers la mise en place d’un **site web statique** hébergé sur une instance **EC2 Amazon Linux**, servie par **Nginx**, et alimentée par des fichiers provenant d’un **repo GitHub**.

Il inclut également des manipulations via **AWS CLI** et **Boto3**, notamment :

- gestion d’instances EC2  
- gestion de buckets S3  
- interaction avec IAM  
- exploration du réseau AWS (VPC, subnets, route tables, IGW)  
- scripts automatisés pour déployer et mettre à jour le site  

---

## 🧩 Architecture globale
```
┌──────────────────────────────┐
│            AWS VPC           │
│        10.0.0.0/16           │
│                              │
Internet        │   │   ┌──────────────────────┐    
│               │   │   Public Subnet      │    │
│               │   │     10.0.1.0/24      │    │
▼               │   │                      │    │
┌──────────────┐        │   │  EC2 Amazon Linux    │    │
│  Client Web  │──────▶│   │  + Nginx             │    │
└──────────────┘        │   │  + Git clone repo    │    │
│   └──────────┬───────────┘     │
│              │                 │
│        Security Group          │
│        (port 80 ouvert)        │
│              │                 │
│        Internet Gateway        │
└──────────────┴─────────────────┘
```

- S3 : stockage / tests via scripts Python
- IAM : permissions pour EC2 & S3
- AWS CLI : gestion EC2 / S3 / EBS

---

## ⚙️ Prérequis

- Compte AWS avec permissions sur EC2 et S3.  
- Clé SSH (PEM/PPK) pour se connecter à l’instance.  
- Git installé sur l’instance EC2.  
- Nginx installé sur l’instance EC2.  
- Python 3 et Boto3 pour exécuter les scripts.

---
## 📁 Contenu du repo
## 🐍 Scripts principaux 

### 🔹 Scripts Python (Boto3)
- **1-FuckBienLaTerre.py**  
  - liste les instances EC2  
  - liste les buckets S3  
  - crée un bucket S3  
  - upload de fichiers  
  - suppression de bucket  

- **5-Get_ec2_publique.py**  
  - récupère l’adresse IP publique d’une instance EC2  

### 🔹 Script Shell
- **4-Setup_Nginx.sh**  
  - installe Nginx  
  - configure le serveur web  
  - prépare l’environnement pour servir le site  

### 🔹 Fichiers Web
- **index.html**, **Repo.html**, **7-IndexRedirection.html**  
  - pages statiques servies par Nginx  

---

## ⚙️ Déploiement du site web sur EC2

### 1) Lancer une instance EC2 Amazon Linux 2  
- Type : t2.micro  
- Security Group : port **80** ouvert  
- Stockage : EBS 8–10 Go  
- IAM Role : accès S3 (si nécessaire)

### 2) Installer Nginx  
```bash
sudo yum update -y
sudo amazon-linux-extras install nginx1 -y
sudo systemctl enable nginx
sudo systemctl start nginx
```

---

## 🛠️ Installation & Déploiement

1. **Cloner le repo sur votre instance EC2 :**
```
cd /usr/share/nginx/html
sudo git clone https://github.com/Anne-LaureS/AWS-Bullchiotte.git
```

2. **Configurer Nginx pour pointer vers le dossier cloné :**
```
server {
    listen 80;
    server_name <YOUR_PUBLIC_IP>;
    root /usr/share/nginx/html/AWS-Bullchiotte;
    index index.html;
    location / {
        try_files $uri $uri/ =404;
    }
}
```

3. **Tester la configuration et redémarrer Nginx :**
```
sudo nginx -t
sudo systemctl restart nginx
```

---

## 💬 Accéder au site via navigateur
```
http://<YOUR_PUBLIC_IP>/
```

---

5. **Exécuter les scripts Python :**
**Lister les instances EC2**
```
python 1-FuckBienLaTerre.py
```

**Créer un bucket S3**
```
python3 1-FuckBienLaTerre.py create-bucket mon-bucket-test
```

**Récupérer l’IP publique d’une instance**
```
python3 5-Get_ec2_publique.py
```

---

## 📬 Contact

Pour plus d’infos ou questions : [Mon GitHub](https://github.com/Anne-LaureS)
