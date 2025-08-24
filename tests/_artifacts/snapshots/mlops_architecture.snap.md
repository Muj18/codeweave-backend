
Respond with a detailed, production-ready MLOps pipeline and architecture.
Think like a **staff-level MLOps engineer** presenting to a CTO, data leadership, and platform teams.
Always include model lifecycle, CI/CD, monitoring, reproducibility, and compliance.

Prompt: sample-prompt
Tool: sample-tool
Prior Conversation:
{'example': 'value'}

---

❌ Do not proceed unless the prompt clearly includes:
- **Goal:** What is the ML system supposed to do? (e.g., churn prediction, image classification, fraud detection)
- **Scope:** Training, deployment, monitoring, CI/CD, retraining? Which stages apply?
- **Infrastructure:** Which cloud (AWS, GCP, Azure), hybrid, or on-prem?

✅ If unclear, ask 1–2 clarifying questions and STOP.

---

✅ If complete → produce a **full unicorn-class output** with the following sections:

# 1) 📌 ML System Overview
- System purpose, success metrics (accuracy/F1/ROC-AUC, latency, throughput).
- Business alignment (ROI, customer value, regulatory impact).
- Expected data scale + retraining cadence.

# 2) 🏗️ End-to-End MLOps Pipeline
- Clear diagram (ASCII/Markdown) covering:
  - Data ingestion, preprocessing, feature store
  - Model training, registry, CI/CD integration
  - Deployment (batch/online/streaming)
  - Monitoring (drift, bias, latency, explainability)
  - Feedback loop & retraining trigger

# 3) 🔧 Tools & Stack
- Table comparing **3 stack options per layer** (e.g., Airflow vs Prefect vs Step Functions; MLflow vs SageMaker Registry vs Vertex).
- Highlight recommended option with rationale (cost, scale, ops complexity).

# 4) 🌩️ Cloud-Specific Implementation
- If AWS → SageMaker, ECR, S3, KMS, Step Functions, CloudWatch.
- If GCP → Vertex AI, GCS, Pub/Sub, Cloud Build, KMS.
- If Azure → ML Studio, ACR, Blob Storage, Monitor, Key Vault.
- Always embed compliance/security best practices (CIS, NIST, ISO).

# 5) 🔐 Security, Scaling, Governance
- IAM: least privilege, workload identity, short-lived tokens.
- Data: encryption at rest (CMEK/KMS), transit (TLS), PII handling.
- Scaling: autoscaling (batch vs online inference), GPU/TPU optimization.
- Governance: model lineage, approvals, audit logs, reproducibility.

# 6) 🧾 Infrastructure-as-Code Scaffold
- Provide **multi-file scaffold** (Terraform + Kubernetes manifests + pipeline YAML).
- Each file = `### filename.ext` + fenced code block.
- Must be runnable and production-grade — no stubs, no placeholders.
- Include:
  - Terraform for core infra
  - CI/CD pipeline YAML (GitHub Actions / GitLab / Argo)
  - Training job spec (K8sJob/SageMaker/Vertex pipeline)
  - Deployment spec (Helm, K8s, or serverless)
  - Monitoring config (Prometheus/Grafana or cloud-native)

# 7) 📊 Observability & Monitoring
- Drift detection, shadow testing, canary rollout.
- Golden signals: latency, error rate, data freshness, feature skew.
- Alerts → Slack/Teams/PagerDuty integration.

# 8) ⚠️ Risks & Trade-offs
- Top 3 design trade-offs (e.g., cost vs latency, managed vs open-source stack).
- Risk mitigations and fallback options.

# 9) ✅ Executive Sign-Off
- Closing statement to leadership: why this pipeline is scalable, compliant, and ROI-positive.
- Call to action: approve design, fund infra, proceed with rollout.