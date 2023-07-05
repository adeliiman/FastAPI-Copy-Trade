# FastAPI-Copy-Trade
<div align="center">
<h1 align="center">FastAPI copy trade App</h1>
<h3 align="center">Sample Project to use FastAPI with Celery and JWT authentication</h3>
</div>
<p align="center">
<a href="https://www.python.org" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a>
<a href="https://fastapi.tiangolo.com/" target="_blank"> <img src="https://styles.redditmedia.com/t5_22y58b/styles/communityIcon_r5ax236rfw961.png" alt="fastapi" width="40" height="40"/> </a>
<a href="https://www.docker.com/" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="40" height="40"/> </a>
<a href="https://www.postgresql.org" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original-wordmark.svg" alt="postgresql" width="40" height="40"/> </a>
<a href="https://git-scm.com/" target="_blank"> <img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git" width="40" height="40"/> </a>
</p>


# Development usage
You'll need to have [Docker installed](https://docs.docker.com/get-docker/).

## Clone the repo
Clone this repo anywhere you want and move into the directory:
```bash
git clone https://github.com/adeliiman/FastAPI-Copy-Trade.git
```

## Enviroment Varibales
environment variables are included in docker-compose.yml file for debugging mode and you are free to change commands inside:

```yaml
version: "3.9"
   
services:
  postgresdb:
    container_name: postgresdb
    image: postgres:15-alpine
    volumes:      
      - ./postgres/data:/var/lib/postgresql/data
    expose:
      - "5432"
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - DB_VENDOR=postgres
      - PGDATA=/var/lib/postgresql/data
    restart: always
  
  # mongodb:
  #   image: mongo:latest
  #   expose:
  #     - '27017'
  #   volumes:
  #     - ./mongodb/data:/data/db
  #     - ./mongodb/config:/data/configdb
  #   environment:
  #     - MONGO_INITDB_DATABASE=mongo
  #     - MONGO_INITDB_ROOT_USERNAME=mongo
  #     - MONGO_INITDB_ROOT_PASSWORD=mongo
  #   restart: unless-stopped


  backend:
    build: 
      context: .
      dockerfile: dockerfiles/dev/fastapi/Dockerfile
    container_name: backend
    command: sh -c "uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
    volumes:
      - ./core:/usr/src/app
    # env_file:
    # - envs/dev/fastapi/.env
    ports:
      - "8000:8000"
    environment:
      - PGDB_PORT=5432
      - PGDB_PASSWORD=postgres
      - PGDB_USERNAME=postgres
      - PGDB_DBNAME=postgres
      - PGDB_HOSTNAME=postgresdb
      - DATABASE_URL=postgresql://postgres:postgres@postgresdb:5432/postgres
      - ENABLE_SENTRY=False
      - SENTRY_DSN=None
      # - MGDB_PORT=27017
      # - MGDB_PASSWORD=mongo
      # - MGDB_USERNAME=mongo
      # - MGDB_DBNAME=mongo
      # - MGDB_HOSTNAME=mongodb
    restart: always

      
    depends_on:
      - postgresdb
      # - mongodb

  smtp4dev:
    image: rnwood/smtp4dev:v3
    restart: always
    ports:
      # Change the number before : to the port the web interface should be accessible on
      - '5000:80'
      # Change the number before : to the port the SMTP server should be accessible on
      - '25:25'
      # Change the number before : to the port the IMAP server should be accessible on
      - '143:143'
    volumes:
      # This is where smtp4dev stores the database..
      - smtp4dev-data:/smtp4dev
    environment:
      - ServerOptions__HostName=smtp4dev

volumes:
  smtp4dev-data:
```

## Build everything

*The first time you run this it's going to take 5-10 minutes depending on your
internet connection speed and computer's hardware specs. That's because it's
going to download a few Docker images and build the Python + requirements dependencies.*

```bash
docker compose up --build
```

Now that everything is built and running we can treat it like any other FastAPI
app. Visit <http://localhost:8000/swagger> in your favorite browser.


# Bugs
Feel free to let me know if something needs to be fixed. or even any features seems to be needed in this repo.

