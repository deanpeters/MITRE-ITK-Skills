# Personas — Examples

Two contrasting examples for the same product context: a data pipeline tool used by government analysts. The good example follows the MITRE ITK approach. The bad example shows the most common failure modes.

---

## Example 1: Well-Constructed Personas (Good)

### Session Info

| Field | Value |
|-------|-------|
| Date | 2025-03-12 |
| Facilitator | Jamie Torres |
| Team / Project | DataBridge v2.0 — federal analytics platform |
| Time Box | 90 minutes |
| Participants | Product lead, UX researcher, 2 engineers, 1 customer success rep |

### Step 1: Existing Research Sources

| Source | Type | Date | Key Themes |
|--------|------|------|------------|
| 14 contextual interviews with field analysts | Interviews | Jan–Feb 2025 | Manual workarounds, trust in data quality, approval bottlenecks |
| Onboarding survey, n=82 | Survey | Q4 2024 | Steep learning curve, low confidence on first use |
| Support ticket analysis, 6-month sample | Support data | 2024 | 43% of tickets relate to export failures |
| 3 days of field observation at regional offices | Observation | Feb 2025 | Multi-screen workflows, frequent interruptions, offline constraints |

**Research gaps:**
- No data yet on senior leadership usage patterns
- Mobile/tablet usage not covered in observation sessions

---

### Step 3: User Archetypes

---

#### Persona 1: Analyst Amy — Primary

| Attribute | Detail |
|-----------|--------|
| **Persona Type** | Primary |
| **Role / Title** | GS-11 Intelligence Analyst, DHS regional office, 4 years in role |
| **Experience Level** | Intermediate |
| **Unique Use-Case** | Produces weekly operational summaries from multiple disconnected data feeds under time pressure |
| **Context / Environment** | Open-plan office, frequent interruptions; works across 3 monitors; intermittent VPN connectivity; files must pass through a data review queue before publication |

**Goals & Motivations**
- Deliver accurate, cited weekly briefs to her supervisor without working late on Fridays
- Build a reputation as the analyst whose data can be trusted without double-checking

**Needs**
- Functional: a single export that combines all three source feeds with audit trail intact
- Emotional: confidence that the numbers she presents won't be challenged in the meeting

**Pain Points & Frustrations**
- Reconciling three export formats manually takes 2+ hours every Wednesday
- Export failures at 4:45pm with no error message and no way to recover the session
- Approval queue adds 48 hours to any rushed deliverable, with no status visibility

**Limitations & Constraints**
- Cannot install software locally — must work within approved toolset
- VPN drops frequently in the regional office; any workflow requiring persistent connection fails

**Representative Quote**
> "The data is usually right, but I still spend half my time proving it's right. If the tool just showed me the audit trail I could stop re-running everything from scratch."

**Evidence Trail**
- Goals: interviews #3, #7, #11
- Pains: support ticket analysis (export failures = 43% of tickets); interviews #5, #9
- Constraints: field observation notes, day 2

---

#### Persona 2: Supervisor Sam — Secondary

| Attribute | Detail |
|-----------|--------|
| **Persona Type** | Secondary |
| **Role / Title** | GS-14 Branch Chief, 12 years in federal service, 3 managing this team |
| **Experience Level** | Novice (product user) |
| **Unique Use-Case** | Reviews and approves analyst outputs; rarely interacts with the tool directly but sets standards for what "good" output looks like |
| **Context / Environment** | Calendar-heavy schedule; reviews deliverables asynchronously on a tablet; values presentation quality as a proxy for analytical rigor |

**Goals & Motivations**
- Deliver reliable, defensible products to leadership without being surprised in the room
- Develop his team's autonomy so he's not the bottleneck on every approval

**Needs**
- Functional: formatted outputs that don't require manual cleanup before forwarding upward
- Social: be seen as running a high-quality, trustworthy analytical operation

**Pain Points & Frustrations**
- Receives outputs with inconsistent formatting that require his own editing before forwarding
- No visibility into where an approval request is sitting in the queue

