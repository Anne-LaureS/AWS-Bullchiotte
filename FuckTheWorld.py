import boto3

# --- Clients AWS (utilise tes credentials ~/.aws/credentials ou variables d'env) ---
ec2 = boto3.client('ec2', region_name='us-east-1')  # adapte la région
s3 = boto3.client('s3', region_name='us-east-1')

# --- EC2 ---
def list_ec2_instances():
    print("=== Liste des instances EC2 ===")
    instances = ec2.describe_instances()
    for res in instances['Reservations']:
        for inst in res['Instances']:
            print(f"ID: {inst['InstanceId']} | State: {inst['State']['Name']} | Type: {inst['InstanceType']}")

def launch_ec2_instance():
    response = ec2.run_instances(
        ImageId='ami-04b70fa74e45c3917',   # AMI Amazon Linux 2 (à jour, région us-east-1)
        InstanceType='t2.micro',
        MinCount=1, MaxCount=1,
        SecurityGroupIds=['sg-0123456789abcdef0'],  # Remplace par ton SG qui ouvre 22/80/5000
        KeyName='ProjetAhmedAWS-key'              # Remplace par ton nom de clé
    )
    instance_id = response['Instances'][0]['InstanceId']
    print(f"Instance lancée : {instance_id}")

# --- S3 ---
def list_s3_buckets():
    print("=== Liste des buckets S3 ===")
    buckets = s3.list_buckets()
    for bucket in buckets['Buckets']:
        print(f"Bucket: {bucket['Name']}")

def create_bucket_and_upload(bucket_name, file_path):
    print(f"Création du bucket {bucket_name} et upload de {file_path}")
    s3.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={'LocationConstraint': 'us-east-1'}
    )
    with open(file_path, 'rb') as f:
        s3.upload_fileobj(f, bucket_name, file_path.split('/')[-1])
    print("Upload terminé ✅")

def delete_bucket(bucket_name):
    print(f"Suppression du bucket {bucket_name}")
    # ⚠️ Supprimer d’abord les objets sinon erreur
    objects = s3.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in objects:
        for obj in objects['Contents']:
            s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
    s3.delete_bucket(Bucket=bucket_name)
    print("Bucket supprimé ✅")

# --- MAIN ---
if __name__ == "__main__":
    list_ec2_instances()
    list_s3_buckets()
    
    # Exemple d'usage (adapte si besoin) :
    # create_bucket_and_upload('projetahmedaws-bucket', 'file.txt')
    # delete_bucket('projetahmedaws-bucket')
    # launch_ec2_instance(
