# Music Vibrationc | Udacity Project

## Introduction

Music Vibration is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

*This project is originally called Fyyur from Udacity's Advanced Web Development Nanodegree*

![plot](/project-img/music-vibration-home-1.png)
![plot](/project-img/music-vibration-venue-1.png)
![plot](/project-img/music-vibration-venue-list-1.png)



## Dependencies

### 1. Backend Dependencies
This tech stack includes the following:
 * **virtualenv** as a tool to create isolated Python environments
 * **SQLAlchemy ORM** to be our ORM library of choice
 * **PostgreSQL** as our database of choice
 * **Python3** and **Flask** as our server language and server framework
 * **Flask-Migrate** for creating and running schema migrations


### 2. Frontend Dependencies

* The Front-end for the project is based on **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for our website's frontend. 

* Bootstrap can be installed by Node Package Manager (NPM). Therefore, if not already, download and install the [Node.js](https://nodejs.org/en/download/). 

* Windows users must run the executable as an Administrator, and restart the computer after installation. After successfully installing the Node, verify the installation as shown below.

```
node -v
npm -v
```

## Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app. Includes your SQLAlchemy models.
                    "python app.py" to run after installing dependencies
  ├── config.py *** Database URLs, CSRF generation, etc
  ├── error.log
  ├── forms.py *** forms
  ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
```

## Overall:

Models are located in the MODELS section of `app.py`.
Controllers are also located in `app.py`.
The web frontend is located in `templates/`, which builds static assets deployed to the web server at `static/`.
Web forms for creating data are located in `forms.py`

##  Prerequisite - Setting up PostgreSQL

In order to run this project successfully, you will need to install and configure postgresql


### 1. Install PostgreSQL

If you don't have PostgreSQL installed, follow the instructions for your operating system.
* On Ubuntu/Debian:

```
sudo apt update
sudo apt install postgresql postgresql-contrib
```

* On macOS (using Homebrew):
```
brew install postgresql
```
* On Windows:

    Download and install PostgreSQL from https://www.postgresql.org/download/windows/.
    Follow the installer prompts to complete the installation.

### 2. Start PostgreSQL Service

* Ensure the PostgreSQL service is running:
On Ubuntu/Debian:

`sudo service postgresql start`

* On macOS:

`brew services start postgresql`

* On Windows:

  Start the PostgreSQL service from the Start menu or use the Services window (services.msc) to start it.

### 3. Create a PostgreSQL Database

Once PostgreSQL is installed and running, create a new database for your project:

```
sudo -u postgres psql
```

In the PostgreSQL shell, run the following commands:

```
CREATE DATABASE your_database_name;
CREATE USER your_user_name WITH PASSWORD 'your_password';
ALTER ROLE your_user_name SET client_encoding TO 'utf8';
ALTER ROLE your_user_name SET default_transaction_isolation TO 'read committed';
ALTER ROLE your_user_name SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE your_database_name TO your_user_name;
```

Exit the PostgreSQL shell:

```
\q
```

### 4. Configure Your Application to Use PostgreSQL

In your project's configuration file (typically something like config.py or .env), set up the PostgreSQL connection.

For example, if you're using SQLAlchemy and .env:
```
DATABASE_URL=postgresql://your_user_name:your_password@localhost:5432/your_database_name
```
Make sure to replace `your_user_name`, `your_password`, and `your_database_name` with the appropriate values.


### 5. Install Required Python Packages

Install the necessary packages to interact with PostgreSQL, such as psycopg2 and Flask-SQLAlchemy:
```
pip install -r requirements.txt
```
### 6. Initialize the Database (if applicable)

If your project requires initializing the database with tables, run the appropriate command for your application to create the necessary tables. For example, in Flask:

```
flask db upgrade

# Or if you're using a custom script:

python manage.py db init
```
## Setup on Your Machine

### 1. Download the project starter code locally
```
git clone https://github.com/rawdaymohamed/music-vibration.git
cd music-vibration
```
Copy `.env.example` and rename the new file to `.env`:

Add your Postgresql database URL (*explained above*) to the .env file

### 2. Initialize and activate a virtualenv using:

```
python -m virtualenv venv
source venv/bin/activate
```
Note - In Windows, the env does not have a bin directory. Therefore, you'd use the analogous command shown below:

```
source venv/Scripts/activate
```
### 3. Install the dependencies: Backend
```
pip install -r requirements.txt
```
### 4. Install the dependencies: Frontend
```
npm install
```    
## 5. Run the development server:

```
export FLASK_APP=myapp
export FLASK_ENV=development # enables debug mode
python3 app.py
```
Verify on the Browser<br> Navigate to project homepage http://127.0.0.1:5000/ or http://localhost:5000