**Limitations & Constraints**
- Reviews on a tablet during commute — cannot interact with complex interfaces
- Doesn't have time to learn the tool; relies on Amy to explain anomalies

**Representative Quote**
> "I trust my team. What I don't trust is getting a question from the Deputy that I can't answer because the data came out of a tool I've never used."

**Evidence Trail**
- Goals and pains: interviews #2, #6 (supervisor interviews)
- Constraints: field observation day 3, tablet review behavior observed

---

### Step 4: Visual Reference & Quotes Summary

| Persona | Primary / Secondary | Image | Signature Quote |
|---------|---------------------|-------|-----------------|
| Analyst Amy | Primary | Mid-30s woman, open-plan office setting | "I still spend half my time proving the data is right." |
| Supervisor Sam | Secondary | 50s man, reviewing document on tablet | "I don't trust getting a question I can't answer because of a tool I've never used." |

### Persona Hierarchy Summary

| Persona | Primary / Secondary | Core Decision |
|---------|---------------------|---------------|
| Analyst Amy | Primary | All workflow design, error recovery, and export decisions optimize for Amy's use case |
| Supervisor Sam | Secondary | Output formatting and audit trail visibility accommodate Sam without disrupting Amy's workflow |

---

**Why this works:**

- **Specific names tied to real roles:** "GS-11 Intelligence Analyst, DHS regional office, 4 years" forces concrete design decisions. "Government analyst" does not.
- **Goals are observable:** "Deliver accurate cited weekly briefs without working late on Fridays" — you can see and measure this. "Be successful" is not observable.
- **Pain points are specific and measurable:** "2+ hours every Wednesday reconciling three export formats" is a design target. "Exports are frustrating" is not.
- **Quotes reveal mindset, not facts:** Both quotes expose what the persona cares about and fears, not what features they want.
- **Evidence trails are explicit:** Every attribute traces back to a real source. No invented attributes.
- **Primary/Secondary hierarchy is clear:** Amy's needs win tradeoffs. Sam is accommodated within Amy's workflow, not the other way around.

---

---

## Example 2: Poorly Constructed Personas (What to Avoid)

---

#### Persona 1: The Analyst

| Attribute | Detail |
|-----------|--------|
| **Role / Title** | Analyst |
| **Experience Level** | Varies |
| **Unique Use-Case** | Uses the platform for their work |
| **Context / Environment** | Office |

**Goals & Motivations**
- Do their job well
- Save time

**Pain Points & Frustrations**
- The tool is sometimes confusing
- Things take too long

**Representative Quote**
> "I want the tool to be easier to use."

---

**Why this fails:**

- **"Analyst" is a category, not a persona.** It covers 50 different roles, experience levels, and use cases. You cannot make a design decision from it.
- **"Experience level: varies" means the persona is actually multiple people.** If experience varies, you have two personas minimum.
- **"Uses the platform for their work" is not a use-case.** It describes literally every user. A use-case is the *specific scenario* this archetype uniquely represents.
- **Goals are internal and unmeasurable.** "Do their job well" cannot inform a single design decision. What does "well" look like? By when? Compared to what?
- **Pain points are vague.** "Confusing" and "takes too long" tell you nothing. What specifically is confusing? Which step takes too long, and how long is too long?
- **The quote is marketing copy.** Every persona of every product in every industry "wants it to be easier to use." This quote carries zero information.
- **No evidence trail.** There is no way to know if any of this came from research or was invented in a meeting.

**How to fix it:**
- Name them: "Analyst Amy, GS-11, DHS regional office, 4 years in role"
- Specify the use-case: "Produces weekly operational summaries from multiple disconnected data feeds under time pressure"
- Make goals observable: "Deliver cited briefs to supervisor before 3pm Friday without manual data reconciliation"
- Quantify pains: "Reconciling three export formats manually takes 2+ hours every Wednesday"
- Use a real quote or leave it as a placeholder: "[PLACEHOLDER — needs interview evidence]"
- Add an evidence trail for every attribute
