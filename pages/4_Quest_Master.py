import streamlit as st

from logic import pending_tasks
from store import load_data, save_data
from ui import render_sidebar
from session_manager import (
    cleanup_expired_sessions,
    create_public_session_token,
    parse_public_session_token,
    validate_session,
)

st.set_page_config(page_title="Quest Master - Student Quest", layout="wide")

# Cleanup expired sessions
cleanup_expired_sessions()

# Restore session from URL params if needed
query_params = st.query_params
if "auth" in query_params:
    session_id = parse_public_session_token(query_params["auth"])
    username = validate_session(session_id)
    if username:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.session_id = session_id

# Check if user is logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("login.py")
    st.stop()

# Once logged in, ensure URL always has session_id for persistence across reloads
if st.session_state.get("session_id"):
    session_id = st.session_state.session_id
    auth_token = create_public_session_token(session_id)
    if query_params.get("auth") != auth_token:
        st.query_params["auth"] = auth_token

st.markdown(
    """
<style>
    :root {
        --qm-page-text: #1f2937;
        --qm-muted-text: #6b7280;
        --qm-card-bg: #f8f9fa;
        --qm-card-alt: #fff9e6;
        --qm-surface: #ffffff;
        --qm-border: #e5e7eb;
        --qm-soft-border: #d1d5db;
        --qm-progress-bg: #f0f2f6;
        --qm-small-bg: #fff9e6;
        --qm-big-bg: #f0e6ff;
        --qm-level-bg: #f3f4f6;
        --qm-level-current-bg: #fde68a;
    }

    @media (prefers-color-scheme: dark) {
        :root {
            --qm-page-text: #e5e7eb;
            --qm-muted-text: #cbd5e1;
            --qm-card-bg: #111827;
            --qm-card-alt: #1f2937;
            --qm-surface: #0f172a;
            --qm-border: #374151;
            --qm-soft-border: #4b5563;
            --qm-progress-bg: #1f2937;
            --qm-small-bg: #1a2234;
            --qm-big-bg: #221a34;
            --qm-level-bg: #1f2937;
            --qm-level-current-bg: #4338ca;
        }
    }

    .quest-header {
        padding: 1.25rem 1.5rem;
        border-radius: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff;
        margin-bottom: 1rem;
    }

    .quest-card {
        padding: 1rem 1rem 0.9rem 1rem;
        border-radius: 0.9rem;
        border: 1px solid var(--qm-border);
        color: var(--qm-page-text);
        background: var(--qm-card-bg);
    }

    .quest-card h4,
    .quest-card p,
    .quest-card li {
        color: inherit;
    }

    .quest-card ul {
        margin: 0.5rem 0 0 1.25rem;
    }

    .subtle {
        color: var(--qm-muted-text);
    }

    .card-title {
        margin-top: 0;
        color: var(--qm-page-text);
    }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="quest-header">
    <h1 style="margin: 0; font-size: 3em;"> Quest Master</h1>
    <p style="font-size: 1.1em; margin: 0.5rem 0 0 0;">Your Personal Achievement System</p>
</div>
""",
    unsafe_allow_html=True,
)


username = st.session_state.get("username")
data = load_data(username)
render_sidebar(data, active_page="Quest Master")
pending = pending_tasks(data)

