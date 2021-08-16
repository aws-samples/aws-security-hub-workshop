# Overview

This workshop is designed to get you familiar with AWS Security Hub so that you can better understand how you would use it in your own AWS environment(s). This workshop is broken into two sections. The first section will guide you through a demonstration of the features and functions of Security Hub. The second section will show you how to use Security Hub to import findings from different data sources, analyze findings so you can prioritize response work, and implement responses to findings to help improve your security posture. 



* **Level**: Intermediate
* **Duration**: 2 - 3 hours
* **<a href="https://www.nist.gov/cyberframework/online-learning/components-framework" target="_blank" rel="noopener noreferrer">CSF Functions</a>**: Detect, Respond
* **<a href="https://d0.awsstatic.com/whitepapers/AWS_CAF_Security_Perspective.pdf" target="_blank" rel="noopener noreferrer">CAF Components</a>**: Detective, Responsive
* **<a href="https://awssecworkshops.com/getting-started/" target="_blank" rel="noopener noreferrer">Prerequisites</a>**: AWS Account, Admin IAM User

## Scenario

Your company is new to the cloud and is steadily migrating workloads into your cloud environment.  To detect security events you are using a mix of 3rd party services, custom scripts, and AWS services.  As a security analyst you are responsible for establishing a solution that will give visibility into security findings related to your AWS environment so that you can properly prioritize and respond to findings.   

## Architecture

For this workshop there will be multiple pieces of infrastructure and AWS services deployed in order to facilitate creation of security findings in Security Hub.  

Multiple EC2 instances will be launched to facilitate the generation of findings from GuardDuty & Inspector.  Additionally these instances will be used to help with demonstration of integration of custom findings into Security Hub.

Multiple AWS services will be configured in the workshop to help facilitate the generation of Security Hub findings.  These services include:

* <a href="https://aws.amazon.com/security-hub/" target="_blank"> AWS Security Hub </a>
* <a href="https://aws.amazon.com/guardduty/" target="_blank"> Amazon GuardDuty </a>
* <a href="https://aws.amazon.com/secrets-manager/" target="_blank"> Amazon Secrets Manager</a>
* <a href="https://aws.amazon.com/inspector/" target="_blank"> Amazon Inspector</a>
* <a href="https://aws.amazon.com/config/" target="_blank"> AWS Config</a>
* <a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html" target="_blank"> AWS IAM Access Analyzer</a>


## Presentation deck
[Security Hub Workshop Presentation](./security-hub-workshop-presentation.pdf)

## Region
Please use **us-west-2 (Oregon)** or **us-east-1 (Virgina)** for this workshop.

## Modules

This workshop is broken up into setup and then four modules: 

Module 0 - [Environment build ](./00-environment-setup.md)  
Module 1 -  [Security Hub Walkthrough ](./01-security-hub-walk-through.md)  
Module 2 -  [Custom Insights & Findings](./02-custom-insights-findings.md)     
Module 3 - [Remediation & Response](./03-remediation-and-response.md)   
Module 4 - [Enrichment & Integration](./04-enrichment-and-integration.md)  



## Contributing
Your contributions are always welcome! Please have a look at the [contribution guidelines](contribute.md) first.

[(Back to top)](#Overview)

## License Summary

The documentation is made available under the Creative Commons Attribution-ShareAlike 4.0 International License. See the [LICENSE](LICENSE) file.

The sample code within this documentation is made available under the MIT-0 license. See the [LICENSE-SAMPLECODE](LICENSE-SAMPLECODE.md) file.

[(Back to top)](#Overview)
