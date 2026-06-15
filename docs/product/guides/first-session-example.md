# First session · concrete example

A textual walkthrough of what a first PhantomOS session actually looks like. No screenshots yet; this is the transcript version. Every line starting with `>` is operator input; every indented block is the agent's response.

The example uses a fictional skincare brand named *Glowco* with one hero product (*Crème Éclat*) and one audience segment (*Femmes 40-55 ans*). Replace with your own.

## Turn 1 · Landing in an empty workspace

> *hey*

    Hey. Quick before we start, pick your mode. If unsure, pick (1), it's the safest.

    (1) New to AI.
    (2) I've used ChatGPT or Claude in chat.
    (3) Comfortable with Claude Code or other agentic tools.
    (4) Expert, skip everything.

    (I'll speak English with you by default. If you'd rather work in another language, tell me.)

The agent waits. The operator picks (3).

## Turn 2 · Short narrative + chairman close

> *3*

    Hey. A classic chatbot is amnesic, here it's the opposite. Your folder becomes a real working memory. Your brands, your clients, your offers, what you learn along the way, your platform rules, everything lives in structured files I consult on every request. Your corrections become my rules.

    My posture: I orchestrate, I delegate to specialized capabilities, I take load off you. No tunnel, no questionnaire. We talk, I run, you validate.

    You pick, I set the pace:

    (a) Go direct. Profile + URL of a brand, I scan in the background.
    (b) Tour of capabilities. 90 seconds on what I can do.
    (c) Challenge the philosophy. Why I work like this.
    (d) Other. Tell me.

## Turn 3 · Async setup via URL

> *a · solo, https://glowco.com*

    OK, solo. I'll launch the scan on https://glowco.com in the background. 3 to 5 minutes. Meanwhile, ask me anything or challenge a point. I'm here.

The agent launches the `snapshot-brand` skill as a subagent and stays conversational. The operator might ask a question, test another capability, or simply wait. Three minutes later the snapshot-brand returns.

## Turn 4 · Snapshot returns

    I have your brand pre-filled from the site. Identity detected: Glowco, premium skincare, FR-first. Hero product: Crème Éclat (89 €, anti-aging). Visible audience: women 40-55 with sensitive skin. Two active offers: single unit, 3-month cure at -10%.

    Want to validate what's right together and complete what's missing ? 3 to 5 min.

## Turn 5 · Validation loop

> *yes*

    OK. First pass, three questions to calibrate.

    Tone: I read serene, expert, zero urgency. Does that match what you'd write yourself, or do you want it sharper ?

The operator answers. The agent records the change, confirms in plain language, moves to the next question. No JSON shown. No file paths. The operator never opens anything.

After three or four turns, the agent closes validation and proposes the Build chantiers.

## Turn 8 · Build chantiers close

    Context is set to about 60%. Before we ship a deliverable, three chantiers to arbitrate:

    (a) Validate the inferred customer and positioning. 15 min, becomes source of truth.
    (b) Set up platform access (Meta Ads, Shopify if you use them). Documented once, reusable.
    (c) Surface past learnings if you have any.
    (d) Other. Tell me.

## Turn 9 · First real deliverable

> *(d) generate 3 ad hooks for the 40-55 audience*

    On it. Pulling brand tone, hero product benefits, audience psychology. Back in 20 seconds.

    Three hooks, calibrated on *serene expert* tone, for the 40-55 audience:

    1. [hook 1]
    2. [hook 2]
    3. [hook 3]

    Notes: hook 2 leans on the *transformation* angle ; 1 and 3 are *efficiency*. If you want a *simplicity* variant, say so.

The operator reads, corrects. The correction gets captured as a reasoning record (*why this angle instead of that one, on this audience*). Next time the agent runs this kind of task, it draws from that record.

## What the operator did not do

- Open a JSON file.
- Copy-paste raw data into a form.
- Navigate a menu of capabilities.
- Re-explain the brand at any point.
- Install anything beyond Claude Code.

## What the workspace now contains

After this session, `brands/glowco/` holds a validated brand entity, one product spec, one audience profile, two offers, and one captured reasoning record in `learnings.json`. Level 1 is complete · the agent can produce calibrated output on demand. Level 2 and 3 fill over time as the operator works.

---

*This example is representative, not prescriptive. Your first session may branch differently · the agent adapts to your comfort level, your profile, and the information you drop in the first message.*
