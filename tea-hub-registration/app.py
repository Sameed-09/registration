"""TEA HUB registration page, ready to run with Streamlit."""

from __future__ import annotations

import sqlite3
import uuid
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import streamlit as st
import streamlit.components.v1 as components
from PIL import Image


APP_DIR = Path(__file__).parent
LOGO_PATH = APP_DIR / "assets" / "ignite.png"
DATABASE_PATH = APP_DIR / "data" / "registrations.db"
EVENT_DEADLINE = datetime(2026, 10, 13, 0, 0, tzinfo=ZoneInfo("Asia/Kolkata"))


def initialise_database() -> None:
    """Create the local registration store if it does not already exist."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS registrations (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                registered_at TEXT NOT NULL
            )
            """
        )


def save_registration(name: str) -> None:
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            "INSERT INTO registrations (id, name, registered_at) VALUES (?, ?, ?)",
            (
                uuid.uuid4().hex,
                name,
                datetime.now(ZoneInfo("Asia/Kolkata")).isoformat(),
            ),
        )


def registration_closed() -> bool:
    return datetime.now(ZoneInfo("Asia/Kolkata")) >= EVENT_DEADLINE


def render_countdown() -> None:
    """Show a browser-updating countdown without an extra package."""
    deadline_utc = EVENT_DEADLINE.astimezone(ZoneInfo("UTC")).strftime("%Y-%m-%dT%H:%M:%SZ")
    components.html(
        f"""
        <style>
          * {{ box-sizing: border-box; }}
          body {{ margin: 0; background: transparent; font-family: Arial, sans-serif; }}
          .countdown {{
            display: flex; justify-content: center; gap: 10px; text-align: center;
          }}
          .unit {{
            width: 78px; padding: 12px 5px; border: 1px solid #f1c9a3;
            border-radius: 10px; background: #fffaf5;
          }}
          .number {{ display: block; color: #7e121b; font-size: 1.6rem; font-weight: 800; line-height: 1; }}
          .label {{ display: block; margin-top: 6px; color: #6b5b51; font-size: .66rem; letter-spacing: .09em; text-transform: uppercase; }}
          #closed {{ display: none; color: #7e121b; font-weight: 700; text-align: center; padding-top: 20px; }}
        </style>
        <div class="countdown" id="countdown">
          <div class="unit"><span class="number" id="days">00</span><span class="label">Days</span></div>
          <div class="unit"><span class="number" id="hours">00</span><span class="label">Hours</span></div>
          <div class="unit"><span class="number" id="minutes">00</span><span class="label">Minutes</span></div>
          <div class="unit"><span class="number" id="seconds">00</span><span class="label">Seconds</span></div>
        </div>
        <div id="closed">Registration is now closed.</div>
        <script>
          const deadline = new Date("{deadline_utc}").getTime();
          const clock = document.getElementById("countdown");
          const closed = document.getElementById("closed");
          const pad = value => String(value).padStart(2, "0");
          function updateClock() {{
            let remaining = deadline - Date.now();
            if (remaining <= 0) {{
              clock.style.display = "none";
              closed.style.display = "block";
              return;
            }}
            const days = Math.floor(remaining / 86400000);
            remaining %= 86400000;
            const hours = Math.floor(remaining / 3600000);
            remaining %= 3600000;
            const minutes = Math.floor(remaining / 60000);
            const seconds = Math.floor((remaining % 60000) / 1000);
            document.getElementById("days").textContent = pad(days);
            document.getElementById("hours").textContent = pad(hours);
            document.getElementById("minutes").textContent = pad(minutes);
            document.getElementById("seconds").textContent = pad(seconds);
          }}
          updateClock();
          setInterval(updateClock, 1000);
        </script>
        """,
        height=100,
        scrolling=False,
    )


def add_style() -> None:
    st.markdown(
        """
        <style>
          .stApp { background: #f5efe7; color: #2f2019; }
          header[data-testid="stHeader"] { background: transparent; }
          #MainMenu, footer { visibility: hidden; }
          .block-container { max-width: 860px; padding-top: 2.4rem; padding-bottom: 3rem; }
          .brand { text-align: center; margin-top: -.5rem; }
          .brand h1 { color: #7e121b; font-family: Georgia, serif; font-size: 2.5rem; letter-spacing: .05em; margin: .45rem 0 .25rem; }
          .brand p { color: #5d4434; font-size: 1.05rem; letter-spacing: .11em; text-transform: uppercase; margin: 0; }
          .deadline { text-align: center; color: #6b5b51; font-size: .87rem; letter-spacing: .04em; margin-top: 1.65rem; }
          .form-title { color: #7e121b; font-family: Georgia, serif; text-align: center; font-size: 1.6rem; margin: .75rem 0 .1rem; }
          .form-caption { text-align: center; color: #6b5b51; margin-bottom: .9rem; }
          div[data-testid="stForm"] { background: #fffdf9; border: 1px solid #ead8c5; border-radius: 16px; padding: 1.35rem 1.5rem .45rem; box-shadow: 0 10px 24px rgba(79, 40, 16, .08); }
          div[data-testid="stTextInput"] input { border-radius: 8px; border-color: #cbb9a9; }
          .stButton > button, .stFormSubmitButton > button { background: #7e121b; border: 1px solid #7e121b; color: white; border-radius: 8px; font-weight: 700; letter-spacing: .02em; }
          .stButton > button:hover, .stFormSubmitButton > button:hover { background: #a11e28; border-color: #a11e28; color: white; }
          .legal { text-align: center; color: #806f62; font-size: .76rem; margin-top: 1rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    logo = Image.open(LOGO_PATH)
    st.set_page_config(page_title="TEA HUB | Ignite Tea Makers", page_icon=logo, layout="centered")
    initialise_database()
    add_style()

    image_column = st.columns([1, 2, 1])[1]
    with image_column:
        st.image(logo, use_container_width=True)
    st.markdown(
        """
        <div class="brand">
          <h1>TEA HUB</h1>
          <p>Ignite Tea Makers</p>
        </div>
        <p class="deadline">Registration closes on 13 October 2026 at 12:00 AM</p>
        """,
        unsafe_allow_html=True,
    )
    render_countdown()

    if registration_closed():
        st.warning("Registration is closed. Thank you for your interest in TEA HUB.")
        return

    st.markdown('<div class="form-title">Register for TEA HUB</div>', unsafe_allow_html=True)
    st.markdown('<div class="form-caption">Please enter your name to secure your registration.</div>', unsafe_allow_html=True)
    with st.form("tea_hub_registration", clear_on_submit=True):
        name = st.text_input("Name", placeholder="Enter your full name", max_chars=100)
        submitted = st.form_submit_button("Register", type="primary", use_container_width=True)

    if submitted:
        cleaned_name = name.strip()
        if len(cleaned_name) < 2:
            st.error("Please enter your name to continue.")
        else:
            save_registration(cleaned_name)
            st.success("Congrats, your registration for TEA HUB is successful.")

    st.markdown('<p class="legal">TEA HUB — Ignite Tea Makers</p>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
