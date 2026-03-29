# 🏥 MedConnect | The Clinical Emergency Infrastructure (v2.1)

**MedConnect** is a professional-grade, high-trust emergency healthcare platform designed to bridge the gap between patients and hospitals with clinical precision. This project moves beyond a simple "SOS app" into a full-scale clinical dispatch system with strict data protocols, real-time logistics, and HIPAA-compliant privacy layers.

---

### ⚡ Emergency Lifecycle & Logic Thresholds

Our system operates on a unique **Radially Expanding Dispatch (RED)** logic to ensure the fastest possible response times while optimizing hospital workload.

#### 1. SOS Radius Expansion Logic
When a user triggers an SOS, the backend does not ping every hospital in the database. Instead, it expands the search radius based on time elapsed to find the *closest* available care first:

| Time Elapsed | Search Radius | Clinical Priority |
| :--- | :--- | :--- |
| **0 - 5 Seconds** | **3 KM** | Primary Immediate Responders |
| **5 - 10 Seconds** | **6 KM** | Local Emergency Centers |
| **10 - 15 Seconds** | **9 KM** | Regional Hospitals |
| **15 - 20 Seconds** | **12 KM** | Specialized Trauma Centers |
| **> 20 Seconds** | **15 KM** (Max) | Wide-Net Emergency Broadcast |

#### 2. SOS State Machine
The system maintains a strict state machine to prevent data collisions:
*   **`SEARCHING`**: Rebroadcasts to hospitals within the current radius. User is locked from creating new requests.
*   **`ASSIGNED`**: A hospital has accepted. Private medical data (EHR) is decrypted/revealed to the specific provider.
*   **`RESOLVED`**: The clinical case is closed. The SOS is archived in the user's `Alert History`.

---

### 🛡️ Data Privacy & Compliance (HIPAA/ABDM)

MedConnect implements a **"Zero-Knowledge Dispatch"** protocol to protect Patient Identifiable Information (PII) during the critical search phase.

*   **Identity Masking**: While an SOS is in `SEARCHING` status, hospitals see the patient as **"Identity Protected (HIPAA)"** and the phone number is **"Hidden for Privacy"**.
*   **Selective Disclosure**: Full name, blood group, allergies, and contact details are **only revealed** to a hospital *after* they formally click "Accept Request," creating a legal audit trail.
*   **EHR Integrity**: Medical records (Allergies, Chronic Conditions) are stored in a structured format ready for ABDM (Ayushman Bharat Digital Mission) integration.

---

### 🚑 Key Features

#### 1. Patient Portal (Individual Hub)
*   **Real-time SOS Dispatch**: One-tap emergency activation that pings the nearest capable medical facilities.
*   **Digital Health Records (EHR)**: Secure storage for critical medical history, blood type, allergies, and chronic conditions.
*   **Emergency Circle**: Management of primary and secondary emergency contacts for automated notifications.
*   **Third-Party Victim Reporting**: Users can report emergencies for others (e.g., a witness at a crash site) using the `is_for_self` toggle.

#### 2. Hospital Portal (Clinical Command Center)
*   **Live SOS Dashboard**: Real-time ticker of inbound emergency requests with distance and estimated arrival times.
*   **Accepted Patient Profile**: Reveals critical EHR context (blood type, allergies) only after a formal dispatch acceptance.
*   **Dispatch History**: Real-time log of managed emergencies for clinical auditing.
*   **Emergency Lifecycle Management**: Includes the "Resolve" state to formally close emergency cases after stabilization.
*   **Hospital Bed Management**: Real-time tracking of `Total Beds` vs. `ICU Beds`.

---

### 🎨 Design Philosophy
The platform utilizes a **Clinical Aesthetic** designed for high-stress environments:
*   **Typography**: Uses `Inter` for maximum legibility.
*   **Color Palette**: "Trust Blue" (#0284c7) and "Safe White" to reduce visual anxiety.
*   **Visual Polish**: 100px branding scale, smooth reveal animations, and optimized spatial density.

---

### 🛠️ Technical Stack

#### **Frontend**
*   **HTML5/CSS3**: Vanilla architecture for maximum performance and zero dependency overhead.
*   **JavaScript (ES6+)**: Handles real-time DOM updates and API interactions.
*   **Modern Web APIs**: Geolocation for tracking, Fetch for data sync.

#### **Backend (Django 5.1 + REST Framework)**
*   **Relational Mapping**: SQLite3 maintains complex relationships between `Users`, `Hospitals`, and `SOSRequests`.
*   **Real-time Layer**: `django-channels` provides the WebSocket infrastructure for the 15km broadcast net.
*   **Concurrency Control**: Uses atomic transactions to ensure data integrity during hospital acceptance.

---

### 📂 Project Structure

```text
├── root files           # Landing page (index.html), Hospitals, About, SOS
├── user/                # Patient Hub & EHR Management
├── hospital/            # Hospital Portal Dashboard
├── admin/               # Site Administration & Audit
├── medconnect_backend/  # Django Core API & Business Logic
├── css/                 # Global Clinical Design System
├── js/                  # Real-time Logic & Dispatch
├── images/              # Verified Clinical Assets
└── tmp/                 # Temporary logs and debug data
```

---

### 🚥 System Constants & Thresholds
*   **Max Active SOS**: 1 per user (prevents spam/confusion).
*   **Default Scale**: 1:1,000 (meters to KM conversion for radius logic).
*   **API Timeout**: 5000ms (configured for rapid failover).
*   **Regulatory Compliance**: National Telemedicine Practice Guidelines (2025).

---
*Created by Devansh Kalwani for the MedConnect-Emergency-Healthcare-System.*
