
# Helpdesk Ticket Management System

A web-based helpdesk ticket management system designed to streamline issue tracking, ticket categorization, and support workflow monitoring. The application combines ticket management with machine learning-based categorization and analytics.

## Features

- **User Authentication:** Secure user login and authentication.
- **Ticket Management:** Create, track, and manage support tickets.
- **Issue Tracking:** Monitor ticket status and progress.
- **ML-Based Ticket Categorization:** Categorize tickets using machine learning.
- **Analytics Dashboard:** Visualize ticket-related information and monitor issue patterns.
- **Database Management:** Store and manage ticket records using SQLite.

## Tech Stack

| Category | Technologies |
|----------|--------------|
| Programming Language | Python |
| Machine Learning | Scikit-learn |
| Database | SQLite |
| Frontend | HTML, CSS |
| Backend | Python |
| Analytics | Dashboard and ticket analysis |

## Project Structure

```text
helpdesk_system/
│
├── app.py
├── templates/
├── static/
├── models/
├── database/
├── requirements.txt
└── README.md
```

> Update the project structure to match your actual repository.

## Machine Learning

The project includes machine learning-based ticket categorization to support helpdesk issue classification.

### Workflow

1. Collect ticket information.
2. Preprocess ticket text or relevant features.
3. Apply the trained classification model.
4. Assign a ticket category.
5. Display ticket information through the application.

> Add the actual algorithm, dataset, and evaluation results once you verify them.

## Analytics Dashboard

The dashboard is designed to support monitoring of helpdesk operations, including:

- Ticket status
- Issue categories
- Ticket distribution
- Support workload

The available metrics depend on the features implemented in the application.

## Installation

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd helpdesk_system
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows:**

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app.py
```

Open the local URL displayed by your application.

## Skills Demonstrated

- Python Programming
- SQL / SQLite Database Management
- Machine Learning
- Ticket Classification
- Data Analysis
- Web Application Development
- Problem Solving

## Future Improvements

- Improve classification accuracy using additional training data.
- Add advanced ticket analytics and reporting.
- Implement priority prediction.
- Enhance dashboard visualizations.
- Deploy the application for real-world use.

## Author

**Anshima Kushwaha**

Chemical Engineering | IIT Jodhpur
