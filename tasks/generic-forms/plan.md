# Implementation Plan: Generic Form System

Source spec: [specs/generic-form-system.md](../../specs/generic-form-system.md) · Mode: plan (read-only, no code changed)
Structure: **5 stacked PRs** — each PR is independently mergeable and deployable, stacked in order.
Reviewed: adversarial verify pass (3 independent critics) applied — see "Verified constraints" below.

## Overview

Build the `generic_forms` engine (Form / FormQuestion / FormAnswer, freeze-on-answer, JSON answers with versioned envelope), expose it over GraphQL, wire grants as the first consumer (6 soft questions move from hardcoded `Grant` columns to dynamic form answers; `gender`/`occupation` stay structured — see build correction below), surface answers in grant admin + export, and render the form dynamically on the frontend.

## Resolved since spec (verified in codebase)

- `react-hook-form` has **zero** usages despite being in package.json; every form (incl. the modern `invitation-letter-form.tsx`) uses `react-use-form-state`. New `DynamicForm` uses `react-use-form-state`. (Spec §3/§8 corrected.)
- Grant's social columns (`website`, `twitter_handle`, …) are **already dead** — not in the GraphQL `Grant` type, not written by the form (socials go through `Participant` via `PublicProfileCard`). They do NOT become form questions. (Spec decision #5 corrected; the soft set was later reduced to 6 — see the build correction below.)
- `send_grant`/`update_grant` are `@transaction.atomic` ([api/grants/mutations.py:226,297](../../backend/api/grants/mutations.py)) — FormAnswer persistence slots into the existing transaction.
- `BaseGrantInput.validate()` (mutations.py:74-111) **mixes** structured-field checks (`full_name`, `grant_type`, departure fields — these STAY) with soft-field checks (max lengths why:1000, python_usage:700, been_to_other_events:500, community_contribution:900, notes:350; required: why, python_usage, been_to_other_events). Only the soft-field portion is superseded by `validate_answers` — structured-field validation must remain untouched.
- **Build correction (user-caught):** `grants/summary.py` aggregates the `gender` AND `occupation` columns for grant summary reporting — both are load-bearing, NOT soft. The dynamic set is 6: `why`, `python_usage`, `been_to_other_events`, `community_contribution`, `age_group`, `notes`. gender/occupation remain optional structured inputs (coalesced to `""` when omitted). Spec decision #5 amended.
- Of the 8 originally-soft columns, exactly **4** lack `blank=True` today: `why`, `python_usage`, `been_to_other_events`, `occupation`. The other 4 (`age_group`, `community_contribution`, `gender`, `notes`) are already `blank=True`. All 8 are NOT NULL at the DB level (`blank=True` is Python-only) — `None` must never reach `Grant.objects.create`.
- django-import-export is **3.3.9**; dynamic per-export fields are supported: `Resource.__init__` deep-copies `self.fields` (sanctioned mutation point), and `GrantAdmin.get_export_resource_kwargs(request, ...)` passes context into `GrantResource.__init__`. Extra instance fields auto-append to export order.
- Conference GraphQL pattern to mirror: `deadline(self, info, type: str)` at [api/conferences/types.py:196](../../backend/api/conferences/types.py#L196). Enum pattern: `strawberry.enum(Model.TextChoices)`.
- Tests: model tests in `generic_forms/tests/`, API tests in `api/generic_forms/tests/` + `api/grants/tests/`; `graphql_client` fixture, factory_boy, `pytest.mark.django_db`.
- No read-only-JSON admin precedent exists — the answers display in GrantAdmin is net-new (simple `format_html` list, no new deps).

## Verified constraints (from the adversarial review — these shape the tasks)

1. **Dotted `answers.<id>` error paths are impossible.** `BaseErrorType.add_error` getattr-traverses statically-typed error classes (api/types.py:33-74); dynamic keys raise `AttributeError`, and strawberry cannot serialize dynamic field names regardless. The in-repo dotted precedent (`materials.0.url`) lives in **api/submissions** (not visa) and works only because `materials: list[ProposalMaterialErrors]` is statically declared. **Decision (resolved, not a risk): `answers_errors: JSON` field on `_GrantErrors`, set by direct assignment.** Spec §5/§8/§11 updated. Frontend consumes `answersErrors` only.
2. **PR3 must survive the exact PR5 payload.** An answers-only submission (all 8 soft fields omitted) must pass: (a) legacy soft-field required/max-length checks run ONLY on the legacy path (answers not provided); (b) soft input `None` values coalesce to `""` before `Grant.objects.create` / the update setattr loop (DB columns are NOT NULL). A named PR3 test sends answers and omits all 8 soft fields.
3. **Frontend codegen needs a deployed backend schema.** `codegen.yml` fetches the schema from a live endpoint; PR CI (`frontend-lint.yml`) codegens against the staging backend (pastaporto), which deploys only via manual `workflow_dispatch`. **PR5 therefore build-depends on PR3 being deployed to staging**, not merely merged. Release step added before PR5. (Optional improvement, needs approval per spec boundaries — CI change: check in a schema snapshot via `strawberry export-schema` and point codegen at the file.)
4. **Deadline-closed behavior stays as-is** (`non_field_errors: "The grants form is not open!"`). No `FormNotAvailable` union member — changing the response shape breaks the deployed frontend. Spec §5 amended accordingly. `answers` with no GRANT form configured → clear field error.
5. **Production data dependency:** the GRANT form must exist (with the 8 questions) in production admin BEFORE PR5 deploys, or the live form loses its soft questions. Seeding command was explicitly cut from scope → this is a manual ops step in Checkpoint 5, on both staging and production. Frontend must also handle `form == null` by blocking submission with a "form not available" state (never submit without answers).
6. **Legacy-field removal follow-up must be two PRs**, not one: (1) frontend-only — strip legacy `GrantErrors` validation selections (submit-grant.graphql:12-34, pages/grants/edit/update-grant.graphql:25-52) and legacy soft-field selections (my-grant.graphql, update-grant.graphql) — deployable against the unchanged backend; (2) after deploy + soak (stale browser tabs still send old payloads), backend-only — remove the legacy input fields. PR5 already stops *sending* soft fields; it also strips whatever legacy selections it can without breaking its own build.

## Architecture decisions

- **Stacked-PR back-compat rule:** every PR leaves `main` deployable (backend deploys before frontend, per deploy.yml ordering). PR3 is strictly additive on the wire: soft fields optional, `answers` optional, legacy shape untouched.
- **Answers storage:** versioned envelope `{"version": 1, "answers": {"<question_pk>": value}}`; GraphQL wire format is the flat map (`strawberry.scalars.JSON`).
- **Question ids as answer keys:** `FormQuestion.pk` stringified; frontend treats them as opaque.
- **Prefill regression accepted and specced** (spec §2 out-of-scope): dateBirth→ageGroup and user.gender prefills drop.
- **Mid-cycle cutover caveat:** grants submitted pre-PR5 (legacy path) have soft answers in columns, not FormAnswer — post-cutover their edit view shows empty dynamic questions. Mitigation: deploy the cutover before grants open for the next conference (ops note in Checkpoint 5); a data backfill is explicitly out of scope.

## Dependency graph

```
PR1 generic_forms app (models + freeze + validate_answers + admin)
 ├── PR2 GraphQL query side (Conference.form(purpose))
 └── PR3 grants backend (Grant.form_answer, mutations, Grant.formAnswers)
      ├── PR4 grant admin display + export           (needs PR3 merged)
      └── PR5 frontend DynamicForm + grant form      (needs PR2 + PR3 DEPLOYED to staging for codegen/CI)
```

Linear stack order: PR1 → PR2 → PR3 → PR4 → PR5. PR4 can start once PR3 merges; PR5 once PR3 reaches staging.

---

## PR1 — `generic_forms` app core (backend only, no consumers)

Suggested branch: `generic-forms/01-app`

### Task 1.1: App skeleton + models + migration

**Description:** Create the `generic_forms` Django app with `Form`, `FormQuestion`, `FormAnswer` models per spec §4 (plain `CharField`/`TextField`, English only), DB constraints, and initial migration. Register in `INSTALLED_APPS` (dotted AppConfig path, `default_auto_field = BigAutoField` like `visa/apps.py`).

**Acceptance criteria:**
- [ ] Models match spec §4: `Form(conference, purpose, name)`, `FormQuestion(form, label, description, question_type, options, required, max_length, order, active)`, `FormAnswer(form PROTECT, user, answers JSON)`.
- [ ] Constraints enforced at DB level: unique `(form, user)` on FormAnswer; at most one form per `(conference, purpose)` when purpose != `generic` (conditional UniqueConstraint).
- [ ] Migration is plain `makemigrations` output; applies cleanly.

**Verification:** `docker exec pycon-backend-1 uv run pytest generic_forms -l` green; `uv run python manage.py makemigrations --check --dry-run` clean afterward.

**Dependencies:** None.
**Files:** `backend/generic_forms/{__init__,apps,models}.py`, `backend/generic_forms/migrations/0001_initial.py`, `backend/pycon/settings/base.py`, `backend/generic_forms/tests/{__init__,factories,test_models}.py`
**Scope:** M

### Task 1.2: Freeze-on-answer enforcement

**Description:** Once `form.answers.exists()`: changing `question_type`/`options`/`required` on a `FormQuestion`, or deleting it, raises `ValidationError`; `label`/`description`/`order`/`active` stay editable. Enforced in the model (`clean()` + `save()` guard + `delete()` override).

**Acceptance criteria:**
- [ ] Semantic-field change on an answered form raises; same change on an unanswered form succeeds.
- [ ] Delete blocked on answered form; `active=False` allowed.
- [ ] Label/description/order edits always allowed.

**Verification:** `docker exec pycon-backend-1 uv run pytest generic_forms/tests/test_models.py -l` green.

**Dependencies:** 1.1.
**Files:** `backend/generic_forms/models.py`, `backend/generic_forms/tests/test_models.py`
**Scope:** S

### Task 1.3: `validate_answers` service + envelope helpers

**Description:** `validate_answers(form, answers: dict) -> dict[str, list[str]]` per spec §4 (unknown/inactive ids, required, per-type checks, option membership incl. every multi_select item, `URLValidator`, `max_length`), plus `wrap_answers` / `unwrap_answers` envelope helpers dispatching on `version`.

**Acceptance criteria:**
- [ ] Every question type has accept + reject cases covered by tests (spec §9 list).
- [ ] Valid input returns `{}`; errors keyed by question id (this dict is exactly what `answers_errors` carries on the wire in PR3).
- [ ] Envelope round-trip: `unwrap(wrap(x)) == x`; unwrap raises on unknown version.

**Verification:** `docker exec pycon-backend-1 uv run pytest generic_forms/tests/test_services.py -l` green.

**Dependencies:** 1.1.
**Files:** `backend/generic_forms/services.py`, `backend/generic_forms/tests/test_services.py`
**Scope:** M

### Task 1.4: Django admin for form authoring

**Description:** `FormAdmin` with `FormQuestionInline` (TabularInline, mirror `SponsorLevelBenefitInline` simplicity; ordered by `order`), raw JSON widget for `options` (decision #7). Freeze rule surfaces as model validation errors in the inline (deviation applied during build: inline-level readonly would also freeze NEW rows, and adding questions to answered forms must stay possible); inline deletion blocked once answered; `Form.conference`/`purpose` readonly once answered. `FormAnswerAdmin` fully read-only (no add/change/delete — deleting answers would unfreeze questions and destroy submissions).

**Acceptance criteria:**
- [ ] Organizer can create a form + questions of every type entirely in admin (success criterion 1).
- [ ] Inline shows semantic fields readonly once the form has answers.
- [ ] FormAnswer visible but not editable in admin.

**Verification:** `docker exec pycon-backend-1 uv run pytest generic_forms -l` green; manual: create form with all 6 question types in local admin.

**Dependencies:** 1.2.
**Files:** `backend/generic_forms/admin.py`, `backend/generic_forms/tests/test_admin.py`
**Scope:** S

### ▣ CHECKPOINT 1 (end of PR1)
- [ ] `pytest generic_forms`, full `pytest`, `ruff check`, `ruff format --check`, `mypy .` all green.
- [ ] PR1 opened; human review before stacking further.

---

## PR2 — GraphQL query side

Suggested branch: `generic-forms/02-graphql-query` (stacked on PR1)

### Task 2.1: Form types + `Conference.form(purpose)` field

**Description:** `api/generic_forms/types.py`: `FormType`, `FormQuestionType` (id, label, description, questionType, required, maxLength, options as `list[FormQuestionOption(id, label)]`), `FormPurpose = strawberry.enum(Form.Purpose)`, `QuestionType = strawberry.enum(FormQuestion.QuestionType)`. Add `form(self, info, purpose: FormPurpose) -> FormType | None` to the Conference type, mirroring `deadline()`. Questions resolver returns active-only, ordered by `order`.

**Acceptance criteria:**
- [ ] Query in spec §5 works verbatim.
- [ ] Returns `null` when no form configured; inactive questions excluded; order respected.

**Verification:** `docker exec pycon-backend-1 uv run pytest api/generic_forms -l` green; `ruff`/`mypy` clean.

**Dependencies:** PR1.
**Files:** `backend/api/generic_forms/{__init__,types}.py`, `backend/api/conferences/types.py`, `backend/api/generic_forms/tests/{__init__,test_form_query}.py`
**Scope:** S

### ▣ CHECKPOINT 2 (end of PR2)
- [ ] Full backend suite + lint + types green. GraphQL schema diff reviewed (additive only). PR2 opened.

---

## PR3 — grants backend integration

Suggested branch: `generic-forms/03-grants-backend` (stacked on PR2)

### Task 3.1: `Grant.form_answer` link + soft-column loosening

**Description:** Add `Grant.form_answer = OneToOneField(generic_forms.FormAnswer, null=True, blank=True, SET_NULL)`. Loosen the **4** currently-required soft columns (`why`, `python_usage`, `been_to_other_events`, `occupation`) to `blank=True` (the other 4 already are). One migration, no data changes. Note: columns remain NOT NULL — the mutation layer must never pass `None` (handled in 3.2).

**Acceptance criteria:**
- [ ] Migration applies; no other schema changes; historical rows untouched.
- [ ] Existing grants test suite green.

**Verification:** `docker exec pycon-backend-1 uv run pytest grants api/grants -l` green.

**Dependencies:** PR1.
**Files:** `backend/grants/models.py`, `backend/grants/migrations/00XX_*.py`
**Scope:** S

### Task 3.2: Mutations accept `answers` (with tests, TDD)

**Description:** `SendGrantInput`/`UpdateGrantInput`: the 8 soft fields become optional; new optional `answers: JSON`. Validation split:
- Legacy soft-field checks (required + max-length subset of `BaseGrantInput.validate`) run **only** when the legacy path is used (`answers` not provided). Structured-field validation (`full_name`, `grant_type`, departure fields, deadline gating) is **unchanged on both paths**.
- Answers path: reject if no GRANT form configured; else `validate_answers`; failures go into new `answers_errors: JSON` field on `_GrantErrors` by direct assignment (NOT `add_error` — dynamic keys can't traverse the typed class; see Verified constraint 1).
Mutation body: inside the existing `@transaction.atomic`, wrap answers into the envelope, `update_or_create` the FormAnswer, link `grant.form_answer`. Soft input `None` values coalesce to `""` before `Grant.objects.create`; `update_grant`'s `asdict(input)` setattr loop skips `answers` and never writes `None` into soft columns. Tests land in this task (failing-first): answers happy path, invalid answers → `answersErrors` + atomic rollback (no Grant, no FormAnswer), **answers-only payload omitting all 8 soft fields end-to-end (the exact PR5 payload)**, legacy-shape regression (today's payload byte-identical behavior), update-no-duplicate (unique constraint), answers-with-no-form rejected, deadline-closed unchanged, structured-field validation unchanged.

**Acceptance criteria:**
- [ ] All paths above covered by tests in `api/grants/tests/`; whole grants suite green.
- [ ] Answers-only payload (no soft fields) succeeds — named test.
- [ ] Legacy payload behavior unchanged — named test.
- [ ] No `None` ever written to a NOT NULL soft column (create or update path).

**Verification:** `docker exec pycon-backend-1 uv run pytest api/grants grants generic_forms -l` green.

**Dependencies:** 3.1.
**Files:** `backend/api/grants/mutations.py`, `backend/api/grants/tests/test_send_grant.py`, `backend/api/grants/tests/test_update_grant.py`
**Scope:** M

### Task 3.3: Expose `Grant.formAnswers` (read side)

**Description:** `formAnswers: JSON | None` on the `Grant` GraphQL type (api/grants/types.py) returning the unwrapped flat map from the linked FormAnswer, `None` when absent. Used by the edit-flow prefill in PR5. Own query test (via `me.grant`).

**Acceptance criteria:**
- [ ] `me.grant.formAnswers` returns the flat map for a grant with FormAnswer; `null` for a legacy grant.

**Verification:** `docker exec pycon-backend-1 uv run pytest api/grants -l` green.

**Dependencies:** 3.2.
**Files:** `backend/api/grants/types.py`, `backend/api/grants/tests/test_grant_type.py` (or existing query test file)
**Scope:** XS

### ▣ CHECKPOINT 3 (end of PR3)
- [ ] Full suite + lint + mypy green. Schema diff additive.
- [ ] Back-compat verified: legacy payload tests green (old frontend deployable against this backend); answers-only payload test green (new frontend's contract already proven).
- [ ] PR3 opened — **key review gate: back-compat story**.
- [ ] After merge: **deploy to staging (pastaporto) via `workflow_dispatch`** — PR5's CI codegen needs this schema live.

---

## PR4 — grant admin display + export

Suggested branch: `generic-forms/04-admin` (stacked on PR3; can start once PR3 merges)

### Task 4.1: Read-only answers display in GrantAdmin

**Description:** New readonly pseudo-field on `GrantAdmin` (in "The Grant" fieldset) rendering the linked FormAnswer as a question-label → answer list via `format_html` (option ids resolved to labels; multi_select joined). Empty state for historical grants. `select_related`/prefetch on the admin queryset (no N+1).

**Acceptance criteria:**
- [ ] Grant with FormAnswer shows Q/A pairs readonly; grant without shows an empty note; changelist/change view query counts stay flat.

**Verification:** `docker exec pycon-backend-1 uv run pytest grants/tests/test_admin.py -l` green; manual admin check.

**Dependencies:** PR3.
**Files:** `backend/grants/admin.py`, `backend/grants/tests/test_admin.py`
**Scope:** S

### Task 4.2: Dynamic export columns

**Description:** `GrantResource.__init__` accepts export context via `GrantAdmin.get_export_resource_kwargs` (import-export 3.3.9 sanctioned path, verified incl. the export-form preview instantiating with the same kwargs), resolves the conference's GRANT form, appends one `Field` per question (column name = question label, `dehydrate_method` reading the FormAnswer). Historical grants export empty cells; legacy soft columns stay in `EXPORT_GRANTS_FIELDS`.

**Acceptance criteria:**
- [ ] Export of grants with FormAnswers yields one column per question, values resolved (labels for options).
- [ ] Export of a historical conference (no form/answers) unchanged vs today.

**Verification:** `docker exec pycon-backend-1 uv run pytest grants/tests/test_admin.py -l` green (resource-level tests).

**Dependencies:** 4.1 (same files).
**Files:** `backend/grants/admin.py`, `backend/grants/tests/test_admin.py`
**Scope:** M

### ▣ CHECKPOINT 4 (end of PR4)
- [ ] Full suite + lint + mypy green. Manual: export CSV from local admin with a seeded form. PR4 opened.

---

## PR5 — frontend DynamicForm + grant form integration

Suggested branch: `generic-forms/05-frontend` (stacked on PR3; **prerequisite: PR3 deployed to staging** so `frontend-lint` codegen sees the new schema)

### Task 5.1: `DynamicForm` component + fragment

**Description:** `frontend/src/components/dynamic-form/`: `form.graphql` fragment (form + questions incl. options), `pnpm codegen`, and `index.tsx` rendering each question by `questionType` via styleguide primitives inside `InputWrapper` (mirror `invitation-letter-form.tsx`): text→`Input`, textarea→`Textarea` (+maxLength), select→`Select`, multi_select→`Checkbox` group, boolean→`Checkbox`, url→`Input`. State via the parent's `react-use-form-state` (answers keyed by question id); errors prop consumes the `answersErrors` map (`question_id → string[]`).

**Acceptance criteria:**
- [ ] Renders all 6 question types from a fragment-typed prop; required marking + maxLength client-side; per-question errors render under fields.
- [ ] No hand edits to generated files.

**Verification:** `cd frontend && pnpm codegen && pnpm test && pnpm build` green (component test for render-by-type).

**Dependencies:** PR2 + PR3 deployed to staging (codegen).
**Files:** `frontend/src/components/dynamic-form/{index.tsx,form.graphql,dynamic-form.test.tsx}` (+ regenerated `src/types.tsx`)
**Scope:** M

### Task 5.2: Grant form integration — new submission flow

**Description:** `grant-form/index.tsx`: fetch `conference.form(purpose: GRANT)`; replace the 6 dynamic soft inputs with `DynamicForm` (gender/occupation selects stay); build the `answers` map on submit and **stop sending the 6 dynamic legacy input fields**; map `answersErrors` to the component. **Null-form guard:** if `form` is `null`, block submission and show a "form not available" state — never submit without answers (Verified constraint 5). Strip the legacy `GrantErrors` validation selections for the 6 dynamic soft fields from `submit-grant.graphql`. Structured fields (fullName, nationality, grantType, travel/visa/accommodation, PublicProfileCard, privacy checkbox) untouched. `GENDER_OPTIONS` and `OCCUPATION_OPTIONS` STAY (gender/occupation remain structured inputs with their hardcoded selects); prune `AGE_GROUPS_OPTIONS` only if nothing else imports it; `GRANT_TYPE_OPTIONS` stays. Accepted regression (specced): dateBirth→ageGroup prefill drops (age group is now a dynamic question).

**Acceptance criteria:**
- [ ] New submission works E2E against local backend with a seeded form (success criterion 6: add question in admin → appears on page, no code change).
- [ ] `form == null` → submission blocked with visible message.
- [ ] Per-question server errors display under the right inputs; no legacy soft fields in the mutation payload.

**Verification:** `cd frontend && pnpm test && pnpm build`; manual: docker-compose, create form in admin, submit a grant.

**Dependencies:** 5.1.
**Files:** `frontend/src/components/grant-form/index.tsx`, `frontend/src/components/grant-form/submit-grant.graphql`, `frontend/src/components/grant-form/options.ts`
**Scope:** M

### Task 5.3: Grant form integration — edit flow

**Description:** Edit-flow prefill from `me.grant.formAnswers`: add `formAnswers` to `pages/grants/edit/my-grant.graphql`, feed into `DynamicForm` initial state; update `pages/grants/edit/update-grant.graphql` (strip legacy soft-field + validation selections, keep structured ones); `pages/grants/edit/index.tsx` passes the form + answers through. Legacy grants (`formAnswers == null`) show empty dynamic questions — accepted mid-cycle caveat (plan decision; cutover deploys before grants open).

**Acceptance criteria:**
- [ ] Edit flow prefills dynamic answers and saves changes (update path, no duplicate FormAnswer).
- [ ] `pnpm build` green; edit page documents carry no legacy soft-field selections.

**Verification:** `cd frontend && pnpm test && pnpm build`; manual: edit a grant submitted via the new flow.

**Dependencies:** 5.2.
**Files:** `frontend/src/pages/grants/edit/{index.tsx,my-grant.graphql,update-grant.graphql}`
**Scope:** S

### ▣ CHECKPOINT 5 — FINAL
- [ ] All spec §11 success criteria pass (walk the list one by one).
- [ ] Full backend suite, `ruff`, `mypy`, `pnpm test`, `pnpm build` green.
- [ ] Manual E2E on docker-compose: author form → submit grant → edit grant → view in admin → export CSV.
- [ ] **Ops before merging PR5:** GRANT form with the 8 current questions created and verified in **staging AND production** admin (manual — seeding command was cut from scope). Cutover timed **before grants open** for the next conference (pre-existing legacy applications would show empty dynamic questions in edit).
- [ ] Follow-up ticketed as **two** PRs (not in stack): (1) frontend-only — remove remaining legacy `GrantErrors`/`Grant` selections; (2) after deploy + soak, backend-only — remove legacy soft input fields.

---

## Risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| PR3 rejects/500s on the future PR5 payload | High | Verified constraint 2 baked into T3.2: conditional legacy validation, None→"" coalescing, named answers-only test |
| PR5 CI codegen can't see PR3 schema | Med | Explicit staging deploy step in Checkpoint 3; optional schema-snapshot improvement (needs approval — CI change) |
| Production GRANT form missing at PR5 deploy → silent soft-answer loss | High | Null-form guard blocks submission (T5.2); manual ops step in Checkpoint 5 for staging + production |
| Mid-cycle cutover: legacy grants' edit view shows empty questions | Med | Deploy before grants open (Checkpoint 5 ops note); backfill explicitly out of scope |
| Legacy-field removal breaks live clients | Med | Follow-up split into frontend-first + soak + backend PRs (Verified constraint 6) |
| Export preview instantiates resource with same kwargs | Low | Known from source read; resource tests cover it |
| `useFormState` dynamic keys awkward for answers record | Low | Single `answers` object in state; component test proves it before integration |

## Parallelization

- PR1 tasks sequential (same files). PR2 once PR1 models stable.
- After PR3 **merges**: PR4 can start. After PR3 **reaches staging**: PR5 can start. PR4 ∥ PR5.

## Open questions

None. All decisions resolved (error wire format committed: `answersErrors`; deadline behavior unchanged; ops steps explicit).
