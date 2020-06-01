# Script that will look for secrets that do not have a rotation interval defined at the company policy level

import boto3
import datetime
import os

secret_client = boto3.client('secretsmanager')
sechubclient = boto3.client('securityhub')

#rotation_minimum = 60
rotation_days_max=int(os.environ['ROTATION_DAYS_MAX'])

def raise_sechub_event (arn, name, rotation_days):
	
	region = arn.split(':')[3]
	account_id = arn.split(':')[4]
	d = datetime.datetime.utcnow() # <-- get time in UTC

	findings = [{
      "SchemaVersion": "2018-10-08",
      "Title": f"Rotation policy non-compliant for secret {name}",
      "Description": f"This secret has a rotation policy of {rotation_days} days that is not compliant with company policy of {rotation_days_max} days or less.",
      "ProductArn": f"arn:aws:securityhub:{region}:{account_id}:product/{account_id}/default",
      "AwsAccountId": account_id,
      "Id": f"outofcompliant-secret-rotation/{name}",
      "GeneratorId": "CUSTOM:SecretRotationDetector",
      "Types": [],
      "CreatedAt": d.isoformat("T") + "Z",
      "UpdatedAt": d.isoformat("T") + "Z",
      "Severity": {
          "Label": "MEDIUM"
      },
      "Resources": [{
          "Type": "Other",
          "Id": arn
      }]
    }]
	
	print (findings)

	import_response = sechubclient.batch_import_findings(
      Findings=findings
    )

	return {
        'statusCode': 200,
  	}

## MAIN ##
def lambda_handler(event, context):
	secrets  = secret_client.list_secrets()
	rotation = {}

	for name in secrets['SecretList']:
		print('******************')
		print (name['Name'])
		secret_name = name['Name']
		secret_arn = name['ARN']


		details = secret_client.describe_secret(
			SecretId = name['Name'])

		key='RotationRules'

		if key in details.keys():
			print ("Rotation Defined")
			print (details['RotationRules'])
			rotation = details['RotationRules']['AutomaticallyAfterDays']
			print (rotation)
			if rotation > rotation_days_max:
				print ("rotation too great")

				sechub_result = raise_sechub_event(secret_arn, secret_name, rotation)
				
			else:
				print("Rotation within limits")

		else:
			print ("Rotation not defined")
			sechub_result = raise_sechub_event(secret_arn, secret_name, "NONE")

	print('******************')
	print ("Done evaluating keys")
