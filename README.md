\# ERPNext Production Automation



Docker-based ERPNext v15 setup with a custom `production\_automation` app.



\## Setup



1\. Copy `.env.example` to `.env` and fill in values

2\. `docker compose up -d`

3\. `docker compose exec backend bench new-site production.localhost --mariadb-user-host-login-scope=% --db-root-password admin --admin-password admin`

4\. `docker compose exec backend bench --site production.localhost install-app erpnext`

5\. `docker compose exec backend bench --site production.localhost install-app production\_automation`



Open http://localhost:8080

