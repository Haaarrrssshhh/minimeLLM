# Project Setup Guide

## Table of Contents
- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Running the Backend](#running-the-backend)
- [Managing Dependencies](#managing-dependencies)
- [Additional Information](#additional-information)

## Introduction
This document provides instructions to set up and run the backend for your Python project. It covers the installation of dependencies, environment configuration, running the code locally, and managing dependencies.

## Prerequisites
Before you begin, ensure you have the following:
- Python 3.11 installed
- Git installed
- Basic knowledge of virtual environments in Python

## Installation
1. **Clone the repository:**
   ```sh
   git clone https://github.com/Haaarrrssshhh/minimeLLM.git
   cd your-repo-name
   ```

## Environment Setup
1. **Create a virtual environment:**
   ```sh
   python3.11 -m venv venv
   ```

2. **Activate the virtual environment:**
   - **For macOS and Linux:**
     ```sh
     source venv/bin/activate
     ```
   - **For Windows:**
     ```sh
     venv\Scripts\activate
     ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

## Running the Backend
To run the backend, use the following command:
```sh
python manage.py runserver
```
This command starts the development server to run the code locally.

## Managing Dependencies
1. **Update `requirements.txt`:**
   If you install new packages or update existing ones, make sure to update `requirements.txt`:
   ```sh
   pip freeze > requirements.txt
   ```

2. **Remove unwanted files from Git:**
   If you've already pushed unwanted files to GitHub, follow these steps to remove them:
   ```sh
   # Remove all files from Git tracking
   git rm -r --cached .

   # Re-add all files, following the new .gitignore rules
   git add .

   # Commit the changes
   git commit -m "Update .gitignore and remove ignored files from tracking"

   # Push the changes to GitHub
   git push origin main  # or your specific branch name
   ```

## Additional Information
- **Deactivating the virtual environment:**
  Once you're done working, you can deactivate the virtual environment with:
  ```sh
  deactivate
  ```