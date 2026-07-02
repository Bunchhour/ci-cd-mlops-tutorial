# Docker Complete Lesson Guide

> **Purpose:** A structured, hands-on learning guide derived from the Docker full course.
> **Audience:** Students and developers building CI/CD or MLOps pipelines.
> **Format:** Each lesson has a concept summary, key commands/examples, and practice exercises.

---

## Table of Contents

| Lesson | Topic |
|--------|-------|
| Lesson 1 | What is Docker & Why Use It |
| Lesson 2 | Docker vs Virtual Machine |
| Lesson 3 | Installing Docker |
| Lesson 4 | Core Concepts: Image vs Container |
| Lesson 5 | Essential Docker Commands |
| Lesson 6 | Port Binding |
| Lesson 7 | Debugging Containers |
| Lesson 8 | Docker Networks |
| Lesson 9 | Developing Locally with Docker |
| Lesson 10 | Docker Compose |
| Lesson 11 | Dockerfile & Building Custom Images |
| Lesson 12 | Private Docker Registry (AWS ECR) |
| Lesson 13 | Deploying with Docker Compose |
| Lesson 14 | Docker Volumes & Data Persistence |

---

## Lesson 1: What is Docker & Why Use It

### Learning Objectives
- Understand what a container is
- Know the problems Docker solves in development and deployment

### Concept

A **container** is a way to package an application with **everything it needs**:
- Application code
- Runtime dependencies
- Configuration files
- Environment variables
- Start scripts

Containers are **portable** — the same package runs identically on any machine.

#### Before Docker: Problems

| Problem | Impact |
|---------|--------|
| Install services directly on OS | Steps differ per OS |
| Multiple steps per service | High chance of errors |
| 10 services = 10 manual setups | Extremely tedious |
| Textual deployment instructions | Miscommunication between teams |
| Dependency version conflicts | Hard-to-debug failures |

#### With Docker: Benefits

| Benefit | How |
|---------|-----|
| One command to pull and run any service | `docker run postgres:9.6` |
| Same command on all operating systems | No OS-specific steps |
| Run multiple versions simultaneously | No conflicts |
| Everything in one image | No env config needed on servers |

### Container Repository (Docker Hub)

**Docker Hub** (hub.docker.com) is the public registry where container images live.
- 100,000+ official images: PostgreSQL, Redis, Jenkins, MongoDB, etc.
- Companies host private repositories for their own application images
- No authentication needed to pull public images

### Practice Exercise
1. Go to hub.docker.com and search for `postgres`
2. Note the official image, available tags (versions), and image size
3. Find an example of an official image vs. a community image


---

## Lesson 2: Docker vs Virtual Machine

### Learning Objectives
- Understand how the OS is structured (kernel vs applications layer)
- Know the key differences between Docker and a VM

### Concept

An operating system has **two layers**:

```
+-----------------------------------+
|         Applications              |  <- Layer 2: Apps, UI, tools
+-----------------------------------+
|          OS Kernel                |  <- Layer 1: Talks to hardware
+-----------------------------------+
```

#### What Each Technology Virtualizes

| Feature | Docker | Virtual Machine |
|---------|--------|-----------------|
| Virtualizes | Application layer only | Full OS (kernel + apps) |
| Uses host kernel | Yes | No (has its own) |
| Image size | A few MB | A few GB |
| Startup speed | Seconds | Minutes |
| Cross-OS compatibility | Limited (needs Linux kernel) | Full |

#### Compatibility Note
- Linux images require a Linux kernel host
- Windows 10+ and modern macOS: Docker runs natively
- Older Windows/Mac: Use **Docker Toolbox** (wraps Oracle VirtualBox)

### Practice Exercise
1. What layer does Docker virtualize?
2. Why are Docker images smaller than VM images?
3. If a teammate has Windows 7 — can they run Docker natively? What is the workaround?

---

## Lesson 3: Installing Docker

### Learning Objectives
- Install Docker on your operating system
- Verify Docker is running correctly

### Installation by OS

