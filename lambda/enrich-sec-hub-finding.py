#Script that is designed to take in a notification from a cloudwatch event rule initiated via a Security Hub 
#custom action and lookup the tags for that instance.  The resulting tags are added as notes to the Finding.

import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def postEnrichmentNote (ENRICHMENT_AUTHOR, ENRICHMENT_TEXT, ENRICHMENT_FINDING_ID):
    
    # This function takes a 'ready to post' enrichment note, author label, and 
    # adds them to a distinct finding ID
    
    logger.info("Text to post: " + ENRICHMENT_TEXT)
    
    secHubClient = boto3.client('securityhub')
    response = secHubClient.update_findings(
        Filters={
            'Id': [
                {
                    'Value': ENRICHMENT_FINDING_ID,
                    'Comparison': 'EQUALS'
                },
            ]
        },
        Note={
            'Text': ENRICHMENT_TEXT,
            'UpdatedBy': ENRICHMENT_AUTHOR
        }
    )
    
def enrichEc2Type(Ec2Finding):
    # this function takes a sechub finding event known to have the resource 
    # type of EC2 instance, describes all tags and returns the tags formatted to post
    
    #clear enrichment text
    localText = ""
    
    ec2client = boto3.client('ec2')
    
    #extract instance ID from the sec hub finding event
    id_arn = Ec2Finding["Resources"][0]['Id']
    instance_id = id_arn.split("/")[1]

    #describe instances
    instance_info = ec2client.describe_instances(InstanceIds=[instance_id])
    
    #loop and append the values and keys of all tags into the Enrichment Text              
    for res in instance_info['Reservations']:
        for ins in res['Instances']:
            for tags in ins['Tags']:
                localText = localText + "[" + tags["Key"]
                localText = localText + "]: "
                localText = localText + tags["Value"]
                localText = localText + " ,"
    
    logger.debug("Tag enrichment complete: " + localText)
    
    return localText
    
def lambda_handler(event, context):

    ENRICHMENT_TEXT = "This Resource Type not supported for enrichment"
    ENRICHMENT_AUTHOR = "SecHubEnrich - General"
    ENRICHMENT_FINDING_ID = ""
    
    #log the event
    logger.info(event)
    
    for findings in event['detail']['findings']:
        
        #determine and log this Finding's ID
        ENRICHMENT_FINDING_ID = findings["Id"]
        logger.info("Finding ID: " + ENRICHMENT_FINDING_ID)
        
    
        #determine and log this Finding's resource type
        resourceType = findings["Resources"][0]["Type"]
        logger.info("Resource Type is: " + resourceType)
    
        #if the target resource is EC2 update the enrichment text with EC2 Tags
        if resourceType == "AwsEc2Instance":
            ENRICHMENT_AUTHOR = "SecHubEnrich - EC2 Tags"
            ENRICHMENT_TEXT = enrichEc2Type(findings)
    
            postEnrichmentNote(ENRICHMENT_AUTHOR, ENRICHMENT_TEXT, ENRICHMENT_FINDING_ID)

    
    return {
        'statusCode': 200,
        'body': json.dumps('function complete')
    }
