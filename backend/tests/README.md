# 🧪 Testing Guide

This project uses `pytest` for running automated tests. Follow the instructions below to set up your environment and execute the test suite.

## ⚙️ Installation & Setup

 **Install dependencies:**
   Make sure you have your `requirements.txt` file ready in the root directory, then run:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Running Tests

### General Test Execution
* **Run all tests:**
  ```bash
  python -m pytest tests/ -v
  ```
* **Run tests until the first failure:**
  ```bash
  python -m pytest -x -v
  ```
* **Run with test coverage report:**
  ```bash
  pytest tests/ -v --cov=. --cov-report=term
  ```

### Running Specific Files
* **Run a single test file (e.g., auth tests):**
  ```bash
  python -m pytest tests/test_auth.py -v
  ```
* **Run a single test file until the first failure:**
  ```bash
  python -m pytest tests/test_auth.py -x -v
  ```
* **Run all citizen tests:**
  ```bash
  pytest tests/test_citizen.py -v
  ```

### Running Specific Test Functions & Patterns
* **Run a specific test function:**
  ```bash
  python -m pytest tests/<filename>::<function_name> -v
  ```
* **Example (Run a specific auth test):**
  ```bash
  python -m pytest tests/test_auth.py::test_login_pending_user -v
  ```
* **Example (Run a specific citizen test):**
  ```bash
  pytest tests/test_citizen.py::test_submit_complaint_success -v
  ```

---

## 📊 Generating Reports

* **Save test results to an HTML report:**
  ```bash
  python -m pytest --html=tests/test_report.html
  ```

## 📊 Generating Coverage Report

* **generate a complete coverage report:**
  ```bash
  ## 📊 Generating Reports

* **Save test results to an HTML report:**
  ```bash
  python -m pytest --html=tests/test_report.html
  ```

