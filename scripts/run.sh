#!/bin/bash
docker-compose up --build -d
docker exec -it api bash -c "python3 -m scripts.setup"
