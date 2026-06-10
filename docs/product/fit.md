# Who PhantomOS is for

An honest audit of the match, grounded in a multi-ecosystem analysis. Covers who gets the most value, who should wait, and who should look elsewhere.

The dominant value angle for DTC paid acquisition operators is threefold : measurable time savings (no re-briefing on every campaign, no switching across Meta / TikTok / Google / Shopify / Klaviyo tabs), a single centralized interface that compounds knowledge across brands and seasons, and the encoded methodology becoming a productized asset over time.

## Onboarding posture

PhantomOS is intentionally light at entry. No upfront questionnaire, no admission form, no exhaustive setup before the first deliverable. The system identifies who the operator is, how they work, and on which contexts they operate. The workspace is immediately usable.

Day one on a new brand or mission : from a URL, the system produces a short defendable brief on product, positioning, and offer in a few minutes. The objective is to demonstrate that the agent's eyes are accurate on the context, not to ship a heavy report. Depth comes later, on demand.

When the operator wants to densify, specialized agents work in parallel on the relevant angles (store, offers, audience, competition). A chairman orchestrator aggregates returns and surfaces inconsistencies in interrogative mode (*I noticed this, intentional ?*), never as an operator error. Encoding depth stays a choice, never a system obligation.

## Best fit (DTC paid acquisition)

**DTC brand founder past month 6 with stable ROAS.** You know your audiences, your angles work, you scale paid spend month over month. PhantomOS encodes what you already know intuitively, makes it operational across creatives and campaigns, and compounds your learnings.

**Growth lead at an agency running 3 to 15 DTC accounts.** You operate multiple brands in parallel, each with their own audiences, angles, and creative libraries. PhantomOS unifies the operational layer : one encoded substrate per client, agents producing assets on demand, learnings captured per brand and patterns surfaced cross-brand.

**Solo DTC paid operator** spending most of their time on Meta Ads, TikTok Ads, Google Ads, and on creative production. The asset accumulation across campaigns and seasons is the structural gain.

**Portfolio operator** managing several DTC brands in own portfolio or in equity. The pattern capture cross-brand and the productized delivery margin land hardest here.

**Small team of two to four operators on the same DTC brand or portfolio.** Lead encodes the method, others contribute and consume. Structural caveats apply (single-writer per workspace, no native RBAC) but fit remains direct.

## Misfit

**Pre-traction founder, day one to month three.** Adopting before positioning and audiences are validated encodes guesses. Burn the setup time on direct customer conversations and ad tests instead. Come back post-first-signal.

**Info-products and B2B services operators.** Different stack (no paid ads infrastructure), different metrics (LTV-driven course funnels, B2B pipeline). PhantomOS ships optimized for DTC paid, not these adjacent verticals. The platform itself is extensible if you encode your own kit, but no shipped kit supports you out of the box.

**Distribution-first creator.** Content volume operator whose core activity is distribution across social platforms (Twitter, YouTube, TikTok, newsletter sends). PhantomOS does not cover social scheduling, audio or video production pipelines, community management, newsletter infrastructure, or checkout.

**Enterprise agency with five-plus people on shared multi-tenant client accounts.** PhantomOS lacks the multi-tenant architecture this implies : strict client data separation, role-based permissions, operator-to-operator handoff, client-facing read-only dashboards. On the roadmap.

**Agencies focused on social organic** or performance creator volume. Different stack, different metrics, no shipped kit.

## What the tour does not tell you

The workspace is only as valuable as the capture discipline behind it. The moat is process, not artifact. A week without logging corrections turns the system into a Notion clone that nobody reads. Two mitigations exist (the agent proposes capture after each deliverable, and `learn-from-session` batches on demand) but neither replaces operator discipline. Honest expectation : if you abandon the capture reflex, the system pays back what you put in and no more.

The Claude Code requirement is a real adoption barrier. Claude Pro, Team, or Max subscription is required. The CLI is not optional : the web app works once the workspace exists, but first setup runs through Claude Code. An operator uncomfortable with a terminal will feel friction for the first forty-five minutes.

**Run one agent at a time per workspace.** PhantomOS does not lock files on writes. If two Claude Code sessions target the same workspace simultaneously (two terminal windows, two parallel IDEs, or a shared cloud clone), concurrent `write_to_context` calls can corrupt the event log or overwrite proposals. Workaround until future iteration : close any other session on the same workspace before starting a new one. Multi-agent orchestration in a single session is fine ; parallel sessions on the same workspace are not.

**Small team caveat.** PhantomOS is single-writer per workspace by design. No native RBAC, no simultaneous-edit resolution, no per-user audit log. The pattern that works : one lead operator owns the workspace and others contribute occasionally or consume read-side. The pattern that breaks : five people editing in parallel on session-state and awareness files.

## Cost honesty, session tokens, subscription, amortization