#### macOS
1. Visit docs.docker.com/get-docker
2. Download Docker Desktop (stable channel) — requires macOS 10.15+, 4 GB RAM min
3. Double-click the .dmg file, drag Docker to Applications
4. Start Docker from Applications; wait for the whale icon in the menu bar

> Note: If you use multiple macOS accounts, quit Docker before switching accounts to avoid conflicts.

#### Windows
1. Check prerequisites:
   - Windows 10 or later (required for native Docker)
   - Virtualization enabled — check via Task Manager > Performance > CPU
2. Download Docker Desktop installer from the stable channel
3. Run installer and follow the wizard
4. After install, search "Docker Desktop" and launch it (does not auto-start)

#### Linux (Ubuntu/Debian)

```bash
# 1. Update and install prerequisites
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg

# 2. Add Docker GPG key and set up stable repository
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 3. Install Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io

# 4. Verify
sudo docker run hello-world
```

#### Legacy Systems — Docker Toolbox
For systems that do not meet native Docker requirements:
1. Download Docker Toolbox from the GitHub releases page
2. Install with all default options (do NOT change anything)
3. Open Docker QuickStart Terminal from your launcher
4. Test with: `docker run hello-world`

### Verify Installation
```bash
docker --version
docker run hello-world
```


---

## Lesson 4: Core Concepts: Image vs Container

### Learning Objectives
- Clearly distinguish between an image and a container
- Understand why images use layered architecture

### Concept

| Term | Definition |
|------|-----------|
| **Image** | A static packaged artifact: the app, dependencies, config, and start script. Like a blueprint. |
| **Container** | A running instance of an image. The live environment where the app executes. |

```
Image (artifact, stored on disk, not running)
     |
     v  docker run
Container (running process with its own virtual filesystem)
```

> **Analogy:** An image is like a class in OOP. A container is a live object (instance) of that class.

#### Image Layer Structure

Docker images are built from **stacked layers**. Each Dockerfile instruction creates a layer.

```
+------------------------------+
|   App Config / Env Vars      |  <- Top layer
+------------------------------+
|   Application Code           |
+------------------------------+
|   Dependencies               |
+------------------------------+
|   Linux Base Image (Alpine)  |  <- Bottom: kept tiny (~5 MB)
+------------------------------+
```

**Why layers matter:**
- Only **changed layers** are re-downloaded when pulling a newer version
- Shared layers between image versions are reused from local cache (faster pulls)

#### Tags (Versions)
```bash
# Latest version (no tag = latest)
docker pull redis

# Specific version
docker pull redis:4.0
docker pull postgres:9.6
```

> **Best practice:** Always pin specific versions in production to avoid unexpected breakage.

### Practice Exercise
```bash
# Pull two versions of Redis
docker pull redis:latest
docker pull redis:4.0

# List all local images
docker images

# Notice both are listed, and shared layers were only downloaded once
```

---

## Lesson 5: Essential Docker Commands

### Learning Objectives
- Pull, run, stop, start, list, and remove containers and images

### Commands

#### Pulling Images
```bash
docker pull <image>:<tag>

# Examples
docker pull postgres:13
docker pull redis
```

#### Running Containers
```bash
# Foreground (attached) - blocks terminal, Ctrl+C to stop
docker run redis

# Background (detached) - terminal stays free
docker run -d redis

# Named + detached
docker run -d --name my-redis redis

# With port binding (host:container)
docker run -d -p 6000:6379 redis

# With environment variables
docker run -d \
  -e POSTGRES_PASSWORD=mysecret \
  --name my-postgres \
  postgres:13
```

> **Key difference:**
> - `docker run` = creates a brand new container from an image
> - `docker start` = restarts an already-existing stopped container

#### Listing Containers
```bash
# Only running containers
docker ps

# ALL containers (running + stopped)
docker ps -a
```

#### Stop & Start
```bash
docker stop <container_id_or_name>
docker start <container_id_or_name>
```

#### Remove Containers & Images
```bash
# Remove a stopped container
docker rm <container_id_or_name>

# Remove an image (must remove container first)
docker rmi <image_id>

# List all local images
docker images
```

