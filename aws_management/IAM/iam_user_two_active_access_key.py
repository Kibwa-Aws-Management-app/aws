import boto3

# AWS 자격 증명 설정
aws_access_key_id = ''
aws_secret_access_key = ''
aws_region = 'ap-northeast-2'  # 사용자 지정 리전 설정

# Boto3 클라이언트 생성
iam_client = boto3.client('iam', region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# 사용자의 활성 액세스 키 확인
try:
    response = iam_client.list_access_keys()
    access_keys = response.get('AccessKeyMetadata', [])
    
    if len(access_keys) >= 2:
        print("사용자는 두 개 이상의 활성 액세스 키를 가지고 있습니다. Pass.")
    else:
        print("사용자는 하나 이하의 활성 액세스 키만 가지고 있습니다. Fail.")
except Exception as e:
    print("사용자의 활성 액세스 키를 확인할 수 없습니다. IAM 서비스에 액세스할 수 있는 권한이 있는지 확인하세요.")
