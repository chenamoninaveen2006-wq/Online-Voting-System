# Elections — Original Design + Flask/SQLite demo

This project uses the uploaded `online_voting_system_camera_fixed.html` as its template, preserving its visual layout, colors, camera flow, candidate cards, and admin screens. The existing demo state store is redirected to Flask endpoints backed by SQLite so state persists beyond browser-only localStorage.

## Run on Windows / VS Code

1. Extract the ZIP and open the extracted `online_voting_original` folder in VS Code.
2. Open Terminal → New Terminal.
3. Run:

```powershell
py -m pip install -r requirements.txt
py app.py
```

4. Keep the terminal open and visit **http://127.0.0.1:5000**. Do not use Live Server port 5500 for this Flask version.

Admin demo login in the original design: `admin` / `admin123`.

## Important limitations

This preserves and persists the original front-end demo, but its voter OTP generation, camera/face checks, and vote decisions still run in browser JavaScript. The SQLite key-value endpoint is for local demonstration and is not a secure election backend. Do not enter real Aadhaar details, use real voter data, expose this app to the internet, or use it for an actual election. A production-quality backend would need server-side OTP validation, server-side vote validation and uniqueness constraints, authentication, authorization, rate limiting, CSRF protection, audit logging, and privacy/security review.
