# Feature Specification: Routing Manifest Schema and Verifier

**Feature Branch**: `feat/routing-manifest-schema`

**Created**: 2026-07-22

**Status**: Draft

**Input**: User description: "Routing manifest schema and verifier. Full design already approved at docs/superpowers/specs/2026-07-22-routing-manifest-schema-design.md — use it as the research input."

## Clarifications

### Session 2026-07-22

- Q: Where does verification look for declaration files? → A: Only in the
  consuming project's own extension configuration directory. The files shipped
  inside the package are templates the installation copies out; verification never
  reads them.
- Q: Where does the catalog of valid workflow stages come from? → A: Parsed from
  the governing document's own catalog table, so code and governance cannot
  diverge. An absent or unreadable table is a loud failure, never an empty list.
- Q: What form does the verification report take? → A: Human-readable text only.
  The pass/fail signal is carried by the exit status, which is all an automated
  gate consumes. No machine-readable output until something needs it.
- Q: Does this project carry its own declarations, or only ship templates? → A:
  Both. This project installs its own declarations so the gate has real files to
  check; a gate whose only input is an empty directory verifies nothing.
- Q: How is "stage not installed" distinguished from "stage unknown"? → A:
  Unknown means absent from the governing catalog and is blocking. Not installed
  means present in the catalog but absent from this project's registered commands,
  and is informational.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Declare how a skill should run (Priority: P1)

A team adopting spec-driven development wants each stage of their workflow to run
under different settings: planning deserves their most capable model and a large
budget, checklist generation does not. Today those decisions live in people's
heads and in whatever each person happens to configure. The team writes one small
file per skill stating the intended provider, effort level, spending ceiling, and
log color, and those files live in the repository where everyone reads the same
answer.

**Why this priority**: Without a written contract there is nothing to verify, and
every other story depends on the file existing and having an agreed shape. This
story alone delivers value even if nothing ever validates it: a reviewer can read
the repository and see what each stage is supposed to cost.

**Independent Test**: Write the two example files, hand them to someone who has
not seen the project, and ask what the planning stage is budgeted at and what
happens when it runs out. They answer correctly from the files alone.

**Acceptance Scenarios**:

1. **Given** a repository with no routing declarations, **When** an author adds a
   declaration file for the planning stage, **Then** the file states the intended
   provider and model by reference rather than by literal name, the effort level,
   the spending ceiling, the action taken when that ceiling is reached, and the
   color used to identify the stage in logs.
2. **Given** a declaration file for a stage that runs work in parallel, **When** a
   reader inspects it, **Then** the file states the concurrency limit and which
   output the stage owns exclusively.
3. **Given** a declaration file, **When** a provider deprecates the model an
   organization was using, **Then** the file requires no edit, because it names
   the setting that carries the model rather than the model itself.

---

### User Story 2 - Catch a broken declaration before it misleads anyone (Priority: P1)

An author writes a declaration that looks reasonable but breaks a project rule:
it omits a spending ceiling, or it lets a stage that writes files silently drop
context when it runs out of budget, or two stages claim the same output file. A
reader would not notice. The project runs a check that reads every declaration
and reports each violation with the rule it breaks, so the problem is found when
the file is written rather than when a run behaves unexpectedly.

**Why this priority**: A declaration nobody validates drifts from the rules
immediately, and the rules it breaks are the ones that protect against
overspending and corrupted output. This story is what turns Story 1 from
documentation into governance.

**Independent Test**: Feed the check a set of deliberately broken declarations
and confirm it reports every planted violation and refuses to pass.

**Acceptance Scenarios**:

1. **Given** a declaration with no spending ceiling, **When** the check runs,
   **Then** it reports the omission as a blocking problem and fails.
2. **Given** a declaration where a file-writing stage is set to drop context on
   budget exhaustion, **When** the check runs, **Then** it reports the
   combination as a blocking problem and fails.
3. **Given** two declarations claiming the same output file, **When** the check
   runs, **Then** it names both files and fails.
4. **Given** a declaration naming a workflow stage that does not exist, **When**
   the check runs, **Then** it reports the unknown stage and fails.
5. **Given** a valid set of declarations, **When** the check runs, **Then** it
   reports no blocking problems and passes.

---

### User Story 3 - Run the check anywhere without false alarms (Priority: P2)

The same check runs on a developer's laptop, where the retrieval tool and the
model settings are present, and on an automated build machine, where neither is.
The build machine must not fail merely for lacking optional tooling, but the
developer should still be told when something is missing that would change how a
run behaves.

**Why this priority**: A check that fails for environmental reasons gets disabled,
and a disabled check protects nothing. This story is what makes the check
survivable in the environments it must run in. It is P2 because the check is
already useful on a developer machine before this distinction exists.

**Independent Test**: Run the check twice against the same valid declarations —
once with the optional tooling and settings present, once without — and confirm
both runs pass while only the second reports advisories.

**Acceptance Scenarios**:

