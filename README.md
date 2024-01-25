## VPN SERVICE
Simple web proxy that allow to collect data management statistics.

### Prerequisites

Docker, Docker Compose must be installed.
If not, please see:

[Docker](https://docs.docker.com/engine/install/) and
[Docker compose](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-22-04)
for installation instructions.


### Installation

1. Clone the repo:
```sh
git clone https://github.com/OleksandrZhydyk/vpn_service.git
``` 

2. Run the command for building and running the images:
```sh
docker compose up -d --build
```

Create a superuser for the Django admin (Optional):
```sh
docker-compose exec vpn_service bash
python src/manage.py createsuperuser
```

### Routes
- Admin Site: http://localhost:8000/admin/
- User:
  - Register: http://localhost:8000/register/
  - Login: http://localhost:8000/login/
  - Logout: http://localhost:8000/logout/
- VPN Service:
  - Site List: http://localhost:8000/statistics/
  - Create Site: http://localhost:8000/statistics/create_site/
  - Delete Site: http://localhost:8000/statistics/delete_site/< pk >/
  - VPN Route Handler: http://localhost:8000/statistics/<site_name>/<site_url>/