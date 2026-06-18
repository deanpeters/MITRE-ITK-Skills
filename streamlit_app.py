"""MITRE ITK Skills — browser-based tool explorer and facilitation guide generator."""

import os
import re
from pathlib import Path

import anthropic
import streamlit as st
import yaml

try:
    from openai import OpenAI as _OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="MITRE ITK Skills",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Provider config
# ---------------------------------------------------------------------------

ANTHROPIC_MODELS = ["claude-opus-4-8", "claude-sonnet-4-6", "claude-haiku-4-5"]
OPENAI_MODELS    = ["gpt-4o", "gpt-4o-mini", "o3-mini"]
PROVIDERS        = ["Anthropic", "OpenAI"] + (["Local model"] if HAS_OPENAI else [])


def is_deployed():
    """True when a server-side Anthropic key is present (Streamlit Community Cloud)."""
    try:
        return bool(st.secrets.get("ANTHROPIC_API_KEY"))
    except Exception:
        return False


def get_llm_config():
    """Return the active provider config dict. Keys come from env vars only."""
    if is_deployed():
        return {
            "provider": "Anthropic",
            "key": st.secrets["ANTHROPIC_API_KEY"],
            "model": "claude-opus-4-8",
            "base_url": None,
        }
    provider = st.session_state.get("llm_provider", "Anthropic")
    if provider == "Anthropic":
        key = os.environ.get("ANTHROPIC_API_KEY", "")
    elif provider == "OpenAI":
        key = os.environ.get("OPENAI_API_KEY", "")
    else:
        key = "ollama"
    return {
        "provider": provider,
        "key":      key,
        "model":    st.session_state.get("llm_model", ANTHROPIC_MODELS[0]),
        "base_url": st.session_state.get("llm_base_url", "http://localhost:11434/v1"),
    }


def llm_ready(config):
    if config["provider"] == "Local model":
        return bool(config["model"].strip())
    return bool(config["key"].strip())


def stream_response(config, system, user_msg):
    """Unified streaming generator. Yields text chunks across all providers."""
    provider = config["provider"]

    if provider == "Anthropic":
        client = anthropic.Anthropic(api_key=config["key"])
        with client.messages.stream(
            model=config["model"],
            max_tokens=2048,
            thinking={"type": "adaptive"},
            system=system,
            messages=[{"role": "user", "content": user_msg}],
        ) as stream:
            yield from stream.text_stream

    elif provider in ("OpenAI", "Local model"):
        kwargs = {"api_key": config["key"] or "ollama"}
        if provider == "Local model":
            kwargs["base_url"] = config["base_url"]
        client = _OpenAI(**kwargs)
        stream = client.chat.completions.create(
            model=config["model"],
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user_msg},
            ],
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta


# ---------------------------------------------------------------------------
# ADL data
# ---------------------------------------------------------------------------

ADL_STEP1_OPTIONS = [
    "Scoping — figuring out who's involved, what the system looks like, or what our culture needs",
    "Defining — not sure what problem to solve, or need to pressure-test a direction",
    "Understanding users — need research, journey maps, or clearer user needs",
    "Generating solutions — have a defined problem and need ideas",
    "Evaluating options — need to test, cut, prioritize, or assess tradeoffs",
    "Reflecting — sprint retro, project wrap-up, or team health check",
    "Other — let me browse all tools",
]

ADL_STEP2_OPTIONS = {
    1: [
        "I don't know who all my stakeholders are yet",
        "I know my stakeholders but need to prioritize who to engage",
        "I need a concrete plan for engaging a specific stakeholder",
        "I need to map the broader system, community, or ecosystem",
        "I need to understand and shape our team or org culture",
        "Multiple of the above",
    ],
    2: [
        "We're probably solving the wrong problem and need to reframe",
        "We have a direction but haven't pressure-tested it for failure",
        "We need to align on long-term purpose (mission/vision)",
        "Multiple of the above",
    ],
    3: [
        "We need to define or sharpen who our user actually is",
        "We need to map their end-to-end experience (stages, pain points, wins)",
        "We need to understand what they need to do, and why (jobs, pains, gains)",
        "We need to understand how they mentally organize information",
        "We need to see both the user experience and the behind-the-scenes operations",
        "Multiple of the above",
    ],
    4: [
        "Broad, free-associative ideation — explore the whole space",
        "Structured, systematic ideation — fill every cell",
        "Embodied ideation — role-play and act out the experience",
        "Analogical thinking — borrow solutions from other domains",
    ],
    5: [
        "Too many ideas — need to converge to the most valuable",
        "Need to test a solution with users before building",
        "Need to remove unnecessary complexity from an existing design",
        "Need to assess whether adding features adds or subtracts value",
    ],
    6: [
        "Sprint retrospective — structured team reflection on a recent sprint",
        "Project or initiative wrap-up",
        "Quick positive/potential/negative scan of a product, process, or system",
    ],
}

