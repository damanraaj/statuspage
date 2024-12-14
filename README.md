# Status Page Application

A modern status page application that allows administrators to manage services and their statuses, while providing a public interface for users to view the current status of all services.

## Features

- Admin dashboard to manage services and their statuses
- Public status page for users
- Real-time status updates
- Service history tracking
- Incident management

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize the database:
```bash
flask db upgrade
```

6. Run the application:
```bash
flask run
```

## Project Structure

```
statuspage/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   └── public.py
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── templates/
│       ├── admin/
│       └── public/
├── migrations/
├── .env.example
├── config.py
├── requirements.txt
└── run.py
```
