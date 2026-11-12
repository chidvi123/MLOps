# Kubernetes

## 1. What is Kubernetes?

**Kubernetes (K8s)** is an open-source container orchestration platform that automates the deployment, scaling, networking, and management of containerized applications.

It helps applications run reliably even when containers fail or traffic increases.

### Why Kubernetes?

- Runs multiple application instances.
- Restarts failed containers.
- Distributes incoming traffic.
- Scales applications based on demand.
- Manages application configuration and storage.

---

## 2. Kubernetes Architecture

A **Kubernetes Cluster** is a group of machines that work together to run containerized applications.

It consists of a Control Plane and Worker Nodes.

```mermaid
flowchart TB
    U["User / kubectl"] --> API

    subgraph CP["CONTROL PLANE"]
        API["API Server"]
        SCH["Scheduler"]
        CM["Controller Manager"]
        ETCD[("etcd")]
        API --> SCH
        API --> CM
        API <--> ETCD
    end

    subgraph W1["WORKER NODE 1"]
        K1["Kubelet"]
        P1["Pod 1"]
        P2["Pod 2"]
        K1 --> P1
        K1 --> P2
    end

    subgraph W2["WORKER NODE 2"]
        K2["Kubelet"]
        P3["Pod 3"]
        K2 --> P3
    end

    API --> K1
    API --> K2
```

### Control Plane

Manages the Kubernetes cluster.

| Component | Responsibility |
|---|---|
| API Server | Entry point for Kubernetes requests |
| Scheduler | Selects a suitable Worker Node for new Pods |
| Controller Manager | Ensures the cluster matches the desired state |
| etcd | Stores cluster configuration and state |

### Worker Node

Runs the actual application workloads.

| Component | Responsibility |
|---|---|
| Kubelet | Ensures Pods are running as instructed |
| Container Runtime | Runs containers |
| Pods | Run application containers |

---

## 3. Kubernetes Core Resources

### Pod

A **Pod** is the smallest deployable unit in Kubernetes. It contains one or more containers.

```mermaid
flowchart TB
    N["Worker Node"]
    N --> P["Pod"]
    P --> C1["Container 1"]
    P --> C2["Container 2"]
```

- Containers inside a Pod share networking.
- A Pod receives its own IP address.
- Pods are replaceable; their IP addresses can change.

### Deployment and ReplicaSet

A **Deployment** manages application updates and the desired number of Pod replicas.

A **ReplicaSet** ensures that the required number of Pods are running.

```mermaid
flowchart TB
    D["Deployment"]
    D --> R["ReplicaSet"]
    R --> P1["Pod 1"]
    R --> P2["Pod 2"]
    R --> P3["Pod 3"]
```

Example: If the desired replica count is 3, Kubernetes tries to maintain 3 running Pods.

If one Pod fails, the ReplicaSet creates a replacement.

---

## 4. Services and Networking

A **Service** provides a stable network endpoint for accessing a group of Pods.

Pod IP addresses can change, but the Service endpoint remains stable.

```mermaid
flowchart TB
    U["Client Request"] --> S["Kubernetes Service"]
    S --> P1["Pod 1"]
    S --> P2["Pod 2"]
    S --> P3["Pod 3"]
```

The Service selects Pods using labels and forwards traffic to eligible Pods.

### Types of Services

| Type | Purpose |
|---|---|
| ClusterIP | Internal access within the cluster |
| NodePort | Exposes the application through a node port |
| LoadBalancer | Exposes the application through an external load balancer |

For our ML API, `ClusterIP` is suitable for internal communication. External access can be provided through an appropriate ingress or load-balancing setup.

---

## 5. Scaling and Self-Healing

### Self-Healing

Kubernetes continuously checks whether the actual state matches the desired state.

```mermaid
flowchart TD
    A["Desired: 3 Pods"] --> B["3 Pods Running"]
    B --> C["One Pod Fails"]
    C --> D["ReplicaSet Detects Missing Pod"]
    D --> E["Replacement Pod Created"]
    E --> F["3 Pods Running Again"]
```

### Horizontal Pod Autoscaler (HPA)

HPA automatically increases or decreases the number of Pod replicas based on observed metrics.

```mermaid
flowchart TD
    A["Monitor CPU Usage"] --> B{"CPU above target?"}
    B -->|Yes| C["Increase Pod Replicas"]
    B -->|No| D{"CPU usage lower?"}
    D -->|Yes| E["Decrease Pod Replicas"]
    D -->|No| F["Keep Current Replicas"]
```

Example configuration:

- Minimum replicas: 2
- Maximum replicas: 5
- Target CPU utilization: 70%

HPA requires a working metrics source, such as Metrics Server. CPU utilization targets also require CPU requests to be configured.

---

## 6. Configuration and Storage

### ConfigMap

A **ConfigMap** stores non-sensitive application configuration separately from application code.

Examples:
- Application environment
- API port
- Model path

```mermaid
flowchart LR
    CM["ConfigMap"] --> P["Pod"]
    P --> C["Container"]
    C --> A["Application Reads Configuration"]
```

### Secret