### Command Flow

```
Docker Hub
    |
    v  docker pull
Local Image Cache
    |
    v  docker run  (creates NEW container each time)
Running Container
    |
    v  docker stop
Stopped Container
    |
    v  docker start  (reuses same container with its config)
Running Container
```

### Practice Exercises

**Exercise A - Container lifecycle:**
```bash
docker pull nginx
docker run -d -p 8080:80 --name my-nginx nginx

# Visit http://localhost:8080

docker stop my-nginx
docker start my-nginx
docker stop my-nginx
docker rm my-nginx
```

**Exercise B - Two versions side-by-side:**
```bash
docker run -d -p 6000:6379 --name redis-latest redis
docker run -d -p 6001:6379 --name redis-old redis:4.0
docker ps
# Both running, no conflict - they use different host ports
```


---

## Lesson 6: Port Binding

### Learning Objectives
- Understand the difference between host port and container port
- Bind ports so services are reachable from outside

### Concept

A container runs in an isolated virtual network. Without port binding, nothing can reach it from outside.

```
YOUR HOST MACHINE
+----------------------------------------------------------+
|  Host Port 6000  ----------->  Container Port 6379       |  (Redis)
|  Host Port 8080  ----------->  Container Port 80         |  (Nginx)
|  Host Port 5432  ----------->  Container Port 5432       |  (Postgres)
+----------------------------------------------------------+
```

#### Syntax
```bash
docker run -p <HOST_PORT>:<CONTAINER_PORT> <image>
```

#### Rules
- **Host ports must be unique** — two containers cannot share the same host port
- **Container ports can be the same** across containers — each container has its own isolated network
- **Without `-p`**, the container is unreachable from the host

#### Example — Two Redis containers simultaneously
```bash
# Redis latest -> accessible at localhost:6000
docker run -d -p 6000:6379 --name redis-latest redis

# Redis 4.0 -> accessible at localhost:6001
docker run -d -p 6001:6379 --name redis-old redis:4.0
```

### Practice Exercise
```bash
# Start two nginx instances on different host ports
docker run -d -p 8080:80 --name nginx-1 nginx
docker run -d -p 8081:80 --name nginx-2 nginx

# Visit http://localhost:8080 and http://localhost:8081

# Try binding a third container to the SAME host port - observe the error
docker run -d -p 8080:80 --name nginx-3 nginx
# Expected: Error - Bind for 0.0.0.0:8080 failed: port is already allocated

# Clean up
docker stop nginx-1 nginx-2 && docker rm nginx-1 nginx-2
```

---

## Lesson 7: Debugging Containers

### Learning Objectives
- View logs from running or stopped containers
- Open an interactive shell inside a container

### Commands

#### View Logs
```bash
# View all logs (snapshot)
docker logs <container_id_or_name>

# Stream logs in real time (like tail -f)
docker logs -f my-redis
```

#### Open an Interactive Shell
```bash
# Bash (most containers)
docker exec -it <container_id_or_name> /bin/bash

# Sh (Alpine-based containers that don't have bash)
docker exec -it <container_id_or_name> /bin/sh
```

Once inside the container shell:
```bash
env                    # view all environment variables
ls -la /home/app       # browse the filesystem
cat /path/to/config    # read configuration files
exit                   # leave the container shell
```

#### Naming Containers for Easy Reference
```bash
# Use --name when running to avoid working with random IDs
docker run -d -p 6001:6379 --name redis-old redis:4.0

# Use the name everywhere
docker logs redis-old
docker exec -it redis-old /bin/sh
docker stop redis-old
```

### Practice Exercise
```bash
# 1. Start postgres with env variables
docker run -d \
  -p 5432:5432 \
  -e POSTGRES_PASSWORD=secret123 \
  -e POSTGRES_USER=admin \
  --name my-db \
  postgres:13

# 2. View startup logs
docker logs my-db

# 3. Enter the container
docker exec -it my-db /bin/bash

# 4. Inside container: verify env vars
env | grep POSTGRES

# 5. Exit and clean up
exit
docker stop my-db && docker rm my-db
```

