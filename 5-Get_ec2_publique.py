import boto3
import time

# --- Configuration ---
REGION = 'us-east-1'                  
SECURITY_GROUP_ID = 'sg-0fce9479219f5758d'
KEY_NAME = 'BadToGo'  # Nom de la key pair dans AWS

ec2 = boto3.client('ec2', region_name=REGION)

# --- Lancer l'instance ---
response = ec2.run_instances(
    ImageId='ami-04b70fa74e45c3917',  # Amazon Linux 2 (us-east-1)
    InstanceType='t2.micro',
    MinCount=1,
    MaxCount=1,
    KeyName=KEY_NAME,
    SecurityGroupIds=[SECURITY_GROUP_ID],
)

instance_id = response['Instances'][0]['InstanceId']
print(f"Instance lancée : {instance_id}")
print("Attente de l'attribution de l'IP publique...")

# --- Attendre que l'instance soit en running et récupérer l'IP publique ---
ec2_resource = boto3.resource('ec2', region_name=REGION)
instance = ec2_resource.Instance(instance_id)

while instance.state['Name'] != 'running':
    print("Instance pas encore en running, attente 5s...")
    time.sleep(5)
    instance.load()

print(f"Instance {instance_id} est running !")
print(f"IP publique : {instance.public_ip_address}")
