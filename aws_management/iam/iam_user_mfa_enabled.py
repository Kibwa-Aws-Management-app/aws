import boto3

def check_user_mfa_enabled():
    session = boto3.Session(profile_name='default') 

    iam_client = session.client('iam')

    users = iam_client.list_users()['Users']
    findings = []

    for user in users:
        username = user['UserName']

        # 사용자 정보 가져오기
        response = iam_client.get_user(UserName=username)
        
        # 사용자의 MFA 활성화 상태 확인
        if 'MFA' in response['User'] and 'MFAEnabled' in response['User']['MFA']:
            if response['User']['MFA']['MFAEnabled']:
                print(f"PASS : User '{username}' is using MFA for AWS console access.")
            else:
                print(f"FAIL : User '{username}' is not using MFA for AWS console access.")
        else:
            print(f"User '{username}' does not have MFA information.")

if __name__ == "__main__":
    check_user_mfa_enabled()
