import boto3


# VPC Flow Log 설정
# VPC Flow Log를 설정하지 않은 경우 Fail, VPC Flow Log를 설정한 경우 Pass
def check_vpc_flow_logs(vpc_id):
    ec2 = boto3.client('ec2', region_name=AWS_REGION)

    response = ec2.describe_flow_logs(
        Filters=[{'Name': 'resource-id', 'Values': [vpc_id]}])
    if len(response['FlowLogs']) == 0:
        return "FAIL - VPC Flow Logs are not configured."

    return "PASS - VPC Flow Logs are configured."


# Endpoint
# VPC endpoint가 모든 권한일 경우 Fail
def check_vpc_endpoint_permissions(endpoint_id):
    ec2 = boto3.client('ec2', region_name=AWS_REGION)

    response = ec2.describe_vpc_endpoints(VpcEndpointIds=[endpoint_id])
    endpoint = response['VpcEndpoints'][0]
    if "*" in endpoint['PolicyDocument']:
        return "FAIL - VPC endpoint has unrestricted permissions."
    return "PASS - VPC endpoint permissions are properly configured."


#  VPC endpoint 신뢰할 수 있는 계정일 경우 Pass, VPC endpoint 신뢰할 수 없는 계정일 경우 Fail
# arn 사용
def check_vpc_endpoint_trusted_account_with_arn(vpc_id, endpoint_id, trusted_account_arn):
    ec2 = boto3.client('ec2', region_name=AWS_REGION)

    response = ec2.describe_vpc_endpoints(VpcEndpointIds=[endpoint_id])
    endpoint = response['VpcEndpoints'][0]

    # 신뢰할 수 있는 arn인지 확인
    if "Statement" in endpoint['PolicyDocument']:
        statements = endpoint['PolicyDocument']['Statement']
        for statement in statements:
            if (
                "Effect" in statement and statement["Effect"] == "Allow" and
                "Principal" in statement and "AWS" in statement["Principal"] and
                statement["Principal"]["AWS"] == trusted_account_arn
            ):
                return "PASS - ", f"VPC Endpoint {endpoint_id} in VPC {vpc_id} can only be accessed from trusted accounts."

    return "FAIL - ", f"VPC Endpoint {endpoint_id} in VPC {vpc_id} can be accessed from non-trusted accounts."


# VPC endpoint 계정 2 개 중 모두 신뢰할 수 있는 계정일 경우 Pass, VPC endpoint 계정 2개 중 한 개만 신뢰할 수 있는 계정일 경우 Fail
def vpc_endpoint_with_two_account_ids_one_trusted_one_not(vpc_id, endpoint_ids, trusted_account_ids):
    ec2 = boto3.client('ec2', region_name=AWS_REGION)
    status = "PASS"  # 기본적으로 "PASS"로 초기화'

    for endpoint_id in endpoint_ids:
        response = ec2.describe_vpc_endpoints(VpcEndpointIds=[endpoint_id])
        endpoint = response['VpcEndpoints'][0]

        if "PolicyDocument" in endpoint:
            policy_document = endpoint['PolicyDocument']
            trusted_count = 0

            if "Statement" in policy_document:
                statements = policy_document['Statement']

                for statement in statements:
                    if (
                        "Effect" in statement and statement["Effect"] == "Allow" and
                        "Principal" in statement and "AWS" in statement["Principal"]
                    ):
                        if isinstance(statement["Principal"]["AWS"], list):
                            for account_id in statement["Principal"]["AWS"]:
                                if account_id in trusted_account_ids:
                                    trusted_count += 1

                        elif isinstance(statement["Principal"]["AWS"], str):
                            if statement["Principal"]["AWS"] in trusted_account_ids:
                                trusted_count += 1

            if trusted_count == 2:
                status = "PASS - ", f"VPC Endpoint {endpoint_ids} in VPC {vpc_id} can only be accessed from trusted accounts."
            else:
                status = "FAIL - ", f"VPC Endpoint {endpoint_ids} in VPC {vpc_id} can be accessed from non-trusted accounts."

    return status


