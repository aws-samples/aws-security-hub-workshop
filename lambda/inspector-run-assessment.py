import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

inspectorclient = boto3.client('inspector')
template_arn = os.environ['Inspector_Assement_Template_ARN']

def lambda_handler(event, context):
	
	logger.info("starting inspector assessment")
	response = inspectorclient.start_assessment_run(
			assessmentTemplateArn=template_arn			
			)
			
	logger.info("inspector assessment start info: " + str(response))		
		
			
