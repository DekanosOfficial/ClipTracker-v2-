# ClipTracker-v2-
# ClipTracker — Setup Guide

A barber loyalty tracker app. Flask backend + React Native (Expo) mobile frontend.

---

## How it works
- Barber adds customers by name & phone
- Every cut is logged with one tap
- 5th cut = 50% off, 10th cut = FREE — tracked automatically
- Cycle resets every 6 months per customer

---

## 1. Backend (Flask)

### Install dependencies
```bash
pip install flask flask-sqlalchemy flask-cors
```

### Run
```bash
python app.py
```

Flask will run on `http://localhost:5000`. The database (`ClipTracker.db`) is created automatically.

---

## 2. Mobile App (React Native + Expo)

### Install Expo CLI (once)
```bash
npm install -g expo-cli
```

### Create a new Expo project
```bash
npx create-expo-app ClipTracker
cd ClipTracker
```

### Replace App.js
Copy the provided `App.js` into the project root, replacing the default one.

### Install dependencies
```bash
npx expo install react-native-safe-area-context react-native-screens
```

### Set your IP address
Open `App.js` and update line 13:
```js
const API_BASE = "http://YOUR_COMPUTER_IP:5000";
```

To find your IP:
- **Windows**: Run `ipconfig` in terminal → look for IPv4 Address
- **Mac/Linux**: Run `ifconfig` → look for `inet` under your Wi-Fi interface

Example: `const API_BASE = "http://192.168.1.42:5000";`

> ⚠️ Your phone and computer must be on the **same Wi-Fi network**.

### Run the app
```bash
npx expo start
```

Scan the QR code with:
- **Android**: Expo Go app (install from Play Store)
- **iPhone**: Camera app (install Expo Go from App Store)

---

## API Endpoints (reference)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dashboard` | Stats for dashboard |
| GET | `/api/customers` | All customers (supports `?search=`) |
| POST | `/api/customers` | Add customer |
| GET | `/api/customers/:id` | Get customer + visit history |
| PUT | `/api/customers/:id` | Edit customer |
| DELETE | `/api/customers/:id` | Delete customer |
| POST | `/api/customers/:id/visit` | Log a new cut |

---

## Loyalty Logic
- Visits 1–4: Normal cut
- Visit 5: **50% off**
- Visits 6–9: Normal cut
- Visit 10: **FREE** — cycle resets automatically
- If 6 months pass without completing a cycle — resets automatically

---

## Files
```
ClipTracker/
│
├── backend/
│   ├── venv/                  ← virtual env (don't touch)
│   ├── instance/
│   │   └── ClipTracker.db       ← auto-created by Flask
│   ├── models.py           ← database tables live here
│   ├── routes.py          ← API endpoints
│   ├── app.py			 ← Flask backend (the server)
│   ├── database.py       ← db initialization
│   └── requirements.txt       ← optional but good practice
│
└── mobile/
    ├── node_modules/          ← auto-created by Expo
    ├── assets/
    ├── App.js                 ← your mobile app goes here (React Native mobile app)
    ├── app.json
    └── package.json
```


## 3. Database

Your database has two tables:

---

**`customers`**
| Column | Type | Description |
|---|---|---|
| `id` | Integer | Unique ID, auto-assigned |
| `first_name` | String | Required |
| `last_name` | String | Optional |
| `phone_no` | String | Optional |
| `visit_count` | Integer | Cuts in current cycle (0–10) |
| `cycle_start_date` | DateTime | When the current 6-month cycle started |
| `last_visit_date` | DateTime | Date of most recent cut |
| `created_at` | DateTime | When the customer was added |

---

**`visits`**
| Column | Type | Description |
|---|---|---|
| `id` | Integer | Unique ID, auto-assigned |
| `customer_id` | Integer | Links to `customers.id` |
| `visited_at` | DateTime | When the cut happened |
| `discount_applied` | String | `"none"`, `"half_off"`, or `"free"` |
| `notes` | String | Optional notes |

---

**How they relate:**
- One customer → many visits (one-to-many)
- Every time you tap "Log New Cut", a new row is added to `visits` and `visit_count` in `customers` goes up by 1
- When `visit_count` hits 10 (free cut), it resets to 0 and `cycle_start_date` updates — starting a fresh cycle
- If 6 months pass since `cycle_start_date`, the count also resets automatically

---

SQLite stores all of this in a single file — `instance/clipcount.db` — which gets created automatically when you first run `python app.py`.
