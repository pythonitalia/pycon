# TODO: Generic Form System

Spec: [specs/generic-form-system.md](../../specs/generic-form-system.md) · Plan: [plan.md](plan.md)
Stack: PR1 → PR2 → PR3 → (PR4 ∥ PR5) · PR5 needs PR3 **deployed to staging** (codegen), not just merged.

## PR1 — `generic_forms` app core (`generic-forms/01-app`) — **PR #4705**
- [x] **T1.1** App skeleton + `Form`/`FormQuestion`/`FormAnswer` + DB constraints + migration + INSTALLED_APPS. (b885f5d0e)
- [x] **T1.2** Freeze-on-answer in model: type/options/required/form + delete blocked once answered (pre_delete signal); label/order/active free. (3dfe2ee76)
- [x] **T1.3** `validate_answers()` + envelope `wrap/unwrap`. (43bb587d5)
- [x] **T1.4** Admin: FormAdmin + FormQuestionInline (freeze via model validation errors — readonly deviation documented in plan), read-only FormAnswerAdmin incl. delete block. (f9c2a273d)
- [x] **▣ CHECKPOINT 1** — 48 app tests, full suite 1191 green, ruff clean; adversarial review (3 lenses) applied (455525748); PR #4705 open. **Human review pending. Manual admin eyeball pending.**

## PR2 — GraphQL query (`generic-forms/02-graphql-query`) — **PR #4707**
- [x] **T2.1** `api/generic_forms/types.py` (Form, FormQuestion, FormQuestionOption, FormPurpose/FormQuestionType enums) + `Conference.form(purpose)`; active-only ordered; null when unconfigured. 7 tests.
- [x] **▣ CHECKPOINT 2** — full suite 1197 green; additive-only schema change; PR #4707 open (stacked on #4705).

## PR3 — grants backend (`generic-forms/03-grants-backend`) — **PR #4709**
- [x] **T3.1** `Grant.form_answer` OneToOne (SET_NULL) + `blank=True` on 4 soft columns; migration 0032. (9d140ff3b)
- [x] **T3.2** Mutations + tests: soft fields optional (build correction: `gender`/`occupation` stay structured — `grants/summary.py` aggregates them; dynamic set = 6) + `answers: JSON`; path-split validation; `answersErrors` JSON via direct assignment; FormAnswer update_or_create in transaction; None→"" coalescing; skip-list on update. Named tests incl. exact-PR5-payload + legacy regression. (8146fb875)
- [x] **T3.3** `Grant.formAnswers` + tests. Gotcha found: `me.grant` returns `from_model()` DETACHED instance (not the model) — `from_model` now attaches `form_answer` for the resolver. (pushed)
- [x] **▣ CHECKPOINT 3** — full suite 1205 green; legacy shape regression-proven; PR #4709 open. **After merge: deploy to staging (workflow_dispatch) for PR5 codegen.**

## PR4 — admin display + export (`generic-forms/04-admin`)
- [ ] **T4.1** GrantAdmin readonly Q/A display (`format_html`), empty state, no N+1. Verify: `pytest grants/tests/test_admin.py` + manual.
- [ ] **T4.2** `GrantResource` dynamic columns via `get_export_resource_kwargs` → `__init__` fields append (3.3.9 verified path, incl. export-form preview); historical export unchanged. Verify: resource tests.
- [ ] **▣ CHECKPOINT 4** — suite green; manual CSV export; PR4 opened.

## PR5 — frontend (`generic-forms/05-frontend`) — **DRAFT PR #4711**
- [x] **T5.1** `dynamic-form/` component + fragment + codegen; all 6 types; errors from `answersErrors`. NOTE: frontend has NO test runner (plan's `pnpm test` assumption wrong) — verification = codegen + type-check + Biome + live SSR check.
- [x] **T5.2** New-submission integration: `form(GRANT)` in GrantDeadline query, 6 dynamic inputs swapped (gender/occupation selects stay), `answers` in payload, null-form guard, legacy selections stripped, AGE_GROUPS_OPTIONS pruned. **Live-verified**: seeded form renders on /en/grants via SSR (criterion 6 ✓).
- [x] **T5.3** Edit flow: `formAnswers` prefill; edit documents stripped; `grant` prop typed from MyGrantQuery (full `Grant` type no longer matches the narrower selection).
- [ ] **▣ CHECKPOINT 5 — FINAL (partially blocked)** — done: criterion 6 live check, codegen/types/Biome green, local `next build` failure verified pre-existing (baseline fails identically at export stage). Pending: manual browser submit+edit (no Chromium in agent env); PR #4711 stays DRAFT until #4709 deployed to staging (CI codegen); **ops: GRANT form in staging + production admin BEFORE merge; cutover before grants open**; follow-up = TWO PRs (frontend strip → soak → backend removal).
