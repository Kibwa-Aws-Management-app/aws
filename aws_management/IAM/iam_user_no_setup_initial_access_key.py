import boto3

# AWS 자격 증명 설정
aws_access_key_id = ''
aws_secret_access_key = ''
aws_region = 'ap-northeast-2'  # 사용자 지정 리전 설정

# Boto3 클라이언트 생성
iam_client = boto3.client('iam', region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# 사용자의 액세스 키 설정 확인
try:
    response = iam_client.list_access_keys()
    access_keys = response.get('AccessKeyMetadata', [])
    
    if len(access_keys) == 0:
        print("사용자의 액세스 키가 설정되지 않았으므로 초기 액세스 키를 설정해야 합니다.")
    else:
        print("사용자의 액세스 키가 설정되어 있습니다. 이것은 보안 위험을 초래할 수 있습니다.")
except Exception as e:
    print("사용자의 액세스 키 설정 여부를 확인할 수 없습니다. IAM 서비스에 액세스할 수 있는 권한이 있는지 확인하세요.")
