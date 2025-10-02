import os
import git
import shutil

def clone_repo_and_get_html(repo_url):
    repo_name = repo_url.split('/')[-1].replace('.git','')
    
    # Supprimer le repo si déjà cloné
    if os.path.exists(repo_name):
        shutil.rmtree(repo_name)
    
    # Cloner le repo
    repo = git.Repo.clone_from(repo_url, repo_name)
    
    # Récupérer les fichiers HTML
    html_files = []
    for root, dirs, files in os.walk(repo_name):
        for file in files:
            if file.endswith('.html'):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    html_files.append(f.read())
    return html_files
