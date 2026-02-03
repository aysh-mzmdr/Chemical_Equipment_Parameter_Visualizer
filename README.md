# Chemical Equipment Parameter Visualizer

A hybrid Web and Desktop application designed to analyze and visualize chemical equipment data. This tool allows users to upload CSV files containing equipment details (Name, Type, Flowrate, Pressure, Temperature), parses the data using a Django backend, and serves analytics to both a React web interface and a PyQt5 desktop application.

## Features
* **Dual Frontend:** Access data via a web dashboard (React) or a native desktop app (PyQt5).
* **Data Analysis:** Automated parsing and summary statistics of chemical equipment parameters using Pandas.
* **Visualization:** Interactive charts (Chart.js for Web, Matplotlib for Desktop) and data tables.
* **History Management:** Automatically stores and retrieves the last 5 uploaded datasets via SQLite.
* **REST API:** A unified Django REST Framework API serving both frontends.

## Tech Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend (Web)** | React.js + Chart.js | Web-based data visualization |
| **Frontend (Desktop)** | PyQt5 + Matplotlib | Native desktop visualization |
| **Backend** | Django + DRF | API & Business Logic |
| **Data Processing** | Pandas | CSV parsing & Analytics |
| **Database** | SQLite | Data persistence (Last 5 uploads) |

## Prerequisites

Before you begin, ensure you have the following installed on your machine:
* **Python 3.8+** (for Backend and Desktop App)
* **Node.js & npm** (for Web Frontend)
* **Git** (for version control)

## Installation & Setup

Cloning the repository:
```bash
git clone https://github.com/aysh-mzmdr/Chemical_Equipment_Parameter_Visualizer.git

cd Chemical_Equipment_Parameter_Visualizer
```

## 1. Backend Setup (Django)
It is recommended to use a virtual environment.
```bash
# Navigate to backend folder
cd backend

# Install Python dependencies 
pip install -r requirements.txt

# Apply database migrations (SQLite)
python manage.py migrate
```

## # Open a new terminal and navigate to the web frontend folder
```bash
cd frontend/web
```
# Install node dependencies
```bash
npm install
```
## Running the Application
To fully utilize the system, you need to keep the Backend server running while using either the Web or Desktop interface.

Step 1: Start the Backend API

```bash
# In your backend terminal
python manage.py runserver
```
The API will be available at http://127.0.0.1:8000/

Step 2: Run the Web Application
```bash
# In your web frontend terminal
npm run dev
```
The web app will open at http://localhost:5173/

Step 3: Run the Desktop Application
```bash
# Open a new terminal, and run the desktop app

cd frontend/desktop
./Application.py
```
