import boto3
import shodan


# AWS Elastic IP 주소 확인
def check_elastic_ip(shodan_api_key, elastic_ip):
    try:
        # Shodan API 초기화
        shodan_api = shodan.Shodan(shodan_api_key)

        # Shodan에서 Elastic IP 주소 확인
        check = shodan_api.host(elastic_ip)

        # Elastic IP 주소가 Shodan에 확인되면 FAIL
        result = "FAIL - Elastic IP address in Shodan."

    except shodan.APIERROR as e:
        if e.value == "No information available for that IP.":
            # Elastic IP 주소가 Shodan에 확인되지 않으면 PASS
            result = "PASS - Elastic IP address not in Shodan."

        else:
            # 다른 오류 처리
            result = str(e)

    print(f"Check Elastic IP address in Shodan : {result}")


# Elastic IP 주소 할당 확인
def check_elastic_ip_assignment(ec2, elastic_ip):
    try:
        response = ec2.describe_addresses(PublicIps=[elastic_ip])
        if response['Addresses']:
            # Elastic IP 주소가 할당되면 PASS
            result = "PASS"
        else:
            # Elastic IP 주소가 할당되지 않으면 FAIL
            result = "FAIL"
    except Exception as e:
        result = str(e)

    print(f"Elastic IP address assignment: {result}")


# EC2 인스턴스 상세 모니터링 확인
def check_instance_detailed_monitoring(ec2, instance_id):
    try:
        response = ec2.describe_instance_attribute(
            InstanceId=instance_id, Attribute='instanceMonitoring')
        if response['InstanceMonitoring']['State'] == 'enabled':
            # 상세 모니터링이 활성화되면 PASS
            result = "PASS - EC2 instance detailed monitoring enabled."
        else:
            # 상세 모니터링이 비활성화되면 FAIL
            result = "FAIL - EC2 instance detailed monitoring not enabled."
    except Exception as e:
        result = str(e)

    print(f"Check EC2 instance detailed monitoring: {result}")


# EC2 인스턴스 IMDSv2 확인
def check_instance_imdsv2(ec2, instance_id):
    try:
        response = ec2.describe_instance_attribute(
            InstanceId=instance_id, Attribute='sriovNetSupport')
        if response['SriovNetSupport']['Value'] == 'simple':
            # IMDSv2가 활성화되면 PASS
            result = "PASS - EC2 instance IMDSv2 enabled."
        else:
            # IMDSv2가 비활성화되면 FAIL
            result = "FAIL - EC2 instance IMDSv2 not enabled."
    except Exception as e:
        result = str(e)

    print(f"Check EC2 instance IMDSv2: {result}")


# EC2 인스턴스의 인터넷 통신 가능여부와 프로파일 설정 여부 확인
def check_instance_internet_and_profile(ec2, instance_id):
    try:
        response = ec2.describe_instances(InstanceIds=[instance_id])
        instance = response['Reservations'][0]['Instances'][0]
        internet_accessible = instance['SourceDestCheck']
        iam_profile = instance.get('IamInstanceProfile', None)

        if internet_accessible and iam_profile:
            # 인터넷 통신 가능하고 프로파일이 설정되면 PASS
            result = "PASS"
        else:
            # 하나라도 설정 안되었으면 FAIL
            result = "FAIL"
    except Exception as e:
        result = str(e)

    print(f"Check EC2 instance internet and profile: {result}")


# Shodan API 키 설정
shodan_api_key = 'your_shodan_api_key'

# Elastic IP 주소, EC2 인스턴스 ID 및 AWS 리전 설정
elastic_ip = 'your_elastic_ip_address'
instance_id = 'your_ec2_instance_id'
aws_region = 'your_aws_region'

# AWS Boto3 클라이언트 초기화
ec2 = boto3.client('ec2', region_name=aws_region)

# Elastic IP 주소 확인
check_elastic_ip(shodan_api_key, elastic_ip)


# Elastic IP 주소 할당 확인
check_elastic_ip_assignment(ec2, elastic_ip)


# EC2 인스턴스 상세 모니터링 확인
check_instance_detailed_monitoring(
    ec2, instance_id)


# EC2 인스턴스 IMDSv2 확인
check_instance_imdsv2(ec2, instance_id)


# EC2 인스턴스의 인터넷 통신 가능여부와 프로파일 설정 여부 확인
check_instance_internet_and_profile(ec2, instance_id)
