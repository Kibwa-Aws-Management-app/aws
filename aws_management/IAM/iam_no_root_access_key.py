import boto3

# AWS 자격 증명 설정
aws_access_key_id = ''
aws_secret_access_key = ''
aws_region = 'ap-northeast-2'  # 사용자 지정 리전 설정 (원하는 리전으로 변경하세요)

# Boto3 클라이언트 생성
iam_client = boto3.client('iam', region_name=aws_region)

# Root 계정의 액세스 키 확인

try:
    response = iam_client.get_access_key_last_used(UserName='root')
    if 'AccessKeyLastUsed' in response:
        print("[경고] Root 계정에 액세스 키가 있습니다. 이것은 보안 위험을 초래할 수 있습니다.")
    else:
        print("Root 계정에는 액세스 키가 없으므로 안전합니다.")
except Exception as e:
    print("Root 계정에 액세스 키가 없거나 IAM 서비스에 액세스할 수 없습니다. 수동으로 확인해주세요.")
