# 🔐 Credential Rotation Tracker (CLI)
![Python](https://img.shields.io/badge/python-3.x-blue)
![CLI Tool](https://img.shields.io/badge/type-CLI-lightgrey)
![Status](https://img.shields.io/badge/status-stable-green)
![License](https://img.shields.io/badge/license-MIT-black)


A lightweight CLI tool to make credential rotation risk visible.

This tool tracks when credentials were last rotated, calculates when they should be rotated again, and clearly highlights overdue and high-risk credentials — without storing secrets or adding infrastructure.

Visibility over automation.

## 🚨 Why This Exists

In real teams, credential rotation quietly breaks down:

- Ownership is unclear
- Rotation schedules differ
- Expired credentials don’t cause immediate failures
- Tracking lives in notes, tickets, or memory

As a result, credentials often remain active far beyond their intended lifetime.

This project addresses that gap by making rotation hygiene explicit, auditable, and hard to ignore.

## ✨ What It Does

Tracks credential rotation metadata (never secrets)

Calculates next rotation due dates

Flags overdue credentials

Highlights credentials approaching risk

Sorts by urgency for quick prioritization

Provides a notification-style audit view for manual reviews

No automation. No background services. Just clarity.

## 🖥 Example Audit Output
```
[OVERDUE] prod-db-password — overdue by 14 days
[WARNING] stripe-api-key  — due in 5 days
[OK]      github-token    — due in 62 days
```

## ▶️ Running the Tool
Designed to be run manually during audits or maintenance reviews.
```bash
python main.py
```
## 🗂 Data Model

The tool stores metadata only in a local JSON file.

Example:
```json
{
  "name": "prod-db-password",
  "last_rotated": "2024-09-01",
  "rotation_interval_days": 90
}
```

- Human-readable
- Auditable
- No secrets stored

## 🧠 Design Philosophy

Visibility over automation

Simplicity over completeness

Local execution over cloud dependencies

Human-readable data over opaque systems

This mirrors how many internal engineering tools are actually built.

## 🧩 Why a CLI?

Matches common internal tooling patterns

Fast, scriptable, low overhead

Avoids UI complexity unrelated to the problem

Encourages intentional, periodic audits

## 📄 Why JSON Instead of a Database?

Data volume is small

No concurrency requirements

Zero setup

Easy to inspect, diff, and version

A database would add complexity without meaningful benefit.

## 🚫 What This Project Is Not

❌ Password manager

❌ Secrets vault

❌ Automated rotation system

❌ Real-time notification service

## ⚠️ Limitations

No encryption of metadata

No background scheduling

Manual execution only

This project prioritizes clarity and control over automation.

## 🤔 Why I Built This

I built this project after noticing how credential rotation is usually handled:
with reminders, notes, or tribal knowledge — until it’s forgotten.

Most security failures aren’t caused by missing tools, but by missing visibility.
This project focuses on making time-based risk obvious, without introducing
automation, infrastructure, or complexity.

The goal was to build something small, realistic, and useful —
the kind of internal tool that quietly improves security hygiene.


## 🧩 Key Takeaway

Good security tools don’t always automate.
Sometimes they simply make invisible problems visible.
