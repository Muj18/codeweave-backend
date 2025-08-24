
You are a **staff-level SRE** providing a **Kubernetes troubleshooting runbook**.  
The output must read like a **production-grade playbook** for on-call engineers.  
Tone: calm, precise, authoritative.  

Prompt: sample-prompt  
Tool: Kubernetes  

---

## 1) Executive Summary
Troubleshooting Kubernetes requires a structured, stepwise approach:  
1. Identify the failing pod/workload  
2. Inspect events, logs, and metrics  
3. Check infra dependencies (network, DNS, storage, IAM)  
4. Apply least-disruptive remediation first  
5. Document & codify into automation/runbooks  

---

## 2) Runbook: Step-by-Step

### a) Pod Failing to Start
\`\`\`bash
kubectl get pods -n <class 'jinja2.utils.Namespace'>
kubectl describe pod sample-pod -n <class 'jinja2.utils.Namespace'>
kubectl logs sample-pod -n <class 'jinja2.utils.Namespace'> --previous
\`\`\`
- Check for `ImagePullBackOff` → validate registry access & credentials  
- Check for `CrashLoopBackOff` → review app/container logs  

### b) Networking / DNS Issues
\`\`\`bash
kubectl exec -it sample-pod -n <class 'jinja2.utils.Namespace'> -- nslookup kubernetes.default
kubectl exec -it sample-pod -n <class 'jinja2.utils.Namespace'> -- curl -vk https://service:port
\`\`\`
- Validate CoreDNS pods are healthy (`kubectl get pods -n kube-system -l k8s-app=kube-dns`)  
- Ensure NetworkPolicy/Calico/Cilium rules are not blocking  

### c) Resource Pressure
\`\`\`bash
kubectl top pod -n <class 'jinja2.utils.Namespace'>
kubectl describe node
\`\`\`
- Look for `OOMKilled` or CPU throttling → tune resource requests/limits  
- Consider Horizontal/Vertical Pod Autoscaler  

### d) Storage / Volume Issues
\`\`\`bash
kubectl describe pvc sample-pvc -n <class 'jinja2.utils.Namespace'>
kubectl get events -n <class 'jinja2.utils.Namespace'> | grep pvc
\`\`\`
- Ensure underlying StorageClass is available  
- Check RWX/RWO access modes match usage  

---

## 3) Observability Hooks
- **Logs**: Centralised aggregation with ELK/Loki, searchable by pod/namespace  
- **Metrics**: Prometheus/Grafana for CPU, memory, network, request latency  
- **Tracing**: Jaeger or OpenTelemetry for cross-service failures  
- **Dashboards**: Live SLO/SLA view for latency, error rates, availability  

---

## 4) Risks & Trade-offs
- ❌ Manual debugging delays MTTR → ✅ Automate via runbooks, alerts, ChatOps  
- ❌ Over-provisioned pods → ✅ Cost impact, rightsize with HPA/VPA  
- ❌ Lack of RBAC → ✅ On-call blocked → create least-privilege troubleshooting role  
- ❌ Debugging in prod with `exec` → ✅ Prefer `kubectl debug` ephemeral containers  

---

## 5) Compliance & Governance
- Maintain **audit logs** of troubleshooting commands (ISO27001/GDPR)  
- Redact **sensitive data** before exporting logs to SIEM  
- Enforce **RBAC + MFA** for kubectl access in prod  
- Ensure IaC (Terraform/Helm) captures any config changes → avoid drift  

---

## 6) Quick Wins
- Add **liveness/readiness probes** → stop routing to broken pods  
- Enable **Vertical Pod Autoscaler** → reduce OOM kills  
- Use **ephemeral debug containers** instead of exec into prod workloads  
- Automate **top 5 playbooks** as Slack/Teams ChatOps commands  
- Build **chaos drills** (node drain, pod kill) to validate resilience  

[END OF TEMPLATE]