---

## Lesson 8: Docker Networks

### Learning Objectives
- Understand how containers communicate with each other
- Create and use a Docker network

### Concept

By default, each container is isolated. To allow containers to talk to each other, place them in the **same Docker network**.

```
HOST MACHINE
+-------------------------------------------------------+
|  DOCKER NETWORK: "my-app-network"                     |
|  +---------------+     +------------------------+     |
|  |  mongodb      | <-- |  mongo-express (UI)    |     |
|  |  container    |     |  container             |     |
|  +---------------+     +------------------------+     |
|         ^                                             |
|         | via localhost:27017                         |
|  Node.js app (running on HOST, outside Docker)        |
+-------------------------------------------------------+
```

#### Key Rules

| Scenario | How to Connect |
|----------|---------------|
| Container to Container (same network) | Use container name as hostname |
| Host app to Container | Use `localhost:<host_port>` |
| Container to Container (app also containerized) | Use service name from compose |

#### Commands
```bash
# Create a network
docker network create mongo-network

# List all networks
docker network ls

# Run containers in the same network
docker run -d \
  --network mongo-network \
  --name mongodb \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=secret \
  mongo

docker run -d \
  --network mongo-network \
  --name mongo-express \
  -p 8081:8081 \
  -e ME_CONFIG_MONGODB_ADMINUSERNAME=admin \
  -e ME_CONFIG_MONGODB_ADMINPASSWORD=secret \
  -e ME_CONFIG_MONGODB_SERVER=mongodb \
  mongo-express
# ME_CONFIG_MONGODB_SERVER=mongodb uses the container NAME as the hostname
```

### Practice Exercise
```bash
# 1. Create a network
docker network create test-net

# 2. Start MongoDB in the network
docker run -d --network test-net --name mongo \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=pass \
  mongo

# 3. Start Mongo Express in the SAME network
docker run -d --network test-net --name mongo-ui \
  -p 8081:8081 \
  -e ME_CONFIG_MONGODB_ADMINUSERNAME=admin \
  -e ME_CONFIG_MONGODB_ADMINPASSWORD=pass \
  -e ME_CONFIG_MONGODB_SERVER=mongo \
  mongo-express

# 4. Open http://localhost:8081 - MongoDB admin UI should load

# 5. Clean up
docker stop mongo mongo-ui && docker rm mongo mongo-ui
docker network rm test-net
```


---

## Lesson 9: Developing Locally with Docker

### Learning Objectives
- Set up a realistic local dev environment using Docker containers
- Connect a host application to containerized services

### Real-World Dev Workflow

```
LOCAL DEVELOPMENT MACHINE
+------------------------------------------------------------------+
|  Node.js App (running on host)                                   |
|      connects to --> mongodb container  (localhost:27017)        |
|                                                                  |
|  Browser                                                         |
|      connects to --> mongo-express      (localhost:8081)         |
|      connects to --> Node.js app        (localhost:3000)         |
+------------------------------------------------------------------+
```

### Step-by-Step Setup

#### Step 1 - Pull required images
```bash
docker pull mongo
docker pull mongo-express
```

#### Step 2 - Create a dedicated network
```bash
docker network create mongo-network
```

#### Step 3 - Start MongoDB
```bash
docker run -d \
  --network mongo-network \
  --name mongodb \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=password \
  mongo
```

#### Step 4 - Start Mongo Express (Admin UI)
```bash
docker run -d \
  --network mongo-network \
  --name mongoexpress \
  -p 8081:8081 \
  -e ME_CONFIG_MONGODB_ADMINUSERNAME=admin \
  -e ME_CONFIG_MONGODB_ADMINPASSWORD=password \
  -e ME_CONFIG_MONGODB_SERVER=mongodb \
  mongo-express
```

