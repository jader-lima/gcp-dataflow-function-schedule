# GCP DataFlow Function Schedule

## Overview

This project showcases the integration of Google Cloud services, specifically Dataflow, Cloud Functions, and Cloud Scheduler, to create a highly scalable, cost-effective, and easy-to-maintain data processing solution. It demonstrates how you can automate data pipelines, perform seamless integration with other GCP services like BigQuery, and manage workflows efficiently through CI/CD pipelines with GitHub Actions. This setup provides flexibility, reduces manual intervention, and ensures that the data processing workflows run smoothly and consistently.

## Table of Contents

- [Technologies Used](#technologies-used)
- [Features](#features)
- [Architecture Diagram](#architecture-diagram)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Setup Instructions](#setup-instructions)
- [Deploying the Project](#deploying-the-project)
  - [Workflow YAML Explanation](#workflow-yaml-explanation)
  - [Workflow Job Steps](#workflow-job-steps)
- [Resources Created After Deployment](#resources-created-after-deployment)
- [Conclusion](#conclusion)
- [Documentation Links](#documentation-links)

## Technologies Used

- **Google Dataflow**  
  Google Dataflow is a fully managed service for stream and batch data processing, which is built on Apache Beam. It allows for the creation of highly efficient, low-latency, and cost-effective data pipelines. Dataflow can handle large-scale data processing tasks, making it ideal for use cases like real-time analytics and ETL jobs.

- **Cloud Storage**  
  Google Cloud Storage is a scalable, durable, and secure object storage service designed to handle large volumes of unstructured data. It is ideal for use in big data analysis, backups, and content distribution, offering high availability and low latency across the globe.

- **Cloud Functions**  
  Google Cloud Functions is a serverless execution environment that allows you to run code in response to events. In this project, Cloud Functions are used to trigger Dataflow jobs and manage workflow automation efficiently with minimal operational overhead.

- **Cloud Scheduler**  
  Google Cloud Scheduler is a fully managed cron job service that allows you to schedule tasks or trigger cloud services at specific intervals. It’s used in this project to automate the execution of the Cloud Functions, ensuring that Dataflow jobs run as needed without manual intervention.

- **CI/CD Process with GitHub Actions**  
  GitHub Actions enables continuous integration and continuous delivery (CI/CD) workflows directly from your GitHub repository. In this project, it is used to automate the build, testing, and deployment of resources to Google Cloud, ensuring consistent and reliable deployments.

- **GitHub Secrets and Configuration**  
  GitHub Secrets securely store sensitive information such as API keys, service account credentials, and configuration settings required for deployment. By keeping these details secure, the risk of leaks and unauthorized access is minimized.

## Features

- Ingest and transform data from Google Cloud Storage using Google Dataflow.
- Encapsulate the Dataflow process into a reusable Dataflow template.
- Create a Cloud Function that executes the Dataflow template through a REST API.
- Automate the execution of the Cloud Function using Cloud Scheduler.
- Implement a CI/CD pipeline with GitHub Actions for automated deployments.
- Incorporate comprehensive error handling and logging for reliable data processing.

## Architecture Diagram

![Architecture Diagram](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/8q2nw194pekf1nfkctbr.png)

## Getting Started

### Prerequisites

Before getting started, ensure you have the following:

- A Google Cloud account with billing enabled.
- A GitHub account.

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/jader-lima/gcp-dataproc-bigquery-workflow-template.git
   cd gcp-dataproc-bigquery-workflow-template

## Set Up Google Cloud Environment

1. **Create a Google Cloud Storage bucket** to store your data.
2. **Set up a BigQuery dataset** where your data will be ingested.
3. **Create a Dataproc cluster** for processing.

## Configure Environment Variables and Secrets

Ensure the following environment variables are set in your deployment configuration or within GitHub Secrets:

- `GCP_BUCKET_BIGDATA_FILES`: Secret used to store the name of the cloud storage
- `GCP_BUCKET_DATALAKE`: Secret used to store the name of the cloud storage
- `GCP_BUCKET_DATAPROC`: Secret used to store the name of the cloud storage
- `GCP_BUCKET_TEMP_BIGQUERY`: Secret used to store the name of the cloud storage
- `GCP_DEVOPS_SA_KEY`: Secret used to store the value of the service account key. For this project, the default service key was used. 
- `GCP_SERVICE_ACCOUNT`: Secret used to store the value of the service account key. For this project, the default service key was used. 
- `PROJECT_ID`: Secret used to store the project id value

## Creat a new service account for deploy purposes 

1. Criar a Conta de Serviço:

gcloud iam service-accounts create devops-dataops-sa \
    --description="Service account for DevOps and DataOps tasks" \
    --display-name="DevOps DataOps Service Account"

2. Conceder Permissões de Acesso ao Storage (Buckets):
Storage Admin (roles/storage.admin): Concede permissões para criar, listar, e manipular buckets e arquivos.

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:devops-dataops-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

3. Conceder Permissões para o Dataflow:
Dataflow Admin (roles/dataflow.admin): Para criar, executar e gerenciar jobs do Dataflow.
Dataflow Developer (roles/dataflow.developer): Permite o desenvolvimento e envio de jobs do Dataflow.


gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:devops-dataops-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/dataflow.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:devops-dataops-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/dataflow.developer"

4. Permissões para Criar e Gerenciar Cloud Functions e Cloud Scheduler:
Cloud Functions Admin (roles/cloudfunctions.admin): Para criar e gerenciar Cloud Functions.
Cloud Scheduler Admin (roles/cloudscheduler.admin): Para criar e gerenciar jobs do Cloud Scheduler.

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:devops-dataops-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/cloudfunctions.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:devops-dataops-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/cloudscheduler.admin"

5. Conceder Permissões para Gerenciar Contas de Serviço:
IAM Service Account Admin (roles/iam.serviceAccountAdmin): Para criar e gerenciar outras contas de serviço.
IAM Service Account User (roles/iam.serviceAccountUser): Para usar as contas de serviço em diferentes serviços.

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:devops-dataops-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/iam.serviceAccountAdmin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:devops-dataops-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/iam.serviceAccountUser"


gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:devops-dataops-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/serviceusage.serviceUsageAdmin"



gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:devops-dataops-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/resourcemanager.projectIamAdmin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:devops-dataops-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/resourcemanager.projectIamAdmin"


6. Permissão para habilitar api services 
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:devops-dataops-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/cloudscheduler.admin"

7. Permissões Adicionais (Opcional):
Compute Admin (roles/compute.admin): Se o seu pipeline precisar criar recursos de computação (por exemplo, instâncias de máquinas virtuais).
Viewer (roles/viewer): Para garantir que a conta possa visualizar outros recursos no projeto.

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:devops-dataops-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/compute.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:devops-dataops-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/viewer"


### Creating github secret

1. To create a new secret:
    1. In project repository, menu **Settings** 
    2. **Security**, 
    3. **Secrets and variables**,click in access **Action**
    4. **New repository secret**, type a **name** and **value** for secret.

![github secret creation](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/i45cicz0q89ije7j70yf.png)

For more details , access :
https://docs.github.com/pt/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions

## Deploying the project <a name="workflow-overview"></a>

Whenever a push to the main branch occurs, GitHub Actions will trigger and run the YAML script. The script contains four jobs, described in detail below. In essence, GitHub Actions uses the service account credentials to authenticate with Google Cloud and execute the necessary steps as described in the YAML file.

## Workflow File YAML Explanation<a name="workflow-yaml-explanation"></a>

Environments Needed
We have variations for basic usage for cluster characteristics, bucket paths, process names and steps 
make workflow. In case of new steps in the workflow or new scripts, new variables can be easily added as below :

```yaml
MY_VAR_NAME : my_var_value 
${{ env.MY_VAR_NAME}}
```

```yaml
env:
    REGION: us-east1
    ZONE: us-east1-b
    GCP_BUCKET_DATAFLOW_TEMPLATE : datalake_dataflow_template_17092024
    GCP_BUCKET_DATAFLOW_TEMPLATE_TEMP : datalake_dataflow_template_temp_17092024
    GCP_BUCKET_DATAFLOW_TEMPLATE_STAGING : datalake_dataflow_template_staging_17092024
    GCP_BUCKET_DATAFLOW_DATA : datalake_dataflow_data_17092024
    TRANSIENT_DATALAKE_FILES: transient
    BUCKET_DATALAKE_FOLDER: transient
    BUCKET_DATALAKE_SILVER_FOLDER : silver
    BUCKET_DATALAKE_SUBJECT_FOLDER : olist
    TEMPLATE_NAME : etl_olist_template    
    INPUT_FOLDER : inputs
    OUTPUT_FOLDER : output
    ITEMS : olist_order_items_dataset.csv
    SELLERS : olist_sellers_dataset.csv
    PRODUCTS : olist_products_dataset.csv
    ORDERS : olist_orders_dataset.csv
    REVIEWS : olist_order_reviews_dataset.csv
    PAYMENTS : olist_order_payments_dataset.csv
    CUSTOMERS : olist_customers_dataset.csv
    GS_PREFIX : gs://
    RUNNER : Dataflow
    FUNCTION_NAME : create_dataflow_job
    ENTRY_POINT : create_dataflow_job
    PYTHON_FUNCTION_RUNTIME : python310
    DATAFLOW_SCRIPTS : dataflow_scripts
    FUNCTION_SCRIPTS : cloud_function_scripts
    ROLE1 : roles/cloudfunctions.invoker
    ROLE2 : roles/dataflow.admin
    ROLE3 : roles/storage.objectViewer
    SCHEDULE_NAME : run_dataflow_job_olist_etl
    DATAFLOW_JOB_NAME : olist_analysis
    WORKER_MACHINE_TYPE : n1-standard-1
    NUM_WORKERS : 2 
    MAX_WORKERS: 2
    GCP_SERVICE_API_1 : cloudbuild.googleapis.com
    GCP_SERVICE_API_2 : run.googleapis.com
    GCP_SERVICE_API_3 : cloudfunctions.googleapis.com
    SERVICE_ACCOUNT_NAME: account-dataflow-scheduler

```

## Workflow Job Steps <a name="enable-services"></a>


- **enable-services**:
This step enables the necessary APIs for Cloud Functions, Dataflow, and the build process.

```yaml
 enable-services:
    runs-on: ubuntu-22.04
    steps:
    - uses: actions/checkout@v2
    
    # Step to Authenticate with GCP
    - name: Authorize GCP
      uses: 'google-github-actions/auth@v2'
      with:
        credentials_json:  ${{ secrets.GCP_DEVOPS_SA_KEY }}

    # Step to Configure  Cloud SDK
    - name: Set up Cloud SDK
      uses: google-github-actions/setup-gcloud@v2
      with:
        version: '>= 363.0.0'
        project_id: ${{ secrets.PROJECT_ID }}
        
    # Step to Configure Docker to use the gcloud command-line tool as a credential helper
    - name: Configure Docker
      run: |-
        gcloud auth configure-docker

    - name: Set up python 3.8
      uses: actions/setup-python@v2
      with:
        python-version: 3.8.16

    # Step to Create GCP Bucket 
    - name: Enable gcp service api's
      run: |-
        gcloud services enable ${{ env.GCP_SERVICE_API_1 }}
        gcloud services enable ${{ env.GCP_SERVICE_API_2 }}
        gcloud services enable ${{ env.GCP_SERVICE_API_3 }}

```

- **deploy-buckets**:
This step creates Google Cloud Storage buckets and copies the required data files and scripts into them.

```yaml
  deploy-buckets:
    needs: [enable-services]
    runs-on: ubuntu-22.04
    timeout-minutes: 10

    steps:
    - name: Checkout
      uses: actions/checkout@v4
    
    - name: Authorize GCP
      uses: 'google-github-actions/auth@v2'
      with:
        credentials_json:  ${{ secrets.GCP_DEVOPS_SA_KEY }}
    
    # Step to Authenticate with GCP
    - name: Set up Cloud SDK
      uses: google-github-actions/setup-gcloud@v2
      with:
        version: '>= 363.0.0'
        project_id: ${{ secrets.PROJECT_ID }}

    # Step to Configure Docker to use the gcloud command-line tool as a credential helper
    - name: Configure Docker
      run: |-
        gcloud auth configure-docker


    # Step to Create GCP Bucket 
    - name: Create Google Cloud Storage - Dataflow Template
      run: |-
        if ! gsutil ls -p ${{ secrets.PROJECT_ID }} gs://${{ secrets.GCP_BUCKET_DATAFLOW_TEMPLATE }} &> /dev/null; \
          then \
            gcloud storage buckets create gs://${{ secrets.GCP_BUCKET_DATAFLOW_TEMPLATE }} --default-storage-class=nearline --location=${{ env.REGION }}
          else
            echo "Cloud Storage : gs://${{ secrets.GCP_BUCKET_DATAFLOW_TEMPLATE }}  already exists" ! 
          fi

    # Step to Create GCP Bucket 
    - name: Create Google Cloud Storage - Dataflow  bucket from temporary files
      run: |-
        if ! gsutil ls -p ${{ secrets.PROJECT_ID }} gs://${{ secrets.GCP_BUCKET_DATAFLOW_TEMPLATE_TEMP }} &> /dev/null; \
          then \
            gcloud storage buckets create gs://${{ secrets.GCP_BUCKET_DATAFLOW_TEMPLATE_TEMP }} --default-storage-class=nearline --location=${{ env.REGION }}
          else
            echo "Cloud Storage : gs://${{ secrets.GCP_BUCKET_DATAFLOW_TEMPLATE_TEMP }}  already exists" ! 
          fi

    # Step to Create GCP Bucket 
    - name: Create Google Cloud Storage - Dataflow  bucket from staging files
      run: |-
        if ! gsutil ls -p ${{ secrets.PROJECT_ID }} gs://${{ secrets.GCP_BUCKET_DATAFLOW_TEMPLATE_STAGING }} &> /dev/null; \
          then \
            gcloud storage buckets create gs://${{ secrets.GCP_BUCKET_DATAFLOW_TEMPLATE_STAGING }} --default-storage-class=nearline --location=${{ env.REGION }}
          else
            echo "Cloud Storage : gs://${{ secrets.GCP_BUCKET_DATAFLOW_TEMPLATE_STAGING }}  already exists" ! 
          fi


    # Step to Create GCP Bucket 
    - name: Create Google Cloud Storage - datalake
      run: |-
        if ! gsutil ls -p ${{ secrets.PROJECT_ID }} gs://${{ secrets.GCP_BUCKET_DATAFLOW_DATA }} &> /dev/null; \
          then \
            gcloud storage buckets create gs://${{ secrets.GCP_BUCKET_DATAFLOW_DATA }} --default-storage-class=nearline --location=${{ env.REGION }}
          else
            echo "Cloud Storage : gs://${{ secrets.GCP_BUCKET_DATAFLOW_DATA }}  already exists" ! 
          fi



    # Step to Upload the file to GCP Bucket - transient files
    - name: Upload transient files to Google Cloud Storage
      run: |-
        TARGET=${{ env.TRANSIENT_DATALAKE_FILES }}
        BUCKET_PATH=${{ secrets.GCP_BUCKET_DATAFLOW_DATA }}/${{ env.BUCKET_DATALAKE_FOLDER }}    
        gsutil cp -r $TARGET gs://${BUCKET_PATH}

```

- **build-dataflow-classic-template**:
Builds and stores a Dataflow template in a Cloud Storage bucket for future execution.

```yaml
build-dataflow-classic-template:
    needs: [enable-services, deploy-buckets]
    runs-on: ubuntu-22.04
    steps:
    - uses: actions/checkout@v2
    
    # Step to Authenticate with GCP
    - name: Authorize GCP
      uses: 'google-github-actions/auth@v2'
      with:
        credentials_json:  ${{ secrets.GCP_DEVOPS_SA_KEY }}

    # Step to Configure  Cloud SDK
    - name: Set up Cloud SDK
      uses: google-github-actions/setup-gcloud@v2
      with:
        version: '>= 363.0.0'
        project_id: ${{ secrets.PROJECT_ID }}
        
    # Step to Configure Docker to use the gcloud command-line tool as a credential helper
    - name: Configure Docker
      run: |-
        gcloud auth configure-docker

    - name: Set up python 3.8
      uses: actions/setup-python@v2
      with:
        python-version: 3.8.16

    - name: Install dependencies apache beam dependencies
      run: |-
        cd ${{ env.DATAFLOW_SCRIPTS }}
        python -m pip install --upgrade pip setuptools==65.5.0 wheel
        pip install coverage
        if [ -f requirements.txt ]; 
          then 
            pip install --verbose -r requirements.txt; 
        fi

    - name: Create Dataflow classic template in Dataflow Template Bucket
      run: |-
        TEMPLATE_NAME=etl_olist_template
        GS_PREFIX=gs://
        GCP_BUCKET_DATAFLOW_TEMPLATE=${{ env.GS_PREFIX }}${{ secrets.GCP_BUCKET_DATAFLOW_TEMPLATE }}/templates/$TEMPLATE_NAME
        GCP_BUCKET_DATAFLOW_TEMPLATE_TEMP=${{ env.GS_PREFIX }}${{ secrets.GCP_BUCKET_DATAFLOW_TEMPLATE_TEMP }}/temp
        GCP_BUCKET_DATAFLOW_TEMPLATE_STAGING=${{ env.GS_PREFIX }}${{ secrets.GCP_BUCKET_DATAFLOW_TEMPLATE_STAGING }}/staging

        python ${{ env.DATAFLOW_SCRIPTS }}/etl_olist_template.py --runner ${{ env.RUNNER }} --project ${{ secrets.PROJECT_ID }} --region ${{ env.REGION }} \
        --staging_location $GCP_BUCKET_DATAFLOW_TEMPLATE_STAGING \
        --temp_location $GCP_BUCKET_DATAFLOW_TEMPLATE_TEMP \
        --template_location $GCP_BUCKET_DATAFLOW_TEMPLATE

```


- **deploy-cloud-function**:
Deploys a Cloud Function that triggers the execution of the Dataflow template using the google-api-python-client library.

```yaml
deploy-cloud-function:
    needs: [enable-services, deploy-buckets, build-dataflow-classic-template]
    runs-on: ubuntu-22.04
    steps:
    - uses: actions/checkout@v2
    
    # Step to Authenticate with GCP
    - name: Authorize GCP
      uses: 'google-github-actions/auth@v2'
      with:
        credentials_json:  ${{ secrets.GCP_DEVOPS_SA_KEY }}

    # Step to Configure  Cloud SDK
    - name: Set up Cloud SDK
      uses: google-github-actions/setup-gcloud@v2
      with:
        version: '>= 363.0.0'
        project_id: ${{ secrets.PROJECT_ID }}
        
    # Step to Configure Docker to use the gcloud command-line tool as a credential helper
    - name: Configure Docker
      run: |-
        gcloud auth configure-docker

    - name: Set up python 3.10
      uses: actions/setup-python@v2
      with:
        python-version: 3.10.12

    - name: Create cloud function
      run: |-
        cd ${{ env.FUNCTION_SCRIPTS }}
        gcloud functions deploy ${{ env.FUNCTION_NAME }} \
        --gen2 \
        --runtime ${{ env.PYTHON_FUNCTION_RUNTIME }} \
        --trigger-http \
        --allow-unauthenticated \
        --region ${{ env.REGION }} \
        --entry-point ${{ env.ENTRY_POINT }}

```

- **deploy-cloud-schedule**:
Creates a Cloud Scheduler job to automate the execution of the Cloud Function, ensuring data is processed at defined intervals.

```yaml
deploy-cloud-schedule:
    needs: [enable-services, deploy-buckets, build-dataflow-classic-template, deploy-cloud-function]
    runs-on: ubuntu-22.04
    timeout-minutes: 10

    steps:
    - name: Checkout
      uses: actions/checkout@v4
    
    - name: Authorize GCP
      uses: 'google-github-actions/auth@v2'
      with:
        credentials_json:  ${{ secrets.GCP_DEVOPS_SA_KEY }}
    
    # Step to Authenticate with GCP
    - name: Set up Cloud SDK
      uses: google-github-actions/setup-gcloud@v2
      with:
        version: '>= 363.0.0'
        project_id: ${{ secrets.PROJECT_ID }}

    # Step to Configure Docker to use the gcloud command-line tool as a credential helper
    - name: Configure Docker
      run: |-
        gcloud auth configure-docker


    - name: Create service account
      run: |-
      
        if ! gcloud iam service-accounts list | grep -i ${{ env.SERVICE_ACCOUNT_NAME}} &> /dev/null; \
          then \
            gcloud iam service-accounts create ${{ env.SERVICE_ACCOUNT_NAME }} \
            --display-name="scheduler dataflow service account"
          fi

    - name: Add the cloudfunctions.invoker role for service account
      run: |-
        gcloud projects add-iam-policy-binding ${{secrets.PROJECT_ID}} \
        --member=serviceAccount:${{env.SERVICE_ACCOUNT_NAME}}@${{secrets.PROJECT_ID}}.iam.gserviceaccount.com \
        --role="${{env.ROLE1}}"

    - name: Add the dataflow.admin role for service account
      run: |-
        gcloud projects add-iam-policy-binding ${{secrets.PROJECT_ID}} \
        --member=serviceAccount:${{env.SERVICE_ACCOUNT_NAME}}@${{secrets.PROJECT_ID}}.iam.gserviceaccount.com \
        --role="${{env.ROLE2}}"

    - name: Add the storage.objectViewer role for service account
      run: |-
        gcloud projects add-iam-policy-binding ${{secrets.PROJECT_ID}} \
        --member=serviceAccount:${{env.SERVICE_ACCOUNT_NAME}}@${{secrets.PROJECT_ID}}.iam.gserviceaccount.com \
        --role="${{env.ROLE3}}"


    - name: Create cloud schedule for dataflow classi template execution
      run: |-
        if ! gcloud scheduler jobs list --location ${{env.REGION}} | grep -i ${{env.SCHEDULE_NAME}} &> /dev/null; \
          then \
            GCP_BUCKET_DATAFLOW_TEMPLATE=${{ env.GS_PREFIX }}${{ secrets.GCP_BUCKET_DATAFLOW_TEMPLATE }}/templates/$TEMPLATE_NAME
            GCP_BUCKET_DATAFLOW_TEMPLATE_TEMP=${{ env.GS_PREFIX }}${{ secrets.GCP_BUCKET_DATAFLOW_TEMPLATE_TEMP }}/temp
            GCP_BUCKET_DATAFLOW_TEMPLATE_STAGING=${{ env.GS_PREFIX }}${{ secrets.GCP_BUCKET_DATAFLOW_TEMPLATE_STAGING }}/staging
            INPUT_ITEMS=${{ env.GS_PREFIX }}${{ secrets.GCP_BUCKET_DATAFLOW_DATA }}/${{ env.BUCKET_DATALAKE_FOLDER }}/${{env.BUCKET_DATALAKE_SUBJECT_FOLDER}}/${{env.ITEMS}}
            INPUT_SELLERS=${{ env.GS_PREFIX }}${{ secrets.GCP_BUCKET_DATAFLOW_DATA }}/${{ env.BUCKET_DATALAKE_FOLDER }}/${{env.BUCKET_DATALAKE_SUBJECT_FOLDER}}/${{env.SELLERS}}   
            INPUT_PRODUCTS=${{ env.GS_PREFIX }}${{ secrets.GCP_BUCKET_DATAFLOW_DATA }}/${{ env.BUCKET_DATALAKE_FOLDER }}/${{env.BUCKET_DATALAKE_SUBJECT_FOLDER}}/${{env.PRODUCTS}}
            INPUT_ORDERS=${{ env.GS_PREFIX }}${{ secrets.GCP_BUCKET_DATAFLOW_DATA }}/${{ env.BUCKET_DATALAKE_FOLDER }}/${{env.BUCKET_DATALAKE_SUBJECT_FOLDER}}/${{env.ORDERS}}    
            INPUT_REVIEWS=${{ env.GS_PREFIX }}${{ secrets.GCP_BUCKET_DATAFLOW_DATA }}/${{ env.BUCKET_DATALAKE_FOLDER }}/${{env.BUCKET_DATALAKE_SUBJECT_FOLDER}}/${{env.REVIEWS}}    
            INPUT_PAYMENTS=${{ env.GS_PREFIX }}${{ secrets.GCP_BUCKET_DATAFLOW_DATA }}/${{ env.BUCKET_DATALAKE_FOLDER }}/${{env.BUCKET_DATALAKE_SUBJECT_FOLDER}}/${{env.PAYMENTS}}     
            INPUT_CUSTOMERS=${{ env.GS_PREFIX }}${{ secrets.GCP_BUCKET_DATAFLOW_DATA }}/${{ env.BUCKET_DATALAKE_FOLDER }}/${{env.BUCKET_DATALAKE_SUBJECT_FOLDER}}/${{env.CUSTOMERS}}  
            DATA_OUTPUT=${{ env.GS_PREFIX }}${{ secrets.GCP_BUCKET_DATAFLOW_DATA }}/${{ env.BUCKET_DATALAKE_SILVER_FOLDER }}/${{env.BUCKET_DATALAKE_SUBJECT_FOLDER}}/   
            


            gcloud scheduler jobs create http ${{env.SCHEDULE_NAME}} \
            --schedule "00 08 * * *" \
            --uri "https://${{env.REGION}}-${{secrets.PROJECT_ID}}.cloudfunctions.net/${{ env.FUNCTION_NAME }}" \
            --http-method "POST" \
            --location=${{env.REGION}} \
            --headers "Content-Type=application/json,User-Agent=Google-Cloud-Scheduler" \
            --time-zone=${{env.TIME_ZONE}} \
            --message-body "{\"project\":\"${{secrets.PROJECT_ID}}\",\"job\":\"${{env.DATAFLOW_JOB_NAME}}\",\"template\":\"$GCP_BUCKET_DATAFLOW_TEMPLATE\",\"parameters\":{\"input_itens\":\"$INPUT_ITEMS\",\"input_seller\":\"$INPUT_SELLERS\",\"input_products\":\"$INPUT_PRODUCTS\",\"input_order\":\"$INPUT_ORDERS\",\"input_reviews\":\"$INPUT_REVIEWS\",\"input_payments\":\"$INPUT_PAYMENTS\",\"input_customer\":\"$INPUT_CUSTOMERS\",\"output\":\"$DATA_OUTPUT\"},\"worker_machine_type\":\"${{ env.WORKER_MACHINE_TYPE}}\",\"num_workers\":${{ env.NUM_WORKERS}},\"max_workers\":${{ env.MAX_WORKERS}},\"staging_location\":\"$GCP_BUCKET_DATAFLOW_TEMPLATE_STAGING\",\"temp_location\":\"$GCP_BUCKET_DATAFLOW_TEMPLATE_TEMP\",\"region\":\"${{env.REGION}}\"}" \
            --oidc-service-account-email "${{env.SERVICE_ACCOUNT_NAME}}@${{secrets.PROJECT_ID}}.iam.gserviceaccount.com"
          fi



```




## Resources Created After Deployment

Upon deployment, the following resources are created:

### Google Cloud Storage Bucket
A Cloud Storage bucket to store data and templates.



![cloud storage](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/8egg4eg3jeonb1bwuu9q.JPG)

### Dataflow Classic Template
A reusable Dataflow template stored in Cloud Storage.





![dataproc-workflow3](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/jj0payqwvuca6pq1vyq1.JPG)

### Cloud Scheduler Job
Automated scheduled jobs for Dataflow executions.




![Cloud Schedule](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/x74p6oys3q5n66vx2ojf.JPG)

## Conclusion<a name="Conclusion"></a>

This project demonstrates how to leverage Google Cloud services like Dataflow, Cloud Functions, and Cloud Scheduler to create a fully automated and scalable data processing pipeline. The integration with GitHub Actions ensures continuous deployment, while the use of Cloud Functions and Scheduler provides flexibility and automation, minimizing operational overhead. This setup is versatile and can be easily extended to incorporate additional GCP services such as BigQuery.

Links and References
[GitHub Repo](https://github.com/jader-lima/gcp-dataflow-function-schedule)
[Cloud Functions](https://cloud.google.com/functions/docs)
[DataFlow](https://cloud.google.com/dataflow/docs)
[Cloud Scheduler](https://docs.github.com/en/actions)

