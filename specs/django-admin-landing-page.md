# Spec: New Django Admin Landing Page

Status: **IMPLEMENTING — T1–T4 done (tests+lint pass), T5 deferred, browser
verification pending**
Author: Claude + Marco
Date: 2026-06-02

## Objective

Replace the stock Django admin index (`/admin/`) — currently a plain table
list of apps/models (`custom_admin/templates/admin/index.html`) — with a
modern **dashboard landing page** rendered as an Astro/React overlay (the
existing custom-admin pattern).

Users: PyCon Italia staff/organizers using the Django admin daily.

Success = on visiting `/admin/`, staff see a redesigned dashboard that:
1. **Visual redesign** — card/grid layout instead of stock app/model table.
2. **Dashboard stats** — widget slots for live metrics (submissions, grants
   pending, tickets, etc.). *Data wiring deferred* — placeholders/empty state
   this phase, layout must accommodate real numbers later.
3. **Quick actions / links** — curated shortcuts to common tasks (e.g. review
   grants, schedule builder, document builders).
4. **Reorganize apps** — group/prioritize apps & models by workflow, not raw
   alphabetical `app_list`.

Out of scope: Wagtail admin (`/cms-admin/`), changing per-model admin pages,
actual stats data sources (separate follow-up).

## Tech Stack

- Backend: Django 5.2.8, plain `django.contrib.admin`
- Overlay: Astro (SSR dev, port 3002) + React 18 + Apollo Client + Tailwind +
  Radix UI — the `custom_admin/` Astro app
- Data (later): existing `/admin/graphql` Strawberry endpoint
  (`api/schema.py`), client-side via Apollo + GraphQL codegen

## Commands

```
# Backend (must run in docker)
docker exec pycon-backend-1 uv run pytest -l -s -vvv
docker exec pycon-backend-1 uv run ruff check
docker exec pycon-backend-1 uv run ruff format

# Astro custom-admin (inside backend/custom_admin)
pnpm dev          # codegen:watch + ws-proxy + astro dev :3002
pnpm codegen      # regenerate typed GraphQL hooks
pnpm build        # production build

# Full stack
docker-compose up
```

## Project Structure (new/changed files)

```
backend/custom_admin/
  src/pages/landing.astro                  → new full-page Astro entry (Approach B)
  src/components/landing/
    root.tsx                               → React root (Apollo Base wrapper)
    dashboard.tsx                          → card grid + sections layout
    quick-actions.tsx                      → curated shortcut cards
    stat-card.tsx                          → reusable metric widget (placeholder)
    landing.graphql                        → stats queries (added when data wired)
  templates/admin/index.html               → MODIFIED (Approach A) OR unused (B)
  admin.py / new AdminSite                 → MODIFIED if Approach B
specs/django-admin-landing-page.md         → this spec
```

## Code Style

Match existing custom-admin React. Example (existing `schedule-builder/root.tsx`):

```tsx
export const LandingRoot = ({ appList, quickLinks }: Props) => {
  return (
    <Base args={{ appList, quickLinks }}>
      <DjangoAdminLayout>
        <Suspense fallback={<Spinner />}>
          <Dashboard />
        </Suspense>
      </DjangoAdminLayout>
    </Base>
  );
};
```

- Astro page receives Django context as `{{ var }}`, injects as React props
  (`client:only`); complex objects via `| to_json_for_prop`.
- Tailwind utility classes; Radix UI for primitives.
- Python: ruff format, existing admin conventions.

## Testing Strategy

- **Python**: pytest. Test the index view returns 200 + correct template/context
  (app grouping, quick links). Located in `backend/custom_admin/tests/`.
- **Frontend**: existing Astro app has minimal tests; add light component render
  checks only if a test setup exists (verify before assuming).
- **Manual**: `docker-compose up`, visit `/admin/`, confirm dashboard renders in
  dev (DEBUG=True proxy) — and that `pnpm build` produces prod assets (prod proxy
  returns 404, served from build).

## Boundaries

- **Always**: run ruff + pytest before commit; match existing overlay pattern;
  keep `/admin/` working for users without overlay JS (graceful base list).
- **Ask first**: subclassing/replacing `admin.site` (AdminSite) [Approach B];
  adding npm/uv dependencies; changing `template_backends.py` proxy logic;
  touching prod static-build pipeline.
- **Never**: commit secrets; break other proxied pages (schedule-builder etc.);
  remove existing `CustomIndexLinks` mechanism without replacement.

## Decisions (locked 2026-06-02)

- **Render: Approach B** — full Astro page on `/admin/`. To avoid re-registering
  ~65 model admins, **override `admin.site.index` method on the existing default
  site** (not a new AdminSite subclass + re-point). The custom index view returns
  `TemplateResponse(request, "astro/landing.html", ctx)` with `each_context` +
  grouped app data + quick links.
- **Grouping**: Claude proposes workflow groups from real model list → Marco edits.
- **Fallback list**: dashboard on top, full "All models" stock list as a section
  below for completeness.

## Key Decision (RESOLVED — see Decisions above)

**How to render the Astro UI on the fixed `/admin/` index route:**

- **Approach A — React island in `index.html`**: Keep Django `index.html`
  (extends `base_site.html`, already Astro-proxied). Mount a React widget for
  dashboard cards/stats. No custom AdminSite. *Pros*: smallest blast radius,
  stock index still works as fallback. *Cons*: less layout control, mixed
  Django-template + island.

- **Approach B — Custom `AdminSite.index()`**: Subclass `AdminSite`, override
  `index()` → `TemplateResponse(request, "astro/landing.html", ctx)`, full Astro
  page (mirrors schedule-builder). *Pros*: full-page control, cleanest match to
  existing pattern. *Cons*: replacing `admin.site` is a global change (must
  re-register all ~65 model admins against new site or set `default_site`);
  higher risk.