st.markdown(
    f"""
<div class="quest-card" style="margin-bottom: 1rem; background: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%); color: white; border: none;">
    <div style="text-align: center;">
        <div style="font-size: 2.25rem;"></div>
        <div style="opacity: 0.9;">Total Coins</div>
        <div style="font-size: 2rem; font-weight: 700;">{int(data['coins'])}</div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    f"""
<div class="quest-card" style="margin-bottom: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none;">
    <div style="text-align: center;">
        <div style="font-size: 2.25rem;"></div>
        <div style="opacity: 0.9;">Current Level</div>
        <div style="font-size: 2rem; font-weight: 700;">Level {int(data['level'])}</div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    f"""
<div class="quest-card" style="margin-bottom: 1rem; background: linear-gradient(135deg, #10b981 0%, #0f766e 100%); color: white; border: none;">
    <div style="text-align: center;">
        <div style="font-size: 2.25rem;"></div>
        <div style="opacity: 0.9;">Active Quests</div>
        <div style="font-size: 2rem; font-weight: 700;">{len(pending)}</div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

st.divider()

st.markdown("###  How It Works")

how_it_works = st.columns(3)

with how_it_works[0]:
    st.markdown(
        """
        <div class="quest-card" style="background: var(--qm-progress-bg); border-left: 4px solid #22c55e;">
            <h4 style="margin-top: 0; color: #22c55e;">1️ Create Quests</h4>
            <p class="subtle">Go to the Tasks page and create tasks with priorities (High, Medium, Low).</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with how_it_works[1]:
    st.markdown(
        """
        <div class="quest-card" style="background: var(--qm-progress-bg); border-left: 4px solid #f59e0b;">
            <h4 style="margin-top: 0; color: #f59e0b;">2️ Complete Quests</h4>
            <p class="subtle">Finish your tasks and earn coins based on difficulty (15, 10, or 5).</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with how_it_works[2]:
    st.markdown(
        """
        <div class="quest-card" style="background: var(--qm-progress-bg); border-left: 4px solid #3b82f6;">
            <h4 style="margin-top: 0; color: #3b82f6;">3️ Level Up</h4>
            <p class="subtle">Earn enough coins to increase your level! Every 50 coins = +1 level.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

st.markdown("###  Reward Milestone Ideas")

rewards_grid = st.columns(2)

with rewards_grid[0]:
    st.markdown(
        """
        <div class="quest-card" style="background: var(--qm-small-bg); border-left: 4px solid #f59e0b;">
            <h4 class="card-title"> Small Rewards</h4>
            <ul>
                <li><strong>20 coins</strong> → Snack break </li>
                <li><strong>30 coins</strong> → 15 minutes gaming </li>
                <li><strong>40 coins</strong> → 30 minutes rest </li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with rewards_grid[1]:
    st.markdown(
        """
        <div class="quest-card" style="background: var(--qm-big-bg); border-left: 4px solid #8b5cf6;">
            <h4 class="card-title"> Big Rewards</h4>
            <ul>
                <li><strong>60 coins</strong> → One episode </li>
                <li><strong>100 coins</strong> → Weekend fun </li>
                <li><strong>150+ coins</strong> → Special treat </li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

st.markdown("###  Level Progression")

level_progress = {
    "Level 1": "0-50 coins",
    "Level 2": "50-100 coins",
    "Level 3": "100-150 coins",
    "Level 4": "150-200 coins",
    "Level 5": "200+ coins",
}

level_columns = st.columns(5)
for idx, (_, range_str) in enumerate(level_progress.items()):
    with level_columns[idx]:
        is_current = idx + 1 == int(data["level"])
        bg_color = "var(--qm-level-current-bg)" if is_current else "var(--qm-level-bg)"
        border_color = "#f59e0b" if is_current else "var(--qm-soft-border)"

        st.markdown(
            f"""
            <div class="quest-card" style="background: {bg_color}; border: 2px solid {border_color}; text-align: center;">
                <p style="font-size: 1.8em; margin: 0; font-weight: 700;">{idx + 1}</p>
                <p style="font-size: 0.85em; color: var(--qm-muted-text); margin: 0.35rem 0 0 0;">{range_str}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.divider()

st.markdown("###  Redeem Your Coins")

rewards = [
    {"name": " Snack Break", "cost": 20, "description": "Quick refreshment time"},
    {"name": " Gaming Session", "cost": 30, "description": "15 minutes gaming"},
    {"name": " Rest Time", "cost": 40, "description": "30 minutes rest/chill"},
    {"name": " Watch Episode", "cost": 60, "description": "One full episode"},
    {"name": " Weekend Fun", "cost": 100, "description": "Special weekend activity"},
    {"name": " Special Treat", "cost": 150, "description": "Something special!"},
]

reward_columns = st.columns(3)
for idx, reward in enumerate(rewards):
    col = reward_columns[idx % 3]
    with col:
        can_afford = int(data["coins"]) >= reward["cost"]
        border_color = "#22c55e" if can_afford else "var(--qm-soft-border)"
        reward_bg = "var(--qm-card-alt)" if reward["cost"] < 60 else "var(--qm-surface)"
        reward_text = "var(--qm-page-text)"
        reward_muted = "var(--qm-muted-text)"

        st.markdown(
            f"""
            <div class="quest-card" style="background: {reward_bg}; border: 2px solid {border_color}; text-align: center; color: {reward_text};">
                <h4 style="margin: 0 0 0.35rem 0; color: {reward_text};">{reward['name']}</h4>
                <p style="margin: 0.35rem 0; color: {reward_muted}; font-size: 0.9em;">{reward['description']}</p>
                <p style="font-size: 1.4em; font-weight: 700; color: #f59e0b; margin: 0.75rem 0 0 0;"> {reward['cost']} coins</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        button_label = (
            f" Redeem {reward['name']}"
            if can_afford
            else f" Need {reward['cost'] - int(data['coins'])} more"
        )

        if st.button(
            button_label,
            key=f"redeem_{reward['cost']}_{reward['name']}",
            disabled=not can_afford,
            use_container_width=True,
        ):
            data["coins"] -= reward["cost"]
            add_history_entry(
                data,
                "reward",
                "redeem",
                title=reward["name"].strip(),
                amount=reward["cost"],
                reward_name=reward["name"].strip(),
            )
            save_data(data, username)
            st.toast(f"Redeemed {reward['name'].strip()} for {reward['cost']} coins")
            st.success(f" Congratulations! You redeemed: {reward['name']}")
            st.balloons()
            st.rerun()
st.divider()

st.markdown("### Reward History")
reward_history = [item for item in data.get("history", []) if item.get("category") == "reward"]
if not reward_history:
    st.info("No reward redemptions yet.")
else:
    for entry in reward_history[:10]:
        title_text = entry.get("title", "Reward")
        amount_text = f" - {int(entry.get('amount', 0))} coins" if entry.get("amount") is not None else ""
        st.write(f"{entry.get('timestamp', '')} - Redeemed: {title_text}{amount_text}")