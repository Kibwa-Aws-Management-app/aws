import boto3

# AWS 자격 증명 설정
aws_access_key_id = ''
aws_secret_access_key = ''
aws_region = 'ap-northeast-2'

# Boto3 클라이언트 생성
ec2_client = boto3.client('ec2', region_name=aws_region)

# 모든 EBS 볼륨 가져오기
response = ec2_client.describe_volumes()

# EBS 볼륨을 반복하며 암호화 설정 여부 확인
for volume in response['Volumes']:
    volume_id = volume['VolumeId']
    is_encrypted = volume['Encrypted']

    if is_encrypted:
        print(f"[PASS] EBS 볼륨 {volume_id}는 암호화가 활성화되어 있습니다.")
    else:
        print(f"[FAIL] EBS 볼륨 {volume_id}는 암호화가 비활성화되어 있습니다.")
