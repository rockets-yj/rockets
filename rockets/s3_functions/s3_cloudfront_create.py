# import boto3

# def create_cloudfront_distribution(bucket_name, distribution_name):
#     # AWS 계정 정보 설정
#     aws_access_key_id = 'AKIAY4FU3OUXBF7JOCX3'
#     aws_secret_access_key = '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'
#     aws_region = 'ap-northeast-2'

#     # Boto3 클라이언트 생성
#     cloudfront_client = boto3.client(
#         'cloudfront',
#         aws_access_key_id=aws_access_key_id,
#         aws_secret_access_key=aws_secret_access_key,
#         region_name=aws_region
#     )

#     # S3 오리진 구성
#     origin_config = {
#         'S3OriginConfig': {
#             'OriginAccessIdentity': ''
#         },
#         'OriginProtocolPolicy': 'https-only',

#         'DomainName': f'{bucket_name}.s3.amazonaws.com'
#     }

#     # 디폴트 캐시 동작 구성
#     default_cache_behavior = {
#         'TargetOriginId': 'S3-' + bucket_name,
#         'ForwardedValues': {
#             'QueryString': False,
#             'Cookies': {'Forward': 'none'},
#             'Headers': ['Origin']
#         },
#         'TrustedSigners': {
#             'Enabled': False,
#             'Quantity': 0
#         },
#         'ViewerProtocolPolicy': 'redirect-to-https',
#         'AllowedMethods': ['GET', 'HEAD'],
#         'SmoothStreaming': False,
#         'Compress': False
#     }

#     # CloudFront Distribution 구성
#     distribution_config = {
#         'CallerReference': 'your-unique-reference',
#         'Aliases': {
#             'Quantity': 0
#         },
#         'DefaultRootObject': 'index.html',
#         'Origins': {
#             'Quantity': 1,
#             'Items': [origin_config]
#         },
#         'DefaultCacheBehavior': default_cache_behavior,
#         'CacheBehaviors': {
#             'Quantity': 0
#         },
#         'CustomErrorResponses': {
#             'Quantity': 0
#         },
#         'Comment': 'Your CloudFront Distribution Comment',
#         'Logging': {
#             'Enabled': False,
#             'IncludeCookies': False,
#             'Bucket': '',
#             'Prefix': ''
#         },
#         'PriceClass': 'PriceClass_All',
#         'Enabled': True
#     }

    # CloudFront Distribution 생성
    # response = cloudfront_client.create_distribution(
    #     DistributionConfig=distribution_config
    # }

#     # 생성된 Distribution ID 출력
#     print(f"CloudFront Distribution created with ID: {response['Distribution']['Id']}")


# CloudFront Distribution 생성 예제
# create_cloudfront_distribution('rockets-yj', 'cftestsong')