1. **Given** valid declarations and an environment missing the optional retrieval
   tool, **When** the check runs, **Then** it passes and reports the absence as an
   advisory rather than a failure.
2. **Given** valid declarations and an environment where the settings carrying
   provider and model are undefined, **When** the check runs, **Then** it passes
   and reports each undefined setting as an advisory.
3. **Given** a declaration for a workflow stage not installed in this project,
   **When** the check runs, **Then** it reports the declaration as inactive and
   passes.

---

### User Story 4 - Prove the check can actually fail (Priority: P2)

A check that has only ever passed carries no information: passing and being
unreachable look identical. The project keeps a set of deliberately broken
declarations and an assertion that the check rejects them for the expected
reasons, so the check's ability to fail is demonstrated rather than assumed.

**Why this priority**: This is a project rule, not a preference, and the project
has already lost time to gates that were green because they were unreachable. It
is P2 rather than P1 only because the check must exist before it can be proven
fallible.

**Independent Test**: Run the assertion against the broken set and confirm it
reports both that the check failed and that it failed for each expected reason.

**Acceptance Scenarios**:

1. **Given** the deliberately broken declaration set, **When** the assertion runs,
   **Then** it confirms the check failed and that every planted violation appears
   in the report.
2. **Given** the check reports a failure for an unexpected reason instead of the
   planted one, **When** the assertion runs, **Then** the assertion itself fails.
3. **Given** the valid declaration set, **When** the assertion runs, **Then** it
   confirms the check passed, proving the check is not a blanket rejector.

---

### Edge Cases

- A declaration file that is not readable as structured data at all reports a
  parse failure naming the file, rather than crashing or being skipped silently.
- A stage declared to run work in parallel while also claiming a single output
  file is contradictory, and is reported as such.
- A declaration listing a context-dropping order while not configured to drop
  context carries dead configuration, and is reported as an advisory.
- A color declared for log output without an accompanying terminal equivalent
  cannot render on a plain build console, and is reported as blocking.
- No declaration files present at all is reported distinctly from success: a
  check with nothing to examine has not passed.
- The governing document's catalog table being absent, renamed, or reformatted
  beyond recognition halts the check with an explicit failure naming what could
  not be read, rather than proceeding against an empty catalog.
- A workflow stage in the catalog with no declaration is reported as an
  informational gap rather than a failure, because declaring every stage is not
  required.

## Requirements *(mandatory)*

### Functional Requirements

**Declaration format**

- **FR-001**: The system MUST define one declaration file per workflow stage,
  stating the stage it governs.
- **FR-001a**: Declarations MUST live in the consuming project's own configuration
  directory for this extension. Verification MUST read only that location. The
  declaration files shipped inside the package are templates that installation
  copies out, and verification MUST NOT treat them as a project's declarations.
- **FR-002**: Declarations MUST reference the provider and model through the name
  of a setting that carries the value, never through a literal provider or model
  name.
- **FR-003**: Declarations MUST express effort on a fixed set of four levels, and
  MUST NOT accept any provider's own effort setting.
- **FR-004**: Declarations MUST state a spending ceiling and the action taken on
  reaching it, chosen from: stop; save recoverable state and stop; or drop
  lower-priority context and continue.
- **FR-005**: Declarations that drop context on exhaustion MUST state the order in
  which context is dropped.
- **FR-006**: Declarations MUST state whether the stage writes artifacts, and MUST
  state which single output the stage owns exclusively, or state that it owns none.
- **FR-007**: Declarations MUST state a log color as both a precise color value
  and a plain-terminal equivalent.
- **FR-008**: Declarations for stages that run work concurrently MUST state a
  concurrency limit.
- **FR-009**: Declarations MUST state whether the stage retrieves context from the
  knowledge graph and, when it does, the budget for that retrieval.
- **FR-010**: Declarations MUST NOT name an execution environment; the environment
  is not part of a stage's configuration.

**Verification**

- **FR-011**: The system MUST reject any declaration containing a property the
  format does not define.
- **FR-012**: The system MUST reject a declaration naming a workflow stage absent
  from the project's catalog of known stages.
- **FR-012a**: The system MUST derive that catalog from the governing document's
  own catalog table rather than from a copy embedded in the checking logic, so
  that adding a stage to governance cannot leave the check silently disagreeing.
- **FR-012b**: The system MUST fail loudly when the governing document or its
  catalog table is absent or unreadable, and MUST NOT fall back to an empty
  catalog — an empty catalog would make every declaration appear to name an
  unknown stage, or make no declaration checkable at all.
- **FR-012c**: The system MUST distinguish a stage that is unknown, meaning absent
  from the catalog, from a stage that is merely not installed, meaning present in
  the catalog but absent from this project's registered commands. The first is
  blocking; the second is informational.
- **FR-013**: The system MUST reject a missing, zero, or negative spending ceiling.
- **FR-014**: The system MUST reject a declaration that both writes artifacts and
  drops context on exhaustion.
