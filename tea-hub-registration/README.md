# TEA HUB registration site

A minimal Streamlit registration website for **TEA HUB — Ignite Tea Makers**. It includes the supplied Ignite Tea Makers logo, a live deadline countdown, a single name field, and the requested success confirmation.

## Run locally

```powershell
cd tea-hub-registration
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Deploy

1. Push this folder to a GitHub repository.
2. Create a new app in Streamlit Community Cloud and select `app.py` as the entry point.
3. Deploy. No secrets or configuration are required.

The app records registrations in `data/registrations.db`. This works on a single host with persistent storage. Streamlit Community Cloud has an ephemeral local filesystem, so use a persistent host (or replace the small SQLite storage functions in `app.py` with a hosted database) if registrations must survive redeploys and restarts.

## Deadline

The deadline is set to **12 October 2026, 12:00 AM Asia/Kolkata** in `app.py`. Change `EVENT_DEADLINE` if the required date or timezone changes.
