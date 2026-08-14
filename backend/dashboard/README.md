# Dashboard data sources

The dashboard always reads conference, proposal, decision, grant, and allocated
budget data from the configured Django database.

Ticket totals, gross ticket revenue, completed refunds, product mix, and the
eight-week sales chart are calculated from Pretix's read-only Items and Orders
APIs.

## Local setup

The default Docker configuration points the backend at an isolated local Pretix
API. Pretix is optional and lives behind the `pretix` Compose profile, so it
does not add startup time to unrelated development work.

To start Pretix without adding staged data:

```sh
docker compose --profile pretix up -d --wait pretix
```

The control panel is at <http://localhost:8345/control/>. The local-only login is
`admin@localhost` / `admin` after running the stage seeder below.

### Dashboard stages

Run the disposable stage seeder from the repository root:

```sh
./scripts/seed-dashboard-stage cfp-open
```

Available stages are:

- `cfp-open`
- `review`
- `ticket-sales`
- `conference-week`
- `post-event`

Each run replaces only the `dashboard-local` conference and the matching
`python-italia-local/dashboard-local` Pretix event. It creates deterministic
proposal, vote, grant, reimbursement, product, order, and ticket histories for
the selected point in time. Open the result at
<http://localhost:8000/dashboard/dashboard-local>. The seeded Pretix shop is at
<http://localhost:8345/python-italia-local/dashboard-local/>.

The seeder refuses to run when Django is not in debug mode or when `PRETIX_API`
does not resolve to `pretix`, `localhost`, or `127.0.0.1`. Local Pretix uses its
own PostgreSQL database and Docker volumes. Stop it with:

```sh
docker compose --profile pretix stop pretix pretix-db
```

Set `LOCAL_PRETIX_API` and `LOCAL_PRETIX_API_TOKEN` only when deliberately
testing a different development instance. The existing `PRETIX_API_TOKEN` in
`.env` is not used by the Compose backend, which prevents a local stage run from
accidentally authenticating to hosted Pretix.

## Production behavior

Production already provides `PRETIX_API` and `PRETIX_API_TOKEN`. The response is
reduced to aggregate values in memory: order codes, attendee details, email
addresses, and other personal data are never cached or sent to the browser.

Pretix aggregates are cached for 15 minutes. API failures render a safe
unavailable state instead of failing the whole dashboard, and that unavailable
state is cached briefly so a Pretix outage cannot create a request storm.

The production dashboard is available at
<https://admin.pycon.it/dashboard> and requires a staff account. Comparisons are
limited to two additional conferences to bound cold-cache Pretix and database
work. Relevant settings are:

```text
DASHBOARD_REQUIRE_STAFF=true
DASHBOARD_MAX_COMPARISON_CONFERENCES=2
DASHBOARD_PRETIX_CACHE_TIMEOUT=900
DASHBOARD_PRETIX_ERROR_CACHE_TIMEOUT=60
PRETIX_API_TIMEOUT=10
PRETIX_API_HOST=
```

Use a least-privilege Pretix token with read access only to the required
organizer/events and the Items and Orders resources.

Before enabling a release, verify the dashboard build check, the focused
dashboard/Pretix tests, and a staff login against the deployed `/dashboard` URL.
Ticket analytics may intentionally show as unavailable while Pretix is
unreachable; proposal and grant analytics should continue to render.
