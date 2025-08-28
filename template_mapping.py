TEMPLATE_MAP = {
    # -------------------------
    # Cloud Architecture
    # -------------------------
    "aws_arch": "solutions_architecture.jinja2",
    "azure_arch": "solutions_architecture.jinja2",
    "gcp_arch": "solutions_architecture.jinja2",
    "others_arch": "solutions_architecture.jinja2",

    # Cloud Quick Tasks
    "aws_quick": "cloud_quick_task.jinja2",
    "azure_quick": "cloud_quick_task.jinja2",
    "gcp_quick": "cloud_quick_task.jinja2",
    "others_quick": "cloud_quick_task.jinja2",

    # -------------------------
    # Infrastructure as Code & Automation
    # -------------------------
    "terraform": "terraform_playbook.jinja2",
    "aws cloudformation": "cloudformation_playbook.jinja2",
    "pulumi": "pulumi_playbook.jinja2",
    "ansible": "ansible_playbook.jinja2",
    "others (iac / automation)": "other_iac_playbook.jinja2",

    # IaC Quick Task + Fix
    "iac_quick_task": "iac_quick_task.jinja2",
    "iac_quick_fix": "iac_quick_fix.jinja2",

    # -------------------------
    # Kubernetes & Containers
    # -------------------------
    "kubernetes_troubleshoot": "k8s_troubleshoot.jinja2",
    "kubernetes": "k8s_playbook.jinja2",
    "docker": "dockerfile_best_practices.jinja2",
    "helm": "helm_chart_helper.jinja2",
    "istio": "istio_playbook.jinja2",
    "openshift": "openshift_playbook.jinja2",
    "others (containers)": "other_universal_playbook.jinja2",

    # K8s Quick Task + Fix
    "k8s_quick_task": "k8s_quick_task.jinja2",
    "k8s_quick_fix": "k8s_quick_fix.jinja2",

    # -------------------------
    # Code & Scripts (dedicated fire templates you have)
    # -------------------------
    "bash": "shell_code_generation.jinja2",
    "shell script": "shell_code_generation.jinja2",
    "python": "python_code_generation.jinja2",
    "go": "go_code_generation.jinja2",
    "javascript": "javascript_code_generation.jinja2",
    "java": "java_code_generation.jinja2",
    "c#": "csharp_code_generation.jinja2",
    "rust": "rust_code_generation.jinja2",
    "powershell": "powershell_code_generation.jinja2",
    "other (script/code)": "other_code_generation.jinja2",

    # -------------------------
    # AI & GenAI
    # -------------------------
    "genai_arch": "genai_architecture.jinja2",
    "genai_quick": "genai_quick_task.jinja2",

    "genai pipelines": "genai_architecture.jinja2",
    "model fine-tuning": "genai_architecture.jinja2",
    "llm deployment": "genai_architecture.jinja2",
    "amazon bedrock": "genai_architecture.jinja2",
    "vertex ai / sagemaker": "genai_architecture.jinja2",
    "others (ai)": "other_universal_playbook.jinja2",

    # GenAI Quick Fix
    "genai_quick_fix": "genai_quick_fix.jinja2",

    # -------------------------
    # Data & MLOps
    # -------------------------
    "data_arch": "data_architecture.jinja2",
    "mlops_arch": "mlops_architecture.jinja2",

    "data engineering": "data_architecture.jinja2",
    "mlops": "mlops_architecture.jinja2",
    "data lake": "data_architecture.jinja2",
    "airflow / dbt": "airflow_dag_or_dbt_model.jinja2",
    "others (data)": "other_universal_playbook.jinja2",

    # Data Quick Task + Fix
    "data_quick_task": "data_quick_task.jinja2",
    "data_quick_fix": "data_quick_fix.jinja2",

    # -------------------------
    # Troubleshooting (General)
    # -------------------------
    "troubleshooting": "troubleshooting.jinja2",
    "file upload analyzer": "troubleshooting.jinja2",

    # -------------------------
    # CI/CD & Platform Automation
    # -------------------------
    "github actions": "gha_workflow.jinja2",
    "gitlab ci/cd": "gitlab_ci_playbook.jinja2",
    "azure devops": "azure_devops_pipeline.jinja2",
    "argocd": "argocd_appset_helper.jinja2",
    "jenkins": "jenkins_playbook.jinja2",
    "observability": "observability_runbook.jinja2",
    "security & compliance": "security_compliance_playbook.jinja2",
    "cost optimization": "cost_quick_wins.jinja2",
    "cloud migrations": "migration_playbook.jinja2",

    # CI/CD Quick Task + Fix
    "cicd_quick_task": "cicd_quick_task.jinja2",
    "cicd_quick_fix": "cicd_quick_fix.jinja2",

    # -------------------------
    # Misc / Other
    # -------------------------
    "api gateway templates": "api_gateway_playbook.jinja2",
    "other": "other_universal_playbook.jinja2",

    # -------------------------
    # Platform Audit
    # -------------------------
    "platform audit": "platform_audit.jinja2"
}
