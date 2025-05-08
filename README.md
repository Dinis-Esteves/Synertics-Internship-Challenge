# Synertics-Internship-Challenge

This project is an automated futures scraping dashboard that collects futures data, stores it in a PostgreSQL database, and displays the information visually. It uses **Django**, **Celery**, **Redis**, and **PostgreSQL**, and is fully containerized with **Docker**.

---

# How to Run

## 1. **Clone the repository**
```bash
git clone git@github.com:Dinis-Esteves/Synertics-Internship-Challenge.git
cd Synertics-Internship-Challenge
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

## 4. **About the Scheduled Task**
Celery is configured and working, but the scheduled task (Periodic Task) does not come pre-configured in the database by default.
You can easily add it via the admin panel:

1. Access http://localhost:8000/admin *(password=user=admin)*

2. Go to "Periodic Tasks".

3. Create a new task with:

4. Name: Daily Scraper (or whatever you prefer)

5. Task: dashboard.tasks.run_scraper

6. Create a crontab schedule with your desired timing.

Setting up this pre-configured system was a bit tricky after completing the Docker setup. I also wasn’t sure what time to configure it, as the website rarely had the daily Excel file available. ☹️
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

# Examples of the automatic messages

<img src="https://github.com/user-attachments/assets/2f159ed1-a59b-4fb4-96fd-a9f5a89864a3" width="300" alt="Correct example">
<img src="https://github.com/user-attachments/assets/7ee6551b-876e-4666-9d8d-c4eeedaa1fb7" width="300" alt="Error example">


