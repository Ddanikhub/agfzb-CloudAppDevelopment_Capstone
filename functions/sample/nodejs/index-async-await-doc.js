
async function main(params) {

    const auth = {
        "COUCH_URL": "https://705b1830-7b57-47a9-bc15-86ca8fee12fb-bluemix.cloudantnosqldb.appdomain.cloud",
        "IAM_API_KEY": "qs-CR3c-ww_auqxziy-3Bp1pjh9FURpTvVP1Fmuwopds",
        "COUCH_USERNAME": "705b1830-7b57-47a9-bc15-86ca8fee12fb-bluemix"
    }
    const { CloudantV1 } = require('@ibm-cloud/cloudant');
    const { IamAuthenticator } = require('ibm-cloud-sdk-core');
    const authenticator = new IamAuthenticator({ apikey: auth.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
        authenticator: authenticator
    });
    cloudant.setServiceUrl(auth.COUCH_URL);

    let findInDocs = await cloudant.postFind({
        db: 'dealerships',
        selector: {
            "st":
                { "$eq": params.st }

        },
        fields: ["_id",
            "id",
            "short_name",
            "full_name",
            "address",
            "city",
            "state",
            "zip",
            "lat",
            "long",
        ],
    }).then(response => {
        //  console.log("State", response.result);
        return { "doc": response.result };
    }).catch(error => {
        if (error.code !== undefined && error.code === "ERR_INVALID_ARG_VALUE") {
            // The request was not sent, so there is no error status code, text and body
            console.log("Invalid argument value: \n" + error.message);
        } else {
            console.log("Error status code: " + error.status);
            console.log("Error status text: " + error.statusText);
            console.log("Error message:     " + error.message);
            console.log("Error details:     " + error.body)
        }
    });

    if (findInDocs.doc.bookmark !== "nil") {
        // All Docs in DB -----------------------------------
        console.log(params)
        console.log(findInDocs);
        return { findInDocs };

    }


    else {
        let allDocs = await cloudant.postAllDocs({
            db: 'dealerships',
            includeDocs: true,
        }).then(response => {
            // console.log(response.result);
            return { "doc": response.result };
        }).catch(error => {
            if (error.code !== undefined && error.code === "ERR_INVALID_ARG_VALUE") {
                // The request was not sent, so there is no error status code, text and body
                console.log("Invalid argument value: \n" + error.message);
            } else {
                console.log("Error status code: " + error.status);
                console.log("Error status text: " + error.statusText);
                console.log("Error message:     " + error.message);
                console.log("Error details:     " + error.body)
            }
        });
        console.log(params)
        console.log(allDocs);
        return { allDocs }
    }
}


