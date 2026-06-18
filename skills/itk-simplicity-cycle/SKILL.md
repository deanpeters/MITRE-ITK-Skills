---
name: itk-simplicity-cycle
description: Equip users with a visual vocabulary for discussing complexity and simplicity in a design to assess and express the value of adding or removing design elements.
intent: Chart a development path and identify which tools to use at each phase. Help frame the problem and establish the “definition of done.” Increase focus on the program’s actual objectives.
type: component
phase: evaluate
outcome: evaluate
difficulty: advanced
group_size: 6+ people
time_required: 60+ minutes
best_for:
  - "Evaluating whether to add or cut features when a product has accumulated complexity that no longer maps to user value"
  - "Deciding the 'definition of done' for an MVP before scope creep pushes the product past elegant simplicity"
  - "Roadmap reviews where the team must justify removing functionality rather than only shipping additions"
  - "Assessing a maturing product whose past differentiators have become table-stakes commodities requiring redesign"
  - "Aligning a team that disagrees on whether the next move is to build more or simplify"
sources:
  - MITRE Innovation Toolkit (ITK)
  - "https://itk.mitre.org/toolkit-tools/simplicity-cycle/"
---

# Simplicity Cycle

## What Is It

Equip users with a visual vocabulary for discussing complexity and simplicity in a design to assess and express the value of adding or removing design elements.

## Why Use It

Chart a development path and identify which tools to use at each phase. Help frame the problem and establish the “definition of done.” Increase focus on the program’s actual objectives.

## When to Use It

When evaluating changes to your system, organization, or design. When scoping out new features for your product.

## How to Do It

1. Using the Simplicity Cycle framework diagram, identify your project’s location on one of the four numbered points listed below. This assessment is typically based on recent actions and tools. (For example, when the team has been adding a lot of features to the system, the project is probably near the Shift or Stop point). START: The design is simple, basic, immature, and delivers little value. The best move involves adding strategies that increase complexity (e.g., Brainstorming, Prototyping). SHIFT: The design has accumulated a critical mass of complexity and now delivers significant value. The best move is to adopt reductive strategies that decrease complexity (e.g., Trimming, Stormdraining). STOP: The design has accumulated too much complexity, which overwhelms value. The best move is to pause, then use reductive tools to significantly reduce complexity. SHIP: The design is elegant: simple and effective, providing maximum value. Declare it complete and send it out into the world! The yellow arrow indicates time pushing things in the direction of decreased goodness, as yesterday’s breakthroughs become tomorrow’s commodities. This brings us back to the start point, where the cycle starts again.
2. Depending on the project’s current location, identify the desired next location. Make a list of action steps and strategies that can help move the project in that direction.


## Key Concepts

**Complexity-Value Map** — The framework plots design complexity against delivered value on two axes, letting teams locate their product visually rather than arguing abstractly. It exposes when added complexity stops producing proportional value.

**Four Phase Points** — Start (simple, low value), Shift (complex, high value—time to reduce), Stop (over-complex, value declining), and Ship (elegant, maximum value). Identifying your point dictates whether additive or reductive strategies are appropriate next.

**Additive vs. Reductive Strategies** — Additive moves (brainstorming, prototyping) increase complexity to chase value; reductive moves (trimming, stormdraining) cut complexity to recover elegance. Knowing which mode you're in prevents adding features when you should be cutting them.

**Elegant Simplicity** — The 'Ship' state where the design is both simple and effective, delivering maximum value with minimal complexity. It's the target outcome and the signal to declare a release complete.

**Commodity Drift** — The principle that time degrades value—today's breakthrough becomes tomorrow's table-stakes—pushing even shipped products back toward the Start point. It explains why no design stays 'done' permanently.

**Definition of Done** — The Simplicity Cycle helps teams set a concrete completion criterion (reaching the Ship point) rather than indefinitely accreting features, anchoring scope decisions to value rather than effort.


## PM Applications

- Use the four-point map during backlog grooming to decide whether the next sprint should add capability or pay down feature debt through deliberate removal.
- Anchor the MVP scope section of a PRD by identifying the Ship point and explicitly listing what will NOT be built to preserve simplicity.
- Run a roadmap review where each major feature line is placed on the complexity-value map to surface candidates for sunset or consolidation.
- Frame an executive briefing on product simplification by visually showing how the product crossed from Shift into Stop, justifying a reduction initiative.
- Inform OKR planning by reframing a quarter's objective from 'ship more features' to 'reduce complexity while holding value' when the product sits past the Shift point.
- Facilitate a discovery or design sprint by establishing whether the team is in an additive (prototype, expand) or reductive (trim, focus) mode before tooling decisions.

## Benefits

- Provides a visual vocabulary to help teams discuss issues of complexity, and select appropriate design tools & approaches. Also helps teams recognize when they have underdefined their goals.

## Common Pitfalls

- Treating it as a one-hour workshop instead of an ongoing vocabulary; the framework loses power if the team doesn't reuse 'Shift/Stop/Ship' language in subsequent planning, so embed it in recurring ceremonies.
- Misdiagnosing the current point because the team conflates effort with value—plotting a feature-heavy product near Ship when it's actually at Stop leads to shipping bloated software.
- Defaulting to additive strategies because adding features feels productive and is easier to celebrate, while reductive moves get deprioritized—forcing the product to overshoot into the Stop quadrant.
- Using the model only on the whole product when complexity lives in specific subsystems; assess components individually or you'll mask localized bloat behind an aggregate score.
- Ignoring commodity drift after shipping, assuming 'done' is permanent—failing to revisit the cycle means yesterday's elegant product silently degrades into a commodity competitors leapfrog.
- Mapping position by gut feel without value evidence; without usage data or customer signals, the four points become opinion, and the resulting cut/add decisions can't be defended to stakeholders.

## Combine With

Trimming Prototyping

## Assets

- PDF: [Download](assets/Simplicity-cycle.pdf)
- PPTX Template: [Download](assets/Simplicity-cycle.pptx)
- Markdown Template: [template.md](template.md)

## Metadata

| Field | Value |
|-------|-------|
| ITK Phase | EVALUATE |
| Difficulty | Advanced |
| Group Size | 6+ people |
| Time Required | 60+ minutes |
| Source | [itk.mitre.org](https://itk.mitre.org/toolkit-tools/simplicity-cycle/) |
