### Cloud Network Timeout Troubleshooting — Production-Grade

**Key Symptoms**
- API calls hang or return `HTTP 504` / `curl` timeout
- Kubernetes pods stuck in `ContainerCreating` due to CNI/network issues
- Terraform or Ansible deployments stall on remote provisioners
- CI/CD pipelines fail fetching external dependencies (pip, apt, docker pull)
- Intermittent connectivity to cloud services, endpoints, or databases

**Immediate Triage**
- Ping/traceroute target endpoints to check latency or packet loss
- Validate DNS resolution:
  - `dig example.com`
  - `nslookup api.service`
- Inspect VPC/Subnet routing tables, NAT gateways, and security groups
- Check cloud provider status page for regional outages (AWS/GCP/Azure)
- For Kubernetes clusters:
  - `kubectl get nodes -o wide`
  - Inspect CNI DaemonSet logs: `kubectl logs -n kube-system ds/<cni-daemonset>`

**Safe Fix — Network Verification and Remediation**
```bash
# AWS: describe VPC route tables
aws ec2 describe-route-tables --filters Name=vpc-id,Values=<vpc-id>

# AWS: verify security groups and NACLs
aws ec2 describe-security-groups --group-ids <sg-id>
aws ec2 describe-network-acls --filters Name=vpc-id,Values=<vpc-id>

# Kubernetes CNI restart (example for AWS VPC CNI)
kubectl -n kube-system rollout restart ds aws-node
kubectl get pods -n kube-system -o wide

# Terraform: extend timeouts for slow network provisioning
resource "aws_instance" "example" {
  timeouts {
    create = "20m"
    update = "15m"
    delete = "15m"
  }
}

# Test external connectivity from CI/CD agent
curl -v https://api.external-service.com
ping -c 5 8.8.8.8