- **FR-015**: The system MUST reject two declarations claiming the same output.
- **FR-016**: The system MUST reject a stage declared concurrent while also
  claiming a single owned output.
- **FR-017**: The system MUST classify every finding as blocking, advisory, or
  informational, and MUST signal failure only when at least one blocking finding
  exists.
- **FR-018**: The system MUST treat a missing optional retrieval tool, an
  undefined provider or model setting, and an unverified environment as advisory
  rather than blocking.
- **FR-019**: The system MUST treat a declaration for an uninstalled stage as
  informational rather than blocking.
- **FR-020**: The system MUST report every finding across all declarations in a
  single run, rather than stopping at the first blocking one.
- **FR-021**: The system MUST report distinctly when it found no declarations to
  examine, and MUST NOT report that condition as success.
- **FR-022**: The system MUST state, in its own output and documentation, that it
  does not verify whether a configured model is available to the caller or in use
  by the current session.

**Invocation and distribution**

- **FR-023**: Users MUST be able to run the verification through a command the
  project provides, on both major operating system families, with equivalent
  behavior.
- **FR-024**: The system MUST run as an automated gate on every proposed change.
- **FR-024a**: This project MUST install its own declarations, not merely ship
  templates, so the gate runs against real files. A gate whose only input is an
  empty directory reports success while verifying nothing.
- **FR-024b**: The report MUST be human-readable text, and the pass or fail
  signal MUST be carried by the run's exit status. No machine-readable report
  format is required until a consumer needs one.
- **FR-025**: The system MUST ship documentation describing every declaration
  field, the mapping from each effort level to each provider's own setting with
  the date that mapping was verified, the finding classification, and the stated
  limits of what verification covers.

**Demonstrated fallibility**

- **FR-026**: The project MUST keep a set of declarations that each violate one
  rule, and MUST assert that verification rejects them naming each expected
  violation.
- **FR-027**: The project MUST keep a valid declaration set and MUST assert that
  verification passes it.

### Key Entities

- **Routing declaration**: One workflow stage's intended execution settings —
  which provider and model to use (by reference), how much reasoning effort, how
  much it may spend and what happens at the limit, whether and how it
  parallelizes, whether it retrieves from the knowledge graph, what it writes, and
  how it appears in logs.
- **Stage catalog**: The set of workflow stages known to exist, against which a
  declaration's target is checked. A declaration naming a stage outside it is
  invalid.
- **Finding**: One result from verification — the declaration it concerns, the
  rule it relates to, its classification as blocking, advisory, or informational,
  and a description an author can act on.
- **Verification report**: The complete set of findings from one run, plus the
  overall pass or fail signal derived solely from whether any blocking finding
  exists.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every rule this feature enforces has been observed rejecting a
  declaration that violates it — no rule is trusted on the basis of having only
  ever passed.
- **SC-002**: A reader who has not seen the project can state a stage's spending
  ceiling, its behavior at that ceiling, and what it writes, using only its
  declaration file.
- **SC-003**: Verification of a complete declaration set finishes in under five
  seconds, so it can run on every proposed change without becoming a reason to
  skip it.
- **SC-004**: Verification passes in an environment lacking every optional tool
  and every provider setting, while still reporting each absence.
- **SC-005**: A declaration requires no edit when a provider renames or deprecates
  a model.
- **SC-006**: An author who introduces a violation learns which rule they broke
  and in which file, without consulting anyone.
- **SC-007**: Both operating system families produce identical findings for
  identical declarations.
- **SC-008**: Adding a stage to the governing catalog makes declarations for that
  stage valid without any change to the checking logic.

## Assumptions

- Verification is a reporting activity. Nothing in this feature causes a workflow
  stage to actually run under its declared settings, because the extension
  mechanism this project builds on provides no means to intercept model
  selection. The declarations are contracts; enforcement of those contracts at
  execution time, if ever built, is separate work.
- Provider and model values are supplied by the environment. This feature defines
  how a declaration names them and verifies whether they are set, not how an
  organization sets them.
- Verifying that a model exists or is reachable would require an authenticated
  call to a provider, and a gate requiring credentials cannot run on a proposed
  change from outside the project. Such verification is therefore excluded.
- The stage catalog is the one recorded in the project's governing document, which
  currently lists nine confirmed stages and one unconfirmed. The unconfirmed stage
  receives no declaration. Reading that table at run time couples the check to the
  document's formatting; the accepted trade is that a formatting change breaks the
  check loudly, which is preferable to a copied list that diverges quietly.
- Two declarations are written in this feature — one for a read-mostly stage and
  one for a concurrent, writing stage — because these exercise opposite ends of
  the format. Declarations for remaining stages follow once the format has been
  proven.
- The retrieval tool is optional at every point. Its absence changes what context
  a stage receives but never whether verification succeeds.
- Authors edit declarations by hand. A published, machine-readable definition of
  the format is what gives them editor assistance, which is why the format is
  defined declaratively rather than only inside the checking logic.
