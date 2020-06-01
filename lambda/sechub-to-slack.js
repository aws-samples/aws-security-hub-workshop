'use strict';
const AWS = require('aws-sdk');
const url = require('url');
const https = require('https');

const webHookUrl = process.env['webHookUrl'];
const slackChannel = process.env.slackChannel;

function postMessage(message, callback) {
const body = JSON.stringify(message);
const options = url.parse(webHookUrl);
options.method = 'POST';
options.headers = {
'Content-Type': 'application/json',
'Content-Length': Buffer.byteLength(body),
};

const postReq = https.request(options, (res) => {
const chunks = [];
res.setEncoding('utf8');
res.on('data', (chunk) => chunks.push(chunk));
res.on('end', () => {
if (callback) {
callback({
body: chunks.join(''),
statusCode: res.statusCode,
statusMessage: res.statusMessage,
});
}
});
return res;
});

postReq.write(body);
postReq.end();
}

function processEvent(event, callback) {
const message = event;
const consoleUrl = `https://console.aws.amazon.com/securityhub`;
const finding = message.detail.findings[0].Types[0];
const findingDescription = message.detail.findings[0].Description;
const findingTime = message.detail.findings[0].UpdatedAt;
const findingTimeEpoch = Math.floor(new Date(findingTime) / 1000);
const account =  message.detail.findings[0].AwsAccountId;
const region =  message.detail.findings[0].Resources[0].Region;
const type = message.detail.findings[0].Resources[0].Type;
const messageId = message.detail.findings[0].Resources[0].Id;
const lastSeen = `<!date^${findingTimeEpoch}^{date} at {time} | ${findingTime}>`;
var color = '#7CD197';
var severity = '';

if (1 <= message.detail.findings[0].Severity.Normalized && message.detail.findings[0].Severity.Normalized <= 39) {severity = 'LOW'; color ='#879596';}
else if (40 <= message.detail.findings[0].Severity.Normalized && message.detail.findings[0].Severity.Normalized <= 69) {severity = 'MEDIUM'; color = '#ed7211';}
else if (70 <= message.detail.findings[0].Severity.Normalized && message.detail.findings[0].Severity.Normalized <= 89) {severity = 'HIGH'; color = '#ed7211';}
else if (90 <= message.detail.findings[0].Severity.Normalized && message.detail.findings[0].Severity.Normalized <= 100) {severity = 'CRITICAL'; color = '#ff0209';}
else {severity = 'INFORMATIONAL'; color = '#007cbc';}

const attachment = [{
"fallback": finding + ` - ${consoleUrl}/home?region=` + `${region}#/findings?search=id%3D${messageId}`,
"pretext": `*AWS SecurityHub finding in ${region} for Acct: ${account}*`,
"title": `${finding}`,
"title_link": `${consoleUrl}/home?region=${region}#/research`,

"text": `${findingDescription}`,
"fields": [
{"title": "Severity","value": `${severity}`, "short": true},
{"title": "Region","value": `${region}`,"short": true},
{"title": "Resource Type","value": `${type}`,"short": true},
{"title": "Last Seen","value": `${lastSeen}`, "short": true}
],
"mrkdwn_in": ["pretext"],
"color": color
}];

const slackMessage = {
channel: slackChannel,
text : '',
attachments : attachment,
username: 'SecurityHub',
'mrkdwn': true,
icon_url: 'https://raw.githubusercontent.com/aws-samples/amazon-securityhub-to-slack/master/images/gd_logo.png'
};

postMessage(slackMessage, (response) => {
if (response.statusCode < 400) {
console.info('Message posted successfully');
callback(null);
} else if (response.statusCode < 500) {
console.error(`Error posting message to Slack API: ${response.statusCode} - ${response.statusMessage}`);
callback(null);
} else {
callback(`Server error when processing message: ${response.statusCode} - ${response.statusMessage}`);
}
});
}
exports.handler = (event, context, callback) => {
        processEvent(event, callback);
};