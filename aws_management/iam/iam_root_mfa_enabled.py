import boto3

def check_root_mfa_enabled():
    
    session = boto3.Session(profile_name='default')  # AWS CLI 프로필 이름으로 설정

    #클라이언트 생성
    iam_client = session.client('iam')

    # Root 계정 MFA 상태 확인
    response = iam_client.get_account_summary()
    is_mfa_enabled = response['SummaryMap']['AccountMFAEnabled'] > 0

    if is_mfa_enabled:
        print("PASS : MFA is enabled for root account.")
    else:
        print("FAIL : MFA is not enabled for root account.")

if __name__ == "__main__":
    check_root_mfa_enabled()
