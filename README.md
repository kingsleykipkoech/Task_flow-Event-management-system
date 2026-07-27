# 📅 TaskFlow Planner

**TaskFlow Planner** is a lightweight, high-performance command-line (CLI) event scheduling and task management system built with Python and backed by a cloud-hosted **Aiven MySQL** database infrastructure. 

Developed as part of the **Introduction to Python Programming and Databases** summative project at African Leadership University (ALU).

---

## 👥 Group 23 Team Members

* **Lilian Kamikazi**
* **Vanessa Kampiire**
* **Gabriel Agaba**
* **Rita Akariza**
* **Kingsley Kipkoech**
* **Felix Mwaniki**

---

## ✨ Key Features

1. **🔒 Role-Based Access Control**:
   - **Planner Role**: Full permissions to create, edit, delete, and import events.
   - **Viewer Role**: Read-only permissions restricted to viewing calendars and searching events.

2. **👤 Dynamic Identity & User Management**:
   - Switch active user profiles on the fly or add/delete members dynamically at runtime.

3. **📁 Category Management**:
   - Organize commitments by **Classes**, **Assignments**, **Personal**, **Others**, and imported `.ics` events.

4. **⏱️ Strict Validation & Dynamic Status Engine**:
   - Enforces valid `YYYY-MM-DD` date and `HH:MM` / `ALL DAY` time formats.
   - Dynamic real-time status calculation:
     - `PENDING`: Scheduled for a future date.
     - `ONGOING`: Scheduled for today.
     - `DUE`: Date has passed and task is incomplete.
     - `DONE`: Manually marked as completed by user.

5. **📅 Terminal Monthly Calendar Grid**:
   - Generates a 7-column monthly matrix directly in the CLI terminal, highlighting current day `[DD]`.
   - Filter schedules by individual group members.

6. **📥 Google & Outlook `.ics` Calendar Import**:
   - Parses exported `.ics` calendar files, extracting `SUMMARY` and `DTSTART` fields to populate MySQL database records automatically under the `Imports` category.

7. **🔔 Non-Blocking Background Reminder Engine**:
   - Fires native desktop notifications (`notify-send` / `win10toast`) upon login.
   - A non-blocking background daemon thread (`daemon=True`) polls MySQL every 60 seconds.
   - Automatically sends formatted SMTP emails **1 hour** and **30 minutes** before event start times to assigned attendees.

---

## 🛠️ Infrastructure & Tech Stack

* **Language**: Python 3
* **Database**: MySQL (Hosted on Aiven Cloud MySQL)
* **Database Connector**: `mysql-connector-python`
* **Protocols**: SMTP over TLS (Port 587) for email delivery
* **OS Support**: Cross-platform (Linux & Windows)

---

## 📁 Repository Structure

```text
├── taskflow.py       # Main CLI application entry point & 6 module implementations
├── connection.py     # Procedural MySQL database manager & migration engine
├── databse.sql       # MySQL table schema definitions
├── .email_config     # Config file for SMTP email credentials (auto-generated)
└── README.md         # Documentation & setup guide
