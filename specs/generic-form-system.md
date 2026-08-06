# Spec: Generic Form System

Status: Approved — ready for planning
Source: Notion draft "Generic Form system" (exported HTML in repo root) + clarifying Q&A
Author: generated via spec-driven-development

---

## 1. Objective

Build a generic, per-conference configurable form system so organizers can change the questions asked in recurring flows (grants, CFP, visa, feedback) **without backend or frontend code changes**. Today every question is a hardcoded model column (`Grant`, `Submission`) or an external Google Form; changing questions for a new conference edition requires coordinated BE + FE work and migrations.

**First consumer (this spec's scope): the grant application form.** The engine is built generically; grants is the first flow wired to it. CFP, visa, and feedback forms are explicitly future slices.

**Target users:**
- *Organizers* — author/edit form questions per conference in Django admin.
- *Attendees/applicants* — fill forms on the Next.js frontend.
- *Maintainers* — stop writing migrations + form components for every question change.

**Success looks like:** an organizer can add, reword, reorder, or deactivate a grant-form question for the next conference entirely from Django admin, and the frontend renders and validates it with zero code changes.

### Decisions already made (via Q&A)

1. **MVP integration target: grants** (biggest pain; `Grant` has ~20 hardcoded answer columns).
2. **Data model: hybrid** — `Form`/`FormQuestion` as normal models (admin-authorable), answers stored as a single `FormAnswer` row per submission with a `JSONField` mapping `question_id → value`. No per-question answer rows.
3. **Versioning: freeze-on-answer** — a question's semantic fields (type, options, required) become immutable once any answer exists for its form. Changes happen by deactivating questions and adding new ones (or cloning the form for a new conference). No snapshot or version-row machinery.
4. **Authoring UI: Django admin** — inline `FormQuestion` editing under `Form`. No custom-admin/Astro builder in this slice.
5. **Load-bearing grant fields stay as `Grant` columns** (confirmed). Fields that drive business logic — `grant_type` (reimbursement categories), `departure_country`/`nationality` (`country_type` derivation, visa), `departure_city`, `needs_funds_for_travel`, `need_visa`, `need_accommodation`, **`gender` and `occupation`** (the grant summary in `grants/summary.py` aggregates both columns for reporting — caught during build) — remain structured columns on `Grant`, as do `full_name`/`name`. The *soft* questions moving into the generic form are exactly: `why`, `python_usage`, `been_to_other_events`, `community_contribution`, `age_group`, `notes`. (Corrected during planning: socials/website do NOT move — the grant form's social inputs are `participant_*` fields handled via `PublicProfileCard`/`Participant` upsert, not Grant columns; Grant's own social columns are already unused by the current flow.) This avoids a question→field mapping layer in the MVP.
6. **English only** — no multi-lingual labels/options (confirmed).
7. **Options-as-JSON admin UX**: raw JSON widget is acceptable — no custom widget (confirmed).
8. **Grant admin export includes dynamic answers in this slice** (confirmed). The existing `GrantResource` (django-import-export, `grants/admin.py`) exports several soft-question columns today; those move to dynamic-answer columns — one column per question of the conference's grant form (the export is already single-conference via `before_export`).
9. **`purpose` enum values for cfp/visa/feedback are added when those slices land**, not preemptively (confirmed).

### Assumptions I'm making (correct before approval if wrong)

1. **No data migration of historical grants.** Old `Grant` columns stay populated and readable for past conferences; new conferences write soft answers to `FormAnswer` only. Legacy columns become nullable/blank-able but are **not dropped** in this slice.
2. **One `FormAnswer` per (form, user).** Matches the existing one-grant-per-user-per-conference constraint. Multi-response generic forms (e.g. anonymous feedback) are future work.
3. **Question labels/descriptions are editable even after answers exist** (typo fixes); only `question_type`, `options`, and `required` freeze. Deletion is blocked once answered — deactivate instead.
4. **New Django app named `generic_forms`** (avoids collision/confusion with `django.forms` and `wagtail.contrib.forms`, which is installed but unused).
5. **Select options live in a `JSONField` on `FormQuestion`** (list of `{id, label}`), not a third model — Django admin can't nest inlines two levels deep, and options-as-JSON keeps authoring on one page.
6. **No file-upload question type in MVP** — it requires extending `files_upload.File.Type`, size limits, and upload permissions. Listed as future work.
7. **No conditional/branching questions in MVP.**

---

## 2. Scope

### In scope

- New `generic_forms` Django app: `Form`, `FormQuestion`, `FormAnswer` models + migrations + admin.
- Question types: `text` (single line), `textarea`, `select`, `multi_select`, `boolean`, `url`.
- Server-side answer validation (required, type, option membership, max length, URL format) following the existing `BaseErrorType` pattern.
- GraphQL: query a conference's form by purpose (id, name, ordered active questions with labels/options); mutation to submit/update answers is folded into the existing grant mutations (see §5).
- Grants integration: `sendGrant`/`updateGrant` accept an `answers` input, validate against the conference's grant form, persist a `FormAnswer` linked from `Grant`.
- Frontend: a reusable `DynamicForm` component (styleguide inputs, `react-use-form-state`) rendering questions by type; grant form page renders its soft-question sections dynamically.
- Django admin: grant admin displays the applicant's dynamic answers read-only alongside the structured fields.
- Grant admin export: `GrantResource` gains one column per question of the conference's grant form, populated from the linked `FormAnswer`; legacy soft-question columns stay for historical exports.
- Freeze-on-answer enforcement at the model layer (not just admin).

### Out of scope (explicitly NOT in this slice)

- CFP/Submission, visa, and feedback form integrations (engine supports `purpose` values for them, but no product wiring).
- Migrating historical `Grant` answer data into `FormAnswer`; dropping legacy `Grant` columns.
- Custom-admin (Astro) form-builder UI; Wagtail integration.
- File-upload, date, number, or conditional question types.
- Anonymous / multi-response forms.
- Generic "form submitted" confirmation email plumbing (draft's idea — good future win, not now; grants keeps its existing notification path).
- Changes to Pretix, Stripe, or the reimbursement flow.
- Profile-based prefill of dynamic answers (today `ageGroup` prefills from `user.dateBirth` and `gender` from `user.gender`; the generic engine has no per-question semantics, so these prefills are dropped — small accepted UX regression).

---

## 3. Tech stack

- **Backend:** Django 5.x (existing), PostgreSQL, Strawberry GraphQL. No new Python dependencies expected.
- **Language:** English only — plain `CharField`/`TextField` for labels, descriptions, option labels. No `I18nCharField`/`I18nTextField`.
- **Frontend:** Next.js (existing), TypeScript, Apollo Client with codegen (`pnpm codegen`), `react-use-form-state` (corrected during planning: `react-hook-form` is in package.json but has zero usages in the codebase — every existing form, including the modern invitation-letter form, uses `react-use-form-state`; the new component follows the actual in-repo pattern), `@python-italia/pycon-styleguide` inputs.
- **Admin:** stock Django admin with `TabularInline`/`StackedInline`.

---

## 4. Data model

```python
# backend/generic_forms/models.py
class Form(TimeStampedModel):
    class Purpose(models.TextChoices):
        GRANT = "grant", _("Grant")
        GENERIC = "generic", _("Generic")   # cfp/visa/feedback added in later slices

    conference = models.ForeignKey("conferences.Conference", on_delete=models.CASCADE,
                                   related_name="forms")
    purpose = models.CharField(max_length=32, choices=Purpose.choices)
    name = models.CharField(max_length=200)
    # constraint: at most one form per (conference, purpose) when purpose != GENERIC


class FormQuestion(TimeStampedModel):
    class QuestionType(models.TextChoices):
        TEXT = "text"
        TEXTAREA = "textarea"
        SELECT = "select"
        MULTI_SELECT = "multi_select"
        BOOLEAN = "boolean"
        URL = "url"

    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="questions")
    label = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    question_type = models.CharField(max_length=32, choices=QuestionType.choices)
    options = models.JSONField(blank=True, default=list)
    # options item shape: {"id": "vegan", "label": "Vegan"}
    required = models.BooleanField(default=False)
    max_length = models.PositiveIntegerField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)  # deactivate instead of delete once answered


class FormAnswer(TimeStampedModel):
    form = models.ForeignKey(Form, on_delete=models.PROTECT, related_name="answers")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    answers = models.JSONField(default=dict)
    # Versioned envelope so the structure can evolve without guessing:
    #   {"version": 1, "answers": {"<question_pk>": value}}
    # version 1 value types by question_type:
    #   text/textarea/url → str, select → option id (str),
    #   multi_select → list[str] of option ids, boolean → bool
    # Readers dispatch on "version"; writers always write the current version.
    # (GraphQL input stays the flat {question_id: value} map — the envelope is
    # a storage concern; the mutation wraps it on persist.)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["form", "user"],
                                               name="unique_form_answer_per_user")]
```

**Grant link:** `Grant.form_answer = models.OneToOneField("generic_forms.FormAnswer", null=True, blank=True, on_delete=models.SET_NULL)`. Soft-question columns on `Grant` become `blank=True` (kept for historical data).

**Freeze-on-answer rule (model layer):** `FormQuestion.clean()`/`save()` raise if `question_type`, `options`, or `required` change while `self.form.answers.exists()`; deletion is blocked via a `pre_delete` signal (covers queryset deletes too). `label`/`description`/`order`/`active` stay editable. `Form.conference`/`purpose` freeze the same way. In admin the rule surfaces as validation errors on the inline (not readonly fields — inline-level readonly would also freeze NEW rows, and adding questions to answered forms must stay possible); the model is the enforcement point. Question `options` are shape-validated at authoring (list of `{id, label}` string pairs, unique ids, required for select types, forbidden otherwise).

**Answer validation (single source of truth):** a `validate_answers(form, answers: dict) -> dict[str, list[str]]` service in `generic_forms/` used by the GraphQL layer: unknown/inactive question ids rejected, required enforced, per-type checks (option membership incl. every item of multi_select, `URLValidator` for url, `max_length` for text types, bool type check).

---

## 5. API design (GraphQL)

Follows the newer one-mutation-per-file pattern and the `api/visa/mutations/request_invitation_letter.py` validation style.

**Query** — extend the existing `Conference` type:

```graphql
conference(code: "pycon2026") {
  form(purpose: GRANT) {   # null if no form configured
    id
    name
    questions {            # active only, ordered
      id
      label
      description
      questionType
      required
      maxLength
      options { id label }
    }
  }
}
```

**Mutations** — no standalone `submitFormAnswers` in this slice. `sendGrant` / `updateGrant` inputs gain an optional `answers: JSON` (map of question id → value). The mutation:
1. Keeps its existing deadline gating unchanged (`non_field_errors: "The grants form is not open!"` via `Conference.is_grants_open`) — no `FormNotAvailable` union member (changing the deadline-closed response shape would break the deployed frontend; decided during planning).
2. If `answers` is provided but the conference has no `GRANT` form, rejects with a clear error. If the form exists, runs `validate_answers`; failures are returned in a dedicated `answersErrors: JSON` field on `GrantErrors` mapping `question_id → [messages]`. (Dotted dynamic paths like `answers.<id>` cannot serialize through the statically-typed error classes — verified during planning; the in-repo dotted-path precedent, `materials.0.url` in `api/submissions`, works only because its container field is statically declared.)
3. Persists `FormAnswer` (create or update), wrapping the input map into the versioned envelope (`{"version": 1, "answers": {...}}`), and links it to the `Grant` in the same transaction.
4. The 8 legacy soft input fields become optional; legacy-shape submissions (soft fields, no `answers`) keep working unchanged until the frontend cutover, then get removed in a post-deploy follow-up.

**Grant type** — exposes `formAnswers: JSON | null` (the unwrapped flat map) so the frontend edit flow can prefill the dynamic questions.

Privacy policy acceptance, Slack notification, and email template lookups keep their current grant-specific wiring — unchanged.

---

## 6. Commands

All backend commands run inside Docker (per CLAUDE.md).

| Purpose | Command |
|---|---|
| Run backend tests (new app) | `docker exec pycon-backend-1 uv run pytest generic_forms/tests api/generic_forms -l -s -vvv` |
| Grants integration tests | `docker exec pycon-backend-1 uv run pytest api/grants grants -l -s -vvv` |
| Full suite | `docker exec pycon-backend-1 uv run pytest` |
| Make migrations | `docker exec pycon-backend-1 uv run python manage.py makemigrations generic_forms grants` |
| Migrate | `docker exec pycon-backend-1 uv run python manage.py migrate` |
| Lint / format | `docker exec pycon-backend-1 uv run ruff check` / `uv run ruff format` |
| Type check | `docker exec pycon-backend-1 uv run mypy .` |
| Frontend codegen (after schema change) | `cd frontend && pnpm codegen` |
| Frontend tests / build | `cd frontend && pnpm test` / `pnpm build` |

---

## 7. Project structure

```
backend/
  generic_forms/                    # NEW app
    models.py                       # Form, FormQuestion, FormAnswer
    services.py                     # validate_answers()
    admin.py                        # Form admin + FormQuestion inline (freeze-aware)
    migrations/
    tests/                          # model + validation tests, factories
  api/
    generic_forms/                  # NEW: FormType, FormQuestionType (query side)
      types.py
    grants/mutations.py             # extend sendGrant/updateGrant with answers
  grants/
    models.py                       # + form_answer FK; soft columns → blank=True
    admin.py                        # + read-only answers display
  pycon/settings/base.py            # + generic_forms in INSTALLED_APPS

frontend/src/
  components/dynamic-form/          # NEW: renders FormQuestion[] via styleguide inputs
    index.tsx
    form.graphql                    # fragment for form + questions
  components/grant-form/            # integrate DynamicForm for soft questions
```

---

## 8. Code style

Backend follows existing conventions — Ruff (lint + format), mypy clean. Mutation validation mirrors the in-repo pattern:

```python
@strawberry.input
class SendGrantInput:
    conference: strawberry.ID
    answers: JSON
    ...

    def validate(self, conference: Conference, form: Form) -> GrantErrors | None:
        errors = GrantErrors()
        if answer_errors := validate_answers(form, self.answers):
            # dedicated JSON field: {question_id: [messages]} — dynamic keys
            # cannot serialize through the statically-typed error fields
            errors.answers_errors = answer_errors
        return errors.if_has_errors
```

Frontend: `react-use-form-state` + `@python-italia/pycon-styleguide` primitives (mirror `invitation-letter-form.tsx`: `InputWrapper` around each field, `MultiplePartsCard` sections); GraphQL documents co-located with components; **never hand-edit generated files** (`src/types.tsx`, `src/generated/`).

---

## 9. Testing strategy

- **Framework:** pytest + factory-based fixtures, in-app `tests/` dirs (existing convention). Frontend: existing `pnpm test` setup for the `DynamicForm` component's rendering/validation mapping.
- **Model tests** (`generic_forms/tests/`): freeze-on-answer (type/options/required change and delete blocked once an answer exists; label/order/active edits allowed); unique (form, user) constraint; one-form-per-(conference, purpose) constraint.
- **Validation tests:** each question type's accept/reject cases — required missing, wrong value type, unknown question id, inactive question id, non-member option, multi_select with one bad item, invalid URL, over max_length.
- **API tests** (`api/` tests): query returns only active questions in order; `sendGrant` with valid answers creates `Grant` + linked `FormAnswer` atomically; invalid answers return per-question errors in `answersErrors` and persist nothing; answers-with-no-form-configured is rejected; grants-deadline-closed behavior unchanged from today; an answers-only payload omitting all 8 legacy soft fields succeeds end-to-end (this is the exact post-cutover frontend payload).
- **Export test:** `GrantResource` export of a grant with a linked `FormAnswer` produces one column per form question with the answer values (option ids resolved to labels); grants without `FormAnswer` (historical) still export cleanly.
- **Regression:** full existing grants test suite stays green — legacy columns still accepted for old data paths.
- Every slice lands with its tests; `pytest`, `ruff check`, `mypy .` green before any commit.

---

## 10. Boundaries

### Always do
- Run backend commands via `docker exec pycon-backend-1 ...` (local venv doesn't work).
- Run `pytest` + `ruff check` + `mypy .` (and `pnpm codegen` after schema changes) before committing.
- Enforce freeze-on-answer in the model, not only in admin.
- Validate answers server-side via `validate_answers` — frontend validation is UX only.
- Keep legacy `Grant` columns readable (admin, exports) for historical conferences.

### Ask first
- Adding any new dependency (backend or frontend).
- Changing which `Grant` fields count as load-bearing (decision #5) — i.e. moving `grant_type`, country, or `need_*` fields into the form.
- Any data migration touching existing `Grant` rows beyond `blank=True` loosening.
- Adding new values to `files_upload.File.Type` (file-upload question type).
- Schema changes to `Submission`, visa, or notification models.
- Dropping or renaming any existing column.

### Never
- Drop legacy `Grant` answer columns in this slice.
- Hand-edit generated GraphQL types (`frontend/src/types.tsx`, `*.generated.ts`).
- Store answers as per-question rows (decision: JSON) or bypass `validate_answers` in any mutation.
- Commit secrets; weaken rate-limit/permission classes on mutations.
- Delete or skip failing tests to get green.

---

## 11. Success criteria

1. Organizer creates a `GRANT` form with questions of every supported type in Django admin, reorders and deactivates questions — no code change needed.
2. Once one answer exists, changing a question's type/options/required or deleting it fails with a clear error in both admin and direct model save; label typo fix still succeeds.
3. `conference.form(purpose: GRANT)` returns the ordered active questions; returns `null` when unconfigured.
4. `sendGrant` with valid `answers` creates `Grant` + linked `FormAnswer` in one transaction; a second submit by the same user for the same conference updates rather than duplicates (existing update path).
5. `sendGrant` with an invalid answer (missing required, bad option, invalid URL) returns per-question errors (`answersErrors` map) and writes nothing; an answers-only payload with no legacy soft fields succeeds.
6. Grant form page on the frontend renders the soft-question sections from the API (verify: add a question in admin → it appears on the page after reload, no deploy of new code).
7. Grant admin shows the applicant's dynamic answers read-only next to structured fields.
8. Grant admin export includes a column per form question with the applicant's answers; exports of historical grants (no `FormAnswer`) still work.
9. Full backend test suite, `ruff check`, `mypy .`, frontend `pnpm build` + `pnpm test` all green.

## 12. Open questions

None — all resolved into decisions #7–#9.
