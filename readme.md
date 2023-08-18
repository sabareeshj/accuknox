## Installation

Follow these steps to set up and run the project locally.

### Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)

### Setup

1. **Clone the repository:**

   ```````bash
   git clone https://github.com/sabareeshj/accuknox.git
   cd social-networking-app``````

   ```````

2. **Create and activate a virtual environment**

   ````bash
   python -m venv venv
   source venv/bin/activate```

   ````

3. **Set up the database (PostgreSQL):**

   - Create a PostgreSQL database with the name, user, and password as specified in your docker-compose.yml (or your local settings).

4. **Apply migrations**
   `python manage.py migrate`
5. **Run the development server**
   `python manage.py runserver`
