# M06 Spark Basics – Python (GCP)

This project demonstrates an end-to-end Spark ETL pipeline deployed on Kubernetes, using GCP and Terraform infrastructure. It fulfills the requirements of the M06 Spark Basics Homework.
## 📌 Project structure

M06_SparkBasics_Python_GCP/
├── etl_job.py
├── Dockerfile
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
        terraform/
                .terraform/terraform.tfstate
├── charts/
│   └── spark-operator-chart/
│       ├── values.yaml
│       └── templates/
│           └── deployment.yaml
├── README.md
├── screenshots/
│   └── *.png
└── .gitignore


## 📌 Steps Completed

### ✅ 1. Terraform Infrastructure (GCP)
- Provisioned GCS bucket: `m06-sparkbasics-gcp-tfstate`
- Provisioned GKE cluster
- Configured with `gcloud auth login`, `gcloud auth configure-docker`, `kubectl`

### ✅ 2. Spark ETL Job
- `etl_job.py` reads **hotels CSV** and **weather Parquet** data
- Uses OpenCage API to enrich hotels with missing coordinates
- Generates **4-character geohash**
- Joins with weather data on geohash (left join)
- Outputs **enriched Parquet dataset partitioned by year/month/day**

### ✅ 3. Docker
- Built custom image `spark-operator:local`
- Pushed to GCR: `gcr.io/m06-sparkbasics-gcp/spark-operator:local`

### ✅ 4. Spark Operator on Kubernetes
- Deployed using Helm chart from `spark-on-k8s-operator`
- Fixed CRDs, image reference, and configuration
- Cleaned up `.gitignore` and removed nested Git issues

### ✅ 5. Final Artifacts
- ✅ Enriched `.parquet` file in GCS
- ✅ Terraform infrastructure
- ✅ Spark ETL job (local + GKE)
- ✅ Working Docker image
- ✅ Clean GitHub repo

---

## 📸 Screenshots to Upload
> Save these from PowerShell or browser, and add them to your repo `screenshots/` folder

1. ✅ Terraform Apply success in PowerShell
2. ✅ Spark ETL job output logs
3. ✅ `gcloud` config list
4. ✅ Parquet files uploaded in GCS bucket (`data/`)
5. ✅ `kubectl get pods` showing the Spark job running or completed
6. ✅ Docker image build + push
7. ✅ GitHub repo structure

---



