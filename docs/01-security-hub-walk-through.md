# Module 1: Security Hub Walkthrough 

In this section of the Security Hub Workshop, you will follow a guided demonstration of the features of Security Hub.  You can use this demonstration to learn about Security Hub's capabilities.   

**Agenda** 20 minutes
 
1. Summary Page
2. Multi-Account Hierarchy
3. Integrations
4. Insights
5. Explore Security Standards

## Security Hub Summary Page

The Security Hub Summary page gives you an overview of security and compliance status of your AWS account(s). 

!!! info "Some of the data in your account may differ from the screenshots and some maybe blank."

1. From the **AWS Console** click **Services** in the top left corner

2. Type **Security Hub** in the services search bar.

3. Select **Security Hub** from the list.

![AWS Console](./images/01-aws-console.png)

4. Click **Summary** on the left hand navigation.

![Security Hub Summary](./images/01-sec-hub-summary.png)

!!! info "Security Hub automatically enables subscriptions to GuardDuty and Inspector.  Also collected, but not used in this workshop are findings from Macie, IAM Access Analyzer, and Firewall Manager."

5. Observe the Passed and Failed status of the **CIS AWS Foundations**.  Even though you just enabled it a few minutes ago, partial results of the 43 total checks have been collected.

!!! info "Refresh your browser to see the latest results.  After you enable a security standard, AWS Security Hub begins to run the checks within 2 hours.  After the initial check, the schedule for each control may be either periodic (12 hours) or change-triggered."

6. Scroll down to the graphs under **Insights** (Your graphs maybe different).  Move your mouse over **New findings over time by provider** and observe the 3 sources of findings that Security Hub is already collecting.  (There will be more throughout this workshop)

![Security Hub Insights](./images/01-sec-hub-insights-findings-by-provider.png)

7. Scroll down further under **Insights**.  Move your mouse over **Accounts with the most findings (by resource type)** and observe the sorted list of AWS resources that have findings to investigated.

![Security Hub Insights](./images/01-sec-hub-insights-findings-by-resource.png)


## Multi Account Hierarchy  
You can invite other AWS accounts to enable AWS Security Hub and become associated with your AWS account. If the owner of the account that you invite enables Security Hub and then accepts the invitation, your account is designated as the master Security Hub account, and the invited accounts become associated as member accounts. When the invited account accepts the invitation, permission is granted to the master account to view the findings in the member account. The master account can also perform actions on findings in a member account.

Security Hub supports up to 1000 member accounts per master, account per Region. The master-member account association is created in only the one Region that the invitation was sent from. You must enable Security Hub in each Region that you want to use it in, and then invite each account to associate as a member account in each Region.  

In this section we will add a member account to your Workshop Security Hub Account.  These instructions use sample information and will not actually setup the Multi-Account Hierarchy. 

!!! info "(Optional)You can invite another AWS account you are the owner of to enable AWS Security Hub and become associated with your Workshop AWS account.  In the steps below, instead of false data use information for another you AWS account you own, you can accept the invitation, and you can enable Security Hub."

1. Click **Settings** on the left hand navigation.

![Security Hub Multi](./images/01-multi-account-settings.png)

2. Click **+ Add accounts** in the above the empty account table.

