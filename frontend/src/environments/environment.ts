/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-rof0zfah257z8231.us.auth0.com', // the auth0 domain prefix
    audience: 'https://dev-rof0zfah257z8231.us.auth0.com/api/v2/', // the audience set for the auth0 app
    clientId: 'CKpgux1QAgvEIL2R3BStTwtRFm5wwaGO', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
