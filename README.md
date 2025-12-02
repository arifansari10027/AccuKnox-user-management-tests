# AccuKnox – User Management Test Automation

This project automates the **User Management module** of the OrangeHRM demo website using **Python + Playwright + Pytest**.

## Video Demonstration

https://github.com/arifansari10027/AccuKnox-user-management-tests/blob/main/Testing-Assignment-Accuknox.mp4

## Features Covered

The following scenarios are automated:

1. Add a new user  
2. Search an existing user  
3. Search an invalid user  
4. Edit user status and validate  
5. Delete a user  

The project uses the **Page Object Model (POM)** design pattern.

---

## Prerequisites

Make sure you have the following installed:

- Python 3.10+
- pip
- Git

---

## 🔧 Installation

Clone the repository:

```bash
git clone https://github.com/arifansari10027/AccuKnox-user-management-tests.git
cd AccuKnox-user-management-tests
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Playwright browsers:

```bash
playwright install
```

How to Run Tests

Run all tests (headed mode):

```bash
pytest -v --headed
```

Run with slow motion (optional):

```bash
pytest -v --headed --slowmo=500
```

Run a specific test case:

```bash
pytest tests/test_user_management.py::test_add_new_user -v --headed
```