TEMPLATE_MAP = {
    # Cloud & Infrastructure
    "AWS": "solutions_architecture.jinja2",
    "Azure": "solutions_architecture.jinja2",
    "GCP": "solutions_architecture.jinja2",
    "Others (Infra)": "solutions_architecture.jinja2",

    # Infrastructure as Code & Automation
    "Terraform": "solutions_architecture.jinja2",
    "AWS CloudFormation": "solutions_architecture.jinja2",
    "Pulumi": "solutions_architecture.jinja2",
    "Ansible": "solutions_architecture.jinja2",
    "Others (IaC / Automation)": "solutions_architecture.jinja2",

    # Kubernetes & Containers
    "Docker": "solutions_architecture.jinja2",
    "Kubernetes": "solutions_architecture.jinja2",
    "Helm": "solutions_architecture.jinja2",
    "Istio": "solutions_architecture.jinja2",
    "OpenShift": "solutions_architecture.jinja2",
    "Others (Containers)": "solutions_architecture.jinja2",

    # Code & Scripts
    "Python": "code_generation.jinja2",
    "Go": "code_generation.jinja2",
    "Bash": "code_generation.jinja2",
    "TypeScript": "code_generation.jinja2",
    "JavaScript": "code_generation.jinja2",
    "Java": "code_generation.jinja2",
    "C#": "code_generation.jinja2",
    "Rust": "code_generation.jinja2",
    "PowerShell": "code_generation.jinja2",
    "Shell Script": "code_generation.jinja2",
    "Other (Script/Code)": "code_generation.jinja2",

    # AI & GenAI
    "GenAI Pipelines (LangChain + Vector DB + RAG)": "genai_architecture.jinja2",
    "Model Fine-Tuning (custom LLMs)": "genai_architecture.jinja2",
    "LLM Deployment (serve models in production)": "genai_architecture.jinja2",
    "Amazon Bedrock (serverless multi-model AI on AWS)": "genai_architecture.jinja2",
    "Vertex AI / SageMaker (cloud AI platforms)": "genai_architecture.jinja2",
    "Others (AI)": "genai_architecture.jinja2",

    # Data & MLOps
    "Data Engineering (merged Data Architect + ETL Pipeline)": "data_architecture.jinja2",
    "Data Lake": "data_architecture.jinja2",
    "Airflow / DBT": "data_architecture.jinja2",
    "MLOps": "mlops_architecture.jinja2",
    "Others (Data)": "mlops_architecture.jinja2",

    # Troubleshooting
    "Troubleshooting (merged Error Diagnosis into this)": "troubleshooting.jinja2",
    "File Upload Analyzer": "troubleshooting.jinja2",

    # CI/CD & Platform Automation
    "GitHub Actions": "solutions_architecture.jinja2",
    "GitLab CI/CD": "solutions_architecture.jinja2",
    "Azure DevOps": "solutions_architecture.jinja2",
    "ArgoCD": "solutions_architecture.jinja2",
    "Jenkins": "solutions_architecture.jinja2",
    "Observability": "solutions_architecture.jinja2",
    "Security & Compliance": "solutions_architecture.jinja2",
    "Cost Optimization": "solutions_architecture.jinja2",
    "Cloud Migrations": "solutions_architecture.jinja2",

    # Misc / Other
    "API Gateway Templates": "solutions_architecture.jinja2",
    "Other": "solutions_architecture.jinja2",

    # Platform Audit
    "Platform Audit": "platform_audit.jinja2"
}