# VIZ Project Backend

## Initial Setup

1. Install Python 3.
1. Setup a virtual environment or similar for installing dependencies.
    ```bash
    python3 -m venv venv 
    ```
1. Activate your virtual environment.
   ```bash
   source venv/bin/activate
   ```
1. Setup your environment variables:
    ```bash
    export ENV=development
    # If you are using PostgresSQL
    export DATABASE_URL="postgres://USER:PASSWORD@HOST:PORT/NAME"
    # If you don't want to install PostgresSQL
    export DATABASE_URL="sqlite:////full/path/to/your/database/file.sqlite"
    export SOCIAL_AUTH_FACEBOOK_KEY=Facebook App ID
    export SOCIAL_AUTH_FACEBOOK_SECRET=Facebook App secret
    export SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=Google OAuth Client ID
    export SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=Google OAuth Client secret
    export SOCIAL_AUTH_GITHUB_KEY=Github OAuth App Client iD
    export SOCIAL_AUTH_GITHUB_SECRET=Github OAuth App Client Secret 
    ```
    Similarly, create a `.env` file with the environment variables.
    ```.env
    ENV=development
    # If you are using PostgresSQL
    DATABASE_URL="postgres://USER:PASSWORD@HOST:PORT/NAME"
    # If you don't want to install PostgresSQL
    DATABASE_URL="sqlite:////full/path/to/your/database/file.sqlite"
    SOCIAL_AUTH_FACEBOOK_KEY=Facebook App ID
    SOCIAL_AUTH_FACEBOOK_SECRET=Facebook App secret
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=Google OAuth Client ID
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=Google OAuth Client secret
    SOCIAL_AUTH_GITHUB_KEY=Github OAuth App Client iD
    SOCIAL_AUTH_GITHUB_SECRET=Github OAuth App Client Secret 
    ```
5. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
1. Create the necessary database tables by applying migrations:
   ```bash
   python manage.py migrate
   ```
6. Run the lightweight Django development server:
   ```
   python manage.py runserver
   ```
   **OR** run a server with production settings locally (requires Heroku CLI):
   ```
   heroku local
   ```
