# Docker example to run redis and package your flask app


### To begin
- Create a Github repo ***dockfunda*** **`WITH README.md checked`**
- Create codespaces on main
- Clone starter
  ```
  git clone https://github.com/ckechios/docker-bootstrap.git
  ```
- Move all files from docker-bootstrap to current working directory
  ```
  mv docker-bootstrap/{,.[^.]}* .
  ```
  - Run above first then
  ```
  rm -rf docker-bootstrap/
  ```

- ### Run Python app
  ```
  pip install -r requirements.txt
  ```
- ### DockerHub
  - > https://hub.docker.com/_/hello-world/
- ### Docker commands
  ```
    docker pull
    docker run
    docker ps
    docker ps -a
    docker ps -aq
    docker stop ech-redis
    docker rm [container-id]
    docker rm ech-redis
    docker images
    docker rm -f $(docker ps -aq)
    docker network ls
  ```
- ### Run Redis server using Docker
  - Run Redis
  - Remove container
  - Rerun to observe data loss
  - Run with mounted volume to show persistence
  - Redis commands reference
  ```
  # Redis commands
  docker run --name ech-redis -p 6379:6379 -d redis
  docker exec -it [redis-container-id] bash
  # in container
  redis-cli
  GET *
  SCAN 0
  KEYS user:c*
  GET user:ck@abc.com    
  
  # with persistence
  docker run --name ech-redis -p 6379:6379 -v $(pwd)/redisdata:/data -d redis --appendonly yes

  ```
- ### URL routes for Python app
  - add_user?email=cian@abc.com&name=cian
  - add_user?email=charles@abc.com&name=charles
  - add_user?email=anna@abc.com&name=Anna
  - search?email=charles@abc.com
  - search?email=cian@abc.com
  - search?email=anna@abc.com
  - get_emails
  - emailbegins?email=a

- ### Dockerize Python app
  - Build Docker Image Python app with Dockerfile
  - Run above app with port exposed, to fail db connection
  - Use Docker Compose to run both Python and Redis in same network
  - Command reference
  ```
  docker build -t echpyred .
  docker run -p 5000:5000 echpyred
  ```

- ### Notes
  - CMD : can override when running image
  - ENTRYPOINT : can not be overridden when container runs. Will always run first
  - Option 2 for importing
    ```
    git remote add start https://github.com/ckechios/docker-bootstrap.git 
    git fetch start
    git merge start/main --allow-unrelated-histories 
    git remote remove start
    ```
  - Resolve conflicts in README.md, accept incoming.
