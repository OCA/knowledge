To configure this module, you need to:

- Go to Settings -> General Settings and scroll down to the Integrations section.

- Enable "Google API", save.

  - field "Google Client ID" - enter the client ID from the Google API console.
  - field "Google API key" - enter the API key from the Google API console.
  - field "Google App ID" - enter the ID of the Google application. The default value is
    `odoo`.

- Next, open your user profile and set up personal access credentials on the "Google
  API" tab.

  - field "Google Scope" - enter the scope for the Google API. The default value is
    `https://www.googleapis.com/auth/drive.readonly`.
  - field "Google Access Token" - your token will be displayed here. It is necessary to
    edit it.
  - field "Google Mime Types" - enter the file formats to be filtered when selecting.
    Example: `application/pdf, image/jpeg, image/png`. By default, all files are
    selected

- You will be asked to authenticate when you add a link for the first time.
