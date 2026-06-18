# Personas Template

Use this template to translate user research into named, evidence-grounded archetypes that align your team on who the product actually serves and drive concrete product decisions.

---

## Session Info

| Field | Value |
|-------|-------|
| Date | [date] |
| Facilitator | [name] |
| Team / Project | [team or initiative name] |
| Time Box | [e.g., 45+ minutes] |
| Participants | [names / roles present] |

---

## Step 1: Assemble Existing Research

List every source you're drawing from. If a source is missing, note it — that's a research gap to close before finalizing.

| Source | Type | Date / Recency | Key Themes Surfaced |
|--------|------|----------------|---------------------|
| [e.g., user interviews, Q2] | [interviews / survey / analytics / support tickets / observation] | [date] | [themes] |
| [source 2] | [type] | [date] | [themes] |
| [source 3] | [type] | [date] | [themes] |

**Research gaps — what you still don't know:**
- [gap 1 — e.g., "No data on how edge-case users experience onboarding"]
- [gap 2]

> **Quality check:** Are your sources recent enough to be reliable? Do they represent the full range of your user group, or only the most accessible cohort?

---

## Step 2: Add Your Own Evidence & Data

Capture new evidence gathered through observing, interviewing, or profiling. The cohort you interview must span the full diversity of your user group — not just the loudest or most convenient participants.

| Method | Who / How Many | Key Findings | Diversity Coverage Notes |
|--------|----------------|--------------|--------------------------|
| [Observation] | [e.g., 5 users in field] | [findings] | [edge cases, accessibility needs, expertise range represented?] |
| [Interviews] | [e.g., 8 users] | [findings] | [coverage notes] |
| [Profiling] | [e.g., analytics cohort] | [findings] | [coverage notes] |

> **Quality check:** Have you interviewed users who struggle with your product, not just power users? Are underrepresented groups included? Silent high-impact users are often the most revealing.

---

## Step 3: Build User Archetypes

Create one block per persona. Each persona must have a **specific name** (e.g., "Acquisition Amy" not "Military User") and represent a **unique use-case** — if two personas behave the same way, merge them.

> **TIP from MITRE ITK:** Useful personas are narrow, not broad. Specify role details — title, specialty, experience level, context — rather than a generic category. "Acquisition Amy, a GS-12 contracting officer with 6 years in federal procurement" is useful. "A government employee" is not.

> **Before you start:** Confirm one persona will be designated **Primary** (the core design target whose needs must be satisfied) and the rest **Secondary** (accommodated but never the deciding vote on tradeoffs).

---

### Persona [N]: [Specific Name]

> **Naming:** Use an alliterative name + specific role. Makes it memorable and forces specificity.

| Attribute | Detail |
|-----------|--------|
| **Persona Type** | [ ] Primary &nbsp;&nbsp; [ ] Secondary |
| **Role / Title** | [specific title, specialty, seniority — not a generic category] |
| **Experience Level** | [ ] Novice &nbsp;&nbsp; [ ] Intermediate &nbsp;&nbsp; [ ] Expert |
| **Unique Use-Case** | [the one scenario only this persona represents] |
| **Context / Environment** | [where they work, what tools they use, what constraints they face] |

> **Quality check:** Could this persona be confused with another one in your set? If so, sharpen the use-case or merge them.

**Goals & Motivations** — *what they are trying to accomplish and why*
- [Goal 1 — observable behavior, not internal state: "Deliver project two weeks ahead of schedule" not "Be successful"]
- [Goal 2]

**Needs**
- [Need 1 — functional: what they need the product to do]
- [Need 2 — emotional or social: how they need to feel or be seen]

**Pain Points & Frustrations**
- [Pain 1 — specific and measurable: "Spends 3 hrs/week manually reconciling data" not "finds tools frustrating"]
- [Pain 2]

**Limitations & Constraints**
- [e.g., intermittent connectivity, accessibility requirement, regulatory restriction, time pressure]

**Representative Quote**
> "[An invented or real quote that summarizes one key issue, concern, or priority for this persona — should reveal mindset, not just facts]"

> **Quality check:** Does this quote sound like something a real person would say? "I need better tools" is not a quote. "I'm three weeks behind on a deliverable because I'm still waiting on sign-off from four people who weren't in the room" is.

**Evidence Trail** — *source for each attribute above*
- Goals: [source]
- Needs: [source]
- Pains: [source]
- Limitations: [source]

---

*(Copy the block above for each additional persona. Keep the set to 2–7. More than that and none gets treated as primary.)*

---

## Step 4: Visual Reference & Signature Quotes Summary

For each persona, identify a representative image (stock photo or sketch) and confirm the signature quote captures a real concern — not marketing copy.

| Persona | Primary / Secondary | Image | Signature Quote |
|---------|---------------------|-------|-----------------|
| [Name 1] | [Primary] | [stock photo link or description] | "[quote]" |
| [Name 2] | [Secondary] | [stock photo link or description] | "[quote]" |
| [Name 3] | [Secondary] | [stock photo link or description] | "[quote]" |

> **Quality check:** Read the quotes aloud. Do they reveal a real concern a real person would voice? Would your team immediately recognize this person from the description?

---

## Persona Hierarchy Summary

One persona must be the primary design target. Secondary personas are accommodated but cannot override the primary when there is a tradeoff.

| Persona | Primary / Secondary | Core Decision This Persona Drives |
|---------|---------------------|-----------------------------------|
| [Name 1] | Primary | [what product decisions this persona governs] |
| [Name 2] | Secondary | [what is accommodated but not prioritized] |
| [Name 3] | Secondary | [accommodation notes] |

> **Quality check:** If two features conflict — one serving the primary, one serving a secondary — does your team know which wins? If not, the hierarchy isn't clear enough.

---

## Diversity Coverage Check

Confirm the persona set spans the real range of your user population.

- [ ] Edge-case and low-frequency users included, not just power users
- [ ] Accessibility needs and constraints represented
- [ ] Range of experience levels (novice through expert) covered
- [ ] Underrepresented or marginalized groups considered
- [ ] Conflicting mental models between user segments captured

---

## Next Actions

- [ ] Anchor PRD "target user" and "user needs" sections to the primary persona: [name]
- [ ] Rewrite user stories as "As [Persona Name]..." to expose real edge cases
- [ ] Map each persona's goals to measurable production behaviors: [metric per goal]
- [ ] Schedule a research refresh to validate and update personas: [date]
- [ ] Pair with Journey Mapping to walk [primary persona] through their end-to-end workflow
- [ ] Pair with Painstorming to go deeper on [primary persona]'s highest-severity pains

---

## Facilitator Checklist

- [ ] Each persona has a specific name and unique use-case (no overlapping archetypes)
- [ ] Every attribute has an evidence trail — no uninvestigated assumptions
- [ ] One persona designated Primary, rest Secondary
- [ ] Persona set represents the full diversity of the user group
- [ ] Signature quotes are specific and revealing, not generic
- [ ] Research gaps identified and assigned for follow-up
