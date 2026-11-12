# Docker — Complete Learning Notes

A comprehensive guide to Docker, covering containerization, architecture, images, containers, Dockerfiles, networking, storage, Docker Compose, Swarm and CI/CD.

Examples throughout this document use a sample **Resume Analyzer / Iris ML application**.

---

# 1. What is Docker?

Docker is a containerization platform that allows us to package an application along with its required dependencies, libraries, runtime and configuration into a portable unit called a **Docker Image**.

This helps applications run consistently across different environments.

### The problem Docker solves

Imagine developing a Resume Analyzer application on your laptop.

Your application requires:

- Python 3.11
- Streamlit
- Scikit-learn
- Pandas
- PDFMiner
- Other dependencies

Everything works perfectly on your laptop.

Now, you deploy the application to a company server. However, the server has a different Python version or incompatible library versions.

The application might fail.

Docker helps solve this problem by packaging the application and its required environment into an image.

The same image can then be used to create containers on different machines that support Docker.

**Main idea:** Docker helps maintain a consistent application environment across development, testing and deployment.

Note: Docker improves portability and consistency, but does not automatically package every external dependency. Databases, credentials, mounted files and external services may still need separate configuration.

### Advantages of Docker

- **Portability:** Run the same packaged application in different supported environments.
- **Consistency:** Reduce environment-related differences.
- **Isolation:** Applications can run in separate containers.
- **Scalability:** Run multiple containers of an application.
- **Reproducibility:** Pin runtime and dependency versions.
- **CI/CD integration:** Automate image building and deployment.

---

# 2. Docker Architecture

Docker follows a client-server architecture.

Its major components are:

1. Docker Client
2. Docker Daemon
3. Docker Image
4. Docker Container
5. Docker Registry

