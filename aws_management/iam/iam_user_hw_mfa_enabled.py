import boto3

def check_user_hardware_mfa_enabled():
    session = boto3.Session(profile_name='default')  # AWS CLI 프로필 이름으로 설정

    iam_client = session.client('iam')

    users = iam_client.list_users()['Users']
    findings = []

    for user in users:
        username = user['UserName']

        # 사용자의 MFA 디바이스 확인
        response = iam_client.list_mfa_devices(UserName=username)

        if 'MFADevices' in response and len(response['MFADevices']) > 0:
            is_hardware_mfa = False
            for device in response['MFADevices']:
                if device['DeviceType'] == 'HardwareMFA':
                    is_hardware_mfa = True
                    break

            if is_hardware_mfa:
                print(f"PASS : User '{username}' has hw MFA enabled.")
            else:
                print(f"FAIL : User '{username}' does not have hw MFA enabled.")
        else:
            print(f"FAIL : User '{username}' does not have any MFA enabled.")

if __name__ == "__main__":
    check_user_hardware_mfa_enabled()
