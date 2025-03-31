# Use a base image with Go + Alpine if you're building from source
FROM golang:1.21-alpine as builder

# Install Git and build tools
RUN apk add --no-cache git make bash

# Set working directory
WORKDIR /go/src/spark-operator

# Clone the Spark Operator repo (or copy your local source code here)
RUN git clone https://github.com/GoogleCloudPlatform/spark-on-k8s-operator.git . \
    && git checkout v1beta2-1.3.8-3.1.1

# Build the Spark Operator binary
RUN make clean && make build

# --- Runtime image ---
FROM gcr.io/distroless/base-debian11

# Copy the compiled binary
COPY --from=builder /go/src/spark-operator/bin/spark-operator /usr/bin/spark-operator

# Optional: expose metrics port
EXPOSE 8080

# Set entrypoint to the Spark Operator binary
ENTRYPOINT ["/usr/bin/spark-operator"]


# Use an official Spark base image (adjust to your Spark version)
#FROM bitnami/spark:3.5.0

# Set the working directory
#WORKDIR /app

# Copy your ETL job script from the correct folder
#COPY src/main/python/etl_job.py .

# (Optional) If you have other required files (e.g., config or dependencies), copy them too:
# COPY requirements.txt .

# Define the default command (you can override this when running)
#CMD ["spark-submit", "/app/etl_job.py"]