![Docker Architecture — Client, Docker Host and Registry](https://docs.docker.com/get-started/images/docker-architecture.webp)

*Source: [Docker Official Documentation — Docker Architecture](https://docs.docker.com/get-started/docker-overview/)*

### 2.1 Docker Client

The Docker Client is the interface through which we interact with Docker.

We generally use the Docker CLI to execute commands.

Examples:

```bash
docker build -t iris-ml-app .
docker run iris-ml-app
docker ps
```

The client sends requests to the Docker Daemon.

### 2.2 Docker Daemon

The Docker Daemon (`dockerd`) is the background service responsible for managing Docker resources.

It handles:

- Building images.
- Creating and running containers.
- Managing networks.
- Managing volumes.
- Pulling and managing images.

The daemon processes instructions from the Docker Client.

### 2.3 Docker Image

A Docker Image is a read-only template used to create containers.

It can contain:

- Base image filesystem components.
- Runtime such as Python.
- Required libraries and dependencies.
- Application source code.
- Model artifacts.
- Default startup configuration.

Example:

```text
iris-ml-app:v1
```

An image is a packaged collection of filesystem layers and image configuration.

### 2.4 Docker Container

A container is a running instance of a Docker Image.

For example:

```bash
docker run iris-ml-app
```

Docker creates and starts a container using the image.

Important points:

- One image can create multiple containers.
- Containers are isolated from one another.
- Each container has its own writable layer.
- Changes inside a container do not normally change the original image.
- A container runs while its main process is running.

### 2.5 Docker Registry

A Docker Registry stores and distributes Docker images.

Docker Hub is a commonly used public registry.

Example:

```bash
docker pull python:3.11
```

This downloads the Python image from the default registry if it is not already available locally.

We can also push our own images to a registry.

```bash
docker push username/iris-ml-app:v1
```

### Architecture summary

```text
             Docker Client
                  |
                  | Docker commands
                  v
             Docker Daemon
              /    |     \
             /     |      \
         Images Containers Networks
             |
             v
        Docker Registry
          (Docker Hub)
```

---

# 3. Docker Host, Image and Container

### Docker Host

A Docker Host is the machine on which Docker runs and manages containers.

It could be:

- Our laptop.
- A company server.
- An AWS EC2 instance.
- Another cloud virtual machine.

The Docker Engine runs on the host and manages containers.

### Difference between Image and Container

| Docker Image | Docker Container |
|---|---|
| Template | Running instance |
| Read-only image layers | Has a writable layer |
| Used to create containers | Executes the application |
| Can create multiple containers | Runs the application process |

Example:

```bash
docker run -d --name app1 iris-ml-app
docker run -d --name app2 iris-ml-app
```

Both containers are created from the same image.

---

# 4. Dockerfile

A Dockerfile is a text file containing instructions that Docker uses to build an image.

It tells Docker:

- Which base image to use.
- Where to work inside the image.
- Which dependencies to install.
- Which project files to copy.
- What command to execute when the container starts.

### Example project structure

```text
Week8_MLOps_HandsOn/
│
├── data/
├── src/
├── artifacts/
├── configs/
├── app/
├── main.py
├── requirements.txt
├── Dockerfile
└── .dockerignore
```

### Sample Dockerfile

```dockerfile
# Base Python image
FROM python:3.11

# Set working directory inside the image
WORKDIR /app

# Copy dependency file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Start the application
CMD ["python", "main.py"]
```

Note: The CMD above is a placeholder for a simple Python entry point. For a FastAPI application, the command could instead be:

```dockerfile
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

The actual command depends on the application's entry point and module structure.

### Dockerfile instructions

| Instruction | Purpose |
|---|---|
| FROM | Selects a base image |
| WORKDIR | Sets the working directory |
| COPY | Copies files into the image |
| RUN | Executes commands during image building |
| CMD | Specifies the default startup command |
| EXPOSE | Documents the intended container port |
| ENV | Sets environment variables |
| ENTRYPOINT | Defines the main executable |

### Understanding each instruction

**FROM**

```dockerfile
FROM python:3.11
```

Uses an existing Python 3.11 image as the base.

**WORKDIR**

```dockerfile
WORKDIR /app
```

Sets `/app` as the working directory inside the image.

It is not the same as the project's `app/` directory on our laptop.

**COPY**

```dockerfile
COPY requirements.txt .
```

Copies the project's `requirements.txt` into the current working directory inside the image.

**RUN**

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

Executes the dependency installation during image building.

**CMD**

```dockerfile
CMD ["python", "main.py"]
```

Specifies the default command to execute when a container starts.

CMD is not executed during the image build.

---

# 5. Docker Build Context

The build context is the set of files and directories made available to Docker during an image build.

Example:

```bash
docker build -t iris-ml-app .
```

Here:

- `docker build` builds an image.
- `-t` assigns a name or tag.
- `iris-ml-app` is the image name.
- `.` represents the current directory as the build context.

Docker uses the Dockerfile and the build context to build the image.

By default, Docker looks for a file named `Dockerfile` in the build context's root.

### .dockerignore

The `.dockerignore` file excludes unnecessary files from the build context.

Example:

```dockerignore
.venv/
.git/
__pycache__/
*.pyc
.env
```

Why use it?

- Avoid copying unnecessary files.
- Reduce the build context size.
- Avoid including local virtual environments.
- Avoid accidentally copying secrets.

Important: `.dockerignore` prevents matching files from entering the build context. It does not remove files that were already copied in earlier image layers or automatically secure external credentials.

---

# 6. Docker Image Layers and Caching

Docker images are composed of filesystem layers and image configuration.

Certain Dockerfile instructions, such as RUN and COPY, generally create filesystem layers.

The final image combines the results of these layers.

### Example

```dockerfile
FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

Think of it this way:

- Base image provides the Python environment.
- Dependency installation adds the required libraries.
- Project copy adds our application files.
- CMD defines the default startup command.

Not every instruction creates a filesystem layer. CMD, for example, sets image configuration rather than adding a filesystem layer.

### Docker caching

Docker can reuse results from earlier build steps when the relevant instruction and its inputs have not changed.

Consider:

```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

Suppose only `main.py` changes.

Docker can reuse the dependency installation result and execute the final COPY step again.

But if `requirements.txt` changes, Docker must rerun the dependency installation step and the subsequent affected steps.

### Why copy requirements first?

This ordering improves build efficiency.

Dependencies generally change less frequently than application code.

By copying the dependency file first, Docker can reuse the dependency installation result when only source code changes.

---

# 7. Docker Hub and Base Images

Docker Hub is a registry where developers can publish and download Docker images.

Example:

```dockerfile
FROM python:3.11
```

Here:

- `python` is the image name.
- `3.11` is its tag.

Docker first checks its local image cache. If the required image is missing, it can pull it from the configured registry.

We can manually download an image using:

```bash
docker pull python:3.11
```

### Base Image vs Our Application Image

```text
Official Python Image
        |
        v
Install dependencies
        |
        v
Copy application code
        |
        v
Our Application Image
```

For example:

```text
python:3.11       -> Existing base image
iris-ml-app:v1    -> Our custom application image
```

---

# 8. Building and Running Docker Containers

### Build an image

Run this command from the project root:

```bash
docker build -t iris-ml-app .
```

This builds an image named `iris-ml-app`.

### Run a container

```bash
docker run iris-ml-app
```

This creates and starts a new container from the image.

### Run in detached mode

```bash
docker run -d iris-ml-app
```

`-d` runs the container in the background.

### Give a container a name

```bash
docker run -d --name resume-analyzer iris-ml-app
```

### Interactive mode

```bash
docker run -it python:3.11 bash
```

- `-i` keeps standard input open.
- `-t` allocates a terminal.

### Automatically remove a container after it exits

```bash
docker run --rm python:3.11 python --version
```

`--rm` automatically removes the container after it exits.

### Useful container commands

```bash
# Show running containers
docker ps

# Show all containers, including stopped ones
docker ps -a

# Stop a container
docker stop resume-analyzer

# Start an existing stopped container
docker start resume-analyzer

# Restart a container
docker restart resume-analyzer

# Remove a stopped container
docker rm resume-analyzer
```

Important distinctions:

- `docker run` creates a new container and starts it.
- `docker stop` stops an existing container.
- `docker start` starts an existing stopped container.
- `docker rm` removes a stopped container.

---

# 9. Port Mapping

Applications running inside containers often expose services through ports.

For example:

| Application | Common default port |
|---|---:|
| Streamlit | 8501 |
| FastAPI / Uvicorn | 8000 |
| React development server | 3000 |
| MongoDB | 27017 |

These are common defaults, not mandatory ports.

### What is port mapping?

Port mapping connects a port on the Docker Host to a port inside a container.

Syntax:

```bash
docker run -p HOST_PORT:CONTAINER_PORT image-name
```

Example:

```bash
docker run -d -p 8501:8501 iris-ml-app
```

Here:

- Host port = 8501
- Container port = 8501

We can access the application through:

```text
http://localhost:8501
```

### Can host and container ports differ?

Yes!

```bash
docker run -d -p 9000:8501 iris-ml-app
```

Here:

- Host port = 9000
- Container port = 8501

Access the application using:

```text
http://localhost:9000
```

The container port must match the port on which the application listens.

### EXPOSE vs -p

```dockerfile
EXPOSE 8501
```

EXPOSE documents the intended container port.

It does not publish the port to the host.

To publish it, use:

```bash
docker run -p 8501:8501 iris-ml-app
```

### Accessing a container from another machine

Suppose the application runs on a cloud server.

Its public IP is:

```text
52.10.20.30
```

If we run:

```bash
docker run -d -p 9000:8501 iris-ml-app
```

A remote user may access it through:

```text
http://52.10.20.30:9000
```

Requirements:

- The server must be reachable.
- The application's server must listen on an appropriate interface, commonly `0.0.0.0` inside the container.
- The cloud firewall/security group must allow the required incoming port.
- The container must be running.

The user accesses the application through the network. They do not automatically get direct access to the container's filesystem.

---

# 10. Docker Volumes

### The problem

Suppose our Resume Analyzer allows users to upload resumes.

The application stores uploaded files inside the container:

```text
/app/uploads/
```

What happens if we remove the container?

The files stored only in the container's writable layer may be lost.

We need persistent storage.

### What is a Docker Volume?

A Docker Volume is persistent storage managed by Docker.

It allows data to survive container removal and recreation, provided the volume itself is retained.

### Create a volume

```bash
docker volume create resume_data
```

### Attach a volume to a container

```bash
docker run -d \
  --name resume-analyzer \
  -v resume_data:/app/uploads \
  iris-ml-app
```

Here:

- `resume_data` = Docker-managed volume.
- `/app/uploads` = Mount location inside the container.

Files written inside `/app/uploads` are stored in the volume.

If we remove the container and create another container using the same volume, the files remain available.

### Important commands

```bash
docker volume ls
docker volume inspect resume_data
docker volume rm resume_data
```

Removing a container does not automatically remove a named volume.

Removing the volume itself can delete the data stored in it.

---

# 11. Bind Mounts

A Bind Mount connects a specific directory or file on the Docker Host to a location inside a container.

Unlike a named volume, we explicitly specify the host path.

### Example

Suppose our project is located at:

```text
C:\Users\PalCh004\Week8_MLOps_HandsOn
```

We can mount it inside a container:

```bash
docker run -v "C:\Users\PalCh004\Week8_MLOps_HandsOn:/app" iris-ml-app
```

Here:

- Host directory = `C:\Users\PalCh004\Week8_MLOps_HandsOn`
- Container directory = `/app`

Changes made to shared files can be reflected on both sides.

### Why use Bind Mounts?

They are useful during development.

For example:

- Edit Python code on our laptop.
- The updated code becomes visible inside the container.
- We can avoid rebuilding the image for every source-code edit, provided the application supports reloading.

Note: Mounting the whole project directory over `/app` can hide files already present at `/app` in the image while the mount is active.

### Volumes vs Bind Mounts

| Docker Volume | Bind Mount |
|---|---|
| Managed by Docker | Uses a specific host path |
| Docker manages its storage location | User specifies source location |
| Useful for persistent application data | Useful for development and sharing files |
| Can survive container deletion | Host files remain according to normal host filesystem behavior |

---

# 12. Environment Variables

Applications often require configuration values.

Examples:

- Database connection strings.
- Application ports.
- Environment names.
- API endpoints.

Hardcoding these values into source code is not a good practice.

### Example

Instead of writing:

```python
MONGO_URI = "mongodb://username:password@host"
```

We can use:

```python
import os

MONGO_URI = os.getenv("MONGO_URI")
```

When running the container:

```bash
docker run -e MONGO_URI="mongodb://database:27017" iris-ml-app
```

Here:

- `-e` passes an environment variable.
- `MONGO_URI` is its name.
- The connection string is its value.

### Why is this useful?

We can use the same Docker image in different environments.

| Environment | Database |
|---|---|
| Development | Development database |
| Testing | Testing database |
| Production | Production database |

We simply provide different configuration values when starting the container.

---

# 13. Docker Secrets

Applications also require sensitive information:

- Database passwords.
- API keys.
- Authentication tokens.
- Credentials.

These should not be hardcoded into source code or Dockerfiles.

Docker Secrets provide a mechanism for storing and delivering sensitive values to authorized services.

### Docker Swarm example

Create a secret:

```bash
echo "my_database_password" | docker secret create mongo_password -
```

An authorized Swarm service can access the secret inside its container as a file:

```text
/run/secrets/mongo_password
```

Python can read it:

```python
with open("/run/secrets/mongo_password", "r") as file:
    password = file.read().strip()
```

### Environment Variables vs Secrets

| Environment Variables | Docker Secrets |
|---|---|
| General configuration | Sensitive information |
| Example: APP_PORT=8000 | Example: Database password |
| Passed as environment values | Made available to authorized services |
| Supported by normal Docker containers | Native Docker Secrets feature is for Swarm services |

Important:

Docker Secrets are a Docker Swarm feature. They are not automatically available to every ordinary container started with `docker run`.

Environment variables are not automatically secure. Sensitive values may be exposed through container configuration, logs or process inspection.

For production systems, companies may also use external secret managers such as HashiCorp Vault and cloud secret-management services.

---

# 14. Docker Networking

### Why do we need networking?

Consider a full-stack Resume Analyzer:

```text
Frontend
   |
   v
Backend
   |
   v
MongoDB
```

We may run each component in a separate container.

The frontend needs to communicate with the backend, and the backend needs to communicate with MongoDB.

Docker Networking enables this communication.

### Docker Host

The Docker Host is the machine running Docker and its containers.

It could be our laptop or a cloud server.

### Bridge Network

A bridge network allows containers on the same Docker Host to communicate.

We commonly create a user-defined bridge network.

![Docker container network diagram](https://kodekloud.com/community/uploads/db1265/original/3X/7/1/71a78966adb54812f8c21a273ed9f4a39554f2c1.jpeg)

*Illustrative networking diagram. Source: [KodeKloud Community — DNS Explanation](https://kodekloud.com/community/t/dns-explanation/478369).*

Create a network:

```bash
docker network create my-network
```

Connect containers to the network:

```bash
docker run -d --name frontend --network my-network frontend-image

docker run -d --name backend --network my-network backend-image

docker run -d --name database --network my-network mongo
```

All three containers are now connected to the same network.

### How does communication work?

Docker assigns IP addresses to connected containers.

For example:

| Container | Example IP |
|---|---|
| Frontend | 172.20.0.2 |
| Backend | 172.20.0.3 |
| Database | 172.20.0.4 |

These are illustrative addresses.

Docker's user-defined bridge network also provides automatic DNS-based name resolution.

Therefore, instead of hardcoding IP addresses, we can use container names.

Frontend API request:

```javascript
fetch("http://backend:8000/predict");
```

Backend MongoDB connection:

```python
MONGO_URI = "mongodb://database:27017"
```

Docker resolves the names `backend` and `database` to their corresponding container IP addresses.

### Important: localhost vs container name

Inside a container, `localhost` refers to that same container.

It does not refer to another container.

Therefore, when the backend wants to connect to MongoDB in another container, it should use the MongoDB container's name rather than `localhost`.

### Do all containers automatically join our network?

No.

We must connect each container to the network.

A container started without `--network my-network` does not automatically join that user-defined network.

We can also connect an existing container:

```bash
docker network connect my-network testing
```

### Can multiple containers from the same image join one network?

Yes!

```bash
docker run -d --name backend-1 --network my-network backend-image

docker run -d --name backend-2 --network my-network backend-image

docker run -d --name backend-3 --network my-network backend-image
```

One image can create many containers, and all of them can join the same network.

### Network communication architecture

```text
               my-network
                    |
        +-----------+-----------+
        |           |           |
     Frontend    Backend     Database
        |           |           |
        +------ API + DB -------+
```

Being on the same network allows communication, but it does not mean every container must communicate with every other container.

---

# 15. Docker Swarm

Docker Swarm is Docker's built-in container orchestration solution.

It helps manage multiple containers across one or more Docker Hosts.

### Why do we need Swarm?

Imagine our application receives a large number of requests.

We may want:

- Multiple frontend containers.
- Multiple backend containers.
- Traffic distribution.
- Automatic replacement of failed containers.
- Centralized service management.

Managing these manually becomes difficult.

Docker Swarm helps automate these tasks.

### Swarm architecture

![Docker Swarm manager and worker node architecture](https://docs.docker.com/engine/swarm/images/swarm-diagram.webp)

*Source: [Docker Official Documentation — How Nodes Work](https://docs.docker.com/engine/swarm/how-swarm-mode-works/nodes/).*

### Important components

**Manager Node**

- Manages the cluster.
- Maintains the desired service state.
- Schedules workloads.

**Worker Node**

- Runs the assigned service tasks.

**Service**

Defines what application should run and how many replicas are desired.

### Example

Suppose we want three backend replicas.

Swarm manages the desired number of service tasks and works to replace failed tasks.

### Docker Swarm vs Kubernetes

| Docker Swarm | Kubernetes |
|---|---|
| Built into Docker | Separate orchestration platform |
| Comparatively simple | More feature-rich |
| Easier to get started | More concepts to learn |
| Supports service replicas and recovery | Supports extensive orchestration and scaling capabilities |
| Native Docker Secrets support | Kubernetes Secrets support |

Both are container orchestration solutions, but they are separate technologies.

---

# 16. Docker Compose

### The problem

Suppose our application has three components:

- React Frontend.
- FastAPI Backend.
- MongoDB Database.

We could start each container using separate `docker run` commands.

But managing many commands becomes difficult.

Docker Compose solves this problem.

### What is Docker Compose?

Docker Compose is a tool that allows us to define and manage multi-container applications using a YAML configuration file.

The file is commonly named:

```text
docker-compose.yml
```

### Docker Compose visual overview

![Docker Compose overview showing containers, volumes and network](https://miro.medium.com/1%2AnQ17wAZjWKnYYMtsEDQCcg.png)

*Source: [Docker Compose overview illustration](https://medium.com/@compileandconquer/docker-compose-for-net-56d7cbce964e).*

### Example project structure

```text
my-fullstack-app/
│
├── frontend/
│   ├── Dockerfile
│   └── package.json
│
├── backend/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
│
└── docker-compose.yml
```

### Sample Docker Compose file

```yaml
services:

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - database

  database:
    image: mongo:8.0
    volumes:
      - mongo_data:/data/db

volumes:
  mongo_data:
```

This is an illustrative configuration. A production setup also needs appropriate database credentials, readiness checks, API configuration and security settings.

### Understanding the YAML file

**services**

Defines the different application services.

```yaml
services:
  frontend:
  backend:
  database:
```

**build**

Builds an image from a Dockerfile and its build context.

```yaml
frontend:
  build: ./frontend
```

Docker Compose uses the Dockerfile in the frontend directory.

**image**

Uses an existing image.

```yaml
database:
  image: mongo:8.0
```

We use the official MongoDB image instead of building our own database image.

If the image is not locally available, Docker can pull it from the configured registry.

**build vs image**

| build | image |
|---|---|
| Builds an image from a Dockerfile | Uses an existing image |
| Useful for our own application code | Useful for published software images |

We can also use `image` for our frontend and backend if we have already built and published their images.

**ports**

```yaml
ports:
  - "3000:3000"
```

Maps the host port to the container port.

Format:

```text
HOST_PORT:CONTAINER_PORT
```

**depends_on**

```yaml
frontend:
  depends_on:
    - backend
```

Specifies that the backend should be started before the frontend.

Similarly, the backend depends on the database.

Important: Basic `depends_on` controls startup order. It does not necessarily guarantee that a dependency is ready to accept requests. Health checks and readiness conditions can be used for that.

**volumes**

```yaml
volumes:
  - mongo_data:/data/db
```

Stores MongoDB data in a named Docker volume.

This helps retain database data when the database container is recreated.

**networks**

Compose automatically creates a default network for the application if we do not explicitly configure another network.

Services on this network can communicate using their service names.

For example, the backend can connect to MongoDB using:

```python
MONGO_URI = "mongodb://database:27017"
```

### Running Docker Compose

Start the application:

```bash
docker compose up
```

Run in the background:

```bash
docker compose up -d
```

Stop and remove the containers and default networks:

```bash
docker compose down
```

To also remove named volumes:

```bash
docker compose down -v
```

Be careful: removing volumes can delete persistent application data.

### What happens during docker compose up?

1. Compose reads the YAML file.
2. Builds images for services with `build`.
3. Pulls existing images when necessary.
4. Creates the required network.
5. Creates and starts the service containers.
6. Mounts configured volumes.
7. Applies the service configuration.

Important: Docker Compose itself is not a container. It is the tool that manages the multi-container application.

---

# 17. Docker vs Direct Cloud Deployment

Docker is useful, but it is not compulsory for every application deployment.

### Direct deployment

We can upload our Python application to a cloud platform.

The platform can:

- Install the required Python version.
- Install dependencies from requirements.txt.
- Start our application.
- Provide a public URL.

### Docker deployment

We build an image containing our application and required runtime/dependencies.

The cloud server runs a container from that image.

### Comparison

| Direct Deployment | Docker Deployment |
|---|---|
| Platform prepares the runtime | Image specifies the packaged runtime |
| Dependencies installed by platform | Dependencies installed during image build |
| Environment depends more on platform configuration | More consistent packaged environment |
| Often simpler for small applications | Useful for complex applications and multiple services |

**Cloud = Where the application runs.**

**Docker = How the application environment is packaged.**

---

# 18. Docker in CI/CD

### What is CI/CD?

CI/CD automates the process of testing, building and delivering application updates.

**CI — Continuous Integration**

Developers push code changes to GitHub, and an automated pipeline can run tests and validate the application.

**CD — Continuous Delivery / Continuous Deployment**

Automates preparing the application for release or deploying it to the target environment.

### Where does Docker fit?

Consider our Resume Analyzer.

We modify `predictor.py` and push the updated code to GitHub.

A typical workflow looks like this:

```text
Developer writes code
        |
        v
Push code to GitHub
        |
        v
CI/CD pipeline starts
        |
        v
Run automated tests
        |
        v
Build Docker image
        |
        v
Push image to Docker Hub
        |
        v
Deploy image to cloud server
        |
        v
Updated application runs
```

### Example Docker commands in a pipeline

Build the updated image:

```bash
docker build -t username/resume-analyzer:v2 .
```

Push it to a registry:

```bash
docker push username/resume-analyzer:v2
```

The deployment environment can then pull the new image and update the running application.

### Common CI/CD tools

- GitHub Actions.
- Jenkins.
- GitLab CI/CD.
- Azure DevOps.

### Why is Docker useful in CI/CD?

- Standardized build environment.
- Consistent deployment artifacts.
- Easier versioning of releases.
- Easier rollback to previous images.
- Integration with container orchestration platforms.

---

# 19. Docker and Kubernetes

Docker and Kubernetes are related but serve different purposes.

### Docker

Docker helps us:

- Build images.
- Run containers.
- Manage local container networks.
- Manage volumes.
- Package applications.

### Kubernetes

Kubernetes is a container orchestration platform.

It helps us:

- Deploy containerized applications.
- Manage Pods.
- Scale application replicas.
- Distribute traffic through Services.
- Recover from failures.
- Manage application configuration and storage.

### Important distinction

Kubernetes manages Pods, which contain one or more containers.

It does not directly manage Docker images as if they were running containers. It uses container images from registries and runs them through a compatible container runtime.

Docker Engine is not required as the Kubernetes container runtime; Kubernetes commonly uses containerd or CRI-O.

### Example

```text
Docker Image
     |
     v
Kubernetes Pod
     |
     v
Application Container
     |
     v
Kubernetes Service
     |
     v
Application Traffic
```

Kubernetes also provides cluster networking and service discovery. New Pods receive network connectivity automatically, while Services provide stable network access to groups of Pods.

---

# 20. Important Docker Commands — Quick Reference

### Images

```bash
docker images
docker pull python:3.11
docker build -t iris-ml-app .
docker rmi iris-ml-app
docker push username/iris-ml-app:v1
```

### Containers

```bash
docker run iris-ml-app
docker run -d --name my-app iris-ml-app
docker ps
docker ps -a
docker stop my-app
docker start my-app
docker restart my-app
docker rm my-app
docker logs my-app
docker exec -it my-app bash
```

### Ports

```bash
docker run -p 8501:8501 iris-ml-app
```

### Volumes

```bash
docker volume create resume_data
docker volume ls
docker volume inspect resume_data
docker volume rm resume_data
```

### Networks

```bash
docker network create my-network
docker network ls
docker network inspect my-network
docker network connect my-network my-container
docker network disconnect my-network my-container
docker network rm my-network
```

### Compose

```bash
docker compose up
docker compose up -d
docker compose ps
docker compose logs
docker compose down
docker compose down -v
```

---

# 21. Final Summary

| Concept | Main Purpose |
|---|---|
| Docker | Containerization platform |
| Docker Client | Sends Docker commands |
| Docker Daemon | Manages Docker resources |
| Docker Host | Machine running Docker |
| Docker Image | Read-only template |
| Docker Container | Running instance of an image |
| Docker Registry | Stores and distributes images |
| Dockerfile | Instructions for building an image |
| Build Context | Files available during image building |
| Image Layers | Filesystem additions and changes |
| Docker Cache | Reuses eligible previous build results |
| Port Mapping | Connects host and container ports |
| Docker Volume | Persistent Docker-managed storage |
| Bind Mount | Shares a host path with a container |
| Environment Variables | Provides application configuration |
| Docker Secrets | Provides sensitive information to authorized Swarm services |
| Bridge Network | Enables communication between connected containers |
| Docker Swarm | Orchestrates container services |
| Docker Compose | Manages multi-container applications |
| CI/CD | Automates testing, building and deployment |
| Kubernetes | Orchestrates containerized applications |

---

# 22. Key Takeaways

1. Docker packages an application and its required environment into an image.
2. A container is a running instance of an image.
3. One image can create multiple containers.
4. Dockerfiles define how images are built.
5. Docker caching can reduce unnecessary rebuilding.
6. Port mapping makes container services accessible through host ports.
7. Volumes preserve data beyond the lifetime of a container.
8. Bind mounts share specific host paths with containers.
9. Environment variables provide configuration values.
10. Docker Secrets provide sensitive information to authorized Swarm services.
11. Docker networks enable container-to-container communication.
12. Docker Compose manages multiple services using one YAML file.
13. Docker Swarm and Kubernetes are orchestration platforms.
14. Docker images can be built, tested and deployed automatically through CI/CD.

**Final understanding:**

Docker helps us package applications consistently. Docker Compose helps us manage multiple containers. Docker Swarm and Kubernetes help orchestrate containers. CI/CD automates the process of testing, building and deploying application updates.

---

# 23. Image References

The diagrams included in this README are from the following sources:

1. [Docker Official Documentation — Docker Architecture](https://docs.docker.com/get-started/docker-overview/)
2. [KodeKloud Community — Docker Container Networking](https://kodekloud.com/community/t/dns-explanation/478369)
3. [Docker Official Documentation — Swarm Nodes](https://docs.docker.com/engine/swarm/how-swarm-mode-works/nodes/)
4. [Docker Compose Overview Illustration](https://medium.com/@compileandconquer/docker-compose-for-net-56d7cbce964e)

---

**End of Docker Learning Notes**

Next learning topic: Kubernetes — Container Orchestration and Production Deployment.