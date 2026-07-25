# Azure Cloud Fundamentals & Data Pipeline Implementation

## Brief Insight
This repository contains the documentation and execution results for an end-to-end cloud data engineering pipeline built entirely within Microsoft Azure. 

The core objective of this project was to establish secure cloud infrastructure and automate data movement. I provisioned Azure Storage accounts to act as data lakes and utilized Azure Data Factory (ADF) as the orchestration engine. The final pipeline successfully reads raw dataset files from a source Blob container, validates the file metadata to ensure data integrity, and securely copies the data to a destination container. 

This assignment served as a hands-on exploration of cloud resource management, Identity and Access Management (IAM) role assignments, and serverless ETL (Extract, Transform, Load) processes using ADF.

## Architecture & Workflow
1. **Resource Setup:** Configured an Azure Resource Group to logically manage all project assets.
2. **Storage Layer:** Deployed an Azure Storage Account with `input-data` and `output-data` Blob containers.
3. **Security & IAM:** Assigned `Reader` and `Storage Blob Data Contributor` roles using Managed Identities to grant ADF secure access to the storage account.
4. **Orchestration (Azure Data Factory):**
   * Configured Linked Services to connect ADF to Blob Storage.
   * Created source and destination Datasets.
   * Built a pipeline utilizing a **Get Metadata** activity to validate the source file's existence before triggering a **Copy Data** activity to move the file to its destination.

## Repository Contents
* `Assignment_Documentation.docx` - Contains comprehensive, step-by-step screenshots validating the deployment of the Resource Group, Storage Containers, IAM Role configurations, pipeline canvas design, and successful pipeline execution logs.

## Tools & Technologies Used
* **Cloud Platform:** Microsoft Azure (Portal)
* **Orchestration:** Azure Data Factory (ADF)
* **Storage:** Azure Blob Storage
* **Security:** Azure Identity and Access Management (IAM)
