# Spec: Schedule Builder — Radix UI Migration

## Objective

Migrate the **custom_admin Schedule Builder** from its current ad-hoc UI (custom
`div` modal, native `<input>`/`<select>`/`<button>`, raw `<h1>`/`<strong>`/`<ul>`
markup, emoji controls) to **Radix UI** — matching the pattern already used by the
**Invitation Letter Document Builder** in the same app.

Scope decision (confirmed with maintainer): **Full overhaul.**
- Replace every custom UI primitive with `@radix-ui/themes` components.
- Redesign the visual presentation of the schedule item card, the add-item modal,
  and the pending-items basket using Radix `Card` / `Badge` / `IconButton` / typography
  for a clean look consistent with the invitation-letter editor.
- Rethink calendar grid presentation spacing and interaction affordances where it
  improves clarity — but **the grid-positioning mechanism (CSS grid + inline
  `gridColumnStart`/`gridRowStart`) and the drag-and-drop logic (`react-dnd`) stay
  functionally identical.**
- The event-type picker (`talk`/`keynote`/`break`/…) becomes a `@radix-ui/themes`
  `Select`.

**Out of scope:** GraphQL queries/mutations, the data model, `react-dnd` wiring,
the Apollo layer, the Astro page entry, and any code outside
`src/components/schedule-builder/` (plus the now-unused `src/components/shared/modal.tsx`).

**User:** PyCon Italia organizers building the conference schedule in the Django admin.

**Success looks like:** identical behavior (create slot, search proposal/keynote,
add custom event, drag items between slots/rooms, unassign to basket, edit in admin),
but the UI is rendered with Radix components, visually consistent with the invitation
letter editor, with no native form controls or the custom modal remaining.

## Tech Stack

- **Framework:** Astro 5 + React 19 (islands), components in `src/components/**`
- **UI:** `@radix-ui/themes` ^3.1.6 (primary) — already installed and wired via
  `<Theme>` in `src/components/shared/base.tsx`
- **Icons:** `lucide-react` ^0.468.0 (e.g. `ChevronLeft`, `ChevronRight`, `Plus`, `Pencil`)
- **Styling:** Tailwind 3.4 — **only** for grid positioning / one-off layout, not for
  component look (follow invitation-letter convention)
- **Utilities:** `clsx`, shared `Spacer` (`src/components/shared/spacer.tsx`)
- **DnD:** `react-dnd` + `react-dnd-html5-backend` (unchanged)
- **Data:** Apollo Client, codegen'd hooks (unchanged)

No new dependencies required — `Select` ships with `@radix-ui/themes`; chevron icons
ship with `lucide-react`.

## Commands

Run inside the custom_admin workspace (`backend/custom_admin`):

```
Build:    pnpm build           # astro build — primary verification gate
Dev:      pnpm dev             # astro dev on :3002 + codegen watch + ws proxy
Codegen:  pnpm codegen         # GraphQL types (not needed unless .graphql changes)
Lint/fmt: npx @biomejs/biome check src/components/schedule-builder
          npx @biomejs/biome format --write src/components/schedule-builder
```

There is no unit-test runner for custom_admin. Verification = clean `pnpm build` +
Biome clean + manual smoke test in the running admin (via `docker-compose up`,
schedule-builder page).

## Project Structure

```
backend/custom_admin/src/components/
├── schedule-builder/                 ← migrate everything here
│   ├── root.tsx                      already Radix (Flex, Spinner) — leave
│   ├── calendar.tsx                  raw <h1>/<button> → Heading/Button(ghost)
│   ├── item.tsx                      ScheduleItemCard <ul><li> → Card/Badge/Text; keep DnD+Tooltip
│   ├── placeholder.tsx               drop zone — keep DnD; text → Text
│   ├── slot-creation.tsx             already Button — tidy/group only
│   ├── pending-items-basket/index.tsx  emoji scroll → IconButton+lucide; Card/Text
│   └── add-item-modal/
│       ├── index.tsx                 custom Modal → Dialog
│       ├── search-event.tsx          <input> → TextField; remove console.log + empty else
│       ├── add-custom-event.tsx      <select>→Select, <input>→TextField, list→Cards, .btn→Button
│       ├── proposal-preview.tsx      .btn → Button; <li>/<strong> → Card/Text/Badge
│       ├── keynote-preview.tsx       same as proposal-preview
│       └── info-recap.tsx            grid+strong/span → Text (or DataList)
├── shared/
│   ├── modal.tsx                     DELETE (only schedule-builder imports it)
│   ├── spacer.tsx                    reuse
│   └── base.tsx                      <Theme> wrapper — leave
└── ...
src/custom-styles.css                 remove `.btn` rule once no longer referenced
```

## Code Style

Follow the invitation-letter editor (`src/components/invitation-letter-document-builder/`).
Components from `@radix-ui/themes`, semantic props over Tailwind, `lucide-react` icons,
compound Dialog/AlertDialog pattern. Example (the reference modal pattern from
`editor-section.tsx`):

