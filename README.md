Bienvenue sur le repo **AWS-Bullchiotte**  

Ce projet illustre la mise en place d'un site web statique sur une instance **EC2 Amazon Linux** avec **Nginx**, en utilisant un repo GitHub comme source du contenu HTML.  

📌 Objectifs
- Démontrer le déploiement d’un site web statique sur AWS EC2.  
- Utiliser **Nginx** pour servir des fichiers HTML/CSS/JS.  
- Automatiser le clonage et la mise à jour depuis GitHub.  
- Bonus : permettre de visualiser directement le contenu du repo sur un navigateur public.
  
⚙️ Prérequis
- Compte AWS avec permission de créer une instance EC2.  
- Clé SSH (PEM/PPK) pour se connecter à l’instance.  
- Git installé sur l’instance EC2.  
- Nginx installé sur l’instance EC2.
  
---
🛠️ Installation & Déploiement
1. Cloner le repo sur votre instance EC2 :
cd /usr/share/nginx/html
git clone https://github.com/Anne-LaureS/AWS-Bullchiotte.git

2. Configurer Nginx pour pointer vers le dossier cloné :
server {
    listen 80;
    server_name <YOUR_PUBLIC_IP>;

    root /usr/share/nginx/html/AWS-Bullchiotte;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}

3. Tester la configuration et redémarrer Nginx :
sudo nginx -t
sudo systemctl restart nginx

4. Accéder au site via navigateur :
http://<YOUR_PUBLIC_IP>/

---

💡 Bonnes pratiques
* Tous les fichiers que vous voulez rendre visibles doivent être dans le repo.
* Pour mettre à jour le site : `git pull origin main` dans le dossier cloné sur l’EC2.
* Toujours vérifier la configuration Nginx avant de redémarrer : `sudo nginx -t`.
* 
---

## 📬 Contact

Pour plus d’infos ou questions : [Mon GitHub](https://github.com/Anne-LaureS)
```