ADL_RECOMMENDATIONS = {
    (1, 0): ["stakeholder-identification-canvas"],
    (1, 1): ["stakeholder-map-and-matrix", "stakeholder-power-categories"],
    (1, 2): ["quickstart-stakeholder-engagement-canvas"],
    (1, 3): ["system-map", "community-map"],
    (1, 4): ["culture-building-canvas"],
    (1, 5): ["stakeholder-identification-canvas", "stakeholder-map-and-matrix", "system-map"],
    (2, 0): ["problem-framing"],
    (2, 1): ["premortem"],
    (2, 2): ["mission-and-vision-canvas"],
    (2, 3): ["problem-framing", "premortem", "mission-and-vision-canvas"],
    (3, 0): ["personas", "painstorming"],
    (3, 1): ["journey-mapping"],
    (3, 2): ["value-proposition-canvas", "painstorming"],
    (3, 3): ["card-sorting"],
    (3, 4): ["service-blueprint"],
    (3, 5): ["personas", "journey-mapping", "value-proposition-canvas"],
    (4, 0): ["mindmapping"],
    (4, 1): ["lotus-blossom"],
    (4, 2): ["bodystorming"],
    (4, 3): ["triz-prism"],
    (5, 0): ["stormdraining"],
    (5, 1): ["prototyping"],
    (5, 2): ["simplicity-cycle", "trimming"],
    (5, 3): ["simplicity-cycle"],
    (6, 0): ["retro-rundown"],
    (6, 1): ["retro-rundown"],
    (6, 2): ["rose-bud-thorn"],
}

PHASE_ORDER = ["scope", "define", "understand", "generate", "evaluate"]

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

@st.cache_data
def load_skills():
    skills = {}
    skills_dir = Path("skills")
    if not skills_dir.exists():
        return skills

    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        content = skill_file.read_text(encoding="utf-8")
        fm = _parse_frontmatter(content)
        if not fm:
            continue

        h1 = re.search(r'^# (.+)$', content, re.MULTILINE)
        raw_name = h1.group(1).strip() if h1 else skill_dir.name.replace("-", " ")
        display_name = _normalize_display_name(raw_name)

        slug = skill_dir.name
        skills[slug] = {
            "slug": slug,
            "display_name": display_name,
            "description": fm.get("description", ""),
            "phase": (fm.get("phase") or "").lower(),
            "difficulty": fm.get("difficulty", ""),
            "group_size": fm.get("group_size", ""),
            "time_required": fm.get("time_required", ""),
            "best_for": fm.get("best_for") or [],
            "content": content,
        }
    return skills


def _normalize_display_name(name):
    PRESERVE = {"TRIZ"}
    return " ".join(
        word if word in PRESERVE else word.title()
        for word in name.split()
    )


def _parse_frontmatter(content):
    m = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {}


