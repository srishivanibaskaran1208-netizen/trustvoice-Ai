TrustVoice is an prototype for AI-Powered Real-Time Detection and Prevention of Voice Cloning Impersonation Attacks. It detects cloned/deepfake voices on calls, cross-checks the speaker's identity, reads intent from what's being said, fuses everything into a single risk score, and — for high-risk calls — automatically verifies with a trusted contact before any harm (like a money transfer) happens.

Risk Formula
Risk = 30% × Voice Authenticity
     + 20% × Speaker Mismatch
     + 25% × Intent Risk
     + 15% × Conversation Risk
     + 10% × Caller History
Score	Classification
0–30	SAFE
31–60	CAUTION
61–80	HIGH
81–100	CRITICAL
Demo Scenario

Caller says: "I'm in an emergency. Please send ₹20,000 immediately."

TrustVoice flags this as CRITICAL IMPERSONATION ATTACK — Risk 94/100, then automatically calls the trusted contact. The contact says the emergency isn't real → ATTACK PREVENTED.

Tech Stack
Layer	Technology
Frontend	React + Vite + Tailwind CSS + HTML (current build: static HTML/Tailwind CDN, pages listed below)
Backend	Python FastAPI (planned — see below)
Database	PostgreSQL (planned)
AI Layer	Modular mock AI now; swappable for real deepfake/speaker/Claude-powered models later
Project Structure
trustvoice/
├── index.html                → redirects to dashboard.html
├── dashboard.html            → KPIs, risk overview, recent calls
├── live-call.html            → live monitor, attack simulation, verification flow
├── trusted-contacts.html     → add / list / delete trusted contacts
├── history.html              → filterable call history
├── assets/
│   ├── theme.css             → shared dark-gold cybersecurity theme
│   └── api.js                → single point of contact with the backend
└── README.md
Pages

Dashboard — total calls, suspicious calls, critical attacks, risk score, voice authenticity, speaker similarity, intent risk, and a live recent-calls feed.

Live Detection — real-time call monitor with a "Run attack simulation" button that plays out the full pipeline end-to-end on the canonical demo scenario, ending in the verification flow.

Trusted Contacts — manage the people TrustVoice will call to independently verify a suspicious request.

Call History — every analyzed call, filterable by Suspicious / Critical.

Frontend ↔ Backend Wiring

All pages talk to the backend exclusively through assets/api.js (TV_API.getSummary(), getCalls(), getContacts(), addContact(), deleteContact(), runDemoAttack(), startVerification(), resolveVerification()).

Each call:

Tries the real API at API_BASE (default http://localhost:8000/api).
Falls back to built-in mock data if the backend isn't reachable.

No frontend code changes are needed once the backend is live — it just starts returning real data instead of mocks.

Expected API contract
Method	Path	Purpose
GET	/api/dashboard/summary	Dashboard KPI tiles
GET	/api/calls?limit=N	Recent / historical calls
GET	/api/calls/:id	Single call detail
GET	/api/contacts	List trusted contacts
POST	/api/contacts	Add a trusted contact
DELETE	/api/contacts/:id	Remove a trusted contact
POST	/api/analysis/demo	Run the detection pipeline on the demo scenario
POST	/api/verification/start	Kick off trusted-contact verification
POST	/api/verification/:id/resolve	Record the contact's YES/NO
Planned Backend (Not Yet Built)
FastAPI service implementing: Authentication, Trusted Contacts, Voice Enrollment, Audio Analysis, Risk Calculation, Call History, Verification.
PostgreSQL tables: users, trusted_contacts, voice_profiles, calls, detection_results, verification_requests.
Mock AI first — every detection module (deepfake, speaker match, intent, STT) starts as a mock/rule-based function returning realistic scores, so the whole prototype runs with no GPU. Each module is isolated behind an interface so a real model (or a Claude-based call) can replace the mock without touching the rest of the pipeline.
Running It Now

No build step required — it's static HTML/CSS/JS.

cd trustvoice
python -m http.server 5500

Or just double-click dashboard.html.

Once the FastAPI backend is running on port 8000 with the routes above, everything switches to live data automatically.
