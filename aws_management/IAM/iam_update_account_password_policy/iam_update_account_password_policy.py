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


# IAM 비밀번호 정책
def iam_update_account_password_policy(users):
    for user in users:

        # 각 IAM 사용자의 비밀번호 정책 가져오기
        password_policy = iam_client.get_account_password_policy()[
            'PasswordPolicy']

        # 90일 이내에 만료되도록 요구
        try:
            if password_policy['MaxPasswordAge'] >= 90:
                warning = f"FAIL - {user['UserName']} password expiration is set greater than 90 days"
                print(warning)
        except:
            print(
                f"PASS - {user['UserName']} password expiration is set lower than 90 days")

        # 24회 이상 재사용 금지
        try:
            if password_policy['PasswordReusePrevention'] >= 24:
                warning = f"FAIL - {user['UserName']} password policy reuse prevention is less than 24 or not set."
                print(warning)
        except:
            print(
                f"PASS - {user['UserName']} password policy reuse prevention is equal to 24.")

        # 비밀번호 최소 길이가 14 이상인지 확인하기
        try:
            if password_policy['MinimumPasswordLength'] < 14:
                warning = f"FAIL- {user['UserName']} password policy does not require minimum length of 14 characters."
                print(warning)
        except:
            print(
                f"PASS - {user['UserName']} password policy requires minimum length of 14 characters.")

        # 특수 문자 사용 요구
        try:
            if password_policy['RequireSymbols'] == False:
                warning = f"FAIL - {user['UserName']} password policy does not require at least one symbol."
                print(warning)
        except:
            print(
                f"PASS - {user['UserName']} password policy requires at least one symbol.")

        # 숫자 사용 요구
        try:
            if password_policy['RequireNumbers'] == False:
                warning = f"FAIL - {user['UserName']} password policy does not require at least one number."
                print(warning)
        except:
            print(
                f"PASS - {user['UserName']} password policy requires at least one number.")

        # 대문자 사용 요구
        try:
            if password_policy['RequireUppercaseCharacters'] == False:
                warning = f"FAIL - {user['UserName']} password policy does not requires at least one uppercase letter."
                print(warning)
        except:
            print(
                f"PASS - {user['UserName']} password policy require at least one uppercase letter.")

        # 소문자 사용 요구
        try:
            if password_policy['RequireLowercaseCharacters'] == False:
                warning = f"FAIL - {user['UserName']} password policy does not requires at least one lowercase letter."
                print(warning)
        except:
            print(
                f"PASS - {user['UserName']} password policy requires at least one lowercase letter.")


iam_update_account_password_policy(users)
