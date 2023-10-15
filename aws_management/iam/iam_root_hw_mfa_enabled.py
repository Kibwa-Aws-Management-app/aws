import boto3

def check_root_hw_mfa_enabled():
    
    session = boto3.Session(profile_name='default')  # AWS CLI 프로필 이름으로 설정

    iam_client = session.client('iam')

    # Root 계정 하드웨어 MFA 상태 확인
    response = iam_client.get_account_summary()
    is_mfa_enabled = response['SummaryMap']['AccountMFAEnabled'] > 0

    if is_mfa_enabled:
        virtual_mfas = iam_client.list_virtual_mfa_devices()
        for mfa in virtual_mfas['VirtualMFADevices']:
            if 'root' in mfa['SerialNumber']:
                print("FAIL : Root account has a virtual MFA instead of a hardware MFA device enabled.")
                return
        print("PASS : Root account has a hardware MFA device enabled.")
    else:
        print("FAIL : Hardware MFA is not enabled for root account.")

if __name__ == "__main__":
    check_root_hw_mfa_enabled()
