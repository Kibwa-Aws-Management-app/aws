# 암호 정책
import boto3
from boto3 import client
# from botocore.exceptions import ClientError

AWS_ACCESS_KEY_ID = 'your_access_key_id'
AWS_SECRET_ACCESS_KEY = 'your_secret_access_key'

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

iam_client = session.client('iam')


# # 새로운 안전한 비밀번호 정책
password_policy = {
    'MaxPasswordAge': 90,  # 90일 이내에 만료되도록 요구
    'PasswordReusePrevention': 24,  # 24회 이상 재사용 금지

    'MinimumPasswordLength': 14,  # 최소 길이 14자 요구
    'RequireSymbols': True,  # 특수 문자 사용 요구
    'RequireNumbers': True,  # 숫자 사용 요구
    'RequireUppercaseCharacters': True,  # 대문자 사용 요구
    'RequireLowercaseCharacters': True,  # 소문자 사용 요구

}

# # AWS IAM에서 비밀번호 정책을 업데이트
iam_client.update_account_password_policy(**password_policy)


# 각 사용자의 비밀번호가 잘 설정되어 있는지 확인하기
# 모든 IAM 사용자 목록 가져오기

users = iam_client.list_users()['Users']
warning = ''

# 비밀번호 길이 확인
# 최소 길이 14자 요구
for user in users:
    # 각 IAM 사용자의 비밀번호 정책 가져오기

    password_policy = iam_client.get_account_password_policy()[
        'PasswordPolicy']

    # 90일 이내에 만료되도록 요구
    if password_policy['MaxPasswordAge'] >= 90:
        warning = f"{user['UserName']} have to change password"
        print(warning)

    # 24회 이상 재사용 금지
    if password_policy['PasswordReusePrevention'] >= 24:
        warning = f"{user['UserName']}'s password has been reused more than 24 times."
        print(warning)

    # 비밀번호 최소 길이가 14 이상인지 확인하기
    if password_policy['MinimumPasswordLength'] < 14:
        warning = f"{user['UserName']}'s password is less than 14 characters"
        print(warning)

    # 특수 문자 사용 요구
    if password_policy['RequireSymbols'] == False:
        warning = "IAM password policy requires at least one symbol"
        print(warning)

    # 숫자 사용 요구
    if password_policy['RequireNumbers'] == False:
        warning = "IAM password policy requires at least one number"
        print(warning)

    # 대문자 사용 요구
    if password_policy['RequireUppercaseCharacters'] == False:
        warning = "IAM password policy requires at least one uppercase letter"
        print(warning)

    # 소문자 사용 요구
    if password_policy['RequireLowercaseCharacters'] == False:
        warning = "IAM password policy requires at least one lowercase letter"
        print(warning)
