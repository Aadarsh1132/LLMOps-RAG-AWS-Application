# 🚀 LLMOps RAG AWS Application 🧠☁️

A **Retrieval-Augmented Generation (RAG)** based QA System powered by **Flask**, built with end-to-end **MLOps best practices**, containerized using **Docker**, deployed using **AWS App Runner**, and integrated with **CI/CD workflows via GitHub Actions**. This project demonstrates how to take an LLM-based application from local development to **production deployment in the cloud**.

---

## 📌 Highlights

- ✅ RAG-based pipeline for QA
- ✅ Built with Python 3.10 & Flask
- ✅ Modular project structure (Ingestion, Retrieval, Generation)
- ✅ Integrated with AWS S3, ECR, IAM
- ✅ CI/CD pipeline with GitHub Actions
- ✅ Dockerized for production-readiness
- ✅ Auto-deployment via AWS App Runner
- ✅ Secrets managed securely via GitHub

---

## 📂 Project Structure
LLMOps-RAG-AWS-Application/ │ ├── app.py # Flask App Entry Point ├── requirements.txt # Python Dependencies ├── Dockerfile # Docker Build Instructions ├── .dockerignore # Docker Ignore Rules ├── .gitignore # Git Ignore Rules ├── .github/ │ └── workflows/ │ └── main.yaml # GitHub Actions CI/CD Pipeline ├── SRC/ │ └── QASystem/ │ ├── init.py │ ├── ingestion.py # Data ingestion logic │ └── retrievalandgeneration.py # RAG pipeline code

