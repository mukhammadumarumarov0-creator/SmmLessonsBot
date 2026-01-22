# 📚 SmmLesson Telegram Bot

SmmLesson Telegram Bot is an educational Telegram bot designed for step-by-step online learning. The bot delivers structured lessons (posts, images, and videos), enforces progress control with tests, and allows admins to track users who successfully complete the full course.

This bot is ideal for **SMM courses, online training programs, and paid/private lessons**.

---

## ✨ Key Features

* 🔐 **User Registration** before accessing lessons
* 🖼 **Post & Image Lessons** (introductory content)
* 🎥 **Video Lessons** with strict order
* 📝 **Tests after each video lesson**
* ✅ Next lesson unlocks **only after passing the test**
* 🔒 Lesson skipping is not allowed
* 📊 **Progress tracking** for every user
* 🧑‍💼 **Admin panel** to monitor completed users
* 📩 Automatic notification when a user finishes the course

---

## 🧠 Learning Flow

1. User starts the bot and completes **registration**
2. Introductory **post/image lessons** are unlocked
3. **Video lessons** become available step by step
4. After each video, a **test** is required
5. Passing the test unlocks the **next lesson**
6. After completing all lessons and tests:

   * User receives a completion message
   * User appears in the admin panel
   * Admin contacts the user manually

---

## 🛠 Tech Stack

* **Python 3.10+**
* **Django** (backend & admin panel)
* **Aiogram** or **python-telegram-bot**
* **PostgreSQL / SQLite**
* **Gunicorn**
* **Nginx**

---

## 📁 Project Structure (example)

```
SmmLessonBot/
├── bot/
│   ├── handlers/
│   ├── keyboards/
│   ├── states/
│   └── services/
├── lessons/
│   ├── models.py
│   ├── tests.py
│   └── admin.py
├── users/
│   ├── models.py
│   └── admin.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🔑 Environment Variables (.env)

Create a `.env` file:

```
DEBUG=False
SECRET_KEY=your_secret_key
TELEGRAM_BOT_TOKEN=your_bot_token
DATABASE_URL=your_database_url
```

---

## 👤 User Registration

During registration, the bot can collect:

* Full name
* Telegram username
* Phone number (optional)

Users **cannot access lessons** until registration is completed.

---

## 📝 Tests & Progress Control

* Each video lesson has a related test
* Tests can be:

  * Multiple choice
  * Single correct answer
* If the user fails:

  * The lesson remains locked
  * The test can be retried

User progress is stored in the database and cannot be bypassed.

---

## 🧑‍💼 Admin Panel

Admins can:

* View all registered users
* Track lesson and test progress
* See users who **completed the entire course**
* Contact users manually after course completion

When a user finishes the course, the bot automatically sends:

> "Congratulations! You have successfully completed the course. Our admin will contact you shortly."

---

## 🧪 Testing

* Register a test user
* Complete lessons step by step
* Fail and pass tests to verify locking logic
* Confirm user appears in admin panel after completion

---

## 📌 Roadmap (Optional)

* [ ] Payment integration
* [ ] Certificate generation
* [ ] Course analytics
* [ ] Multi-course support

---

## 👨‍💻 Author

Developed by **Muhammadumar Umarov**
Telegram: @Muhammadumar_umarov
Python Developer

---
