import boto3


# Boto3 클라이언트 생성
# NOTE: 통과는 False!!!!
class IAMBoto3:

    def __init__(self):
        self.iam_client = boto3.client('iam')
        self.iam_list = []
        for u in self.iam_client.list_users()['Users']:
            self.iam_list.append(u['UserName'])

    # 유저의 정보 가져오기
    def get_user_info(self, user_name):
        info = self.iam_client.get_user(UserName=user_name)
        print(info)

    # 인라인 정책에 관리자 권한이 없습니다.
    # 사용자가 만든 미첨부 정책에 관리자 권한이 없습니다.
    # 사용자가 만든 첨부 정책에 관리자 권한이 없습니다.
    def check_no_user_inline_policy(self):
        for username in self.iam_list:
            if self.check_no_user_inline_policy_with_username(username):
                print(f"'{username}'에서 인라인 정책 관리자 권한이 있음이 발견 되었습니다.")

    def check_no_user_inline_policy_with_username(self, user_name):
        try:
            # iam 계정의 인라인 정책 리스트
            inline_policy = self.iam_client.list_user_policies(UserName=user_name)["PolicyNames"]

            for inline in inline_policy:
                policy = self.iam_client.get_user_policy(
                    UserName=user_name,
                    PolicyName=inline
                )
                check_inline_is_adminAccess = policy['PolicyDocument']['Statement'][0]
                if "*" in check_inline_is_adminAccess['Action'] \
                        and "*" in check_inline_is_adminAccess['Resource']:
                    print("[FAIL] 인라인 정책에 관리자 권한이 있습니다.")
                    return True
        except Exception as e:
            print(f"[FAIL]인라인 정책을 살펴 보던 중 문제가 발생했습니다. {e}")
            return True
        print(f"[PASS] '{user_name}'에 인라인 정책이 없거나, 정책에 관리자 권한이 없습니다. ")
        return False

    # 첨부 정책에 관리자 권한이 없습니다.
    def check_no_AA_in_attach(self):
        for username in self.iam_list:
            if self.check_no_AA_in_attach_with_username(username):
                print(f"""{username}에서 인라인 정책 관리자 권한이 있음이 발견 되었습니다.""")

    def check_no_AA_in_attach_with_username(self, user_name):
        try:
            policy = self.iam_client.list_attached_user_policies(UserName=user_name)
            AA = policy['AttachedPolicies']
            for aa in AA:
                print(aa)
                if 'Management' in aa['PolicyName']:
                    print("[FAIL] 첨부 정책에 관리자 권한이 있습니다.")
                    return True
        except Exception as e:
            print(f"첨부 정책 관리자 권한을 확인하던 중 오류가 발생하였습니다. : {e}")
            return True
        print(f"[PASS] '{user_name}'에 첨부 정책에 관리자 권한이 없습니다.")
        return False

    def check_no_role_policy(self):
        roles = self.iam_client.list_roles()
        for r in roles['Roles']:
            self.check_no_role_policy_with_roleName(r['RoleName'])

    # 사용자 정의 정책을 통한 롤 가정을 허용하지 않습니다. = PASS
    def check_no_role_policy_with_roleName(self, role_name):
        role = self.iam_client.get_role(RoleName=role_name)
        if role['Role']['AssumeRolePolicyDocument'] is exit:
            print(f"[FAIL] '{role_name}'이 룰 가정을 허용합니다.")
            return True
        print(f"[PASS] '{role_name}'이 룰 가정을 허용하지 않습니다.")
        return False

    # Root 계정을 사용하지 않고 IAM 사용자 또는 역할을 사용합니다. => ROOT 계정 사용하고 있으면 나가리
    def check_root_user(self):
        for u in self.iam_list:
            self.check_root_user_with_username(u)

    def check_root_user_with_username(self, user_name):
        user = self.iam_client.get_user(UserName=user_name)
        root_user = user['User']['Arn'][:4]
        if root_user == 'root':
            print(f"[FAIL] '{user_name}'이 root 계정입니다.")
            return True
        print(f"[PASS] '{user_name}'이 root 계정이 아닙니다.")
        return False