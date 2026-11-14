import streamlit as st
from datetime import date, time, timedelta
from demo_data import DEMO_BRIEFING, RECENT_BRIEFINGS

import os
from dotenv import load_dotenv
from tavily import TavilyClient
from google import genai
from google.genai import types

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

tavily_client = None

if TAVILY_API_KEY:
    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

gemini_client = None

if GEMINI_API_KEY:
    gemini_client = genai.Client(api_key=GEMINI_API_KEY,http_options=types.HttpOptions(timeout=60000))

st.set_page_config(page_title="MeetMind AI", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root { --bg:#0B1220; --panel:#111C30; --panel2:#16243B; --cyan:#22D3EE; --violet:#8B5CF6; --text:#F8FAFC; --muted:#9AAAC0; --green:#10B981; }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp { background: radial-gradient(circle at 80% 0%, rgba(34,211,238,.08), transparent 28%), var(--bg); color:var(--text); }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#0E192B,#0B1220); border-right:1px solid rgba(148,163,184,.13); }
[data-testid="stSidebar"] * { color:var(--text); }
h1,h2,h3 { font-family:'Space Grotesk',sans-serif !important; color:var(--text) !important; }
p, label, .stMarkdown { color:var(--text); }
small, .muted { color:var(--muted) !important; }
.block-container { padding-top:2rem; padding-bottom:3rem; max-width:1440px; }
div[data-testid="stMetric"] { background:linear-gradient(145deg,#14233A,#101B2D); border:1px solid rgba(148,163,184,.16); padding:18px 20px; border-radius:16px; }
div[data-testid="stMetricLabel"] { color:#9AAAC0; }
div[data-testid="stMetricValue"] { color:#F8FAFC; }
.stButton > button, .stDownloadButton > button { border-radius:10px; border:1px solid rgba(34,211,238,.35); background:linear-gradient(90deg,#0891B2,#0E7490); color:white; font-weight:700; min-height:42px; }
.stButton > button:hover, .stDownloadButton > button:hover { border-color:#22D3EE; color:white; background:#0E7490; }
div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea, div[data-testid="stDateInput"] input, div[data-testid="stTimeInput"] input, div[data-testid="stSelectbox"] div[role="combobox"] { background:#111C30; color:#F8FAFC; border:1px solid #2B3B54; border-radius:10px; }
hr { border-color:rgba(148,163,184,.16); }
.mm-card { background:linear-gradient(145deg,rgba(22,36,59,.96),rgba(17,28,48,.96)); border:1px solid rgba(148,163,184,.16); border-radius:16px; padding:20px; height:100%; }
.mm-kicker { color:#22D3EE; text-transform:uppercase; letter-spacing:.13em; font-size:.72rem; font-weight:700; }
.mm-muted { color:#9AAAC0; font-size:.9rem; }
.mm-pill { display:inline-block; padding:5px 10px; border-radius:999px; background:rgba(34,211,238,.10); color:#67E8F9; border:1px solid rgba(34,211,238,.22); font-size:.78rem; }
.mm-title { font-family:'Space Grotesk',sans-serif; font-size:2rem; font-weight:700; letter-spacing:-.04em; }
.mm-gradient { background:linear-gradient(90deg,#22D3EE,#A78BFA); -webkit-background-clip:text; color:transparent; }
[data-testid="stDataFrame"] { border:1px solid rgba(148,163,184,.15); border-radius:12px; }
/* Glassmorphism effect */
.stApp [data-testid="stVerticalBlock"] > div:has(.mm-card) {
    backdrop-filter: blur(18px);
}

.mm-card {
    background: rgba(255, 255, 255, 0.07);
    border: 1px solid rgba(255, 255, 255, 0.16);
    border-radius: 18px;
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
}

.stButton > button {
    border-radius: 12px;
    border: 1px solid rgba(34, 211, 238, 0.35);
    transition: all 0.3s ease;
}
/* Premium glassmorphism for all form elements */

.stApp [data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 255, 255, 0.055);
    border: 1px solid rgba(255, 255, 255, 0.16);
    border-radius: 18px;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.22);
}

/* Input fields */
/* Premium dark glass input fields */
.stApp input,
.stApp textarea,
.stApp [data-baseweb="select"] > div {
    background: rgba(17, 28, 55, 0.85) !important;
    color: #F8FAFC !important;
    border: 1px solid rgba(34, 211, 238, 0.35) !important;
    border-radius: 12px !important;
    box-shadow: inset 0 1px 8px rgba(0, 0, 0, 0.15);
}

.stApp input:focus,
.stApp textarea:focus {
    border-color: #22D3EE !important;
    box-shadow: 0 0 0 2px rgba(34, 211, 238, 0.2) !important;
}
/* Labels */
.stApp label {
    color: #E2E8F0 !important;
}

/* Glass buttons */
.stApp button {
    border-radius: 12px;
    transition: all 0.3s ease;
}
/* Premium cyan gradient buttons */
.stApp button[kind="primary"] {
    background: linear-gradient(135deg, #22D3EE, #3B82F6) !important;
    color: #081226 !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    padding: 12px 22px !important;
    transition: all 0.3s ease;
}

.stApp button[kind="primary"]:hover {
    background: linear-gradient(135deg, #67E8F9, #60A5FA) !important;
    transform: translateY(-2px);
    box-shadow: 0 5px 20px rgba(34, 211, 238, 0.3);
}
/* Unified dark navy form fields */
.stApp input,
.stApp textarea,
.stApp select,
.stApp [data-baseweb="select"] > div,
.stApp input[type="date"],
.stApp input[type="time"],
.stApp [data-testid="stDateInput"] input,
.stApp [data-testid="stTimeInput"] input {
    background-color: #111C36 !important;
    color: #F8FAFC !important;
    border: 1px solid rgba(34, 211, 238, 0.45) !important;
    border-radius: 12px !important;
    color-scheme: dark;
}

/* Dark navy date and time fields */
.stApp [data-testid="stDateInput"] input,
.stApp [data-testid="stTimeInput"] input,
.stApp input[type="date"],
.stApp input[type="time"] {
    background: #111C36 !important;
    background-color: #111C36 !important;
    color: #F8FAFC !important;
    border: 1px solid rgba(34, 211, 238, 0.45) !important;
    border-radius: 12px !important;
    color-scheme: dark !important;
}

/* Calendar and clock icons */
.stApp input[type="date"]::-webkit-calendar-picker-indicator,
.stApp input[type="time"]::-webkit-calendar-picker-indicator {
    filter: invert(1);
}

/* Fix date and time input backgrounds */
.stApp [data-testid="stDateInput"] div[data-baseweb="input"],
.stApp [data-testid="stTimeInput"] div[data-baseweb="input"] {
    background: #111C36 !important;
    background-color: #111C36 !important;
    border: 1px solid rgba(34, 211, 238, 0.45) !important;
    border-radius: 12px !important;
}

.stApp [data-testid="stDateInput"] input,
.stApp [data-testid="stTimeInput"] input {
    background: transparent !important;
    color: #F8FAFC !important;
    color-scheme: dark;
}

/* Improve placeholder readability */
.stApp input::placeholder,
.stApp textarea::placeholder {
    color: #AAB8D0 !important;
    opacity: 1 !important;
}

/* Dropdown options */
.stApp [role="option"] {
    background-color: #111C36 !important;
    color: #F8FAFC !important;
}
/* MeetMind AI - Submit Button */
.stApp [data-testid="stFormSubmitButton"] button {
    background: linear-gradient(135deg, #22D3EE, #3B82F6) !important;
    color: #081226 !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    min-height: 48px !important;
}

.stApp [data-testid="stFormSubmitButton"] button:hover {
    background: linear-gradient(135deg, #67E8F9, #60A5FA) !important;
    box-shadow: 0 5px 20px rgba(34, 211, 238, 0.3);
}
/* Fix Streamlit status messages */
.stApp [data-testid="stAlert"] {
    background: rgba(34, 211, 238, 0.10) !important;
    color: #F8FAFC !important;
    border: 1px solid rgba(34, 211, 238, 0.35) !important;
    border-radius: 12px !important;
}

/* Fix content containers */
.stApp [data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(17, 28, 55, 0.85) !important;
    border: 1px solid rgba(34, 211, 238, 0.25) !important;
    border-radius: 14px !important;
}

/* Fix text inside alerts */
.stApp [data-testid="stAlert"] p {
    color: #F8FAFC !important;
}

.stTextArea textarea {
    color: #FFFFFF !important;
    background-color: #111827 !important;
    -webkit-text-fill-color: #FFFFFF !important;
    caret-color: #FFFFFF !important;
}
</style>
""", unsafe_allow_html=True)

if "briefing" not in st.session_state:
    st.session_state.briefing = None
if "active_page" not in st.session_state:
    st.session_state.active_page = "Dashboard"

def open_briefings_page(item):
    st.session_state["selected_briefing"] = item
    st.session_state["pending_page"] = "My Briefings"

def go_to_new_research():
    st.session_state["pending_page"] = "New Research"

if "pending_page" in st.session_state:
    st.session_state["active_page"] = st.session_state.pop("pending_page")

with st.sidebar:
    engine_status = (
    "Tavily + Gemini connected"
    if tavily_client and gemini_client
    else "Partially connected"
    if tavily_client or gemini_client
    else "Demo mode"
    )
    st.markdown("<div style='display:flex;align-items:center;gap:10px;padding:8px 0 22px'><div style='font-size:30px'>🧠</div><div><div style='font-family:Space Grotesk;font-size:21px;font-weight:700'>MeetMind <span style='color:#22D3EE'>AI</span></div><div style='font-size:11px;color:#9AAAC0;letter-spacing:1px'>INTELLIGENCE WORKSPACE</div></div></div>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("WORKSPACE", ["Dashboard", "New Research", "My Briefings", "Evidence Explorer", "Settings"], key="active_page")
    st.markdown("---")
    st.markdown(f"<div class='mm-card'><div class='mm-kicker'>Research engine</div><p style='margin:8px 0 4px;font-weight:700'>{engine_status}</p><div class='mm-muted'>Connect Tavily + Bifrost after the UI review.</div></div>", unsafe_allow_html=True)
    st.caption("MeetMind AI · Prototype v0.1")

def header(kicker, title, subtitle):
    st.markdown(f"<div class='mm-kicker'>{kicker}</div><div class='mm-title'>{title}</div><p class='mm-muted'>{subtitle}</p>", unsafe_allow_html=True)

def card(title, body, tag=None):
    tag_html = f"<span class='mm-pill'>{tag}</span>" if tag else ""
    st.markdown(f"<div class='mm-card'>{tag_html}<h3 style='font-size:1.05rem;margin:12px 0 8px'>{title}</h3><div class='mm-muted'>{body}</div></div>", unsafe_allow_html=True)

if page == "Dashboard":
    header("YOUR RESEARCH WORKSPACE", "Prepare for every meeting with <span class='mm-gradient'>clarity.</span>", "Turn recent company developments into concise, source-backed meeting intelligence.")
    st.write("")
    a,b = st.columns([1.5,1])
    with a:
        st.markdown("<div class='mm-card'><div class='mm-kicker'>Start here</div><h2 style='margin:10px 0 6px'>What do you need to know before your next meeting?</h2><p class='mm-muted'>Research a company or person and generate a focused briefing from recent public information.</p></div>", unsafe_allow_html=True)
        st.button("+ Start new research", use_container_width=True, on_click=go_to_new_research)
    with b:
        st.markdown("<div class='mm-card'><div class='mm-kicker'>MeetMind workflow</div><p>① Meeting context</p><p>② Recent web research</p><p>③ AI analysis</p><p>④ Evidence-backed briefing</p><span class='mm-pill'>Tavily + Bifrost integration planned</span></div>", unsafe_allow_html=True)
    st.write("")
    st.markdown("### Workspace overview")
    m1,m2,m3 = st.columns(3)
    m1.metric("Briefings created", "04")
    m2.metric("Sources collected", "38")
    m3.metric("Research window", "30 days")
    st.markdown("### Recent briefings")
    for i, item in enumerate(RECENT_BRIEFINGS):
         with st.container(border=True):
            c1, c2, c3 = st.columns([3, 2, 1])
            c1.markdown(f"**{item['company']}**")
            c2.caption(f"{item['topic']} · {item['date']}")
            c3.button("View briefing", key=f"view_{i}", on_click=open_briefings_page, args=(item,))
                
elif page == "New Research":
    header("RESEARCH WORKFLOW", "New meeting research", "Add meeting context. MeetMind will use it to shape a focused briefing.")
    st.markdown("<div class='mm-card'><div class='mm-kicker'>Step 01 · Meeting context</div><p class='mm-muted'>Required: company or person and scheduled meeting time. Other details help tailor the research.</p></div>", unsafe_allow_html=True)
    with st.form("research_form"):
        col1,col2 = st.columns(2)
        with col1:
            company = st.text_input("Company or organisation *", placeholder="e.g. Microsoft")
            person = st.text_input("Person / meeting participant", placeholder="Optional")
            meeting_type = st.selectbox("Meeting type", ["Business discussion", "Job interview", "Partnership", "Investor meeting", "Sales meeting", "Other"])
        with col2:
            meeting_date = st.date_input("Meeting date", value=date.today()+timedelta(days=2))
            meeting_time = st.time_input("Meeting time", value=time(10,0))
            objective = st.text_input("Meeting objective", placeholder="e.g. Explore a technology partnership")
        notes = st.text_area("Additional context", placeholder="What would you particularly like to understand before the meeting?", height=100)
        submitted = st.form_submit_button("Generate briefing preview", use_container_width=True)

    if submitted:
        if not company.strip():
            st.error("Please enter a company or organisation.")
        else:
            st.session_state.briefing = {
                "company": company.strip(),
                "person": person.strip(),
                "meeting_type": meeting_type,
                "meeting_date": meeting_date.strftime("%d %b %Y"),
                "meeting_time": meeting_time.strftime("%I:%M %p"),
                "objective": objective.strip(),
                "notes": notes.strip()
            }

            briefing = st.session_state.briefing
            generated_text = ""

            st.success("Meeting context saved successfully!")

            st.markdown("---")
            header(
                "AI RESEARCH PREVIEW",
                "Your Meeting Briefing",
                "A structured preparation workspace for your upcoming meeting."
            )

            st.markdown(f"""
            <div class="mm-cards">
                <div class="mm-kicker">MEETING OVERVIEW</div>
                <h3>{briefing['company']}</h3>
                <p><b>Participant:</b> {briefing['person'] or 'Not specified'}</p>
                <p><b>Meeting type:</b> {briefing['meeting_type']}</p>
                <p><b>Date:</b> {briefing['meeting_date']}</p>
                <p><b>Time:</b> {briefing['meeting_time']}</p>
                <p><b>Objective:</b> {briefing['objective'] or 'Not specified'}</p>
            </div>
            """, unsafe_allow_html=True)

            results = []

            # 1. Fetch research using Tavily first
            st.markdown("### Research Findings")

            if tavily_client:
                try:
                    research_query = (
                        f"Research {briefing['company']} specifically. "
                        f"Meeting objective: {briefing['objective']}. "
                        f"Find recent company news, products, services, "
                        f"AI developments, business strategy, partnerships, "
                        f"and information directly relevant to this meeting. "
                        f"Additional context: {briefing['notes']}. "
                        f"Exclude unrelated companies and irrelevant results."
                    )

                    with st.spinner("Researching with Tavily..."):
                        tavily_response = tavily_client.search(
                            research_query,
                            search_depth="advanced",
                            max_results=5
                        )

                    results = tavily_response.get("results", [])

                except Exception as e:
                    st.error(f"Research error: {e}")
            else:
                st.warning(
                    "Tavily API key not found. "
                    "Please check your .env file."
                )

                        
            briefing["sources"] = [
                 {
                    "title": result.get("title", "Untitled source"),
                    "url": result.get("url", "")
                    }
                    for result in results
                    if result.get("url")
                    ]
           
            # 2. Prepare research context for Gemini

            if results:
                summary_text = "\n\n".join(
                    f"Source: {result.get('title', 'Untitled')}\n"
                    f"URL: {result.get('url', 'Not available')}\n"
                    f"Content: {result.get('content', '')[:1800]}"
                    for result in results[:5]
                )
            else:
                summary_text = (
                    "No live research sources were retrieved. "
                    "Do not invent company developments or present "
                    "unverified information as fact."
                )

            # 3. Generate Executive Summary using Gemini
            st.markdown("### Generated Briefing")

            if not gemini_client:
                st.warning(
                    "Gemini API key not found. "
                    "Please check GEMINI_API_KEY in your .env file."
                )

            else:
                generated_text = ""
                try:
                    prompt = f"""
                    You are MeetMind AI, a professional meeting research assistant.
                    Prepare a concise, useful meeting briefing using the information below.
                    COMPANY: {briefing['company']}
                    PARTICIPANT: {briefing['person'] or 'Not specified'}
                    MEETING TYPE: {briefing['meeting_type']}
                    MEETING OBJECTIVE: {briefing['objective'] or 'Not specified'}
                    ADDITIONAL CONTEXT: {briefing['notes'] or 'None provided'}
                    RESEARCH SOURCES:
                    {summary_text}
                    Create these sections:
                    1. Executive Summary
                    Summarise the most important verified developments relevant to
                    this meeting.
                    2. Important Business Developments
                    Explain the key developments and why they matter.
                    3. Five Useful Meeting QuestionsSuggest five specific questions aligned with the meeting objective.
                    4. Potential Partnership Opportunities
                    Suggest realistic opportunities, clearly labelled as suggestions.
                    IMPORTANT RULES:
                    - Use only information supported by the supplied research.
                    - Do not invent facts, dates, statistics, or announcements.
                    - Distinguish verified information from your own suggestions.
                    - Mention source titles when discussing factual developments.
                    - If research is unavailable, clearly state that limitation.
                    - Use professional headings and concise bullet points.
                    """

                    with st.spinner("Generating briefing with Gemini..."):
                        gemini_response = gemini_client.models.generate_content(
                            model="gemini-3.8-flash",
                            contents=prompt
                        )

                    generated_text = (
                        gemini_response.text.strip()
                        if gemini_response.text
                        else ""
                    )

                    if generated_text:
                        st.text_area("Generated Briefing", value=generated_text, height=300)
                    else:
                        st.warning(
                            "Gemini returned an empty response. "
                            "Please try generating the briefing again."
                        )

                except Exception as e:
                    st.error(f"Gemini generation error: {e}")


            # 4. Key Discussion Points
                    st.markdown("### Key Discussion Points")
                    st.markdown("""
                    - Understand the organisation's background.
                    - Identify relevant business developments.
                    - Prepare questions aligned with the meeting objective.
                    - Explore potential partnership opportunties based on verifed information.""")

            # 5. Display research results
            if results:
                for i, result in enumerate(results, 1):
                    st.markdown(
                        f"**{i}. {result.get('title', 'Untitled source')}**"
                    )

                    content = result.get("content", "").strip()
                    st.write(
                        content[:1200] + "..."
                        if len(content) > 1200 else content
                    )

                    st.markdown(
                        f"[Read source]({result.get('url', '#')})"
                    )
                    st.divider()
            else:
                st.info("No research results found.")

            # 6. Sources and References
            st.markdown("### Sources & References")

            if results:
                for i, result in enumerate(results, 1):
                    st.markdown(
                        f"**{i}. {result.get('title', 'Untitled source')}**"
                    )
                    st.caption(result.get("url", ""))
                    st.markdown(
                        f"[Open source]({result.get('url', '#')})"
                    )
            else:
                st.info("No source references available yet.")

            # Save generated briefing
            briefing["briefing"] = generated_text

            briefing["sources"] = [
                {
                    "title": result.get("title", "Untitled source"),
                    "url": result.get("url", "")
                }
                for result in results
                if result.get("url")
            ]

            st.session_state["selected_briefing"] = briefing    
            
elif page == "My Briefings":
    header(
        "YOUR LIBRARY",
        "My Briefings",
        "View your meeting preparation and research sources."
    )

    selected = st.session_state.get("selected_briefing")

    if selected:
        st.markdown("### Selected Briefing")

        with st.container(border=True):
            st.subheader(selected.get("company", "Company"))
            st.write(f"**Topic:** {selected.get('topic') or selected.get('objective') or 'Not available'}")
            st.write(f"**Date:** {selected.get('date') or selected.get('meeting_date') or 'Not available'}")

        st.markdown("### Generated Briefing")
        briefing = selected.get("briefing", "")
        if briefing:
            st.text_area("Generated Briefing", height=400, value=briefing, key="generated_briefing", disabled=True)
        else:
            st.info("No AI-generated briefing saved for this briefing yet.")

        st.markdown("### Sources & References")
        sources = selected.get("sources", [])
        if sources:
            for i, source in enumerate(sources, 1):
                st.markdown(f"**{i}. {source.get('title', 'Source')}**")
                st.caption(source.get("url", ""))
                if source.get("url"):
                    st.markdown(f"[Open reference]({source['url']})")
        else:
            st.info("No reference links are saved for this briefing yet.")

        if st.button("Back to Dashboard"):
            st.session_state["pending_page"] = "Dashboard"
            st.rerun()

    else:
        st.info("Select View Briefing from the Dashboard to open a briefing.")

    st.markdown("---")
    st.markdown("### All Recent Briefings")

    for item in RECENT_BRIEFINGS:
        with st.container(border=True):
            st.markdown(f"**{item['company']}**")
            st.caption(f"{item['topic']} · {item['date']}")
        

elif page == "Evidence Explorer":
    header("SOURCE TRANSPARENCY", "Evidence explorer", "Inspect source details, publication dates and the claims they support.")
    selected = st.session_state.get("selected_briefing")

    if selected:
        sources = selected.get("sources", [])

        if sources:
            for i, source in enumerate(sources, 1):
                with st.container(border=True):
                    st.markdown(
                        f"**{i}. {source.get('title', 'Untitled source')}**"
                    )

                    published = (
                        source.get("published_date")
                        or source.get("published")
                        or source.get("date")
                        or "Date not provided"
                    )
                    st.caption(f"Publication date: {published}")

                    url = source.get("url", "")
                    if url:
                        st.markdown(f"[Open source]({url})")

                    content = source.get("content", "")
                    if content:
                        st.write(content[:800])
        else:
            st.info("No research sources are saved for this briefing yet.")
    else:
        st.info("Open a briefing from My Briefings to explore its sources.")

elif page == "Settings":
    header("PREFERENCES", "Settings", "Configure your MeetMind AI workspace.")
    card("Appearance", "Midnight Intelligence · Dark Navy, Cyan and Violet", "Current theme")
    card("Research window", "Previous 30 days, based on source publication dates where available.", "Default")
    card(
        "Integrations",
        f"Tavily: {'Connected' if tavily_client else 'Not connected'} | "
        f"Gemini: {'Connected' if gemini_client else 'Not connected'}",
        "Connected" if tavily_client and gemini_client
        else "Partially connected" if tavily_client or gemini_client
        else "Not connected"
    )
    st.markdown("### Prototype status")
    st.write("MeetMind AI prototype. Tavily provides web research and Gemini generates AI-powered meeting briefings. Authentication and persistent storage are not yet enabled.")

st.markdown("---")
st.write("Tavily client:", bool(tavily_client))
st.write("Gemini client:", bool(gemini_client))

st.markdown(
    f"""
    <div class='mm-card'>
    <div class='mm-kicker'>Research engine</div>
    <p style='margin:8px 0 4px;font-weight:700'>
    {engine_status}
    </p>
    <div class='mm-muted'>
    Live research and AI briefing status.
    </div>
    </div>
    """,
     unsafe_allow_html=True
    )