#### Step 5 - Connect your application
```javascript
// In your Node.js app (running on the HOST machine)
const mongoUri = 'mongodb://admin:password@localhost:27017';

// If your app is also containerized (same Docker network as MongoDB)
const mongoUri = 'mongodb://admin:password@mongodb:27017';
//                                          ^^^^^^^
//                            Use the container name, not localhost
```

### Practice Exercise
1. Pull `mongo` and `mongo-express`
2. Create a Docker network `dev-net`
3. Start both containers in `dev-net`
4. Open Mongo Express at http://localhost:8081
5. Create a database `userdb` with a collection `users`
6. Connect from a Node.js script using `localhost:27017`
7. Insert a document and verify it appears in Mongo Express


---

## Lesson 10: Docker Compose

### Learning Objectives
- Write a docker-compose.yml file
- Start and stop multi-container setups with single commands

### Why Docker Compose?

| Without Compose | With Compose |
|-----------------|--------------|
| Long `docker run` command per container | One YAML file for all services |
| Must remember all flags and env vars | Readable, version-controlled config |
| Manually create networks | Network created automatically |
| Multiple commands to start/stop | `docker compose up -d` / `docker compose down` |

### docker-compose.yml Structure

```yaml
version: '3'
services:
  <service-name>:           # becomes the container name AND hostname in the network
    image: <image>:<tag>
    ports:
      - "<host>:<container>"
    environment:
      - KEY=value
    depends_on:
      - <other-service>     # wait for this service to be up first
    volumes:
      - <vol-name>:<container-path>

volumes:
  <vol-name>:               # declare named volumes used above
```

### Full Example - MongoDB + Mongo Express

```yaml
version: '3'
services:
  mongodb:
    image: mongo
    ports:
      - "27017:27017"
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=password

  mongo-express:
    image: mongo-express
    ports:
      - "8081:8081"
    environment:
      - ME_CONFIG_MONGODB_ADMINUSERNAME=admin
      - ME_CONFIG_MONGODB_ADMINPASSWORD=password
      - ME_CONFIG_MONGODB_SERVER=mongodb
    depends_on:
      - mongodb
```

> No `networks:` section needed! Docker Compose automatically creates a shared network for all services.

### Key Commands

```bash
# Start all services in background
docker compose up -d

# Stop and remove all containers + networks
docker compose down

# View logs of all services
docker compose logs

# View logs of one specific service
docker compose logs mongodb

# List running compose services
docker compose ps
```

### Practice Exercise
1. Create `docker-compose.yml` with the MongoDB + Mongo Express example above
2. Run `docker compose up -d`
3. Run `docker network ls` - find the auto-created network
4. Open http://localhost:8081 - admin UI should load
5. Run `docker compose down` and verify all containers and network are removed


---

## Lesson 11: Dockerfile & Building Custom Images

### Learning Objectives
- Write a Dockerfile to package your own application
- Build, tag, and run a custom Docker image

### Concept

A Dockerfile is a text script of instructions that Docker reads to build a custom image.

```
Source Code + Dockerfile
        |
        v  docker build
  Custom Docker Image
        |
        v  docker run
     Container
```

### Dockerfile Instructions

| Instruction | Purpose | Example |
|-------------|---------|---------|
| FROM | Base image to start from | `FROM node:18-alpine` |
| WORKDIR | Set working directory inside the image | `WORKDIR /home/app` |
| COPY | Copy files from host into image | `COPY package*.json ./` |
| RUN | Execute a shell command during build | `RUN npm install` |
| ENV | Set environment variables | `ENV NODE_ENV=production` |
| EXPOSE | Document which port the app uses | `EXPOSE 3000` |
| CMD | Default command when container starts | `CMD ["node", "server.js"]` |

### Example Dockerfile - Node.js App

```dockerfile
# 1. Start from a lightweight Node.js base image
FROM node:18-alpine

# 2. Set the working directory inside the container
WORKDIR /home/app

# 3. Copy package files FIRST (enables Docker layer caching for npm install)
COPY package*.json ./

# 4. Install dependencies (only re-runs if package.json changed)
RUN npm install

# 5. Copy the rest of the application code
COPY . .

# 6. Set environment variables
ENV MONGO_DB_USERNAME=admin \
    MONGO_DB_PWD=password

# 7. Expose the application port
EXPOSE 3000

# 8. Start the application
CMD ["node", "server.js"]
```

