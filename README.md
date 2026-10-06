# 🔐 Secure Enterprise RAG with Role-Based Access Control

## 📌 Project Overview

Secure Enterprise RAG is a Retrieval-Augmented Generation (RAG) application designed to provide secure access to enterprise documents based on user roles and permissions.

The system retrieves relevant information from company documents, applies Role-Based Access Control (RBAC), and sends only authorized information to the Large Language Model (LLM).

This prevents unauthorized users from accessing confidential enterprise information.

---

## 🎯 Objectives

- Build a secure enterprise RAG system.
- Retrieve relevant information from company documents.
- Apply role-based permissions before sending information to the LLM.
- Prevent unauthorized document access.
- Protect sensitive HR, Finance, and Legal information.
- Test the system against prompt-injection attempts.
- Provide a simple web interface using Gradio.

---

## 🏗️ System Architecture

```text
                    User
                      |
                      ↓
                Gradio Interface
                      |
                      ↓
                 User Role
                      |
                      ↓
                   Query
                      |
                      ↓
              Document Retrieval
                      |
                      ↓
                  RBAC Filter
                      |
              ┌───────┴────────┐
              ↓                ↓
        Authorized         Unauthorized
          Chunks               Chunks
              |                  |
              ↓                  ↓
          Ollama LLM        Blocked
              |
              ↓
          Final Answer