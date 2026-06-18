---
name: card-sorting
description: This hands-on activity allows participants to communicate and document their mental model and how they think about a set of information, creating a logical structure (e.g., relationships, sequences, timing).
intent: Determine how to organize and structure information that makes sense to users. Understand the mental models of an individual or a group of people. Explore and assess multiple arrangements and architectures.
type: component
phase: understand
outcome: understand
difficulty: advanced
group_size: 4+ people
time_required: 45+ minutes
best_for:
  - "Designing or restructuring information architecture for a product's navigation, menus, or feature taxonomy before UI design"
  - "Validating whether your proposed feature grouping matches how target users mentally categorize the domain"
  - "Reconciling conflicting stakeholder views on how to organize a complex settings page, dashboard, or content hierarchy"
  - "Discovery research to surface user mental models when designing onboarding flows or categorizing a large content library"
  - "Reducing navigation confusion and support tickets by grounding menu structure in actual user categorization patterns"
sources:
  - MITRE Innovation Toolkit (ITK)
  - "https://itk.mitre.org/toolkit-tools/card-sorting/"
---

# Card Sorting

## What Is It

This hands-on activity allows participants to communicate and document their mental model and how they think about a set of information, creating a logical structure (e.g., relationships, sequences, timing).

## Why Use It

Determine how to organize and structure information that makes sense to users. Understand the mental models of an individual or a group of people. Explore and assess multiple arrangements and architectures.

## When to Use It

When you need to produce an information architecture, introduce structure into a large collection of data, or validate assumptions about how participants categorize information.

## How to Do It

1. Write or print the information onto index cards, paper, or labels. The information on the cards could be single words, phrases, or sentences. Mark each card with an identification number for easy documenting after the sort.
2. Create a set of category titles you think may help get the participants started, or provide blank cards for participants to create their own categories. Differentiate the category titles from the rest of the cards for the participants to sort.
3. Ask the participant to sort the cards one by one in a way that makes sense to them on a large, blank surface, using the existing categories and creating any categories they feel are missing. Asking the participant to speak through their sorting process can provide additional insights about how they think about the information at hand.
4. After the participants sort the deck, take a picture for your records and use the identification numbers to record the categories and card order. Shuffle the card deck between users to eliminate any card order biases.
5. After collecting sort results from all participants, look for trends such as common categories, cards that end up grouped together, or cards grouped under similar categories.


## Key Concepts

**Mental Model** — The internal map users hold of how concepts relate and where things belong. Surfacing it reveals the gap between your product's structure and users' expectations, which drives findability and learnability.

**Open vs. Closed Sort** — In an open sort participants create their own category labels; in a closed sort they sort into predefined categories. Open sorts reveal natural groupings and vocabulary; closed sorts validate an existing architecture.

**Information Architecture** — The structural design of how content and features are organized, labeled, and navigated. Card sorting produces the evidence base for IA decisions instead of relying on internal assumptions.

**Card Granularity** — The level of detail on each card (single word, phrase, or task). Mismatched granularity skews groupings, so cards should represent comparable units of information at the same level of abstraction.

**Agreement Analysis** — Looking across participant sorts for cards that consistently cluster together or split apart. High-agreement clusters become confident IA decisions; contested cards flag ambiguous labels needing further research.

**Order Bias** — The tendency for the initial card sequence to influence how participants group. Shuffling the deck between sessions prevents the presentation order from artificially shaping the resulting structure.


## PM Applications

- Define the navigation hierarchy and menu taxonomy for a new product before writing the IA section of a PRD or handing off to design
- Validate proposed feature groupings during discovery sprints by running closed sorts with representative users against your draft architecture
- Restructure an overgrown settings or admin area by running open sorts to discover how users expect controls to be grouped and labeled
- Inform backlog organization and epic structure by grounding how you cluster related capabilities in real user mental models rather than internal team boundaries
- Surface terminology and labeling decisions for UX copy and user stories, capturing the vocabulary participants naturally use for categories
- Align cross-functional stakeholders in a roadmap or design review by showing evidence-based groupings that resolve debates about how to organize content

## Benefits

- Easy to visually rearrange items and pieces and quickly test out different structures, discover connections, etc.

## Common Pitfalls

- Using cards at inconsistent granularity (mixing high-level features with granular settings), which produces incoherent groupings that can't be translated into a usable hierarchy
- Running only open sorts when you actually need to validate a specific architecture — leaving you with a sprawl of inconsistent labels that are impossible to consolidate into a decision
- Recruiting internal team members or stakeholders instead of real users, so the sort reflects your existing org structure rather than the user mental model you set out to learn
- Skipping the shuffle between participants, letting card order bias create false clustering patterns you then mistake for genuine agreement
- Sorting too many cards in one session (fatigue past ~40-50 cards), causing participants to rush and dump cards into arbitrary piles that pollute your trend analysis
- Treating card sort output as final IA without follow-up tree testing, so unvalidated category labels ship and generate findability problems and support tickets

## Combine With

Mindmapping to come up with a large amount of ideas to sort Trimming to narrow down the amount of cards to sort Lotus Blossom = Card Blossom Journey Map = Journey Sorting

## Assets

- PDF: [Download](assets/Card-sorting.pdf)
- PPTX Template: [Download](assets/Card-sorting.pptx)
- Markdown Template: [template.md](template.md)

## Metadata

| Field | Value |
|-------|-------|
| ITK Phase | UNDERSTAND |
| Difficulty | Advanced |
| Group Size | 4+ people |
| Time Required | 45+ minutes |
| Source | [itk.mitre.org](https://itk.mitre.org/toolkit-tools/card-sorting/) |