> **Layer Caching Tip:** Copy package.json and run npm install BEFORE copying all source files.
> This way, npm install only re-runs when dependencies change, not on every code edit.

### Build and Run Commands

```bash
# Build image from Dockerfile in current directory
docker build -t my-app:1.0 .
#            -t = name:tag
#            .  = build context (current directory)

# List images to verify your new image appears
docker images

# Run your image
docker run -d -p 3000:3000 --name my-app my-app:1.0

# After modifying Dockerfile or code - rebuild:
docker stop my-app
docker rm my-app
docker rmi my-app:1.0
docker build -t my-app:2.0 .
```

### Practice Exercise

1. Create `server.js`:
```javascript
const http = require('http');
const server = http.createServer((req, res) => {
  res.writeHead(200);
  res.end('Hello from Docker!');
});
server.listen(3000, () => console.log('Listening on port 3000'));
```

2. Create `package.json`:
```json
{
  "name": "my-docker-app",
  "version": "1.0.0",
  "main": "server.js"
}
```

3. Write a `Dockerfile` using the example above

4. Build and run:
```bash
docker build -t my-app:1.0 .
docker run -d -p 3000:3000 --name my-app my-app:1.0
```

5. Visit `http://localhost:3000` - should show "Hello from Docker!"

6. Inspect the container:
```bash
docker exec -it my-app /bin/sh
ls /home/app     # verify files were copied
env              # verify ENV vars are set
exit
```


---

## Lesson 12: Private Docker Registry (AWS ECR)

### Learning Objectives
- Create a private registry on AWS ECR
- Tag, authenticate, and push an image
- Pull from ECR on a remote server

### Why a Private Registry?

Your app image built by CI/CD (Jenkins, GitHub Actions, etc.) must be stored somewhere:
- Private - no public access to your proprietary code
- Accessible by dev/staging/prod servers
- Versioned via image tags

Common options: AWS ECR, Azure ACR, Google GCR, GitHub GHCR, Docker Hub (private), Nexus, Harbor.

### AWS ECR Workflow

#### Step 1: Create a repository in AWS Console
```
AWS Console -> Elastic Container Registry -> Create Repository
  Name: my-app
```
> In AWS ECR, each image gets its own repository. Different versions (tags) live inside it.

#### Step 2: Authenticate Docker with ECR
```bash
# Replace <account-id> and <region>
aws ecr get-login-password --region us-east-1 \
  | docker login --username AWS --password-stdin \
    <account-id>.dkr.ecr.us-east-1.amazonaws.com
```

#### Step 3: Tag your image with the ECR URL
```bash
# Format: <registry-url>/<repo-name>:<tag>
docker tag my-app:1.0 \
  <account-id>.dkr.ecr.us-east-1.amazonaws.com/my-app:1.0
```

#### Step 4: Push the image
```bash
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/my-app:1.0
```

#### Step 5: On a server - pull the image
```bash
# Authenticate first
aws ecr get-login-password --region us-east-1 \
  | docker login --username AWS --password-stdin \
    <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Pull the image
docker pull <account-id>.dkr.ecr.us-east-1.amazonaws.com/my-app:1.0
```

### Practice Exercise
1. Create an ECR repository named `my-docker-app` in the AWS console
2. Authenticate your local Docker to ECR
3. Tag your `my-app:1.0` image with the full ECR repository URL
4. Push the image
5. Verify it appears in the ECR console with the correct tag

---

## Lesson 13: Deploying with Docker Compose

### Learning Objectives
- Write a production docker-compose.yml that includes your custom image
- Deploy all services on a remote server with one command

### Production Docker Compose File

On a dev/staging server, you run your app image (from private ECR) alongside public dependencies.

