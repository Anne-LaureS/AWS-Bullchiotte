import boto3

# Clients AWS
ec2 = boto3.client('ec2', region_name='us-east-1')
s3 = boto3.client('s3', region_name='us-east-1')

def lister_ec2():
    print("\n=== Liste des instances EC2 ===")
    instances = ec2.describe_instances()
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            print(f"ID: {instance['InstanceId']} | State: {instance['State']['Name']} | Type: {instance['InstanceType']}")

def lister_s3():
    print("\n=== Liste des buckets S3 ===")
    buckets = s3.list_buckets()
    for bucket in buckets['Buckets']:
        print(f"- {bucket['Name']}")

def creer_bucket():
    bucket_name = input("Nom du bucket à créer : ")
    try:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': boto3.session.Session().region_name}
        )
        print(f"✅ Bucket '{bucket_name}' créé avec succès.")
        fichier = input("Chemin du fichier à uploader (laisser vide pour ignorer) : ")
        if fichier:
            key = fichier.split("/")[-1]
            s3.upload_file(fichier, bucket_name, key)
            print(f"📂 Fichier '{fichier}' uploadé dans '{bucket_name}'")
    except Exception as e:
        print(f"❌ Erreur : {e}")

def supprimer_bucket():
    bucket_name = input("Nom du bucket à supprimer : ")
    try:
        # Vider le bucket avant suppression
        objets = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in objets:
            for obj in objets['Contents']:
                s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
            print(f"🗑 Bucket '{bucket_name}' vidé.")
        
        s3.delete_bucket(Bucket=bucket_name)
        print(f"✅ Bucket '{bucket_name}' supprimé avec succès.")
    except Exception as e:
        print(f"❌ Erreur : {e}")

def menu():
    while True:
        print("\n===== FuckBienLeWorld Menu =====")
        print("1. Lister les instances EC2")
        print("2. Lister les buckets S3")
        print("3. Créer un bucket et uploader un fichier")
        print("4. Supprimer un bucket")
        print("5. Quitter")
        
        choix = input("👉 Choisis une option : ")

        if choix == "1":
            lister_ec2()
        elif choix == "2":
            lister_s3()
        elif choix == "3":
            creer_bucket()
        elif choix == "4":
            supprimer_bucket()
        elif choix == "5":
            print("Bye 👋 FuckBienLeWorld.py terminé.")
            break
        else:
            print("⚠️ Choix invalide, réessaye !")

if __name__ == "__main__":
    menu()
