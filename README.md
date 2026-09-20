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

## Enabling Django Debug Toolbar

To enable the Django Debug Toolbar, set the `ENABLE_DJANGO_DEBUG_TOOLBAR` variable to `true` in your `.env` file:

```text
ENABLE_DJANGO_DEBUG_TOOLBAR=true
```

## Durable workflows (Resonate)

Long, multi-step operations run as [Resonate](https://www.resonatehq.io/)
durable workflows, executed by the `resonate-worker` service (`docker-compose
up` starts it, along with the Resonate server and its UI at
http://localhost:8005).

Workflows live in `<app>/workflows.py` (or `<app>/workflows/`); they are
registered against the instance returned by `pycon.resonate_app.get_resonate()`
and discovered automatically by the worker. Synchronous, ORM-using steps are
wrapped with `pycon.resonate_app.database_step`.

The worker restarts itself when the code changes, like `runserver` does, so
editing a workflow is enough to see it run in its new shape. Pass `--no-reload`
to turn that off; outside `DEBUG` it is off to begin with.

To start a workflow from Django (a view, an admin action, a command), use
`pycon.resonate_app.start_workflow(name, workflow_id, ...)`. The workflow id is
the idempotency key: creating the same id twice joins the existing run.

Creating the next edition of the conference is one of those workflows: select
the conference to use as base in the admin and run the *Create new conference
using this one as base* action, which asks for the code, name, hostname and
dates of the new edition (prefilled with the next year's) and starts the
workflow.

It copies configuration only (deadlines, shifted by the new start date;
durations; the schedule days, laid out over the new dates with the rooms and
slots of the edition it copies; sponsor levels, benefits and special options;
email templates; menus, copy and FAQs; forms and their questions; voting
included events). Everything produced during an edition -- proposals, the talks
scheduled into those slots, keynotes, sponsors, grants, vouchers, answers -- is
not copied, and neither are the pretix ids or the logo.

## External repos

Repos used by this project are in separate repositories.

| Name          | Description                                             | Link                                                   |
| ------------- | ------------------------------------------------------- | ------------------------------------------------------ |
| Pretix Extended API | Pretix plugin to expose more APIs                   | https://github.com/pythonitalia/pretix-plugin-extended-api |
| Pretix Attendance certificate | Pretix plugin to generate and send Attendance certificates | https://github.com/pythonitalia/pretix-plugin-attendance-certificate |
