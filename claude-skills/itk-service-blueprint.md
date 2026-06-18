# ITK: Service Blueprint

Help a product practitioner apply **Service Blueprint** from the MITRE Innovation Toolkit.

**Phase:** UNDERSTAND · **Difficulty:** Advanced · **Group:** 5+ people · **Time:** 60+ minutes

> Outline and visualize a service to connect the user experience, or “frontstage,” to what happens behind-the-scenes, or “backstage.”

---

## When This Tool Fits Best

- Diagnosing root causes of a complex problem that spans multiple teams, systems, or touchpoints before committing roadmap resources
- Aligning cross-functional stakeholders on how frontstage user experience maps to backstage operations and dependencies
- Identifying handoff failures and orchestration gaps when a user journey crosses organizational or technical boundaries
- Planning a service redesign where fixing the visible experience requires changing backend processes, policies, or systems
- Surfacing systemic friction and ownership ambiguity that single-team retrospectives or journey maps cannot reveal

---

## Key Concepts

**Frontstage vs. Backstage** — Frontstage is everything the user directly experiences; backstage is the people, systems, and processes invisible to them. Mapping both reveals where backend constraints silently degrade the user experience.

**Line of Visibility** — The boundary separating what users see from what happens behind the scenes. Tracing how actions cross this line exposes where frontstage promises break against backstage reality.

**Touchpoint** — A specific point of interaction between the user and the service at each step. Cataloging touchpoints clarifies where to instrument metrics and where experience quality is won or lost.

**Critical Moment** — A point of pain or breakdown that erodes the user's experience. Isolating critical moments turns a sprawling map into a prioritized list of fixes with measurable impact.

**Blueprint Layers** — Stacked rows of detail per step: actor, system, observation, data, policy, question, critical moment, and idea. Layering forces teams to expose hidden dependencies and rules behind each interaction.

**Scenario Statement** — A structured framing in the form 'A user tries to ___, experiences ___, resulting in ___.' It scopes the blueprint to a concrete, high-impact path rather than the entire service.

---

## Common Pitfalls to Watch For

- Blueprinting the entire service instead of one scoped scenario, producing a sprawling map too dense to drive any decision or prioritization.
- Filling the frontstage layers while leaving backstage actors, systems, and policies vague, which hides the real root causes the tool exists to surface.
- Treating the blueprint as a documentation deliverable rather than working backward from critical moments to concrete service changes, so insights never reach the backlog.
- Running the workshop without the backstage owners (engineering, ops, support) present, leaving system and policy layers inaccurate and fixes unimplementable.
- Skipping the data layer and ranking critical moments by opinion rather than evidence, leading to investment in low-impact fixes that don't move metrics.
- Confusing this with a journey map and stopping at the user experience, missing the cross-team handoffs and dependencies that only a full blueprint reveals.

---

## How to Help

- **Read context first.** Before asking anything, check what the user has already shared — their role, product, team size, timeline, what phase of work they're in.
- **Experienced users can skip straight to the work.** If they name this tool directly or describe a clear situation, help them run it — don't force a guided flow.
- **Use the Adaptive Decision Ladder when the situation is unclear.** Offer numbered options; the user can reply `2`, `1 & 3`, or describe freely. Skip steps that context already resolves.
- **Walk through the facilitation steps** from the full skill reference, adapting language and examples to their specific product context.
- **Surface pitfalls proactively** — especially those most likely given what they've shared.
- **Suggest complementary tools** when the conversation reveals adjacent needs.
- **Stay grounded in product artifacts**: PRDs, OKRs, roadmaps, user stories, sprint ceremonies, stakeholder briefings.

## Full Reference

→ [`skills/service-blueprint/SKILL.md`](../skills/service-blueprint/SKILL.md)
