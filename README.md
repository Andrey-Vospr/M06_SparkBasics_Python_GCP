# M06 Spark Basics – Python (GCP)

This project demonstrates building a Spark ETL pipeline using Python, Docker, Kubernetes, and GCP. The pipeline processes hotel and weather data, enriches the dataset using OpenCage Geolocation API and Geohash, and stores the results in a GCP bucket in Parquet format.

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


## 📌 Tools & Services Used
## ✅ 1. Apache Spark (via PySpark)

## ✅ 2. Google Cloud Platform (GCP)

## ✅ 3. Google Kubernetes Engine (GKE)

## ✅ 4. Terraform

## ✅ 5. Docker

## ✅ 6. OpenCage Geocoding API

## ✅ 7. Helm + Spark Operator


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

### ✅ Final Enriched Output:
gs://storage-bucket-polished-owl/hotels_enriched.parquet/


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



