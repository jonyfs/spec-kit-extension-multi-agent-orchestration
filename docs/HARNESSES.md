# Harness Capability Matrix

The maintained artifact required by Constitution Principle XVI. It records, for
each execution harness, how routing-manifest values reach the run, whether
interactive confirmation is available, the log color depth, the concurrency model
(which determines whether Principle XXI macro-parallelism is possible), and
whether the graphify retrieval tool is available.

> **Almost every row is `unverified`.** Counting harnesses is not supporting them
> (Principle XVI, XX). A row becomes `verified` only when a real executed run or
> that harness's current documentation has been recorded here with a date. The
> README MUST NOT claim a harness this table has not verified.
>
> Two rows are `verified` as of 2026-07-23, each against a real executed run of
> the routing verifier, and each scoped to exactly what that run exercised:
>
> - **Claude Code CLI** — `validate-routing.py` was run in this harness, reading
>   the manifests directly from the working tree; `graphify` resolved on PATH;
>   ANSI rendered; interactive confirmation and git worktrees were available.
> - **GitHub Actions** — the CI `routing` job ran the verifier on an ubuntu-latest
>   runner, reading manifests from the `actions/checkout` working tree, with no
>   interactive confirmation and ANSI in the build console
>   (`spec-kit-extension-multi-agent-orchestration` PR #2, run 29975597363).
>   What is verified is manifests-reach-the-run-via-checkout; **env injection of
>   the provider/model variables was not exercised** (they were unset and produced
>   advisories), so that mechanism remains unverified for this harness.
>
> `TODO(HARNESS_VERIFICATION)`: every other row below is unverified as of
> 2026-07-23.

## Categories

### Traditional CI/CD

| Engine | Values reach the run via | Interactive confirm | Color | Concurrency | graphify | Status |
|---|---|---|---|---|---|---|
| GitHub Actions | `actions/checkout` working tree (verified); step `env:` injection (unverified) | no | ANSI in build console | separate runners | usually absent | **verified 2026-07-23** (checkout path only) |
| GitLab CI | job `variables` | no | ANSI | separate runners | usually absent | unverified |
| CircleCI | context/job env | no | ANSI | separate executors | usually absent | unverified |
| Travis CI | env in `.travis.yml` | no | ANSI | separate VMs | usually absent | unverified |
| Azure Pipelines | pipeline variables | no | ANSI | separate agents | usually absent | unverified |

### Cloud-native orchestrators

| Engine | Values reach the run via | Interactive confirm | Color | Concurrency | graphify | Status |
|---|---|---|---|---|---|---|
| Argo Workflows | pod env + mounted volume | no | hex to dashboard | pods, isolated volumes | image-dependent | unverified |
| Tekton | task params/env | no | hex to dashboard | pods | image-dependent | unverified |
| Kubernetes Jobs | container env | no | structured logs | pods | image-dependent | unverified |
| Apache Airflow | task env / XCom | no | web UI logs | workers | image-dependent | unverified |
| Temporal | activity env | no | structured logs | workers | image-dependent | unverified |

### Enterprise clouds

| Engine | Values reach the run via | Interactive confirm | Color | Concurrency | graphify | Status |
|---|---|---|---|---|---|---|
| AWS CodePipeline | stage env / build spec | no | structured JSON | separate builds | image-dependent | unverified |
| Google Cloud Build | step env | no | structured JSON | separate builds | image-dependent | unverified |
| Jenkins | job env / credentials | no | ANSI or structured | executors | image-dependent | unverified |

### IDE and dev environments

| Engine | Values reach the run via | Interactive confirm | Color | Concurrency | graphify | Status |
|---|---|---|---|---|---|---|
| GitHub Codespaces | shell env, working tree | yes | ANSI in terminal | shared checkout | installable | unverified |
| Local Docker Compose | service env | partial | ANSI | shared filesystem | installable | unverified |
| Nomad | task env | no | structured logs | allocations | image-dependent | unverified |

### Terminal AI agents

| Engine | Values reach the run via | Interactive confirm | Color | Concurrency | graphify | Status |
|---|---|---|---|---|---|---|
| Claude Code CLI | working tree, shell env | yes | ANSI streamed | worktrees | on PATH here | **verified 2026-07-23** |
| GitHub Copilot CLI | shell env | yes | ANSI | shared checkout | installable | unverified |
| Cursor | workspace env | yes | ANSI | shared checkout | installable | unverified |
| Local routers | shell env | varies | ANSI | varies | installable | unverified |

## Cross-cutting constraints

**Interactive confirmation.** In a non-interactive harness (every CI/CD and most
orchestrators above), a manifest requesting confirmation takes the declared
non-interactive fallback. For a write, a push, or a pull request that fallback is
to refuse, matching Principle XIV's confirm-by-default posture.

**Log rendering degrades in a fixed order:** 24-bit hex where available, then the
declared ANSI code, then plain text — never to no output (Principle XVI). This is
why every manifest declares both a hex color and an ANSI code.

**Filesystem isolation** determines whether Principle XXI macro-parallelism is
available. A harness giving each concurrent job its own checkout can run features
in parallel worktrees; one sharing a single checkout must fall back to serial
rather than interleaving features. The "Concurrency" column records which each
harness provides.

**graphify availability** determines whether a stage's declared retrieval runs or
falls back to its non-graph context path (Principle XXIV). Its absence is always a
warning, never a failure — so the "graphify" column never gates support.
