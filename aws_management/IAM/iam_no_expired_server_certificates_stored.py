import boto3
import datetime

# AWS 자격 증명 설정
aws_access_key_id = '' 
aws_secret_access_key = ''
aws_region = 'ap-northeast-2'  # 사용자 지정 리전 설정

# Boto3 클라이언트 생성
acm_client = boto3.client('acm', region_name=aws_region)

# 모든 서버 인증서 가져오기
try:
    response = acm_client.list_certificates()
    certificates = response.get('CertificateSummaryList', [])
    
    if not certificates:
        print("서버 인증서가 발견되지 않았습니다. Pass.")
    else:
        expired_certificates = []
        current_date = datetime.datetime.utcnow()
        
        for certificate in certificates:
            certificate_arn = certificate['CertificateArn']
            response = acm_client.describe_certificate(CertificateArn=certificate_arn)
            certificate_not_after = response['Certificate']['NotAfter']
            
            if current_date > certificate_not_after:
                expired_certificates.append(certificate_arn)
        
        if expired_certificates:
            print(f"다음 서버 인증서가 만료되었습니다: {expired_certificates}. Fail.")
        else:
            print("만료된 서버 인증서를 저장하고 있지 않습니다. Pass.")
except Exception as e:
    print("서버 인증서 상태를 확인할 수 없습니다. ACM 서비스에 액세스할 수 있는 권한이 있는지 확인하세요.")