3. Enter **111122223333** (Four 1's, 2's, & 3's) in the **Account ID** field.

4. Click **Add**

!!! info "Be sure to hit the tab key to get the Add button to enable.  The email does not need to be the AWS account owner.  The Add workflow allows you to add multiple member account invitations at a time."

![Security Hub Multi](./images/01-multi-account-add.png)

5. Click **Next**

6. Click **Invite** in the Status field of the member accounts table.

7. Click **Invite**.

!!! info "At this point a user with the appropriate permissions in the destination AWS account could accept this invite from the master account"

![Security Hub Multi](./images/01-multi-account-invited.png)

## Integrations
In this section, we will walk through the Security Hub side of enabling a partner integration. Security Hub provides the ability to integrate security findings from AWS services and third-party products.  For third-party products Security Hub gives you the ability to selectively enable the integrations and give you access to the configuration instructions related to the third-party product.   
 
Security Hub detects and consolidates only those security findings from the supported AWS and partner product integrations that are generated after Security Hub is enabled in your AWS accounts. It doesn't retroactively detect and consolidate security findings that were generated before you enabled Security Hub. 

1. Click on **Integrations** from the left-hand navigation pane. 

![Security Hub Integrations](./images/01-integrations-all.png)


2. Scroll through the list of available integrations.  Return to the top and **search** for a SaaS based solution such as: **Checkpoint: Dome9 Arc**, **Palo Alto Networks: Redlock**, or **Symantec: Cloud Workload Protect**.   

![Integrations Search](./images/01-integrations-search.png)

3. Click **Accept Findings**.  Review the permissions required for the integration. 

![Integrations Enable](./images/01-integrations-enable.png)

4. Click **Accept findings**. 

!!! info "This will put in place a service policy allowing the partner solution to send findings information into this account.   To use in your account, you would still need to complete the **Configure** step on the Partner solution so findings that are created by the partner solution are sent to Security Hub. "

![Integrations Configure](./images/01-integrations-configure.png)

## Findings
Security Hub imports findings AWS security services, third-party product integrations that you enable, and custom integrations you build. Security Hub consumes these findings using a standard findings format called AWS Security Finding Format (ASFF), which eliminates the need for time-consuming data conversion efforts. Security Hub then correlates the findings across integrated products to prioritize the most important ones. For more information about the findings format, see <a href="https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-findings-format.html" target="_blank">AWS Security Finding Format</a>.  

1. Click on **Findings** from the left-hand navigation pane. 

![Findings List](./images/01-findings-list.png)

2. Click in the Search bar and select **Severity label** and enter **MEDIUM** (it must be all capitalized). 

![Findings Search](./images/01-findings-search.png)

3. Click **Apply**.   

4. Select a **Title** of any finding to see more information.

![Findings Info](./images/01-findings-detail.png)

5. Click the arrow next to **Resources** on bottom right.

![Findings Resources](./images/01-findings-resources.png)

6. Click the [+] to the right of this findings **Resource Type** (e.g. AwsS3Bucket). this will add it as a filter to the search. 

![Findings Search](./images/01-findings-search-s3.png)

## Insights  
A Security Hub Insight is a collection of related findings defined by an aggregation statement and optional filters. An insight identifies a security area that requires attention and intervention. Security Hub offers several managed (default) insights that you can't modify or delete. You can also create custom insights to track security issues unique to your AWS environment and usage.  

1. Click on **Insights** from the left-hand navigation pane. 

![Insights Summary](./images/01-insights-summary.png)

2. Filter for insight **severity**.

![Insights Filter](./images/01-insights-filter.png)

3. Click on **24. Severity by counts of findings**.

![Insights 18](./images/01-insights-24.png)

!!! info "The **Group By: Resource Id** in the filter is what makes this an Insight"

4. Select a **Severity Label** (e.g. Critical) to see the underlying finding(s).

## Security Standards 
Security Hub currently supports multiple security standards:

- Payment Card Industry Data Security Standard (PCI DSS) v3.2.1:
>The Payment Card Industry Data Security Standard (PCI DSS) standard in Security Hub consists of a set of AWS security best practices controls. Each control applies to a specific AWS resource, and relates to one or more PCI DSS version 3.2.1 requirements. A PCI DSS requirement can be related to multiple controls. The details page for each PCI DSS control lists the specific PCI DSS requirements that are related to that control.The PCI DSS Compliance Standard in Security Hub is designed to help you with your ongoing PCI DSS security activities. The controls cannot verify whether your systems are compliant with the PCI DSS standard. They can neither replace internal efforts nor guarantee that you will pass a PCI DSS assessment.
- AWS Foundational Security Best Practices v1.0.0:
> The AWS Foundational Security Best Practices standard is a set of controls that detect when your deployed accounts and resources deviate from security best practices. The controls include best practices from across multiple AWS services. Each control belongs to one of the following categories, which are based on the functions described in the NIST Cybersecurity Framework. 

- Center for Internet Security (CIS) AWS Foundations v1.2.0:
> AWS Security Hub has satisfied the requirements of CIS Security Software Certification and is hereby awarded CIS Security Software Certification for the following CIS Benchmarks: CIS Benchmark for CIS Amazon Web Services Foundations Benchmark, v1.2.0, Level 1 and Level 2



To run the CIS AWS Foundations standard's compliance checks on your environment's resources, Security Hub either runs through the exact audit steps prescribed for the checks in <a href="https://www.cisecurity.org/benchmark/amazon_web_services/" target="_blank"> Securing Amazon Web Services</a> or uses specific AWS Config managed rules. Therefore, for the CIS AWS Foundations standard to be functional in Security Hub, when you enable it in a particular account, you must also enable AWS Config in that account. Security Hub doesn't manage AWS Config for you. For this workshop Config has already been enabled for you.

!!! info "The first round of compliance checks will be done within 2 hours of enabling security hub and then runs every 12 hours."

1. Click on **Security standards**.

![Security Standards](./images/01-standards-home.png)

!!! info "Note the Security score should have changed from you first enabled the CIS standard."

2. Click **View Results** for CIS AWS Foundations Benchmark v1.2.0.

![CIS Standard Results](./images/01-standards-cis-results.png)

3. Filter on **4.1**.

![CIS 4.1](./images/01-standards-cis-4-1.png)

4. Click **4.1 Ensure no security groups allow ingress from 0.0.0.0/0**. 

![CIS 4.1](./images/01-standards-cis-4-1-detail.png)

5. Scroll down and you will notice there are some **FAILED** and some **PASSED** 

6. Select a **FAILED** Findings.  Notice the definition of CIS 4.1.

7. Click the **Remediation**, to open guidance in a new tab.

!!! info "AWS Security Hub Security Standards provide remediation guidance for each check."

![CIS 4.1](./images/01-standards-cis-4-1-remediation.png)


Now that you have explored Security Hub's capabilities, you can proceed to the next module.





















