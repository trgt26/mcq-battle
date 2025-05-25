# MCQ-Battle Backend API 🧠⚔️

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)

**MCQ-Battle** is a backend API built with **FastAPI**, **SQLModel**, and **MySQL** using **aiomysql** for asynchronous database operations. It supports user management, battle matchmaking, real-time scoring, and more.

---

## 🛠 Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: MySQL
- **ORM**: [SQLModel](https://sqlmodel.tiangolo.com/) (built on SQLAlchemy + Pydantic)
- **Async Driver**: [aiomysql](https://pypi.org/project/aiomysql/)
- **Authentication**: JWT 
- **Documentation**: Swagger UI (built-in)
- **Testing**: Pytest
- **Containerization**: Docker (optional)

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/MCQ-Battle.git
cd MCQ-Battle
```


### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=mysql+aiomysql://username:password@localhost:3306/mcq_battle
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Make sure the `DATABASE_URL` uses `mysql+aiomysql` for async support.

### 5. Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at:
📍 `http://127.0.0.1:8000`

---

## 📘 API Documentation

FastAPI provides auto-generated interactive docs:

* Swagger UI: `http://127.0.0.1:8000/docs`
* ReDoc: `http://127.0.0.1:8000/redoc`

---

## 🧪 Running Tests

If you're using `pytest`, you can run:

```bash
pytest
```

Make sure to configure a separate test database and use isolated test sessions to avoid affecting production data.

---

## 🔄 Database Setup with SQLModel

To create tables using SQLModel (with async support), use an async function like:

```python
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel
from app.db import engine

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
```

Run this at startup or in a script to initialize the schema.

---

## ✨ Features

* User registration and login
* Multiple-choice question management
* Game creation and matchmaking
* Real-time scoring logic
* Leaderboards and stats
* JWT-based authentication

---

## 📌 Future Improvements

* Real-time gameplay with WebSockets
* Admin panel for question upload
* Player vs Player (PvP) ranking system
* Docker & CI/CD setup
* Rate limiting and throttling

---

## 🧑‍💻 Contributing

Pull requests are welcome!
For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🧠 Built for learning, speed, and MCQ battle glory!

