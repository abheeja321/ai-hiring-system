# Zecpath AI Hiring System: Horizontal Scalability Strategy

As the platform scales to support large enterprise hiring pipelines, the system must shift from vertical scaling (adding larger instance types) to a horizontal, distributed architecture. 

## 1. Load Balancing Configuration
To handle concurrent inbound API traffic, we will deploy **AWS Application Load Balancers (ALB)** or **NGINX Reverse Proxies**.
*   **Routing Logic**: Traffic will be routed based on endpoint types. Heavy, asynchronous processing routes (e.g., `/api/v1/ai/parse-resume/`) will route to specific high-capacity worker pools, while real-time conversational APIs (e.g., `/api/v1/ai/interview/`) will route to low-latency websocket clusters.
*   **Auto-Scaling Groups**: The ALB will trigger auto-scaling policies based on CPU utilization and request latency, dynamically spinning up new container instances during peak hiring seasons (e.g., University recruitment periods).

## 2. Microservice Deployment
We will containerize the application using **Docker** and orchestrate the pods using **Kubernetes (EKS)**.
*   **Web API Pods**: Lightweight, fast-scaling pods dedicated strictly to routing, authentication, database read/writes, and returning HTTP responses.
*   **Worker Pods (Celery/RabbitMQ)**: Dedicated background workers processing the `ThreadPoolExecutor` and heavy LLM ingestion tasks. These pods will be scaled independently of the Web APIs to ensure background tasks do not exhaust frontend memory pools.
*   **GPU Node Affinity**: If we deploy proprietary edge vision models for behavioral tracking, Kubernetes node affinity rules will map those specific microservices directly to GPU-backed EC2 instances (e.g., `g4dn` series).

## 3. Database & Caching Optimization
*   **Redis Implementation**: Beyond the Python-level `functools.lru_cache`, we will implement a distributed Redis cluster. This allows multiple web nodes to share cached `JobProfile` parsing and ATS heuristic configurations, preventing redundant processing across different servers.
*   **PostgreSQL Read Replicas**: The primary database will handle write-heavy operations (e.g., creating `AIArtifact` tables), while reporting tools and the HR Analytics Dashboard will route their heavy `select_related` analytical queries to read-only replicas to protect the primary cluster's throughput.

## 4. Rate Limiting & API Security
*   **Throttling**: Implement token-bucket rate limiting at the API Gateway level (e.g., 100 requests / minute / tenant) to prevent noisy-neighbor problems where one bulk-upload monopolizes the Celery workers.
*   **Circuit Breakers**: If external LLM providers experience severe latency or outages (triggering repeated 503s), the circuit breaker pattern will temporarily halt outbound requests and fallback to cached heuristics or queue the tasks for later, protecting the platform from cascaded timeout failures.
