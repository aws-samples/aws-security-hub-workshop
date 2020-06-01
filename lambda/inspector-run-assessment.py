import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

inspectorclient = boto3.client('inspector')
ssmclient = boto3.client('ssm')
template_arn = os.environ['Inspector_Assement_Template_ARN']
assessment_param = os.environ['Inspector_Assement_Complete_Param']

def lambda_handler(event, context):
	#get the external parameter of run status, this is to prevent continuous scanning during the lab
	ssm_response = ssmclient.get_parameter(
    	Name=assessment_param,
		)
	assessment_status = ssm_response["Parameter"]["Value"]
	
	logger.info("Lambda envoked, assessment status: " + assessment_status)

	if assessment_status != "Complete":
		response = inspectorclient.start_assessment_run(
				assessmentTemplateArn=template_arn			
				)
				
		logger.info("start inspector assessment: " + str(response))		
		
		ssm_response = ssmclient.put_parameter(
				Name=assessment_param,
				Value='Complete',
				Type='String',
				Overwrite=True
			)
		
		logger.info("updated status: " + str(ssm_response))		