def _extract_section(content, heading):
    m = re.search(rf'## {re.escape(heading)}\n\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    return m.group(1).strip() if m else ""


# ---------------------------------------------------------------------------
# Navigation helpers
# ---------------------------------------------------------------------------

def go(page, **kwargs):
    st.session_state.page = page
    for k, v in kwargs.items():
        st.session_state[k] = v


def reset():
    for k in ["page", "adl_step1", "adl_step2", "adl_time", "adl_group", "selected_skill"]:
        st.session_state.pop(k, None)


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

def render_sidebar():
    with st.sidebar:
        st.markdown("## MITRE ITK Skills")
        st.caption("27 tools · 5 innovation phases")

        if st.button("Start over", use_container_width=True):
            reset()
            go("landing")
            st.rerun()

        if not is_deployed():
            st.divider()
            _render_provider_config()

        st.divider()
        st.caption("[MITRE ITK](https://itk.mitre.org) · CC BY-NC-SA 4.0")
        st.caption("[GitHub](https://github.com/deanpeters/MITRE-ITK-Skills)")


def _render_provider_config():
    st.caption("**LLM provider**")

    provider = st.selectbox(
        "Provider",
        PROVIDERS,
        index=PROVIDERS.index(st.session_state.get("llm_provider", "Anthropic")),
        label_visibility="collapsed",
        key="_provider_select",
    )
    st.session_state.llm_provider = provider

    if provider == "Anthropic":
        model = st.selectbox("Model", ANTHROPIC_MODELS, key="_anthropic_model")
        st.session_state.llm_model = model
        if os.environ.get("ANTHROPIC_API_KEY"):
            st.success("ANTHROPIC_API_KEY detected")
        else:
            st.warning("Set ANTHROPIC_API_KEY in your environment")

    elif provider == "OpenAI":
        model = st.selectbox("Model", OPENAI_MODELS, key="_openai_model")
        st.session_state.llm_model = model
        if os.environ.get("OPENAI_API_KEY"):
            st.success("OPENAI_API_KEY detected")
        else:
            st.warning("Set OPENAI_API_KEY in your environment")

    elif provider == "Local model":
        base_url = st.text_input(
            "Base URL",
            value=st.session_state.get("llm_base_url", "http://localhost:11434/v1"),
            key="_local_url",
        )
        st.session_state.llm_base_url = base_url
        model = st.text_input(
            "Model name",
            placeholder="llama3.2",
            value=st.session_state.get("llm_model", ""),
            key="_local_model",
        )
        st.session_state.llm_model = model


# ---------------------------------------------------------------------------
# Page: Landing
# ---------------------------------------------------------------------------

def page_landing(skills):
    st.title("MITRE ITK Skills")
    st.markdown(
        "27 innovation and design-thinking tools from the "
        "[MITRE Innovation Toolkit](https://itk.mitre.org), "
        "adapted for product managers, product owners, and business analysts."
    )
    st.divider()

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.subheader("Help me pick a tool")
        st.caption("Answer a few questions and get a recommendation matched to your situation.")
        if st.button("Get a recommendation →", key="btn_adl", use_container_width=True, type="primary"):
            go("adl_step1")
            st.rerun()

    with col2:
        st.subheader("I know what I need")
        st.caption("Browse all 27 tools by phase and jump straight to the one you want.")
        if st.button("Browse tools →", key="btn_direct", use_container_width=True):
            go("direct_select")
            st.rerun()

    st.divider()
    st.caption(f"{len(skills)} tools loaded across 5 phases.")


# ---------------------------------------------------------------------------
# Page: ADL Step 1
# ---------------------------------------------------------------------------

def page_adl_step1():
    st.title("Where are you right now?")

    choice = st.radio(
        "Situation",
        ADL_STEP1_OPTIONS,
        index=None,
        label_visibility="collapsed",
    )

    col_back, col_next = st.columns([1, 5])
    with col_back:
        if st.button("← Back"):
            go("landing")
            st.rerun()
    with col_next:
        if st.button("Next →", type="primary", disabled=choice is None):
            idx = ADL_STEP1_OPTIONS.index(choice) + 1
            if idx == 7:
                go("direct_select")
            else:
                go("adl_step2", adl_step1=idx)
            st.rerun()


# ---------------------------------------------------------------------------
# Page: ADL Step 2
# ---------------------------------------------------------------------------

def page_adl_step2():
    step1 = st.session_state.get("adl_step1", 1)
    step1_label = ADL_STEP1_OPTIONS[step1 - 1].split(" — ")[0]

    st.title("What specifically do you need?")
    st.caption(f"Situation: {step1_label}")

    options = ADL_STEP2_OPTIONS.get(step1, [])
    choice = st.radio("Need", options, index=None, label_visibility="collapsed")

    col_back, col_next = st.columns([1, 5])
    with col_back:
        if st.button("← Back"):
            go("adl_step1")
            st.rerun()
    with col_next:
        if st.button("Next →", type="primary", disabled=choice is None):
            go("adl_step3", adl_step2=options.index(choice))
            st.rerun()


# ---------------------------------------------------------------------------
# Page: ADL Step 3
# ---------------------------------------------------------------------------

def page_adl_step3():
    step1 = st.session_state.get("adl_step1", 1)
    step2 = st.session_state.get("adl_step2", 0)
    step1_label = ADL_STEP1_OPTIONS[step1 - 1].split(" — ")[0]
    step2_options = ADL_STEP2_OPTIONS.get(step1, [])
    step2_label = step2_options[step2] if step2 < len(step2_options) else ""

    st.title("Quick constraints")
    st.caption(f"{step1_label} → {step2_label}")

    time_choice = st.radio(
        "Time available",
        ["Under 45 minutes", "45–90 minutes", "Multiple sessions are fine"],
        index=1,
    )
    group_choice = st.radio(
        "Group size",
        ["Solo or pair (1–3 people)", "Small team (4–8 people)", "Large group (9+ people)"],
        index=1,
    )

    col_back, col_next = st.columns([1, 5])
    with col_back:
        if st.button("← Back"):
            go("adl_step2")
            st.rerun()
    with col_next:
        if st.button("See recommendations →", type="primary"):
            go("adl_recommendation", adl_time=time_choice, adl_group=group_choice)
            st.rerun()


# ---------------------------------------------------------------------------
# Page: ADL Recommendation
# ---------------------------------------------------------------------------

def page_adl_recommendation(skills):
    step1 = st.session_state.get("adl_step1", 1)
    step2 = st.session_state.get("adl_step2", 0)
    time_pref = st.session_state.get("adl_time", "")

    recommended_slugs = ADL_RECOMMENDATIONS.get((step1, step2), [])
    tight_time = "Under 45" in time_pref

    st.title("Recommended tools")

    if not recommended_slugs:
        st.info("No exact match — browse all tools below.")
    else:
        rank_labels = ["Primary recommendation", "Also consider", "Or try"]
        for i, slug in enumerate(recommended_slugs[:3]):
            skill = skills.get(slug)
            if not skill:
                continue

            time_req = skill.get("time_required", "")
            time_minutes = int(re.search(r"\d+", time_req).group()) if re.search(r"\d+", time_req) else 0
            warn_time = tight_time and time_minutes > 45

            with st.container(border=True):
                st.caption(rank_labels[i] if i < len(rank_labels) else "Also consider")
                st.subheader(skill["display_name"])
                st.write(skill["description"])

                col_meta, col_btn = st.columns([3, 1])
                with col_meta:
                    st.caption(
                        f"Phase: {skill['phase'].upper()} · "
                        f"{skill['difficulty']} · "
                        f"{skill['group_size']} · "
                        f"{skill['time_required']}"
                    )
                    if warn_time:
                        st.warning(f"Typically needs {time_req} — may be tight for your window.")
                with col_btn:
                    btn_type = "primary" if i == 0 else "secondary"
                    if st.button("Run this →", key=f"rec_{slug}", type=btn_type):
                        go("skill_runner", selected_skill=slug)
                        st.rerun()

    st.divider()
    col_back, col_browse = st.columns(2)
    with col_back:
        if st.button("← Start over", use_container_width=True):
            reset()
            go("landing")
            st.rerun()
    with col_browse:
        if st.button("Browse all tools", use_container_width=True):
            go("direct_select")
            st.rerun()


# ---------------------------------------------------------------------------
# Page: Direct select
# ---------------------------------------------------------------------------

def page_direct_select(skills):
    st.title("Browse tools")

    phase_options = ["All phases"] + [p.upper() for p in PHASE_ORDER]
    phase_filter = st.selectbox("Filter by phase", phase_options)

    filtered = {
        slug: s for slug, s in skills.items()
        if phase_filter == "All phases" or s["phase"].upper() == phase_filter
    }

    if not filtered:
        st.info("No tools found.")
        return

    by_phase = {}
    for slug, skill in filtered.items():
        by_phase.setdefault(skill["phase"].upper(), []).append((slug, skill))

    for phase in [p.upper() for p in PHASE_ORDER]:
        if phase not in by_phase:
            continue
        st.subheader(phase)
        for slug, skill in sorted(by_phase[phase], key=lambda x: x[1]["display_name"]):
            with st.container(border=True):
                col_info, col_btn = st.columns([4, 1])
                with col_info:
                    st.markdown(f"**{skill['display_name']}**")
                    st.caption(skill["description"])
                    st.caption(
                        f"{skill['difficulty']} · "
                        f"{skill['group_size']} · "
                        f"{skill['time_required']}"
                    )
                with col_btn:
                    if st.button("Run →", key=f"direct_{slug}"):
                        go("skill_runner", selected_skill=slug)
                        st.rerun()

    if st.button("← Back"):
        go("landing")
        st.rerun()


# ---------------------------------------------------------------------------
# Page: Skill runner
# ---------------------------------------------------------------------------

def page_skill_runner(skills):
    slug = st.session_state.get("selected_skill")
    skill = skills.get(slug)

    if not skill:
        st.error("Skill not found.")
        if st.button("← Back"):
            go("landing")
            st.rerun()
        return

    st.title(skill["display_name"])
    st.caption(
        f"Phase: {skill['phase'].upper()} · "
        f"{skill['difficulty']} · "
        f"{skill['group_size']} · "
        f"{skill['time_required']}"
    )

    with st.expander("About this tool"):
        what = _extract_section(skill["content"], "What Is It")
        when = _extract_section(skill["content"], "When to Use It")
        if what:
            st.markdown("**What Is It**")
            st.markdown(what)
        if when:
            st.markdown("**When to Use It**")
            st.markdown(when)
        if skill.get("best_for"):
            st.markdown("**Best for:**")
            for item in skill["best_for"]:
                st.markdown(f"- {item}")

    st.divider()
    st.subheader("Set up your session")
    st.caption("The more context you provide, the more tailored the facilitation guide.")

    with st.form("session_form"):
        project = st.text_input(
            "Product or project",
            placeholder="e.g., DataBridge v2.0 — federal analytics platform",
        )
        goal = st.text_area(
            "What do you want to walk away with from this session?",
            placeholder=(
                "e.g., A prioritized shortlist of the 3 most critical stakeholder groups "
                "to engage before the discovery kickoff next week."
            ),
            height=100,
        )
        col_size, col_time = st.columns(2)
        with col_size:
            team_size = st.selectbox(
                "Team size",
                ["Solo or pair (1–3)", "Small team (4–8)", "Large group (9+)"],
                index=1,
            )
        with col_time:
            time_box = st.selectbox(
                "Time available",
                ["30 minutes", "45 minutes", "60 minutes", "90 minutes", "Multiple sessions"],
                index=2,
            )
        extra = st.text_area(
            "Anything else I should know? (optional)",
            placeholder=(
                "e.g., Government client, strict procurement rules. "
                "Several stakeholders are skeptical of the initiative."
            ),
            height=80,
        )
        submitted = st.form_submit_button("Generate facilitation guide →", type="primary")

    if submitted:
        config = get_llm_config()
        if not llm_ready(config):
            if is_deployed():
                st.error("Something went wrong — please try again later.")
            else:
                provider = config["provider"]
                if provider == "Anthropic":
                    st.error("ANTHROPIC_API_KEY not found. Set it in your environment and restart the app.")
                elif provider == "OpenAI":
                    st.error("OPENAI_API_KEY not found. Set it in your environment and restart the app.")
                else:
                    st.error("Enter a model name for your local endpoint.")
        elif not goal.strip():
            st.warning("Describe what you want to walk away with — that's how the guide gets tailored.")
        else:
            _run_session(skill, project, goal, team_size, time_box, extra, config)

    if st.button("← Pick a different tool"):
        go("landing")
        st.rerun()


def _run_session(skill, project, goal, team_size, time_box, extra, config):
    system = f"""You are an expert facilitator and product practitioner helping a team run the MITRE ITK "{skill['display_name']}" exercise.

Generate a tailored, ready-to-use facilitation guide for this specific session — not a generic description of the tool. The facilitator has already read the skill documentation. Optimize for what they actually need to run the session well given their context.

Full skill documentation for reference:

{skill['content']}"""

    context_lines = [
        f"- Product / project: {project or 'Not specified'}",
        f"- Session goal: {goal}",
        f"- Team size: {team_size}",
        f"- Time available: {time_box}",
    ]
    if extra.strip():
        context_lines.append(f"- Additional context: {extra.strip()}")

    user_msg = f"""I want to run a {skill['display_name']} session.

{chr(10).join(context_lines)}

Please generate a tailored facilitation guide structured as:

1. **Opening framing** — 1–2 sentences to read aloud that set context for the team, specific to our project and goal
2. **Step-by-step instructions** — adapted to our team size and time box; cut or compress steps that won't fit; flag which steps are highest-leverage if time is short
3. **Watch-outs for our situation** — 2–3 specific failure modes given what I've told you about our context, not generic warnings
4. **What "done" looks like** — the concrete deliverable or decision the team should be able to make at the end of this session

Be specific and direct. Optimize for someone running this in {time_box} with {team_size}."""

    st.divider()
    st.subheader("Facilitation guide")

    output = st.empty()
    text_so_far = ""

    with st.spinner("Generating..."):
        try:
            for chunk in stream_response(config, system, user_msg):
                text_so_far += chunk
                output.markdown(text_so_far)
        except anthropic.AuthenticationError:
            st.error("Anthropic authentication failed — check your API key in the sidebar.")
        except Exception as e:
            st.error(f"Error: {e}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    render_sidebar()

    if "page" not in st.session_state:
        st.session_state.page = "landing"

    skills = load_skills()
    page = st.session_state.page

    if page == "landing":
        page_landing(skills)
    elif page == "adl_step1":
        page_adl_step1()
    elif page == "adl_step2":
        page_adl_step2()
    elif page == "adl_step3":
        page_adl_step3()
    elif page == "adl_recommendation":
        page_adl_recommendation(skills)
    elif page == "direct_select":
        page_direct_select(skills)
    elif page == "skill_runner":
        page_skill_runner(skills)
    else:
        go("landing")
        st.rerun()


if __name__ == "__main__":
    main()
