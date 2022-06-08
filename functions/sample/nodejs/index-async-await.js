/**
 * Get all dealerships
 */

var jauth = require('./.creds-sample.json');

var params = {
  "COUCH_URL": "https://705b1830-7b57-47a9-bc15-86ca8fee12fb-bluemix.cloudantnosqldb.appdomain.cloud",
  "IAM_API_KEY": "qs-CR3c-ww_auqxziy-3Bp1pjh9FURpTvVP1Fmuwopds",
  "COUCH_USERNAME": "705b1830-7b57-47a9-bc15-86ca8fee12fb-bluemix"
}

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
  const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
  const cloudant = CloudantV1.newInstance({
    authenticator: authenticator
  });
  cloudant.setServiceUrl(params.COUCH_URL);
  try {
    let dbList = await cloudant.getAllDbs();
    console.log("dbs", dbList.result)
    return { "dbs": dbList.result };
  } catch (error) {
    return { error: error.description };
  }
}

main(params)
