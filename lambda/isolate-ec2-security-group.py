# Lambda function that will switch the security groups on an EC2 instance to the security group that is defined in the function environment variables.
# Environment variables required:
#            - Security_SG - name of the security group used by the security team to investigate an instance
#            - Corp_CIDR - CIDR block of the corporate network to access the instane to investigate


import json
import os
import boto3
from botocore.exceptions import ClientError
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2client = boto3.client('ec2')
corp_cidr = os.environ['Corp_CIDR']
security_team_name = os.environ['Security_Group_Name']


def create_security_sg(vpc_id):

    sg_group_id = None

    try:
        response = ec2client.create_security_group(
            Description='Security Team Security Group ',
            GroupName=security_team_name,
            VpcId=vpc_id
        )
        sg_group_id = response["GroupId"]
    except ClientError as e:
        logger.exception(e)

    if sg_group_id != None:
        try:
            response = ec2client.authorize_security_group_ingress(
                GroupId=sg_group_id,
                IpPermissions=[
                    {
                        'FromPort': 3389,
                        'ToPort': 3389,
                        'IpProtocol': 'tcp',
                        'IpRanges': [
                            {
                                'CidrIp': corp_cidr,
                                'Description': 'Corp Office'
                            },
                        ]
                    },
                    {
                        'FromPort': 22,
                        'ToPort': 22,
                        'IpProtocol': 'tcp',
                        'IpRanges': [
                            {
                                'CidrIp': corp_cidr,
                                'Description': 'Corp Office'
                            },
                        ]
                    },
                ],
            )
        except ClientError as e:
            logger.exception(e)
    
    return sg_group_id




def lambda_handler(event, context):
    
    security_team_sg = None
    sec_groups = []
    vpc_id = None


    logger.info(event)
    for findings in event['detail']['findings']:
        for res in findings['Resources']:
            id_arn = (res['Id'])
            print(id_arn)
            instance_id = id_arn.split("/")[1]
            print(instance_id)

    instance_info = ec2client.describe_instances(
        InstanceIds=[instance_id])


    # Get all the Security Groups for the instance
    for res in instance_info['Reservations']:
        for ins in res['Instances']:
            for sg in ins['SecurityGroups']:
                sec_groups.append(sg['GroupId'])
                print(sec_groups)

                logger.info(
                    'Modifying Security Groups for Instance ID: %s', instance_id)
                logger.info('## Original Security Groups ##')
                logger.info(sec_groups)

    for res in instance_info['Reservations']:
        for ins in res['Instances']:
            vpc_id = ins['VpcId']
            print(vpc_id)

    try:
        all_security_groups = ec2client.describe_security_groups()
    except ClientError as e:
        logger.exception(e)

    
    for sg in all_security_groups['SecurityGroups']:
        if sg['GroupName'] == security_team_name and sg['VpcId'] == vpc_id:
            security_team_sg = sg['GroupId']

    # modify_instance_attribute will wipe out all the existing security groups with the new one
    logger.info('Modified instance to now have security group: %s',
                security_team_sg)

    if security_team_sg == None:
        security_team_sg = create_security_sg(vpc_id)  
    
    if security_team_sg == None:
        return 500
        
    try:
        response = ec2client.modify_instance_attribute(
            InstanceId=instance_id, Groups=[security_team_sg])
    except ClientError as e:
        logger.exception(e)
        return 500

    return response['ResponseMetadata']['HTTPStatusCode']
