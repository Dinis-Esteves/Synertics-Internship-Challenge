# Synertics-Internship-Challenge

This project is an automated futures scraping dashboard that collects futures data, stores it in a PostgreSQL database, and displays the information visually. It uses **Django**, **Celery**, **Redis**, and **PostgreSQL**, and is fully containerized with **Docker**.

---

# How to Run

## 1. **Clone the repository**
```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
```


## 2. **Set up your email environment variables**

You'll need a Gmail App Password (or other SMTP service).
Create a .env file or add directly to settings.py the following variables:

```
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```
**Do not use your main Gmail password. Create an App Password.**

[How to create a Gmail App Password](https://support.google.com/accounts/answer/185833)


## 3. **Start the application with Docker Compose**
   ```bash
   docker compose up --build
   ```
Access in your browser: http://localhost:8000

## About the Scheduled Task
Celery is configured and working, but the scheduled task (Periodic Task) does not come pre-configured in the database by default.
You can easily add it via the admin panel:

Access http://localhost:8000/admin (password=user=admin)

Go to "Periodic Tasks".

Create a new task with:

Name: Daily Scraper (or whatever you prefer)

Task: dashboard.tasks.run_scraper

Create a crontab schedule with your desired timing.

# Project Checklist:

- Functional scraping ✅

- PostgreSQL storage ✅

- Django dashboard ✅

- Async tasks with Celery ✅

- Scheduling with Celery Beat ✅

- Dockerized ✅

- Ready to run via docker compose ✅

- Visible logs in terminal ✅

- Email notifications (via SMTP) ✅
