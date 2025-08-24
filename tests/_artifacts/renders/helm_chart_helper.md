# templates/helm_chart_helper.jinja2

You are a **staff-level Platform Engineer** tasked with producing a production-grade **Helm Chart Helper Playbook**.  
The output must:  
- Be written as if reviewed by senior architects and CTOs.  
- Cover **Helm chart design for Kubernetes apps** with **values.yaml, templates, helpers, and best practices**.  
- Include **multi-cloud (AWS EKS, Azure AKS, GCP GKE)**, **automation (IaC, Terraform, ArgoCD, GitHub Actions)**, **resilience (HA, multi-AZ, DR, RPO)**, **observability (metrics, logs, tracing, SLOs)**, **security & compliance (IAM, RBAC, least privilege, encryption, PCI, ISO 27001, HIPAA, GDPR)**, **cost optimization (rightsizing, spot, savings plans)**, **risks**, **runbook**, and **quick wins/gotchas**.  
- Provide **complete Helm YAML snippets**.  
- Use structured markdown with clear sections.  

---

## 1) Executive Summary
- **Prompt:** sample-prompt  
- **Tool:** Helm Chart Helper Playbook  
- **Cloud/Runtime:** sample-cloud  
- **Prior Context:** sample-conversation  

This playbook defines **Helm best practices** for production-grade Kubernetes apps across multi-cloud environments.  

---

## 2) Architecture Diagram
```mermaid
graph TD
    Dev[Developer] --> Repo[Helm Repo]
    Repo --> CI[GitHub Actions Lint/Test]
    CI --> ArgoCD[ArgoCD Deployment]
    ArgoCD --> K8s[Multi-Cloud Cluster (EKS/AKS/GKE)]
    K8s --> Obs[Metrics/Logs/Tracing/SLOs]
    K8s --> Sec[RBAC/IAM/KMS/Compliance]
    K8s --> DR[HA / Multi-AZ / DR]
```

---

## 3) Core Architecture
- **Automation**: Helm + ArgoCD + GitHub Actions → GitOps pipeline.  
- **Resilience**: multi-AZ worker nodes, PodDisruptionBudgets, tested DR with defined RPO/RTO.  
- **Security**: RBAC roles per namespace, IAM roles for service accounts (IRSA), KMS secret encryption.  
- **Compliance**: PCI-DSS, ISO 27001, HIPAA, GDPR guardrails built into CI/CD.  
- **Observability**: Prometheus metrics, Grafana dashboards, OpenTelemetry tracing, SLO error budgets.  
- **Cost**: HPA with rightsizing, spot + savings plans, proactive scaling policies.  

---

## 4) Production-Grade Examples

### values.yaml
```yaml
replicaCount: 3
image:
  repository: myregistry/myapp
  tag: "1.0.0"
  pullPolicy: IfNotPresent

resources:
  requests:
    cpu: "500m"
    memory: "512Mi"
  limits:
    cpu: "1"
    memory: "1Gi"

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 75
```

### deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Chart.Name }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: {{ .Chart.Name }}
  template:
    metadata:
      labels:
        app: {{ .Chart.Name }}
    spec:
      serviceAccountName: {{ .Chart.Name }}-sa
      containers:
      - name: app
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        ports:
        - containerPort: 8080
        resources:
          {{- toYaml .Values.resources | nindent 10 }}
        envFrom:
        - secretRef:
            name: {{ .Chart.Name }}-secrets
```

### service.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ .Chart.Name }}
spec:
  type: ClusterIP
  ports:
    - port: 80
      targetPort: 8080
  selector:
    app: {{ .Chart.Name }}
```

---

## 5) Runbook – Step-by-Step
1. Update **values.yaml** → commit PR.  
2. **CI (GitHub Actions)** runs: `helm lint`, `helm template`, security scans.  
3. **ArgoCD** auto-syncs chart to target cluster.  
4. Validate:
   - `kubectl get pods`
   - dashboards in Grafana (latency, error rates, resource usage).  
5. Rollback via:  
   - `helm rollback <release>`  
   - ArgoCD UI → select previous sync.  
6. Verify secrets rotation & RBAC policies.  

---

## 6) Risks, Trade-Offs & Limitations
| Risk | Mitigation |
|------|------------|
| Drift between clusters | GitOps auto-sync |
| Secret leakage | Vault/Secrets Manager + IRSA |
| Cost overruns | Rightsizing + autoscaling |
| Compliance drift | Policy-as-code (OPA/Gatekeeper) |

**Trade-offs & Limitations:**  
- Over-customization in `values.yaml` → brittle charts.  
- Helm templating can be harder to debug than Kustomize.  
- Complex charts may slow down CI/CD pipelines.  

---

## 7) Quick Wins & Gotchas
- ✅ Add `helm lint` & `helm unittest` in CI/CD.  
- ✅ Define **PodDisruptionBudgets** for HA.  
- ✅ Automate SLO dashboards (latency, availability, cost).  
- ✅ Cost KPI: reduce node spend by 20% using spot + autoscaling.  

**Gotchas:**  
- Missing `resources` → cluster instability.  
- Forgetting `helm dependency update` breaks CI/CD.  
- Large values.yaml with unvalidated params → deploy drift.  

---

## ✅ End of Template