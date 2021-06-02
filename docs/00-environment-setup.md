# Environment Setup
This workshop's procedures use multiple Lambda functions, EC2 instances, and other AWS resources created via CloudFormation templates. In this module, you will ensure that the right security services are configured and then deploy the template to create the overall workshop resources.

**Agenda**
 
1. Determine status of Security Hub, Config, and GuardDuty - 5 min
2. Deploy workshop CloudFormation stack  - 10 min


## Determine status of Security Hub, Config, and GuardDuty.

### Skip this section if you're using a new account

If you are using a new AWS account, then you can skip this section and proceed to [Deploy workshop CloudFormation stack](#deploy-workshop-cloudformation-stack). That section uses a CloudFormation template to automatically enable AWS Config, AWS SecurityHub, and Amazon GuardDuty services in the appropriate AWS Region.

### Check the status of the services if reusing an existing account

If you are using an AWS account in which these services may have already been enabled, use the following instructions to determine the status of these services so that you can properly configure the CloudFormation template in the next section.

![AWS Console](./images/01-aws-console.png)

1. From the **AWS Console** click **Services** in the top left corner

2. Type **Config** in the search bar, and select **Config** from the list.

3. If you see **Get started** in the center of the page, Config is **not** enabled.

    ??? info  "Optional Step: Click here for instructions on how to manually enable and set up AWS Config."

        1. From the <a href="https://console.aws.amazon.com/config/home" target="_blank">AWS Config dashboard</a>, click **Get Started**

        2. Step 1: Settings - Leave all of the default settings. Click **Next**. This will record all resources supported in this region and create a bucket to log data. It will also create an AWS Config service-linked role granting AWS Config the access recorded for it to function.

        3. Step 2: Rules - Under the field to filter by rule name, click **Select All**. This will highlight the AWS Config rules displayed. Then click **Next**. In your actual environment, you may want to pick and choose which rules are appropriate to enable for your workload.

        4. Step 3: Review - Click **Confirm**.

    ###

4. From the **AWS Console** click **Services** in the top left corner

5. Type **GuardDuty** in the search bar, and select **GuardDuty** from the list.

6. If you see **Get started** in the center of the page, GuardDuty is **not** enabled.

    ??? info  "Optional Step: Click here for instructions on how to manually enable and set up GuardDuty."

        1. From the <a href="https://console.aws.amazon.com/guardduty/home" target="_blank">GuardDuty page</a>, click **Get Started**.

        2. On the "Welcome to GuardDuty" screen, click **Enable GuardDuty**.

    ###

7. From the **AWS Console** click **Services** in the top left corner

8. Type **Security Hub** in the services search bar, and select **Security Hub** from the list.

9. If you see  **Go to Security Hub** on the right side of the page, Security Hub is **not** enabled.

    ??? info  "Optional Step: Click here for instructions on how to manually enable and set up AWS Security Hub."

        1. From the <a href="https://console.aws.amazon.com/securityhub/home" target="_blank">AWS Security Hub page</a>, click **Go to Security Hub**

        2. On the "Welcome to AWS Security Hub" screen, check the boxes for all of the Security Standards. Then click **Enable Security Hub**.

    ###

## Deploy workshop CloudFormation stack

To configure the workshop you will need to deploy the master workshop template.

!!! info "Before you deploy the CloudFormation template feel free to view it <a href="https://github.com/aws-samples/aws-security-hub-workshop/blob/master/templates/sechub-workshop-setup-template.json" target="_blank" rel="noopener noreferrer">here</a href>."

Region| Deploy
------|-----
US West 2 (Oregon) | <a href="https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=SecurityHubWorkshop&templateURL=https://sa-security-specialist-workshops-us-west-2.s3-us-west-2.amazonaws.com/security-hub-workshop/templates/sechub-workshop-setup-template.json" target="_blank">![Deploy Module 1 in us-west-2](./images/deploy-to-aws.png)</a>|
US East 1 (Virgina) | <a href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=SecurityHubWorkshop&templateURL=https://sa-security-specialist-workshops-us-east-1.s3.amazonaws.com/security-hub-workshop/templates/sechub-workshop-setup-template.json" target="_blank">![Deploy Module 1 in us-east1](./images/deploy-to-aws.png)</a>

1. Click the **Deploy to AWS** button above.  This will automatically take you to the console to run the template, click Next to get to the Specify Details page. 

2. On the **Specify Details** section enter the necessary parameters as shown below. 

If you're using a new AWS account, select "Yes-Enable..." for GuardDuty, SecurityHub, Config to have the CloudFormation template enable these services.

    | Parameter | Value  |
    |---|---|
    | Stack name | SecurityHubWkshp  |
    | EnableGuardDuty | **Yes-Enable GuardDuty** or **No-GuardDuty is already enabled**  |
    | EnableSecurityHub| **Yes-Enable Security Hub** or **No-Security Hub is already enabled**|
    |EnableConfig| **Yes-Enable Config** or **No-Config is already enabled**|

    **Leave all other parameters with their default values**

    
3. Once you have entered your parameters click **Next**.
4. Click **Next** again. \(leave everything on this page at the default\)

5. Finally, scroll down and check the boxes to acknowledge that the template will create IAM resources and that the template will need CAPABILITY_AUTO_EXPAND.  Then click **Create**.

![IAM Capabilities](./images/00-stack-acknowledge.png)

This will bring you back to the CloudFormation console. You can refresh the page to see the stack starting to create. This template will create five nested templates and should take 5-10 minutes to complete.  Before moving on, make sure the stack is in a **CREATE_COMPLETE** status as shown below.

![Stack Complete](./images/01-stack-complete.png)


!!! info "Once the full stack creation is done you should see findings created in Security Hub over the next 30 minutes of this workshop."

After you have successfully created the stack, you can proceed to the next module.