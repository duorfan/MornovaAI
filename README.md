# 🌅 Mornova AI

**Mornova AI** is a personalized wake-up assistant that transforms your morning routine with **smart lighting**, **AI-driven scheduling**, and **music integration**. It replaces harsh alarms with a gentle, adaptive wake-up experience informed by real-time weather and calendar insights.

---

## 🚀 Overview

- Gradually wakes you using light and ambient sound.
- Adjusts wake-up time based on your schedule and local weather.
- Includes AI interaction via a dashboard.
- Supports touch-based snooze interaction on the physical lamp.
- Designed for bedside use with a clean, minimalist form factor.

🎥 [View Final Project Documentation on Notion](https://duorfan.notion.site/198f98b6add9801f99aad12e02392304)

---

## 🛠️ System Diagram

The system connects a physical Raspberry Pi lamp with a web dashboard and external APIs.

![Mornova AI System Diagram](assets/mornova_diagram.png)

**How it works:**
1. User sets preferences on the dashboard.
2. APIs fetch real-time weather and calendar data.
3. AI suggests wake-up adjustments.
4. Raspberry Pi triggers gradual light/sound wake-up.
5. User can snooze via tap; feedback loop refines future behavior.

🧠 See [`pseudocode.py`](pseudocode.py) for the logic breakdown.

---

## 🌟 Key Features

- ☀️ **Light-Based Wake-Up** – Simulates sunrise through gradual brightness.
- 🧠 **AI-Powered Alarms** – Adjusts alarms based on weather & schedule.
- 🎶 **Spotify Integration** – Plays custom morning playlists or ambient sounds.
- 🗣️ **Voice & Touch** – AI interaction via dashboard, snooze via long press.
- 🌙 **Night Mode** – Wind-down routines with low light and calming audio.

---

## 🧱 Tech Stack

| Layer        | Technology                                  |
|--------------|----------------------------------------------|
| Backend      | Python (Flask)                              |
| AI Logic     | OpenAI GPT (via API)                        |
| APIs Used    | Google Calendar, OpenWeather, Spotify       |
| Frontend     | React.js (dashboard interface)              |
| Edge Compute | Raspberry Pi 4 for physical interactions    |

---

## 🔌 Hardware (Prototype)

- Raspberry Pi 4 Model B
- 2× Adafruit NeoPixel Stick (Warm White)
- Adafruit I2S MEMS Microphone + Speaker
- FSR 402 Pressure Sensor
- 3D-Printed Base + Acrylic Dome

💡 Estimated Cost: ~$100  
🛍️ Target Retail Price: $89–120

---

## 🎥 Demo Videos

- 📺 [Dashboard Interaction (Alarm Setting + AI)](https://drive.google.com/file/d/1NrXBb0FtNcpzGW6EcHTI8UtsXKu7ezDG/view?usp=sharing)
- 💡 [Lamp Wake-Up + Snooze Function](https://drive.google.com/file/d/15KDBSX7jFJIbbD8OeluvzQp-x8XT8nSY/view?usp=sharing)


---

## ✨ Credits

Created by [@duorfan](https://github.com/duorfan)  
A Duor.fun production 🌱

---

