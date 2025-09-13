FastAPI + gRPC Authentication Service
A lightweight authentication system built with FastAPI and gRPC, designed for high-performance APIs and microservices.

**🔑 Features**
User registration & login
JWT-based authentication (access & refresh tokens)
Secure password hashing (bcrypt/argon2)
gRPC communication between services
FastAPI REST endpoints for external clients
Role-based access control (optional)

**🛠 Tech Stack**
FastAPI – REST API framework
gRPC – High-performance RPC framework
Protocol Buffers (Protobuf) – Service definitions
SQLite / PostgreSQL / MySQL – Database (choose your backend) Default is MYSQL
JWT – Token-based authentication


**📦 Installation**
Clone the repository:
git clone https://github.com/your-username/fastapi-grpc-auth.git
cd fastapi-grpc-auth


**Create a virtual environment & install dependencies:**
python -m venv myVenv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt


**⚡ Running the Service**

**Start FastAPI server:**
uvicorn app.main:app --reload
**or **
fastapi dev app/main.py

**Start gRPC server:**
python uer-api-service/server.py