Recommendation: **A** for first iteration (low risk, ships the redesign +
quick-links + reorg), migrate to **B** later if full-page control needed.

## Plan (Phase 2)

### Proposed app/model groups (Marco to confirm/edit)

1. **Program** — Submission, SubmissionType, SubmissionTag, SubmissionComment,
   Vote, RankSubmission, RankRequest, RankStat, UserReview, ReviewSession,
   Keynote, Event
2. **Schedule & Video** — ScheduleItem, ScheduleItemInvitation, Room, Day,
   ScheduleItemSentForVideoUpload, WetransferToS3TransferRequest
3. **Finance** — Grant, GrantReimbursement, GrantReimbursementCategory,
   GrantConfirmPendingStatusProxy, Invoice, Sender, Address, Item,
   BillingAddress, PretixPayment, StripeSubscriptionPayment, Membership
4. **Sponsors** — Sponsor, SponsorBenefit, SponsorLevel, SponsorSpecialOption,
   SponsorLead
5. **People** — User, Participant, AttendeeConferenceRole, BadgeScan,
   InvitationLetterRequest, InvitationLetterConferenceConfig, Organizer,
   Notification, VolunteerDevice
6. **Conference setup** — Conference, Topic, AudienceLevel, Deadline,
   ConferenceVoucher, ChecklistItem, Language
7. **Content & CMS** — Post, Page, GenericCopy, FAQ, Menu, MenuLink, JobListing,
   Subscription (newsletter)
8. **Comms** — EmailTemplate, SentEmail
9. **System** — APIToken, GoogleCloudOAuthCredential, File

Any model not listed falls through to an "Other" group automatically (no model
silently dropped).

### Implementation order (dependency-ordered)

1. Backend: custom index view overriding `admin.site.index`, building grouped
   `app_list` + quick-links context → `TemplateResponse("astro/landing.html")`.
   Verify with stock template first (no Astro) so backend is provable alone.
2. Astro page `landing.astro` + React `landing/` components (Base/Apollo wrapper,
   Dashboard grid, group cards, quick-action cards, stat-card placeholder).
3. "All models" full stock list as a collapsible section below dashboard.
4. Stats: leave `stat-card` placeholders; add `landing.graphql` + wiring in a
   follow-up once data sources picked.

### Risks / mitigation

- **Overriding `admin.site.index`** could break if Django internals change →
  keep view thin, reuse `each_context` + `get_app_list`, cover with a test.
- **Grouping drift** as models added → "Other" catch-all + a test asserting
  every registered model lands in exactly one group.
- **Prod proxy** returns 404 for `/astro/*` when DEBUG=False → ensure prod path
  uses built assets (same as schedule-builder); verify `pnpm build`.

## Tasks (Phase 3)

- [ ] **T1 — Backend custom index view**
  - Acceptance: `/admin/` served by custom view; context has grouped app_list
    (per groups above + Other catch-all) + quick_links; falls back to stock
    template render OK.
  - Verify: `pytest backend/custom_admin/tests/test_index.py` (200, groups,
    every model present once); manual `/admin/`.
  - Files: `custom_admin/admin.py` (or new `custom_admin/index.py`),
    `custom_admin/apps.py` (wire override on ready), test file.
- [ ] **T2 — Astro landing page + React shell**
  - Acceptance: `landing.astro` renders Dashboard via React island; receives
    grouped data + quick links as props.
  - Verify: `docker-compose up`, visit `/admin/`, dashboard cards show; `pnpm build`.
  - Files: `src/pages/landing.astro`, `src/components/landing/root.tsx`,
    `dashboard.tsx`.
- [ ] **T3 — Group cards + quick actions + stat-card placeholders**
  - Acceptance: workflow group cards link to model changelists; quick-action
    cards link correctly; stat-cards show empty/placeholder state.
  - Verify: manual click-through; visual check.
  - Files: `src/components/landing/{dashboard,quick-actions,stat-card}.tsx`.
- [ ] **T4 — "All models" fallback section**
  - Acceptance: full stock app/model list present below dashboard.
  - Verify: manual; rare model (e.g. Language) reachable.
  - Files: `dashboard.tsx` (+ template if needed).
- [ ] **T5 — Stats data wiring (follow-up, deferred)**
  - Acceptance: stat-cards show real counts via `/admin/graphql`.
  - Verify: codegen + query returns numbers.
  - Files: `landing.graphql`, `api/...` resolvers, `stat-card.tsx`.

## Success Criteria

- [x] `/admin/` served by custom dashboard view (groups/quick_links context).
- [x] Apps/models reorganized into 9 workflow groups + Other catch-all.
- [x] Quick-action shortcuts (schedule builder, grants, submissions) built.
- [x] Stat-card widget slots render with placeholder dash state.
- [x] All-models fallback section (collapsible).
- [x] ruff + pytest pass (5 tests); biome clean on new TS.
- [ ] Browser check: `docker-compose up` shows page; `pnpm build` succeeds.
- [ ] No regression: other admin pages + proxied Astro pages still work (verify
      in browser).

## Open Questions

1. **Approach A vs B?** (see Key Decision) — recommend A.
2. **Which quick actions** to feature? (need Marco's list of top daily tasks)
3. **App grouping** — what workflow groups? (e.g. "Content", "Program",
   "Finance/Grants", "Users", "System"?)
4. Which **stats** to slot in (even as placeholders) so layout is sized right?
5. Should stock app/model list remain accessible (e.g. below dashboard / a
   "All models" section) for completeness?
