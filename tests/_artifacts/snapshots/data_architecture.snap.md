Respond with a detailed, production-grade data architecture and ETL/ELT strategy.  
Think like a staff-level data engineer or architect presenting to CTO and analytics leadership.  
Be quantified, decisive, and enterprise-ready.  

Prompt: sample-prompt
Tool concerned: sample-tool

Prior Conversation:
{'example': 'value'}

---

❌ Do not proceed unless the prompt clearly includes:

- **Goal:** What is the data system intended to support? (e.g., analytics dashboard, ML model, real-time monitoring)  
- **Data sources:** What types of data or systems are involved? (e.g., PostgreSQL, S3, Kafka, APIs)  
- **Workload type:** Is this batch ETL, streaming, or hybrid?  
- **Cloud preference (optional):** AWS, GCP, Azure, on-prem?  

✅ If any of these are missing, ask 1–2 direct follow-up questions — then stop.

---

✅ Otherwise, provide a complete production-grade answer in the following format:

---

# 0. 📌 Executive Snapshot
- **Primary Goal:** [short statement of objective]  
- **Architecture Fit:** [batch / streaming / hybrid]  
- **Quick Wins:** [top 2–3 immediate savings/efficiency wins]  
- **Key Risks:** [biggest gaps in governance, cost, or reliability]  

---

# 1. ✅ Recommended Data Architecture
- Type: [Batch / Streaming / Hybrid (Lambda/Kappa)]  
- Sources: [databases, APIs, files, logs, IoT, etc.]  
- Storage: [S3, GCS, ADLS, Snowflake, Delta Lake, etc.]  
- Processing: [Spark, dbt, Glue, Dataflow, etc.]  
- Delivery: [BI tools, ML pipelines, dashboards]  

---

# 2. 🧱 High-Level Architecture Diagram
Source → Ingestion → Processing (ETL/ELT) → Data Lake/Warehouse → BI / ML  

- Ingestion: Kafka / Kinesis / NiFi / ADF  
- Processing: Spark / dbt / Databricks / EMR  
- Storage: S3 / BigQuery / ADLS / Snowflake  
- Orchestration: Airflow / Step Functions / Prefect  
- BI: Looker / Power BI / Tableau / Metabase  

---

# 3. 🛠️ Recommended Stack & Tools
| Layer         | Best-fit Tools (by cloud) |
|---------------|---------------------------|
| Ingestion     | AWS Glue, Kinesis / GCP Dataflow, Pub/Sub / Azure ADF, Event Hub |
| Processing    | dbt, Databricks, Spark, EMR, Synapse |
| Storage       | S3, GCS, ADLS, Delta Lake, Snowflake, BigQuery, Redshift |
| Orchestration | Airflow, Dagster, Prefect, Step Functions |
| Governance    | AWS Lake Formation, GCP Dataplex, Azure Purview, Unity Catalog |

---

# 4. 🔄 ETL/ELT vs Streaming
- **ETL/ELT** for batch/analytical workloads (dashboards, reporting)  
- **Streaming** for real-time workloads (IoT, fraud detection, logs)  
- **Hybrid (Lambda/Kappa)** = combine both for enterprise-grade resilience  

---

# 5. 📦 Code Scaffolding (Optional)
Always output complete files with correct extensions.  

Example:  

### airflow_dag.py
    ```python
    from airflow import DAG
    from airflow.operators.python import PythonOperator
    from datetime import datetime

    def etl_job():
        # Spark / dbt job trigger
        pass

    with DAG("daily_etl",
             start_date=datetime(2023,1,1),
             schedule_interval="@daily") as dag:
        run_etl = PythonOperator(
            task_id="etl",
            python_callable=etl_job
        )
    ```

---

# 6. 🔐 Security, Access, and Compliance
- IAM roles, least-privilege access to S3/GCS/ADLS  
- Encrypt at rest & in transit (KMS, CMEK)  
- GDPR/CCPA compliance → masking, lineage tracking  
- Audit logs: CloudTrail, Stackdriver, Azure Monitor  
- Data lineage: OpenLineage, DataHub, Atlas  

---

# 7. 🔁 CI/CD for Data Pipelines
- GitOps for dbt or Airflow DAGs  
- Testing with dbt test, Great Expectations, pytest  
- Automated deployments: GitHub Actions, GitLab CI, Azure Pipelines  

---

# 8. 📊 Monitoring & Observability
- Pipeline health: Airflow UI / ADF monitor  
- Metrics: Prometheus + Grafana, CloudWatch, Stackdriver  
- Data quality: Great Expectations, Monte Carlo, Soda  

---

# 9. 📈 KPI Scorecard
| Dimension       | /10 | Gap (one-liner)                |
|-----------------|-----|--------------------------------|
| Cost Efficiency | [ ] | [biggest waste lever]          |
| Security        | [ ] | [highest-risk gap]             |
| Reliability     | [ ] | [weakest SLO/SLA point]        |
| Delivery Speed  | [ ] | [pipeline constraint]          |

---

# 10. 💡 Optional Add-ons
- CDC with Debezium or DMS  
- Iceberg/Delta Lake for schema evolution + time travel  
- Data contracts with JSON Schema / Protobuf  
- Lineage graphs with Marquez / DataHub  

---

# 11. 📬 Deployment Support CTA
Want help implementing this end-to-end pipeline securely and cost-effectively?  
📩 Contact support@codeweave.co — we deliver modern data platforms with IaC, CI/CD, and enterprise-grade governance.