# 라우팅 테이블 페어링
# VPC와 라우팅 테이블이 잘 페어링되어 있지 않은 경우 Fail, VPC와 라우팅 테이블이 잘 페어링되어 있는 경우  Pass
def check_vpc_routing_table_peering(vpc_id, routing_table_id):
    ec2 = boto3.client('ec2', region_name=AWS_REGION)

    response = ec2.describe_route_tables(RouteTableIds=[routing_table_id])
    route_table = response['RouteTables'][0]

    if "Associations" in route_table:
        for association in route_table['Associations']:
            if "Main" not in association:
                associated_vpc_id = association.get("Main", {}).get("VpcId")
                if associated_vpc_id == vpc_id:
                    return "PASS - ", f"VPC and routing table are properly peered."

    return "FAIL - ", f"VPC and routing table are not properly peered."


# 서브넷
# VPC 서브넷이 없을 경우 Fail
def check_vpc_subnets(vpc_id):
    ec2 = boto3.client('ec2', region_name=AWS_REGION)

    response = ec2.describe_subnets(
        Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
    subnets = response['Subnets']

    if subnets:
        return "PASS - ", "Subnets exist in the VPC."

    return "FAIL - ", "No subnets found in the VPC."


# VPC 서브넷 다른 가용 영역(az)일 경우 Pass, VPC 서브넷 같은 가용 영역(az)일 경우 Fail
def check_subnet_availability_zone(subnet_id):
    ec2 = boto3.client('ec2', region_name=AWS_REGION)

    response = ec2.describe_subnets(SubnetIds=[subnet_id])
    subnet_availability_zone = response['Subnets'][0]['AvailabilityZone']

    vpc = response['Subnets'][0]['VpcId']
    response = ec2.describe_vpcs(VpcIds=[vpc])
    vpc_availability_zone = response['Vpcs'][0]['AvailabilityZone']

    if subnet_availability_zone == vpc_availability_zone:
        return "FAIL - Subnet is in the same Availability Zone as the VPC."
    return "Pass - Subnet is in a different Availability Zone than the VPC."


# elbv2
# elbv2 로깅을 사용하도록 설정하지 않은 경우 Fail, elbv2 로깅을 사용하도록 설정한 경우 Pass
def check_elbv2_logging_enabled():
    elbv2 = boto3.client('elbv2', region_name=AWS_REGION)

    response = elbv2.describe_load_balancers()
    elb_logging_disabled_count = 0

    for elb in response['LoadBalancers']:
        load_balancer_name = elb['LoadBalancerName']
        attributes = elbv2.describe_load_balancer_attributes(
            LoadBalancerName=load_balancer_name)
        for attr in attributes['Attributes']:
            if attr['Key'] == 'access_logs.s3.enabled' and attr['Value'] == 'false':
                elb_logging_disabled_count += 1

    if elb_logging_disabled_count > 0:
        return "FAIL - ", f"{elb_logging_disabled_count} ELBv2 load balancer(s) have logging disabled."

    return "PASS - ", "ELBv2 load balancers have logging enabled."


# 이제 위의 함수를 사용하여 각 조건에 대한 결과
AWS_REGION = 'us-east-1'
trusted_account_arn = 'arn:aws:iam::YOUR_ACCOUNT_NUMBER:root'

vpc_id = 'your_vpc_id'
endpoint_id = 'your_vpc_endpoint_id'
subnet_id = 'your_subnet_id'
routing_table_id = 'your_routing_table_id'
endpoint_ids = ['your_endpoint_ids']
trusted_account_ids = 'your_account_ids'

print("VPC Flow Logs 설정:", check_vpc_flow_logs(vpc_id))
print("VPC Endpoint 권한:", check_vpc_endpoint_permissions(endpoint_id))
print("VPC Endpoint 신뢰할 수 있는 계정:",
      check_vpc_endpoint_trusted_account_with_arn(vpc_id, endpoint_id, trusted_account_arn))
print("VPC Endpoint 2개 계정 신뢰 확인:", vpc_endpoint_with_two_account_ids_one_trusted_one_not(
    vpc_id, endpoint_ids, trusted_account_ids))
print("VPC Routing:", check_vpc_routing_table_peering(vpc_id, routing_table_id))
print("VPC 서브넷:", check_vpc_subnets(vpc_id))
print("VPC 서브넷 가용 영역:", check_subnet_availability_zone(subnet_id))
print("ELBv2 로깅:", check_elbv2_logging_enabled())
