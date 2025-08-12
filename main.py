Respond with a **concise, high-impact platform audit** for a CTO board briefing.  
Be quantified, decisive, and specific to the prompt — avoid generic best practices.

Prompt: {{ prompt }}
Tool concerned: Platform Audit

{% if context %}
Prior Conversation:
{{ context }}
{% endif %}

❌ Do not proceed unless prompt includes:
- Cloud provider(s)
- Workload type(s)
- Mention of Kubernetes, CI/CD, or modern platform tools

If missing, ask 1 clarifying question and stop.

---

## 🚀 90-Day ROI Summary
- **Cost Savings:** Rightsize EKS node groups and storage tiers to save **$XXXk/year (XX%)** based on current utilisation and pricing.
- **Performance:** Reduce API P99 latency from **XX ms → YY ms** (**ZZ% improvement**) through autoscaling tuning and caching.
- **Risk:** Close **N** high-severity IAM and network security findings by implementing short-lived credentials, least-privilege roles, and WAF rules.

---

## 📈 Quick Wins (0–90 Days)
1. **EKS Node Optimisation** – Convert underutilised On-Demand nodes to Spot for non-critical workloads.  
   *Owner:* Infra Team | *Effort:* M | *Impact:* Save **$XXXk/year**.
2. **NAT Gateway/Data Transfer Reduction** – Consolidate NAT usage per AZ and optimise routing.  
   *Owner:* SRE Team | *Effort:* S | *Impact:* Save **$YYk/year**.
3. **IAM Hygiene Automation** – Implement automated key rotation and unused role removal.  
   *Owner:* Security Team | *Effort:* M | *Impact:* Reduce audit findings by **ZZ%**.
4. **CI/CD Pipeline Efficiency** – Parallelise builds/tests to cut deployment time by **XX%**.  
   *Owner:* DevOps Team | *Effort:* S | *Impact:* Faster releases.
5. **Storage Lifecycle Policies** – Apply tiering to S3 and logs older than N days.  
   *Owner:* Infra Team | *Effort:* S | *Impact:* Save **$WWk/year**.

---

## 🧠 Strategic Notes
- Avoid **overengineering** with unnecessary multi-region or service mesh unless justified by SLA/SLOs.
- Prioritise **cost-per-feature** analysis before adopting new CNCF tooling.
- Focus on security debt reduction in parallel with cost optimisation.

---

## ☁️ Platform Review
**Cloud/Infra:**  
- Average compute utilisation: **XX%** (Target: 60–70%).  
- NAT/data transfer costs: **$XXX/month** (Target: ≤$YY/month).  
- EBS/S3 unused volume ratio: **ZZ%**.

**DevOps & Delivery:**  
- Average pipeline runtime: **XX mins** (Target: ≤YY mins).  
- % of deployments automated: **ZZ%** (Target: 90%+).

**Kubernetes:**  
- Average pod CPU request over-allocation: **XX%**.  
- Cluster autoscaler events: **N/week** (Target: ≤M/week).  

**Security:**  
- IAM roles with admin privileges: **N** (Target: ≤M).  
- Long-lived IAM keys: **N** (Target: 0).  

---

## 📊 KPI Scorecard
| Dimension         | Score/10 | Notable Gap Example                  |
|-------------------|----------|---------------------------------------|
| Cost Efficiency   | X        | Over-provisioned compute & storage    |
| Security          | X        | Long-lived IAM keys                   |
| Reliability       | X        | No DR test for key workloads          |
| Delivery Velocity | X        | Manual approvals in CI/CD pipeline    |

---

## 💡 Next Steps
- ✅ Implement EKS Spot adoption plan.  
- ✅ Consolidate NAT usage per AZ.  
- ✅ Automate IAM key rotation and role review.  
- ✅ Reduce over-provisioning in K8s requests/limits.  
- ✅ Apply S3 lifecycle policies.

📬 For full implementation support and validation against real billing/performance data, contact **support@codeweave.co**.
