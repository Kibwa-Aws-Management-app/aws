import boto3
from datetime import datetime, timezone

session = boto3.Session(profile_name='default')  # AWS CLI 프로필 이름으로 설정

iam_client = session.client('iam')

def check_iam_user_credentials():
    users = iam_client.list_users()['Users']
    userSet = set() 

    for user in users:
        user_name = user['UserName']
        access_keys = iam_client.list_access_keys(UserName=user_name)['AccessKeyMetadata']

        if user_name in userSet:
            continue  # 이미 출력한 사용자는 continue

        for key in access_keys:
            access_key_id = key['AccessKeyId']
            status = key['Status']
            date_str = key['CreateDate'].strftime("%Y-%m-%d %H:%M:%S")
            create_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)

            if status == 'Active':
                inactive_days = (datetime.now(timezone.utc) - create_date).days

                if inactive_days <= 90:
                    if inactive_days <= 30:
                        message = f"s Access Key {access_key_id} - Inactivity within 30 days."
                    elif 30 < inactive_days <= 45:
                        message = f"s Access Key {access_key_id} - Inactivity exceeding 30 days but within 45 days."
                    else:
                        message = f"Inactivity exceeding 45 days but within 90 days."

                    print(f"PASS : User {user_name}'{message}")
                    userSet.add(user_name)  # 사용자를 이미 출력한 목록에 추가
                else:
                    print(f"FAIL : User {user_name}'s Access Key {access_key_id} - exceeds 90 days of inactivity.")
                    userSet.add(user_name)  # 사용자를 이미 출력한 목록에 추가
            else:
                print(f"User {user_name}' is inactive.")

if __name__ == "__main__":
    check_iam_user_credentials()
