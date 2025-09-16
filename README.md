# 🚀 FastAPI + gRPC Authentication Service

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-🔥-green)
![gRPC](https://img.shields.io/badge/gRPC-Enabled-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

A **lightweight, high-performance authentication system** built with **FastAPI** and **gRPC**, designed for modern APIs and microservices.

---

## 🔑 Features

- ✅ User **registration & login**
- 🔒 **JWT-based authentication** (access & refresh tokens)
- 🛡️ Secure **password hashing** (bcrypt / argon2)
- 🔗 **gRPC communication** between internal services
- 🌐 **FastAPI REST endpoints** for external clients
- 🧑‍🤝‍🧑 Optional **role-based access control (RBAC)**

---

## 🛠 Tech Stack

- ⚡ [FastAPI](https://fastapi.tiangolo.com/) – REST API framework  
- 🔥 [gRPC](https://grpc.io/) – High-performance RPC framework  
- 📦 [Protocol Buffers](https://protobuf.dev/) – Service definitions  
- 🗄️ Database: **MySQL (default)** | PostgreSQL | SQLite  
- 🔑 [JWT](https://jwt.io/) – Token-based authentication  
- 🔐 [bcrypt](https://pypi.org/project/bcrypt/) / [argon2](https://pypi.org/project/argon2-cffi/) – Password hashing  

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/your-username/fastapi-grpc-auth.git
cd fastapi-grpc-auth


# Create virtual environment
python -m venv myVenv

# Activate (Linux/Mac)
source myVenv/bin/activate

# Activate (Windows)
myVenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt


▶️ Start FastAPI server
uvicorn app.main:app --reload

or

fastapi dev app/main.py


▶️ Start gRPC server
python user-api-service/server.py

```