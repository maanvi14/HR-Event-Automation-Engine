# HR Event Automation Engine

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![n8n](https://img.shields.io/badge/n8n-Workflow%20Automation-orange)
![FastAPI](https://img.shields.io/badge/FastAPI-Microservice-green)
![Cloudinary](https://img.shields.io/badge/Cloudinary-Image%20Hosting-blue)
![Google Chat](https://img.shields.io/badge/GChat-Webhook%20Delivery-success)
![Railway](https://img.shields.io/badge/Railway-Deployed-black)
![Status](https://img.shields.io/badge/Status-Active-success)

An automated HR workflow system that generates **personalized employee celebration cards** (birthdays & work anniversaries) and delivers them seamlessly to **Google Chat**.

Built using **n8n + Python microservices**, the system eliminates manual effort for HR/marketing teams and ensures timely, consistent engagement.
<img width="1389" height="521" alt="image" src="https://github.com/user-attachments/assets/cc6e1356-98f1-446c-a6e6-0b31a8abf8a8" />


---

## 🚀 Live Workflow

🔗 **Deployed Endpoint:**  
https://primary-production-c83d6.up.railway.app/workflow/TBuD2PFW8B8FDlfw

---

## 💡 Problem

HR and marketing teams often manually:
- Track employee birthdays & anniversaries  
- Design celebration creatives  
- Send messages across internal platforms  

This process is:
- Time-consuming  
- Error-prone  
- Not scalable  

---

##  Solution

This system automates the entire workflow:

- 📅 Detect upcoming events (Birthday / Anniversary)  
- 🖼️ Generate personalized cards dynamically  
- ☁️ Upload images to cloud storage  
- 💬 Deliver directly to Google Chat via webhook  

---

## 🧠 Key Features

### 🔹 Automated Workflow (n8n)
- Event-triggered automation pipeline  
- Handles scheduling and orchestration  
- Connects all services seamlessly  

---

### 🔹 Dynamic Card Generation
- Python microservice generates:
  - Birthday cards 🎂  
  - Work anniversary cards 🎉  
- Personalization:
  - Name  
  - Photo  
  - Event type  
  - Branding  

---

### 🔹 Cloud Image Hosting
- Images uploaded to **Cloudinary**
- Public URLs generated for sharing  

---

### 🔹 Google Chat Integration
- Cards delivered via **GChat webhook**
- Ready-to-use formatted messages  

---

## 🏗️ System Architecture

1. Event Trigger (n8n)
2. Fetch Employee Data
3. Call Python Microservice
4. Generate Personalized Card
5. Upload to Cloudinary
6. Send to Google Chat (Webhook)

---

## 🧩 Tech Stack

| Layer | Technology |
|------|-----------|
| Workflow Automation | n8n |
| Backend Service | Python (FastAPI) |
| Image Processing | PIL / Custom Templates |
| Cloud Storage | Cloudinary |
| Messaging | Google Chat Webhooks |
| Deployment | Railway + Render |

---

## 🔌 API Overview

### 🔹 Card Generation Service

```http
POST /generate-card
Request:

{
  "name": "Maanvi Verma",
  "event_type": "birthday",
  "image_url": "employee_photo_url"
}

Response:

{
  "card_url": "https://cloudinary.com/generated-card.jpg"
}
```
🔹 n8n Workflow
1. Trigger: Scheduled / Event-based
2. Calls Python microservice
3. Sends final message to Google Chat via webhook

## ⚙️ Setup Instructions
### 1️. Clone Repository
```bash
git clone https://github.com/your-username/HR-Event-Automation-Engine.git
cd HR-Event-Automation-Engine
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
### 3. Run Python Service
```bash
python main.py
```
### 4. Configure n8n Workflow
```bash
Import workflow JSON
```
```bash
Set:
Webhook URLs
Cloudinary credentials
Google Chat webhook
💬 Example Output
🎂 Birthday celebration card with employee name & image
🎉 Work anniversary card with branding
Delivered directly to the team communication channel.
```
🔐 Design Principles
1. Fully automated (no manual intervention)
2. Scalable workflow architecture
3. Modular microservice design
4. Real-time delivery via webhooks
🚀 Future Improvements
1. Email & Slack Integration

Extend delivery to multiple communication channels

2. Template Customization UI

Allow HR teams to design templates dynamically

3. Database Integration

Store employee data in a structured DB (PostgreSQL)

4. Analytics Dashboard

Track engagement (views, clicks, reactions)
