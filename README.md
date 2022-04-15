# Django test project

The idea of the site is to make a digital building management system.

## Test data users

The password for all users: admin123123

User emails:

| email | account type |
| --- | --- |
| todor.zhivkov@bkp.com | superuser |
| jeffrey.dahmer@killer.com | manager |
| edmund.kemper@killer.com | manager |
| mikhail.popkov@killer.com | manager |
| katherine.knight@killer.com | manager |
| andrei.chikatilo@killer.com | user |

## Loading the sample data

You need to create a **.env** file in the project dir with the following variables (example):

```env
DEBUG='False'
APP_ENVIRONMENT='PROD'
DB_HOST='db'
DB_NAME='proprietor'
DB_USER='milen'
DB_PASSWORD='ebiMuMamata'
NGINX_HOST='0.0.0.0'
NGINX_PORT='8080'
PROD_HOST='app'
```

Then, spin up the containers:

```bash
docker-compose up -d --build
```

To check the application logs:

```bash
docker logs -f proprietor_app_1
```
