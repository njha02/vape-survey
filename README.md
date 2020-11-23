## flask-template

### Quick Start

```
conda create -n flask-template python=3.6
source activate flask-template
pip install -r webapp/requirements.txt
cd webapp
flask run
```

### Local Dev
```
cd webapp
./start.sh
```

### Deploy
```
cd webapp
./deploy.sh
```

### First time setting up project:

1. Create secret.yaml with:

```yaml
env_variables:
  SECRET_KEY: "" # replace with uuid.uuid4()
```
2. Create gcloud project
3. Run gcloud app deploy --project <project-name>
4. Download app engine service account key as secret.json
5. Put secret.json and secret.yaml into google bucket
6. Update google bucket location in deploy and start scripts
