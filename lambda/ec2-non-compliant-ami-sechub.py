#Script that is designed to take in a notification from a config rule that is looking to see if an EC2 instance is 
#running a compliant AMI or not (approved-amis-by-id)
#If the resource in the message is not compliant then a finding gets created in Security Hub
# If the resource is compliant then any open findings in security hub get archived

import boto3
import json
import datetime
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

sechubclient = boto3.client('securityhub')

def lambda_handler(event, context):
	logger.info('Event Data')
	logger.info(event)


	compliance_type = event["detail"]["newEvaluationResult"]["complianceType"]
	account_id = event["detail"]["awsAccountId"]
	region = event["detail"]["awsRegion"]
	resource_id = event["detail"]["newEvaluationResult"]["evaluationResultIdentifier"]["evaluationResultQualifier"]["resourceId"]


	if compliance_type == 'NON_COMPLIANT':
		logger.info("Resource is out of compliance")
		
		d = datetime.datetime.utcnow() # <-- get time in UTC
		

		findings = [{
    		"SchemaVersion": "2018-10-08",
    		"Title": f"Unapproved AMI used for instance {resource_id}",
    		"Description": "This instance is running with an AMI that is not approved for use.",
    		"ProductArn": f"arn:aws:securityhub:{region}:{account_id}:product/{account_id}/default",
    		"AwsAccountId": account_id,
    		"Id": f"unapproved-ami/{resource_id}",
    		"GeneratorId": "CUSTOM:UnapprovedAMIs",
    		"Types": [],
    		"CreatedAt": d.isoformat("T") + "Z",
    		"UpdatedAt": d.isoformat("T") + "Z",
    		"Severity": {
        		"Label": "MEDIUM"
    		},
    		"Resources": [{
        		"Type": "AwsEc2Instance",
        		"Id": f"arn:aws:ec2:{region}:{account_id}:instance/{resource_id}"
    		}]
		}]

		logger.info ('Creating a finding')

		import_response = sechubclient.batch_import_findings(
			Findings=findings
		)

		logger.info('Response from creating finding')
		logger.info(import_response)

# if compliant and a finding exists then archive it
	elif compliance_type == 'COMPLIANT':
		logger.info('Resource is in compliance')

		filters = {
    		"ProductArn": [{
        		"Value": f"arn:aws:securityhub:{region}:{account_id}:product/{account_id}/default",
        		"Comparison": "EQUALS"
    		}],
    		"Id": [{
        		"Value": f"unapproved-ami/{resource_id}",
        		"Comparison": "EQUALS"
    		}],
    		"RecordState": [{
    			"Value": "ACTIVE",
    			"Comparison": "EQUALS"
    		}]
		}

		logger.info('Checking for existing findings')

		get_findings_response = sechubclient.get_findings(
    		Filters=filters
		)

		logger.info('Results from get findings')
		logger.info(get_findings_response)

		#verify that there is a finding returned back.
		findings = get_findings_response["Findings"]
		if findings:

			#Ok to update

			logger.info('There was a finding to update')

			note= {
				"Text": "Updated as now compliant",
				"UpdatedBy" : "Lambda"
			}

			logger.info ('Updating existing finding to ARCHIVED')

			update_response = sechubclient.update_findings(
				Filters=filters,
				Note=note,
				RecordState='ARCHIVED')

			logger.info('output from update finding')
			logger.info (update_response)

		else:
			logger.info ("no findings to update.  Leaving alone")

	return {
        'statusCode': 200,
    }




