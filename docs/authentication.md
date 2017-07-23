# Authentication

The authentication is done via [Python Social Auth for django](https://github.com/python-social-auth/social-app-django).

See below how to configure the applications for each provider.


## Twitter

Go to [apps.twitter.com/](https://apps.twitter.com/) and create a new application. Make sure that the
**Callback URL** is filled with the following url:

    https://domain/complete/twitter

Once the application has been created fill the **Privacy Policy URL** and **Terms of Service URL** fields.
This are required to get the user's email when they sign in.

Then go to the **Permissions** tab and change the access to **Read only** since we don't need to write
tweets on the user behalf. Also make sure that **Request email addresses from users** inside Additional Permissions
is ticked.

Finally you can go inside **Keys and Access Tokens** and get the **Consumer Key (API Key)** and
**Consumer Secret (API Secret)** that are required by the backend. You should then set the following
environment variables:

    SOCIAL_AUTH_TWITTER_KEY=XXXXXXXXXXXXXXXXXXXXXX
    SOCIAL_AUTH_TWITTER_SECRET=XXXXXXXXXXXXXXXXXXXXXX

