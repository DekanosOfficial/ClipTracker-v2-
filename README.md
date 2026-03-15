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
│   ├── app.py			 ← Flask backend (your server)
│   └── requirements.txt       ← optional but good practice
│
└── mobile/
    ├── node_modules/          ← auto-created by Expo
    ├── assets/
    ├── App.js                 ← your mobile app goes here (React Native mobile app)
    ├── app.json
    └── package.json
```
