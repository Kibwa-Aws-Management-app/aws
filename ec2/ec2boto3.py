import boto3


class EC2Boto3:

    def __init__(self):
        self.ec2_client = boto3.client('ec2')

    # 네트워크 ACL이 TCP 포트(22)의 인바운드 트래픽 허용 여부
    # 비허용 = PASS
    def is_tcp_22_disallowed_in_nacl(self, nacl_id):
        response = self.ec2_client.describe_network_acls(NetworkAclIds=[nacl_id])
        for entry in response['NetworkAcls'][0]['Entries']:
            if entry['RuleAction'] == 'allow' and entry['Protocol'] == '6' and entry['PortRange']['From'] == 22:
                return False  # Allowed
        return True  # Disallowed or Not found

    # 보안 그룹이 인터넷에서 TCP 포트(20, 21)의 인바운드 트래픽 허용 여부 확인
    # 비허용 = PASS
    def is_tcp_20_21_disallowed_in_sg(self, sg_id):
        response = self.ec2_client.describe_security_groups(GroupIds=[sg_id])
        for permission in response['SecurityGroups'][0]['IpPermissions']:
            if permission['IpProtocol'] == 'tcp' and (permission['FromPort'] == 20 or permission['FromPort'] == 21):
                return False  # Allowed
        return True  # Disallowed or Not found

    # 보안 그룹이 인터넷에서 mysql DB에 대한 TCP 포트(3306)의 인바운드 트래픽 허용 여부 확인
    # 비혀용 = PASS
    def is_tcp_3306_disallowed_in_sg(self, sg_id):
        response = self.ec2_client.describe_security_groups(GroupIds=[sg_id])
        for permission in response['SecurityGroups'][0]['IpPermissions']:
            if permission['IpProtocol'] == 'tcp' and permission['FromPort'] == 3306 \
                    and '0.0.0.0/0' in [ip['CidrIp'] for ip in permission['IpRanges']]:
                return False  # Allowed
        return True  # Disallowed or Not found

    # 보안 그룹이 퍼블릭 IPv4 주소 대역('0.0.0.0/0')에 대한 인바운드 트래픽 허용 여부 확인
    # 비혀용 = PASS
    def is_all_traffic_disallowed_from_public_ipv4(self, sg_id):
        response = self.ec2_client.describe_security_groups(GroupIds=[sg_id])
        for permission in response['SecurityGroups'][0]['IpPermissions']:
            if '0.0.0.0/0' in [ip['CidrIp'] for ip in permission['IpRanges']]:
                return False  # Allowed
        return True  # Disallowed or Not found

    # 보안 그룹이 기본적으로 모든 인바운드, 아웃바운드 트래픽을 제한하도록 구성 여부 확인
    # 제한 있는 구성 = PASS
    def is_all_traffic_limited_in_sg(self, sg_id):
        inbound = self.ec2_client.describe_security_groups(GroupIds=[sg_id])['SecurityGroups'][0]['IpPermissions']
        outbound = self.ec2_client.describe_security_groups(GroupIds=[sg_id])['SecurityGroups'][0]['IpEgress']

        if not inbound and not outbound:
            return True  # Both inbound and outbound are restricted
        return False

    # 사용되지 않는 보안그룹 식별
    # 사용 = PASS
    def identify_unused_security_groups(self):
        response = self.ec2_client.describe_security_groups()
        all_instances = self.ec2_client.describe_instances()
        used_sgs = []
        for reservation in all_instances['Reservations']:
            for instance in reservation['Instances']:
                for sg in instance['SecurityGroups']:
                    used_sgs.append(sg['GroupId'])

        for sg in response['SecurityGroups']:
            if sg['GroupId'] not in used_sgs:
                return False
