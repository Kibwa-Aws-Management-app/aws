import boto3


aws_access_key = 'YOUR_ACCESS_KEY'
aws_secret_key = 'YOUR_SECRET_KEY'
aws_region = 'YOUR_AWS_REGION'


s3 = boto3.client('s3', aws_access_key_id=aws_access_key,
                  aws_secret_access_key=aws_secret_key, region_name=aws_region)

block_acl = True
bucket_name = 'your-bucket-name'

# S3가 계정에 대해 공개 액세스 차단이 있는지 확인


def check_s3_public_access_block():
    s3 = boto3.client('s3')

    response = s3.get_public_access_block(Bucket='your-bucket-name')

    if (response['PublicAccessBlockConfiguration']['BlockPublicAcls']
        and response['PublicAccessBlockConfiguration']['IgnorePublicAcls']
        and response['PublicAccessBlockConfiguration']['BlockPublicPolicy']
            and response['PublicAccessBlockConfiguration']['RestrictPublicBuckets']):
        return "PASS - S3 public access is blocked for the account."

    return "FAIL - S3 public access is not fully blocked for the account."


#  버킷에 대해 블록 공개 액세스가 있는지 확인
def check_s3_bucket_public_access(bucket_name):
    s3 = boto3.client('s3')

    response = s3.get_bucket_policy_status(Bucket=bucket_name)

    if response['PolicyStatus']['IsPublic']:
        return "PASS - S3 bucket has public access."

    return "FAIL - S3 bucket does not have public access."


# 계정 수준에서 모든 S3 공개 액세스가 차단되어 있는지 확인
def check_account_level_s3_public_access_block():
    s3 = boto3.client('s3')

    response = s3.get_public_access_block(AccountId='your-account-id')

    if (response['PublicAccessBlockConfiguration']['BlockPublicAcls']
        and response['PublicAccessBlockConfiguration']['IgnorePublicAcls']
        and response['PublicAccessBlockConfiguration']['BlockPublicPolicy']
            and response['PublicAccessBlockConfiguration']['RestrictPublicBuckets']):
        return "PASS - Account level S3 public access is blocked."

    return "FAIL - Account level S3 public access is not fully blocked."


# S3 버킷이 ACL을 사용하지 못하도록 설정되어 있는지 확인
def check_s3_bucket_acl(block_acl):
    s3 = boto3.client('s3')

    response = s3.get_bucket_acl(Bucket='your-bucket-name')

    if block_acl:
        for grant in response['Grants']:
            if 'AllUsers' in grant.get('Grantee', {}).get('URI', ''):
                return "FAIL - S3 bucket uses ACL and has public access."

        return "PASS - S3 bucket does not use ACL for public access."

    return "FAIL - Invalid input for 'block_acl'."


# S3 버킷에 서버 측 암호화가 되어 있는지 확인
def check_s3_bucket_encryption():
    s3 = boto3.client('s3')

    response = s3.get_bucket_encryption(Bucket='your-bucket-name')

    if 'ServerSideEncryptionConfiguration' in response:
        return "PASS - S3 bucket has server-side encryption enabled."

    return "FAIL - S3 bucket does not have server-side encryption enabled."


# S3 버킷이 MFA 삭제가 가능한지 확인
def check_s3_bucket_mfa_delete():
    s3 = boto3.client('s3')

    response = s3.get_bucket_versioning(Bucket='your-bucket-name')

    if 'MFADelete' in response and response['MFADelete'] == 'Enabled':
        return "PASS - S3 bucket has MFA delete enabled."

    return "FAIL - S3 bucket does not have MFA delete enabled."


# 각 함수를 호출하여 결과 출력
print("S3 Account Public Access:", check_s3_public_access_block())
print("Bucket Public Access:", check_s3_bucket_public_access(bucket_name))
print("Account Level Public Access:",
      check_account_level_s3_public_access_block())
print("Bucket ACL Usage:", check_s3_bucket_acl(block_acl))
print("Server-Side Encryption:", check_s3_bucket_encryption())
print("MFA Delete Capability:", check_s3_bucket_mfa_delete())
