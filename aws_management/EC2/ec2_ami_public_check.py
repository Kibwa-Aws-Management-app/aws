import boto3

# AWS 자격 증명 설정
aws_access_key_id = ''
aws_secret_access_key = ''
aws_region = 'ap-northeast-2'

# Boto3 클라이언트 생성
ec2_client = boto3.client('ec2', region_name=aws_region)

# 모든 AMI 이미지 가져오기
response = ec2_client.describe_images(Owners=['self'])

# AMI 이미지를 반복하며 공개 여부 확인
for ami in response['Images']:
    ami_id = ami['ImageId']
    is_public = ami['Public']

    if is_public:
        print(f"[FAIL] AMI 이미지 {ami_id}는 공개되어 있습니다.")
    else:
        print(f"[PASS] AMI 이미지 {ami_id}는 비공개입니다.")
