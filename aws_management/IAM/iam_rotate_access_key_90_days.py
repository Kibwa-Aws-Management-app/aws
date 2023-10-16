import boto3
from datetime import datetime, timedelta, timezone

# AWS 자격 증명 설정
aws_access_key_id = ''
aws_secret_access_key = ''
aws_region = 'ap-northeast-2'  # 사용자 지정 리전 설정

# Boto3 클라이언트 생성
iam_client = boto3.client('iam', region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# IAM 사용자의 비밀 액세스 키 확인
access_key_id = 'AKIAUPLQBCHXMSGQK4MV'  # 확인할 IAM 사용자의 액세스 키 ID
response = iam_client.get_access_key_last_used(AccessKeyId=access_key_id)

if 'AccessKeyLastUsed' in response and 'LastUsedDate' in response['AccessKeyLastUsed']:
    last_used_date = response['AccessKeyLastUsed']['LastUsedDate']
    current_date = datetime.now(timezone.utc)  # "offset-aware"한 시간으로 만듭니다.
    rotation_threshold = timedelta(days=90)  # 비밀 액세스 키가 90일 이상 사용되었을 때 순환해야 함
    rotation_date = last_used_date + rotation_threshold

    if current_date > rotation_date:
        print(f"[!!경고!!] {access_key_id} 엑세스 키는 90일 이상 사용되었습니다. 마지막 사용 날짜는 {last_used_date}입니다. 엑세스 키를 순환해야 합니다.")
    else:
        print(f"{access_key_id} 엑세스 키는 90일 이내에 사용되었으므로 여전히 유효합니다. 마지막 사용 날짜는 {last_used_date}입니다.")
else:
    print(f"{access_key_id} 엑세스 키는 아직 사용된 적이 없습니다.")
