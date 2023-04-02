# Hire And Learn Django Project

# How To Deploy

```
    If you are Windows user, clone this project using following command -
    git clone https://github.com/someuser/somerepo --config core.autocrlf=false
    Or try another ways to turn off autocrlf
```

0. clone this repository
1. install docker & docker-compose
2. cd to folder where manage.py is living
3. run

```
    docker-compose up --build
    It will take no more than 20 seconds.
```
4. Visit - http://localhost:8000

# Project Ideas

- Add Rabbit as messaging broker to send E-mail for newly registered users.
- Restore JWT2 Authentication with Google
- Make Pivottable more usable and informative 
- Add new app - FreeResources which syncs all tech newses/resources From Georgian market
- Where possible, optimize queries to make retrievals fast
- Add celery for sync processes
- Integrate test payment APIs (BOG/TBC)
- Make naming files more efficient for usage
- Integrate ASG Interface in the whole project, to be notified anywhere if someone messages you.
- Deploy project on Linode.

# Important
- Fix ASGI