```yaml
version: '3'
services:

  # Your custom application - pulled from private ECR
  my-app:
    image: <account-id>.dkr.ecr.us-east-1.amazonaws.com/my-app:1.0
    ports:
      - "3000:3000"
    environment:
      - MONGO_DB_USERNAME=admin
      - MONGO_DB_PWD=password
    depends_on:
      - mongodb

  # MongoDB - pulled from public Docker Hub
  mongodb:
    image: mongo
    ports:
      - "27017:27017"
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=password
    volumes:
      - mongo-data:/data/db

  # Admin UI - optional but useful
  mongo-express:
    image: mongo-express
    ports:
      - "8081:8081"
    environment:
      - ME_CONFIG_MONGODB_ADMINUSERNAME=admin
      - ME_CONFIG_MONGODB_ADMINPASSWORD=password
      - ME_CONFIG_MONGODB_SERVER=mongodb
    depends_on:
      - mongodb

volumes:
  mongo-data:
```

### Deployment Steps on a Server

```bash
# 1. Authenticate to ECR to enable pulling private images
aws ecr get-login-password --region us-east-1 \
  | docker login --username AWS --password-stdin \
    <account-id>.dkr.ecr.us-east-1.amazonaws.com

# 2. Copy or create docker-compose.yml on the server

# 3. Start all services
docker compose up -d

# 4. Verify everything is running
docker ps

# 5. Watch the logs
docker compose logs -f
```

### Important: DB Connection URL Inside a Container

When your app runs **inside Docker** (not on the host), change `localhost` to the **MongoDB service name**:

```javascript
// WRONG - only works when app runs on the host directly
const uri = 'mongodb://admin:password@localhost:27017';

// CORRECT - works when app is inside a Docker container on the same compose network
const uri = 'mongodb://admin:password@mongodb:27017';
//                                      ^^^^^^^^
//       This is the service name defined in docker-compose.yml
```

Docker Compose puts all services on the same network, so the service name acts as the hostname.


---

## Lesson 14: Docker Volumes & Data Persistence

### Learning Objectives
- Understand why containers lose data on restart
- Use named volumes to persist database data

### The Problem: No Persistence by Default

A container's file system is virtual and temporary. When a container is removed, all data inside is permanently lost.

```
Container created  ->  data written to virtual filesystem
Container removed  ->  virtual filesystem deleted  ->  DATA IS GONE
New container      ->  starts with empty filesystem again
```

This is critical for databases: MongoDB, PostgreSQL, MySQL, Redis all store files that must persist.

### Docker Volumes - The Solution

A Docker Volume mounts a host directory into the container's virtual filesystem. Data syncs in both directions.

```
HOST MACHINE                          CONTAINER
/var/lib/docker/volumes/              /data/db
  mongo-data/_data/    <==========>   (MongoDB stores data files here)
```

When the container restarts (even after docker rm), data is restored from the host-side volume.

### Three Volume Types

| Type | Syntax | Host Path | Best For |
|------|--------|-----------|----------|
| Host Volume | `-v /host/path:/container/path` | You choose | Dev - specific paths |
| Anonymous Volume | `-v /container/path` | Docker auto-assigns | Rarely useful |
| Named Volume (recommended) | `-v my-vol:/container/path` | Docker manages | Production use |

> Use Named Volumes in production. Docker manages the storage location. You reference volumes by name, not path.

### Using Named Volumes

#### With docker run:
```bash
docker run -d \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=password \
  -v mongo-data:/data/db \
  --name mongodb \
  mongo
```

#### With Docker Compose (recommended):
```yaml
version: '3'
services:
  mongodb:
    image: mongo
    ports:
      - "27017:27017"
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=password
    volumes:
      - mongo-data:/data/db       # named-volume : container-path

  my-mysql:
    image: mysql
    environment:
      - MYSQL_ROOT_PASSWORD=secret
    volumes:
      - mysql-data:/var/lib/mysql  # separate named volume for MySQL

volumes:
  mongo-data:     # declare ALL named volumes used above here
  mysql-data:
```

### Common Database Data Paths

