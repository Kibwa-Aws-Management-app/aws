import boto3

# AWS 자격 증명 설정
aws_access_key_id = ''
aws_secret_access_key = ''
aws_region = 'ap-northeast-2'

# Boto3 클라이언트 생성
ec2_client = boto3.client('ec2', region_name=aws_region)

# 모든 EBS 스냅샷 가져오기
response = ec2_client.describe_snapshots(OwnerIds=['self'])

# EBS 스냅샷을 반복하며 공개 여부 확인
for snapshot in response['Snapshots']:
    snapshot_id = snapshot['SnapshotId']
    is_public = snapshot['Public']

    if is_public:
        print(f"[FAIL] EBS 스냅샷 {snapshot_id}는 공개되어 있습니다.")
    else:
        print(f"[PASS] EBS 스냅샷 {snapshot_id}는 비공개입니다.")
