<p align="center">
    <img src="https://avatars1.githubusercontent.com/u/3573467?s=96" alt="Python Italia Logo" />
</p>

# PyCon Italia website

> The monorepo for the new PyCon Italia website, based on Django, Strawberry,
> Next.js and React.

## How to setup

Use our local docker-compose setup to start all services you need.

After cloning the project, you can run:

```
docker-compose up
```

to start the services.

You will find the services at the following ports:

| Service name         | Address               |
| -------------------- | --------------------- |
| Backend              | http://localhost:8000/admin - http://localhost:8000/cms-admin |
| Frontend             | http://localhost:3000 |

Everything you need to get started is already configured
and will work out of the box.

If you need to work with our Stripe or Pretix integration, you will have to ask
on Slack which secret key you need and why you need it.

Once given, create a `.env` file at the project root with inside:

```text
STRIPE_PUBLIC_KEY=
PRETIX_API_TOKEN=
STRIPE_WEBHOOK_SIGNATURE_SECRET=
STRIPE_SECRET_API_KEY=
```

Adding the secret keys after the `=` symbol.

## External repos

Repos used by this project are in separate repositories.

| Name          | Description                                             | Link                                                   |
| ------------- | ------------------------------------------------------- | ------------------------------------------------------ |
| Pretix Extended API | Pretix plugin to expose more APIs                   | https://github.com/pythonitalia/pretix-plugin-extended-api |
| Pretix Attendance certificate | Pretix plugin to generate and send Attendance certificates | https://github.com/pythonitalia/pretix-plugin-attendance-certificate |

[<img src="https://www.datocms-assets.com/31049/1618983297-powered-by-vercel.svg">](https://vercel.com?utm_source=python-italia&utm_campaign=oss)
