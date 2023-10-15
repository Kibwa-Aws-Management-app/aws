import boto3

def check_administrator_access_with_mfa():
    session = boto3.Session(profile_name='default')  # AWS CLI 프로필 이름으로 설정

    iam_client = session.client('iam')

    administrator_access_policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
    users = iam_client.list_users()['Users']
    findings = []

    for user in users:
        username = user['UserName']

        # 사용자의 관리자 액세스 정책 확인
        response = iam_client.list_attached_user_policies(UserName=username)

        for policy in response['AttachedPolicies']:
            if policy['PolicyArn'] == administrator_access_policy_arn:
                # 사용자가 관리자 액세스 정책을 가지고 있는지
                response_mfa = iam_client.list_mfa_devices()

                if 'MFADevices' in response_mfa and len(response_mfa['MFADevices']) > 0:
                    # MFA를 사용
                    print(f"PASS : User '{username}' has administrator access with MFA enabled.")
                else:
                    # MFA를 사용X
                    print(f"FAIL : User '{username}' has administrator access with MFA disabled.")
                    findings.append(username)

    if not findings:
        print("PASS : No users with administrator access and MFA disabled.")

if __name__ == "__main__":
    check_administrator_access_with_mfa()