There is a real session cost. The agent loads the agent contract, the active context, and the relevant resources on every session. A Claude Pro, Team, or Max subscription is required on top. PhantomOS is not free. The honest question is not whether it costs tokens, but whether the token efficiency is better or worse than the alternative for your usage pattern.

**Structural reasons PhantomOS is more token-efficient on anchored work** :

1. **Zero re-briefing.** Every new ChatGPT or Claude chat with full re-briefing costs 2 to 5K tokens just to set up context. Across 100 sessions, that is 200 to 500K wasted re-brief tokens. PhantomOS reads the context from files ; zero re-brief.
2. **Selective indexed loading.** `query-context` plus `index.json` pull only what is relevant for the current task. Classical vector RAG loads ten to twenty chunks of marginal relevance per query. Indexed loading wastes fewer tokens on context the task does not need.
3. **Prompt caching on stable context.** Anthropic's five-minute cache TTL covers `CLAUDE.md`, core entity files, and stable resources. After the first read in a session, repeated reads are effectively free. Fresh-session patterns do not benefit the same way.
4. **Parametric composition amortizes per deliverable.** Generating one hundred creative variants by traversing curated banks (mechanics, angles, audiences, proof) is cheaper in tokens than a hundred blank prompts each carrying full context.
5. **Compound across sessions.** A learning captured once is consulted fifty times over six months. Alternative patterns re-explain the same learning every time, which is linear cost without amortization.

**Where PhantomOS is more expensive than the alternative** :

- One-shot, non-anchored questions. *"Quick question about a framework"* in PhantomOS carries 5 to 15K tokens of overhead that a plain Claude chat does not. Use the right tool for the right query.
- Operators who set up the workspace but do not reuse it. Setup cost is real ; without amortization it is wasted.
- First thirty days. Compound effects have not yet kicked in.

**Where it becomes clearly more efficient** :

- Repeated anchored work, daily operations on the same context.
- Mass generation via parametric composition.
- Cross-referenced queries that would otherwise require full re-explanation.
- Dense exploration sessions where the prompt cache absorbs repeated reads.
- Multi-context workflows where registries and learnings are mutualized.

**Empirical proof per operator, not aggregate.** No published benchmark across operators on identical tasks exists. The honest path : run the comparison on your own usage curve over 30 to 60 days. The structural arguments above (cache savings, re-brief avoided, indexed retrieval, parametric composition output-per-token, compound across sessions) rest on measurable primitives. The on-demand `benchmark-tokens` skill (planned) reads your session token consumption and compares against a baseline scenario you provide, on your real workspace, with your real brands. Generic benchmarks across abstract operators always lie ; per-operator benchmarks on real usage tell the truth.

## Agency client-data tension (DTC growth lead specific)

A growth lead at an agency who encodes brand-specific knowledge per DTC client into PhantomOS faces a contractual question on retainer termination : the encoded substrate (audiences, angles, creatives, learnings) belongs to whom ? The agency, the client, or both ? PhantomOS does not enforce this. The pattern that works in practice :

- **Workspace separation.** One workspace per client brand. The encoded substrate per brand stays portable. On retainer termination, the workspace transfers to the client (export of `brands/{slug}/` folder), or stays with the agency, depending on the service contract.
- **Operator-side discipline.** No skill handles this split today. It requires explicit framing in the service contract (workspace ownership, transfer clause, encoded data property).
- **Vertical pack roadmap.** A formal multi-tenant agency layer with native client-data separation, role-based permissions, and exit licensing is on the roadmap.

## Workaround for small teams (2 to 5 operators)

Single-writer per workspace by design. For agencies running multiple DTC clients with 2 to 5 operators, the operational pattern that works :

- **One workspace per client brand**, owned by the senior operator who encodes the methodology.
- **Junior operators consume read-only**, propose corrections via plain text or PR-style discussion, the senior commits to the workspace.
- **Workspace handoff at retainer end** : export the brand folder, transfer to the client, or keep as agency IP depending on the service contract.

Native multi-operator (role-based access, simultaneous editing, client read-only dashboards) is on the roadmap. Until then, this workaround covers the realistic 2 to 5 person agency case without ownership ambiguity.

## When to revisit this page

The extractibility test (every core feature must survive swapping the craft's central entity, otherwise it ships in a vertical pack ; see `docs/system/extending.md`) applies to every feature and every profile. If your situation fits neither the best-fit nor the misfit descriptions, read the related vertical pack sections of `docs/vision/roadmap.md` before investing. The product evolves ; what's misfit today may become fit in six months if the corresponding vertical pack ships.

---

> **Why this doc exists :** every tool has a fit curve and most marketing hides it. PhantomOS has specific sweet spots and specific misfits. Making them explicit up front saves the operator from adopting at the wrong time, in the wrong configuration, or for the wrong expectation. The product is strong inside its scope and honest about what it does not cover.
