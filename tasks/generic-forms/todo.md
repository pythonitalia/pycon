# TODO: Generic Form System

Spec: [specs/generic-form-system.md](../../specs/generic-form-system.md) · Plan: [plan.md](plan.md)
Stack: PR1 → PR2 → PR3 → (PR4 ∥ PR5) · PR5 needs PR3 **deployed to staging** (codegen), not just merged.

## PR1 — `generic_forms` app core (`generic-forms/01-app`) — **PR #4705**
- [x] **T1.1** App skeleton + `Form`/`FormQuestion`/`FormAnswer` + DB constraints + migration + INSTALLED_APPS. (b885f5d0e)
- [x] **T1.2** Freeze-on-answer in model: type/options/required/form + delete blocked once answered (pre_delete signal); label/order/active free. (3dfe2ee76)
- [x] **T1.3** `validate_answers()` + envelope `wrap/unwrap`. (43bb587d5)
- [x] **T1.4** Admin: FormAdmin + FormQuestionInline (freeze via model validation errors — readonly deviation documented in plan), read-only FormAnswerAdmin incl. delete block. (f9c2a273d)
- [x] **▣ CHECKPOINT 1** — 48 app tests, full suite 1191 green, ruff clean; adversarial review (3 lenses) applied (455525748); PR #4705 open. **Human review pending. Manual admin eyeball pending.**

## PR2 — GraphQL query (`generic-forms/02-graphql-query`)
- [ ] **T2.1** `api/generic_forms/types.py` (FormType, FormQuestionType, enums, options) + `Conference.form(purpose)` (mirror `deadline()`); active-only ordered; null when unconfigured. Verify: `pytest api/generic_forms`.
- [ ] **▣ CHECKPOINT 2** — suite green; schema diff additive; PR2 opened.

## PR3 — grants backend (`generic-forms/03-grants-backend`)
- [ ] **T3.1** `Grant.form_answer` OneToOne (SET_NULL) + `blank=True` on the 4 required soft columns (`why`, `python_usage`, `been_to_other_events`, `occupation`); one migration. Columns stay NOT NULL — mutations must never pass `None`.
- [ ] **T3.2** Mutations + tests (TDD): 8 soft fields optional + optional `answers: JSON`; legacy soft-field checks run only when `answers` absent (structured-field validation unchanged on both paths); errors via `answers_errors: JSON` **direct assignment** (dotted paths impossible — verified); FormAnswer `update_or_create` in existing transaction; `None`→`""` coalescing on create; setattr skip-list on update. Named tests: **answers-only payload (exact PR5 shape)**, legacy-shape regression, invalid→atomic rollback, no-form-configured rejected, deadline-closed unchanged, update-no-duplicate.
- [ ] **T3.3** `Grant.formAnswers: JSON|null` on GraphQL type + query test (`me.grant.formAnswers`).
- [ ] **▣ CHECKPOINT 3** — suite green; back-compat verified both directions; PR3 opened; **after merge: deploy to staging (workflow_dispatch) for PR5 codegen**.

## PR4 — admin display + export (`generic-forms/04-admin`)
- [ ] **T4.1** GrantAdmin readonly Q/A display (`format_html`), empty state, no N+1. Verify: `pytest grants/tests/test_admin.py` + manual.
- [ ] **T4.2** `GrantResource` dynamic columns via `get_export_resource_kwargs` → `__init__` fields append (3.3.9 verified path, incl. export-form preview); historical export unchanged. Verify: resource tests.
- [ ] **▣ CHECKPOINT 4** — suite green; manual CSV export; PR4 opened.

## PR5 — frontend (`generic-forms/05-frontend`) — start only after PR3 on staging
- [ ] **T5.1** `dynamic-form/` component + fragment + codegen; 6 types via styleguide + InputWrapper (mirror invitation-letter-form); errors from `answersErrors` map; component test. Verify: `pnpm codegen && pnpm test && pnpm build`.
- [ ] **T5.2** New-submission integration: fetch `form(GRANT)`, swap 8 hardcoded inputs for DynamicForm, `answers` in payload (drop legacy 8), **null-form guard blocks submission**, strip legacy validation selections from submit-grant.graphql, prune dead options.ts constants. Verify: pnpm test/build + manual submit.
- [ ] **T5.3** Edit flow: `formAnswers` into my-grant.graphql, prefill DynamicForm, strip legacy selections from edit documents. Verify: pnpm build + manual edit.
- [ ] **▣ CHECKPOINT 5 — FINAL** — spec §11 walked one-by-one; manual E2E (author → submit → edit → admin → export); **ops: GRANT form created in staging + production admin BEFORE merge; cutover before grants open**; follow-up ticketed as TWO PRs (frontend strip → soak → backend input removal).
