from aws_cdk import (
    Stack,
    aws_iot as iot,
)
from constructs import Construct

class CdkIotStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        cert_arn = 'arn:aws:iot:ap-northeast-1:647271430098:cert/4a50ae8f9d9284eb59186612cab913312b473a2dc1f7d6aad9b951b82fc4f275'
        region = 'ap-northeast-1'
        account = '647271430098'
        
        # モノ
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_iot/CfnThing.html
        thing = iot.CfnThing(
            self,
            'MyThing',
            thing_name='my-first-thing',
        )
        
        # モノと証明書の紐づけ
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_iot/CfnThingPrincipalAttachment.html
        thing_principal_attachment = iot.CfnThingPrincipalAttachment(
            self,
            'AttachCertificateToMyThing',
            principal=cert_arn,
            thing_name=thing.thing_name,
        )
        
        # ポリシー
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_iot/CfnPolicy.html
        policy = iot.CfnPolicy(
            self,
            'IotPolicy',
            policy_document={
				"Version":"2012-10-17",
				"Statement":[
					{
						"Effect":"Allow",
						"Action":[
							"iot:Connect",
							"iot:Publish",
							"iot:Subscribe",
							"iot:Connect",
							"iot:Receive"

						],
						"Resource":[
							f"arn:aws:iot:{region}:{account}:client/{thing.thing_name}"
						]
					},
					{
						"Effect": "Allow",
						"Action": [
							"iot:Publish"
						],
						"Resource": [
							f"arn:aws:iot:{region}:{account}:topic/*"
						]
				    }
				]
			},
			policy_name='iot-policy',
        )
        
        # ポリシーと証明書の紐づけ
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_iot/CfnPolicyPrincipalAttachment.html
        policy_principal_attachment = iot.CfnPolicyPrincipalAttachment(
            self,
            'AttachCertificateToPolicy',
            policy_name=policy.policy_name,
            principal=cert_arn,
        )
        
        # 依存関係の挿入
        thing_principal_attachment.add_dependency(thing)
        policy_principal_attachment.add_dependency(policy)