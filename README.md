# HacktivityReport
## Overview
This telegram bot was created to collect hacktivity reports from different platforms (currently it supports only Hackerone) and send it to the end user in Telegram.

## Setup
<details><summary><h3>Already deployed Telegram bot</h3></summary>
<p>

[![Telegram](https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Telegram_2019_Logo.svg/30px-Telegram_2019_Logo.svg.png)](https://t.me/HacktivityReports_bot)

**NB:** This telegram bot deployed using the free version of [Render](https://render.com/) and it has some limitations. The main issue is that PostgreSQL database will be removing every 90 days. So after each 90 days I will be recreate a new database and beacause of this you may get old reports.
  
  
</p>
</details>
<details><summary><h3>Docker container</h3></summary>
<p>

1. Install [Docker](https://www.docker.com/)
2. Create new bot in Telegram using [BotFather](https://t.me/BotFather)
3. Install [ngrok](https://ngrok.com/) or any other local tunneling tool and run it.
4. Clone the repository with `git clone https://github.com/Vorshik/HacktivityReport.git`.
5. Go into a cloned folder with `cd HacktivityReport`.
6. Create new **.env** file in this folder with the content as in the [.env_example](.env_example) file.
![Image_env](https://user-images.githubusercontent.com/58830879/190621889-52106519-957e-4bf7-a50d-815b47f627ab.png)
7. Create a docker volume with `docker volume create dbBackup` to avoid duplicates in case docker stops.
8. Use `docker image build -t hacktivity .`. 
9. Use `docker run --rm --env-file=.env -v dbBackup:/HacktivityReport/bot/database/ -p <PORT_specified_in_the_tunneling_tool>:8000  hacktivity`
10. Send command **/start** to telegram bot.
 
</p>
</details>
<details><summary><h3>From sources</h3></summary>
<p>

1. Create new bot in Telegram using [BotFather](https://t.me/BotFather).
2. Install [ngrok](https://ngrok.com/) or any other local tunneling tool and run it.
3. Install [pipenv](https://pipenv.pypa.io/en/latest/).
4. Clone the repository with `git clone https://github.com/Vorshik/HacktivityReport.git`.
5. Go into a cloned folder with `cd HacktivityReport`.
6. Create new **.env** file in this folder with the content as in the [.env_example](.env_example) file.
![Image_env](https://user-images.githubusercontent.com/58830879/190621889-52106519-957e-4bf7-a50d-815b47f627ab.png)
7. Run `pipenv install` to install all dependences and create virtual environment.
8. Run `pipenv shell` activate this project's virtualenv.
9. In virtualenv run `flask db upgrade` to create a database and apply the migration to the database.
10. In virtualenv run `gunicorn -b 127.0.0.1:<PORT_specified_in_the_tunneling_tool> --timeout 0 app:app` to run the application.
11. Send command **/start** to telegram bot.
 
</p>
</details>