```tsx
import { Dialog, Button, Flex, Text, TextField } from "@radix-ui/themes";
import { Pencil } from "lucide-react";

<Dialog.Root open={isOpen} onOpenChange={(o) => !o && close()}>
  <Dialog.Content maxWidth="768px">
    <Dialog.Title>Add event to schedule</Dialog.Title>
    <Flex direction="column" gap="4">
      <SearchEvent />
      <AddCustomEvent />
    </Flex>
  </Dialog.Content>
</Dialog.Root>
```

Select pattern (replacing the native `<select>`):

```tsx
import { Select } from "@radix-ui/themes";

<Select.Root value={type} onValueChange={setType}>
  <Select.Trigger placeholder="Choose one" />
  <Select.Content>
    <Select.Item value="talk">Talk</Select.Item>
    <Select.Item value="keynote">Keynote</Select.Item>
    {/* … */}
  </Select.Content>
</Select.Root>
```

Conventions:
- `Button variant="ghost"` for icon/inline actions, `variant="soft"` / `color="gray"`
  for secondary, solid default for primary; `color="crimson"` for destructive.
- Typography: `Heading` / `Text` instead of `<h1>`/`<strong>`/`<span>`.
- Spacing: `Flex`/`Grid` props (`gap`, `p`, `mt`) and the shared `Spacer`, not Tailwind margins.
- Keep Tailwind **only** where it positions grid cells or does layout Radix props can't express.
- Keep existing `react-dnd` `useDrag`/`useDrop` hooks exactly; only the rendered markup changes.

## Testing Strategy

- **No automated tests exist** for custom_admin; do not add a test framework as part
  of this migration (out of scope — flag separately if desired).
- **Primary gate:** `pnpm build` succeeds with no TypeScript errors.
- **Lint gate:** Biome check clean on `src/components/schedule-builder`.
- **Manual smoke test** in the running admin after each task (see Boundaries → Always):
  1. Slot creation buttons add slots of each duration/type.
  2. Drag an item from one placeholder to another slot/room → persists.
  3. Drag an item to the basket → unassigns; basket scroll buttons appear & work.
  4. Click an empty placeholder → Dialog opens; search returns proposals/keynotes;
     "Add to schedule in <lang>" creates item & closes dialog.
  5. Add-custom-event: list options create items; "create by hand" with Select type
     + title creates an item.
  6. "Edit" on a card and "Edit day in admin" open the Django admin editor modal.
  7. Speaker-availability badges/tooltips still render.

## Boundaries

- **Always:**
  - Run `pnpm build` + Biome after each task; fix before moving on.
  - Preserve every `react-dnd` hook, GraphQL call, and prop contract.
  - Keep behavior identical — this is a UI swap, not a feature change.
  - Migrate one file (or one tightly-coupled pair) per commit.
- **Ask first:**
  - Adding any new dependency (none expected).
  - Changing GraphQL `.graphql` files or codegen output.
  - Changing the grid-positioning math in `calendar.tsx` / `item.tsx`.
  - Any visible behavior change beyond appearance.
- **Never:**
  - Touch code outside `schedule-builder/` except deleting `shared/modal.tsx` and
    removing the dead `.btn` rule.
  - Remove the availability-badge / tooltip logic.
  - Leave native `<input>`/`<select>`/`<button className="btn">` or the custom `Modal`.
  - Commit the stray `console.log` (remove it during the search-event task).

## Success Criteria

- [ ] `grep -rn "shared/modal\|className=\"btn\|<select\|<input " src/components/schedule-builder`
      returns nothing (no native controls / custom modal left).
- [ ] `src/components/shared/modal.tsx` deleted; `.btn` rule removed from `custom-styles.css`.
- [ ] Add-item modal renders via Radix `Dialog`; event-type via Radix `Select`.
- [ ] Schedule item card, basket, previews use Radix `Card`/`Badge`/`Text`/`IconButton`.
- [ ] `pnpm build` passes; Biome check clean.
- [ ] All 7 manual smoke-test flows pass with unchanged behavior.
- [ ] Visual style is consistent with the invitation-letter editor.

## Plan (implementation order)

Bottom-up: shared/leaf pieces first so parents compose cleanly, modal last.

1. **info-recap.tsx** (leaf, pure presentation) → Radix `Text`/`DataList`.
2. **item.tsx → ScheduleItemCard** redesign with Radix `Card`/`Badge`/`Text`/`Button`;
   keep DnD `useDrag`, availability badge + `Tooltip`. (`Item` grid wrapper math unchanged.)
