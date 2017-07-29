gcloud app deploy ./index.yaml --quiet
gcloud app deploy ./cron.yaml --quiet
gcloud app deploy ./queue.yaml --quiet
gcloud app deploy ./app.yaml --project PROJECT_ID --version 1 --quiet