A **Secret** stores sensitive information such as passwords, API keys, and tokens.

```mermaid
flowchart LR
    S["Kubernetes Secret"] --> P["Pod"]
    P --> C["Container"]
    C --> A["Application Uses Credentials"]
```

Secrets can be exposed to containers as environment variables or mounted files.

**Important:** Base64 encoding is not encryption. Secrets need appropriate access controls and encryption-at-rest protection.

### Persistent Volume (PV) and Persistent Volume Claim (PVC)

- **PV:** A storage resource available to the cluster.
- **PVC:** A request for storage made by an application.
- **StorageClass:** Defines how storage can be dynamically provisioned.

```mermaid
flowchart TB
    P["Pod"] --> PVC["Persistent Volume Claim"]
    PVC --> PV["Persistent Volume"]
    PV --> S["Underlying Storage"]
```

A Pod must mount the PVC to access the storage.

PV/PVC are useful when application data must survive Pod replacement. They are not automatically required for every ML API.

---

## 7. Production Concepts

### Liveness and Readiness Probes

Both probes check application health, but they serve different purposes.

| Probe | Purpose | On Failure |
|---|---|---|
| Liveness | Checks whether the container is healthy | Container can be restarted |
| Readiness | Checks whether the application can accept traffic | Pod is removed from Service endpoints |

```mermaid
flowchart TB
    P["Pod"] --> L["Liveness Probe"]
    P --> R["Readiness Probe"]
    L -->|Unhealthy| X["Restart Container"]
    R -->|Not Ready| Y["Stop Sending Traffic"]
```

### Resource Requests and Limits

- **Requests:** Resources Kubernetes uses when scheduling a Pod.
- **Limits:** Maximum resources a container can consume.

Example:

```yaml
resources:
  requests:
    cpu: "250m"
    memory: "256Mi"
  limits:
    cpu: "500m"
    memory: "512Mi"
```

### Rolling Updates and Rollbacks

**Rolling Update:** Gradually replaces old application Pods with new ones.

**Rollback:** Returns a Deployment to a previous revision.

```mermaid
flowchart LR
    A["Old Version"] --> B["Create New Pods"]
    B --> C["Replace Old Pods Gradually"]
    C --> D["New Version Running"]
    D -. "If deployment fails" .-> E["Rollback"]
    E --> A
```

---

## 8. Complete ML Application Deployment Flow

This is how Kubernetes fits into our ML deployment project.

```mermaid
flowchart TB
    A["Trained ML Model"]
    B["FastAPI Application"]
    C["Docker Image"]
    D["Container Registry"]
    E["Kubernetes Cluster"]
    F["Deployment"]
    G["Pods"]
    H["Service"]
    I["User / Client"]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    H --> I
```

**Flow explanation:**

1. Train and package the ML model.
2. Build a Docker image containing the API, model, and dependencies.
3. Push the image to a container registry.
4. Kubernetes pulls the image from the registry.
5. A Deployment creates and manages Pods.
6. A Service provides a stable endpoint to access the API.
7. Kubernetes monitors and manages the application.

---

## 9. kubectl Commands

`kubectl` is the command-line tool used to communicate with the Kubernetes API Server.

| Command | Purpose |
|---|---|
| `kubectl get pods` | List Pods |
| `kubectl get deployments` | List Deployments |
| `kubectl get services` | List Services |
| `kubectl get nodes` | List Worker Nodes |
| `kubectl get namespaces` | List Namespaces |
| `kubectl apply -f deployment.yaml` | Create or update resources |
| `kubectl describe pod <pod-name>` | View Pod details |
| `kubectl logs <pod-name>` | View container logs |
| `kubectl delete -f deployment.yaml` | Delete resources defined in a file |
| `kubectl get hpa` | View autoscaler status |

---

## 10. Kubernetes Project Structure

```text
Week8_MLOps_HandsOn/
│
├── app/
│   └── main.py
│
├── artifacts/
│   └── packaged_model/
│
├── Dockerfile.fastapi
│
└── kubernetes/
    ├── namespace.yaml
    ├── deployment.yaml
    ├── service.yaml
    ├── configmap.yaml
    ├── secret.yaml
    ├── persistent-volume.yaml
    ├── persistent-volume-claim.yaml
    └── hpa.yaml
```

### Important

Not every Kubernetes resource is mandatory for every application.

| Resource | Purpose |
|---|---|
| Namespace | Organizes application resources |
| Deployment | Manages application Pods |
| Service | Provides stable networking |
| ConfigMap | Stores non-sensitive configuration |
| Secret | Stores sensitive configuration |
| PV/PVC | Provides persistent storage when needed |
| HPA | Automatically scales Pod replicas |

ConfigMaps, Secrets, and PVCs must be explicitly connected to the Deployment/Pods to be used. HPA requires metrics and appropriate resource requests.

---

## 11. What Kubernetes Does NOT Do

- It does not train ML models.
- It does not build Docker images.
- It does not automatically fix application bugs.
- It does not guarantee application security.
- It does not automatically create every required storage or networking resource.

**Kubernetes orchestrates containerized applications. It does not replace the tools used to build those applications.**

