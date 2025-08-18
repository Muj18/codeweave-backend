TEMPLATE_MAP = {
    # Cloud & Infrastructure
    "aws": "solutions_architecture.jinja2",
    "azure": "solutions_architecture.jinja2",
    "gcp": "solutions_architecture.jinja2",
    "others (infra)": "solutions_architecture.jinja2",

    # Infrastructure as Code & Automation
    "terraform": "terraform_playbook.jinja2",
    "aws cloudformation": "cloudformation_snippet.jinja2",
    "pulumi": "pulumi_snippet.jinja2",
    "ansible": "ansible_playbook.jinja2",
    "others (iac / automation)": "other_iac_playbook.jinja2",

    # Kubernetes & Containers
    "kubernetes": "k8s_playbook.jinja2",
    "docker": "dockerfile_best_practices.jinja2",
    "helm": "helm_chart_helper.jinja2",
    "istio": "istio_policy_helper.jinja2",
    "openshift": "openshift_admin_helper.jinja2",
    "others (containers)": "other_universal_playbook.jinja2",

    # Code & Scripts
    "bash": "code_generation.jinja2",
    "python": "code_generation.jinja2",
    "go": "code_generation.jinja2",
    "typescript": "code_generation.jinja2",
    "javascript": "code_generation.jinja2",
    "java": "code_generation.jinja2",
    "c#": "code_generation.jinja2",
    "rust": "code_generation.jinja2",
    "powershell": "code_generation.jinja2",
    "shell script": "code_generation.jinja2",
    "other (script/code)": "other_code_playbook.jinja2",

    # AI & GenAI
    "genai pipelines": "genai_architecture.jinja2",
    "model fine-tuning": "genai_architecture.jinja2",
    "llm deployment": "genai_architecture.jinja2",
    "amazon bedrock": "genai_architecture.jinja2",
    "vertex ai / sagemaker": "genai_architecture.jinja2",
    "others (ai)": "other_universal_playbook.jinja2",

    # Data & MLOps
    "data engineering": "data_architecture.jinja2",
    "mlops": "mlops_architecture.jinja2",
    "data lake": "data_architecture.jinja2",
    "airflow / dbt": "airflow_dag_or_dbt_model.jinja2",
    "others (data)": "other_universal_playbook.jinja2",

    # Troubleshooting
    "troubleshooting": "troubleshooting.jinja2",
    "file upload analyzer": "troubleshooting.jinja2",

    # CI/CD & Platform Automation
    "github actions": "gha_workflow.jinja2",
    "gitlab ci/cd": "gitlab_ci_pipeline.jinja2",
    "azure devops": "azure_devops_pipeline.jinja2",
    "argocd": "argocd_appset_helper.jinja2",
    "jenkins": "jenkinsfile_helper.jinja2",
    "observability": "observability_runbook.jinja2",
    "security & compliance": "security_compliance_playbook.jinja2",
    "cost optimization": "cost_quick_wins.jinja2",
    "cloud migrations": "migration_playbook.jinja2",

    # Misc / Other
    "api gateway templates": "api_gateway_playbook.jinja2",
    "other": "other_universal_playbook.jinja2",

    # Platform Audit
    "platform audit": "platform_audit.jinja2"
}