3. **proposal-preview.tsx** + **keynote-preview.tsx** → `Card`/`Badge`/`Text`, `.btn`→`Button`.
4. **search-event.tsx** → `TextField`; remove `console.log` + empty `else`.
5. **add-custom-event.tsx** → Radix `Select`, `TextField`, `Button`; option list → Cards/Buttons.
6. **add-item-modal/index.tsx** → Radix `Dialog`; then **delete `shared/modal.tsx`**.
7. **calendar.tsx** → `Heading` + ghost `Button` for "Edit day in admin"; keep grid.
8. **placeholder.tsx** → `Text` for labels; keep DnD + grid positioning.
9. **pending-items-basket/index.tsx** → `Card`, `IconButton` + lucide chevrons (replace
   👈/👉), `Text`; keep DnD + scroll logic.
10. **slot-creation.tsx** → tidy grouping (already `Button`).
11. **Cleanup:** remove `.btn` from `custom-styles.css`; final `pnpm build` + Biome + full smoke test.

Risk notes:
- DnD drag preview uses the rendered node — verify drag still grabs the card after the
  `Card` redesign (item.tsx task).
- Radix `Dialog` traps focus/scroll; the old modal set `body.overflow` manually — Dialog
  handles this, so confirm background scroll-lock still works and remove the manual logic.
- Radix `Select` is portal-rendered inside the Dialog — confirm it layers above the
  Dialog overlay (z-index) when open.

## Tasks

- [ ] **T1 — info-recap** → Radix typography.
  - Acceptance: label/value pairs render via `Text`; no raw `<strong>`/`<span>`.
  - Verify: `pnpm build`; modal preview shows recap unchanged.
  - Files: `add-item-modal/info-recap.tsx`

- [ ] **T2 — ScheduleItemCard redesign**.
  - Acceptance: card uses `Card`/`Badge`/`Text`/`Button`; type+duration+status+title+
    speakers+TM+Edit all present; availability warning badge + `Tooltip` intact; `useDrag` unchanged.
  - Verify: `pnpm build`; drag still works; card readable.
  - Files: `item.tsx`

- [ ] **T3 — proposal & keynote previews**.
  - Acceptance: `.btn`→`Button`; `<li>`/`<strong>`→`Card`/`Text`; availability chip→`Badge`.
  - Verify: `pnpm build`; search results render; add buttons work.
  - Files: `add-item-modal/proposal-preview.tsx`, `add-item-modal/keynote-preview.tsx`

- [ ] **T4 — search-event**.
  - Acceptance: `<input>`→`TextField` (autofocus kept); `console.log` + empty `else` removed.
  - Verify: `pnpm build`; typing searches.
  - Files: `add-item-modal/search-event.tsx`

- [ ] **T5 — add-custom-event**.
  - Acceptance: native `<select>`→Radix `Select`; `<input>`→`TextField`; `.btn`→`Button`;
    quick-option list → Radix Cards/Buttons; create-by-hand validation unchanged.
  - Verify: `pnpm build`; both create paths work; Select layers above Dialog.
  - Files: `add-item-modal/add-custom-event.tsx`

- [ ] **T6 — modal → Dialog + delete custom Modal**.
  - Acceptance: `index.tsx` uses `Dialog.Root/Content/Title`; `shared/modal.tsx` deleted;
    no manual `body.overflow` code remains; open/close still driven by `useAddItemModal`.
  - Verify: `pnpm build`; `grep -rn shared/modal src` empty; dialog opens/closes/scroll-locks.
  - Files: `add-item-modal/index.tsx`, **delete** `shared/modal.tsx`

- [ ] **T7 — calendar header**.
  - Acceptance: `<h1>`→`Heading`; "Edit day in admin" `<button>`→ ghost `Button`; grid untouched.
  - Verify: `pnpm build`; day header renders; edit-in-admin opens.
  - Files: `calendar.tsx`

- [ ] **T8 — placeholder**.
  - Acceptance: labels via `Text`; DnD `useDrop` + grid inline styles unchanged.
  - Verify: `pnpm build`; drop targets + add-on-click work.
  - Files: `placeholder.tsx`

- [ ] **T9 — pending-items basket**.
  - Acceptance: container→`Card`; 👈/👉→`IconButton` + lucide `ChevronLeft/Right`;
    labels→`Text`; DnD + scroll logic unchanged.
  - Verify: `pnpm build`; unassign drop + scroll buttons work.
  - Files: `pending-items-basket/index.tsx`

- [ ] **T10 — slot-creation tidy**.
  - Acceptance: grouped/labeled with Radix layout; behavior identical.
  - Verify: `pnpm build`; each slot button creates a slot.
  - Files: `slot-creation.tsx`

- [ ] **T11 — cleanup + final verify**.
  - Acceptance: `.btn` removed from `custom-styles.css`; all success-criteria greps empty.
  - Verify: `pnpm build` + Biome clean + full 7-flow smoke test.
  - Files: `src/custom-styles.css`

## Open Questions

- None blocking. (Note for later, not this migration: custom_admin has no automated
  tests — worth adding component tests for the schedule builder in a follow-up.)
