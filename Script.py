from flask import Flask, render_template, request, redirect
import boto3
import os
import git
import shutil

app = Flask(__name__)

# ------------------------------
# CONFIGURATION AWS
# ------------------------------

ec2 = boto3.client('ec2', 'us-east-1')
s3 = boto3.client('s3', 'us-east-1')

# ------------------------------
# UTILITAIRES
# ------------------------------
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

# ------------------------------
# ROUTES FLASK
# ------------------------------
@app.route('/')
def index():
    # Lister instances EC2
    try:
        instances = ec2.describe_instances()
        instance_list = []
        for res in instances['Reservations']:
            for i in res['Instances']:
                instance_list.append({
                    'id': i['InstanceId'],
                    'state': i['State']['Name'],
                    'type': i['InstanceType'],
                    'public_ip': i.get('PublicIpAddress', 'N/A')
                })
    except Exception as e:
        instance_list = f"Erreur récupération EC2: {e}"

    # Lister buckets S3
    try:
        buckets = s3.list_buckets()['Buckets']
    except Exception as e:
        buckets = f"Erreur récupération S3: {e}"
    
    return render_template('index.html', instances=instance_list, buckets=buckets)

@app.route('/create_bucket', methods=['POST'])
def create_bucket():
    bucket_name = request.form['bucket_name']
    try:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': REGION}
        )
    except Exception as e:
        return f"Erreur création bucket: {e}"
    return redirect('/')

@app.route('/delete_bucket', methods=['POST'])
def delete_bucket():
    bucket_name = request.form['bucket_name']
    try:
        s3.delete_bucket(Bucket=bucket_name)
    except Exception as e:
        return f"Erreur suppression bucket: {e}"
    return redirect('/')

@app.route('/upload_file', methods=['POST'])
def upload_file():
    bucket_name = request.form['bucket_name']
    file = request.files['file']
    try:
        s3.upload_fileobj(file, bucket_name, file.filename)
    except Exception as e:
        return f"Erreur upload: {e}"
    return redirect('/')

@app.route('/launch_instance', methods=['POST'])
def launch_instance():
    try:
        instance = ec2.run_instances(
            ImageId='ami-0c02fb55956c7d316',  # Amazon Linux 2 us-east-1
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            SecurityGroups=['default']  # Vérifie que le SG permet SSH
        )
    except Exception as e:
        return f"Erreur lancement instance: {e}"
    return redirect('/')

@app.route('/clone_repo', methods=['POST'])
def clone_repo():
    repo_url = request.form['repo_url']
    try:
        html_files = clone_repo_and_get_html(repo_url)
    except Exception as e:
        return f"Erreur clonage repo: {e}"
    return render_template('repo.html', html_files=html_files)

# ------------------------------
# LANCEMENT FLASK
# ------------------------------
if __name__ == '__main__':
    # Flask écoute sur toutes les interfaces pour accès public
    app.run(host='0.0.0.0', port=5000, debug=True)
