Bienvenue sur le repo **AWS-Bullchiotte**  

Ce projet illustre la mise en place d'un site web statique sur une instance **EC2 Amazon Linux** avec **Nginx**, en utilisant un repo GitHub comme source du contenu HTML.  

# AWS-Bullchiotte

📌 Objectifs
- Démontrer le déploiement d’un site web statique sur AWS EC2.  
- Utiliser **Nginx** pour servir des fichiers HTML/CSS/JS.  
- Automatiser le clonage et la mise à jour depuis GitHub.  
- Bonus : permettre de visualiser directement le contenu du repo sur un navigateur public.  
- Fournir des scripts Python pour interagir avec AWS (EC2, S3).

---

🐍 Scripts principaux 
`1-FuckBienLaTerre.py`

Ce script permet de gérer des ressources AWS via **Boto3** :

- Lister toutes les instances **EC2**.  
- Lister tous les **buckets S3**.  
- Créer un bucket S3 et y uploader des fichiers.  
- Supprimer un bucket S3 existant.

> ⚠️ Nécessite une configuration AWS valide (`~/.aws/credentials`) avec des droits suffisants.

---

⚙️ Prérequis

- Compte AWS avec permissions sur EC2 et S3.  
- Clé SSH (PEM/PPK) pour se connecter à l’instance.  
- Git installé sur l’instance EC2.  
- Nginx installé sur l’instance EC2.  
- Python 3 et Boto3 pour exécuter les scripts.

---

## 🛠️ Installation & Déploiement

1. **Cloner le repo sur votre instance EC2 :**

cd /usr/share/nginx/html
git clone https://github.com/Anne-LaureS/AWS-Bullchiotte.git

2. **Configurer Nginx pour pointer vers le dossier cloné :**

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

sudo nginx -t
sudo systemctl restart nginx

4. **Accéder au site via navigateur :**

http://<YOUR_PUBLIC_IP>/
```

5. **Exécuter les scripts Python :**

python3 1-FuckBienLaTerre.py
```

---

## 📁 Structure du repo

```
AWS-Bullchiotte/
│
├─ index.html          # Page principale du site
├─ style.css           # Feuille de style CSS
├─ 1-FuckBienLaTerre.py  # Script pour gérer EC2 et S3
├─ scripts/            # Scripts JS (si applicable)
└─ README.md           # Ce fichier
```

---

## 💡 Bonnes pratiques

* Tous les fichiers que vous voulez rendre visibles doivent être dans le repo.
* Pour mettre à jour le site : `git pull origin main` dans le dossier cloné sur l’EC2.
* Toujours vérifier la configuration Nginx avant de redémarrer : `sudo nginx -t`.
* Pour le script Python, veillez à avoir les permissions nécessaires sur AWS.

## 📬 Contact

Pour plus d’infos ou questions : [Mon GitHub](https://github.com/Anne-LaureS)
```
