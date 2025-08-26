# 🚀 Production-Grade FastAPI Service with MySQL and Kafka

This repository contains a **production-ready, modular FastAPI application** designed for high-performance API service delivery. It leverages **MySQL** for reliable relational data storage and **Apache Kafka** for robust stream processing and event-driven architecture.

The architecture follows best practices in modularization, enabling easy scalability, maintainability, and clean separation of concerns across the codebase.

## ✨ Features

- ✅ Built with FastAPI for fast, asynchronous API endpoints with automatic OpenAPI (Swagger) docs  
- ✅ Modular code structure for scalable development and clear separation of API, database models, and business logic  
- ✅ MySQL backend providing transactional and persistent storage  
- ✅ Kafka integration for real-time stream processing and asynchronous event handling  
- ✅ Dockerized for seamless deployment and environment parity across stages  

## 🚀 Getting Started

### 🔧 Prerequisites

- Docker and Docker Compose installed on your machine

### ▶️ Running the Service

1. Navigate to the root directory of the repository.  
2. Build and start the service containers using Docker Compose: `docker-compose up –build`
3. Once running, access the interactive API documentation at: `https://127.0.0.1/docs`

   
This Swagger UI allows you to explore and test all API endpoints easily.
<img width="1463" height="753" alt="image" src="https://github.com/user-attachments/assets/08445f21-5d7a-47c6-ae0c-124a1f1afa91" />


Additional Information

	•	The `add_user` endpoint is used to add a new user directly into the `mydb.users` table in MySQL.
 
	•	The `order` endpoint is used to add a new order through the Kafka topic called `test-topic`.
 
	•	If you want to change the MySQL or Kafka connection parameters, you can edit the `environment.yaml` configuration file.

 📖 Medium Blog
Read the detailed blog on Medium explaining this project and its design here: [BLOG](https://medium.com/@tusharsharma_60127/i-made-a-production-ready-fastapi-service-with-mysql-kafka-a6c29270e830)
 
---

Feel free to contribute, raise issues, or submit pull requests to enhance this project!


