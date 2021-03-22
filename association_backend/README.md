<p align="center">
    <img src="https://avatars1.githubusercontent.com/u/3573467?s=96" alt="Python Italia Logo" />
</p>

# PyCon Italia website - Association Service

> The Association service to handle Pycon User Association Subscriptin Management
> Written in Starlette, Strawberry, Pydantic and SQLAlchemy using DDD approach

## How to setup

To install this service make you sure you have poetry installed, then run the
following command in the backend directory:

    poetry install

This will create the virtual environment and install all the dependencies
(including dev ones).

Create a `.env` file by copying the `.env.sample`, this will setup basic
environment variables for debugging.

To make sure everything went fine you can run the tests:

    poetry run task test
Note:

`poetry run` will run the command inside the virtual environment, without you
having to manually activate it.

To create the Database and update its structure run:

    createdb YOUR_DATABASE_NAME -U postgres
    poetry run task migrate

Once that's done we can run the dev server by running:

    poetry run task server

To check if the API is up an running go to `http://localhost:8060/graphql`


## Stripe Setup

- [Product and price creation](https://dashboard.stripe.com/test/products)
- Set STRIPE_SUBSCRIPTION_PRODUCT_ID & STRIPE_SUBSCRIPTION_PRICE_ID in your .env
- [API Key + API Secret](https://dashboard.stripe.com/test/apikeys)
- Set STRIPE_SUBSCRIPTION_API_KEY & STRIPE_SUBSCRIPTION_API_SECRET in your .env
- [Webhook Creation and Configuration](https://dashboard.stripe.com/test/webhooks)
- Set STRIPE_WEBHOOK_SIGNATURE_SECRET in your .env
- Add (at least) these events to your webhook:

   • checkout.session.completed

   • customer.subscription.updated

   • customer.subscription.deleted

   • invoice.paid

- [Email configuration](https://dashboard.stripe.com/settings/emails)
- [For Invoice Email handling, visit Invoice settings](https://dashboard.stripe.com/settings/billing/automatic)