| Database | Data Path Inside Container |
|----------|---------------------------|
| MongoDB | `/data/db` |
| MySQL / MariaDB | `/var/lib/mysql` |
| PostgreSQL | `/var/lib/postgresql/data` |
| Redis | `/data` |

### Practice Exercise - Prove Data Persists

```bash
# 1. Start MongoDB WITH a named volume
docker run -d \
  -p 27017:27017 \
  -v mongo-data:/data/db \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=password \
  --name test-mongo \
  mongo

# 2. Open Mongo Express (or use mongosh) and insert some documents into a collection

# 3. Completely DESTROY the container
docker stop test-mongo
docker rm test-mongo

# 4. Create a BRAND NEW container using the SAME named volume
docker run -d \
  -p 27017:27017 \
  -v mongo-data:/data/db \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=password \
  --name test-mongo-2 \
  mongo

# 5. Verify your data is still there
# The named volume persisted the data even though the container was removed
```

---

## Quick Reference Cheat Sheet

### Images
```bash
docker images                                    # List local images
docker pull <image>:<tag>                        # Download from registry
docker rmi <image_id>                            # Delete local image
docker build -t <name>:<tag> .                   # Build from Dockerfile in current dir
docker tag <image> <registry>/<repo>:<tag>       # Tag for push to registry
docker push <registry>/<repo>:<tag>              # Push image to registry
```

### Containers
```bash
docker run -d -p <host>:<cont> --name <n> <img>  # Create and start container
docker ps                                         # List running containers
docker ps -a                                      # List all (including stopped)
docker stop <id|name>                             # Stop a container
docker start <id|name>                            # Restart a stopped container
docker rm <id|name>                               # Delete a container
```

### Debugging
```bash
docker logs <id|name>               # View container logs
docker logs -f <id|name>            # Follow/stream logs in real time
docker exec -it <id|name> /bin/bash # Open bash shell inside container
docker exec -it <id|name> /bin/sh   # Open sh shell (Alpine containers)
```

### Networks
```bash
docker network create <name>        # Create a new network
docker network ls                   # List all networks
docker network rm <name>            # Delete a network
```

### Docker Compose
```bash
docker compose up -d                # Start all services in background
docker compose down                 # Stop and remove containers + network
docker compose logs                 # View all service logs
docker compose logs <service>       # View logs of one service
docker compose ps                   # List compose-managed services
```

### Volumes
```bash
docker volume ls                    # List all volumes
docker volume inspect <name>        # Show volume details and mount path
docker volume rm <name>             # Delete a volume
```

---

## Full Project Workflow Summary

```
STEP 1 - DEVELOP LOCALLY
  docker pull mongo / redis / postgres      <- pull service dependencies
  docker compose up -d                      <- start everything with one command
  code your app, connect via localhost

STEP 2 - PACKAGE YOUR APP
  Write Dockerfile
  docker build -t my-app:1.0 .

STEP 3 - PUSH TO PRIVATE REGISTRY
  docker tag my-app:1.0 <ecr-url>/my-app:1.0
  docker push <ecr-url>/my-app:1.0

STEP 4 - DEPLOY TO SERVER
  docker login    (authenticate to private registry)
  copy docker-compose.yml to server
  docker compose up -d

STEP 5 - PERSIST DATA
  Add named volumes in docker-compose.yml for all stateful containers
```

---

## Further Learning Resources

| Topic | Resource |
|-------|----------|
| Docker Official Docs | https://docs.docker.com |
| Docker Hub | https://hub.docker.com |
| AWS ECR Docs | https://docs.aws.amazon.com/ecr/ |
| Docker Compose Reference | https://docs.docker.com/compose/compose-file/ |
| Dockerfile Reference | https://docs.docker.com/engine/reference/builder/ |
| Dockerfile Best Practices | https://docs.docker.com/develop/develop-images/dockerfile_best-practices/ |

---

*Lesson guide converted from the Docker full course transcript.*
*Work through each lesson and complete every practice exercise to build real-world Docker confidence.*
