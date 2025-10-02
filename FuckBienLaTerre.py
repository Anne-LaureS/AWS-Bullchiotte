import boto3
import os

# ===== CONFIG =====
REGION = "us-east-1"   # ⚡ change si besoin (ex: "eu-west-3" pour Paris)

# Clients AWS
ec2 = boto3.client("ec2", region_name=REGION)
s3 = boto3.client("s3", region_name=REGION)


# ===== EC2 =====
def list_ec2_instances():
    print("=== Liste des instances EC2 ===")
    instances = ec2.describe_instances()
    for res in instances["Reservations"]:
        for inst in res["Instances"]:
            print(f"ID: {inst['InstanceId']} | State: {inst['State']['Name']} | Type: {inst['InstanceType']}")


# ===== S3 =====
def list_s3_buckets():
    print("=== Liste des buckets S3 ===")
    buckets = s3.list_buckets()
    for bucket in buckets["Buckets"]:
        print(f"Bucket: {bucket['Name']}")


def create_bucket_and_upload(bucket_name, file_path):
    print(f"Création du bucket {bucket_name} et upload de {file_path}...")

    # Création du bucket (avec région)
    if REGION == "us-east-1":
        # Particularité : us-east-1 ne doit PAS avoir de LocationConstraint
        s3.create_bucket(Bucket=bucket_name)
    else:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": REGION}
        )

    # Upload du fichier
    with open(file_path, "rb") as f:
        s3.upload_fileobj(f, bucket_name, os.path.basename(file_path))

    print("✅ Bucket créé et fichier uploadé.")


def delete_bucket(bucket_name):
    print(f"Suppression du bucket {bucket_name}...")

    # Supprimer d'abord les objets
    objects = s3.list_objects_v2(Bucket=bucket_name)
    if "Contents" in objects:
        for obj in objects["Contents"]:
            s3.delete_object(Bucket=bucket_name, Key=obj["Key"])

    s3.delete_bucket(Bucket=bucket_name)
    print("✅ Bucket supprimé.")


# ===== MENU =====
def menu():
    while True:
        print("\n===== FuckBienLaTerre Menu =====")
        print("1. Lister les instances EC2")
        print("2. Lister les buckets S3")
        print("3. Créer un bucket et uploader un fichier")
        print("4. Supprimer un bucket")
        print("5. Quitter")

        choice = input("👉 Choisis une option : ")

        if choice == "1":
            list_ec2_instances()
        elif choice == "2":
            list_s3_buckets()
        elif choice == "3":
            bucket_name = input("Nom du bucket à créer : ")
            file_path = input("Chemin du fichier à uploader : ")
            create_bucket_and_upload(bucket_name, file_path)
        elif choice == "4":
            bucket_name = input("Nom du bucket à supprimer : ")
            delete_bucket(bucket_name)
        elif choice == "5":
            print("Bye 👋")
            break
        else:
            print("❌ Option invalide.")


if __name__ == "__main__":
    menu()
