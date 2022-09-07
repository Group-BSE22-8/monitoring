# Flask API Template

This project is aimed at checking the status of the physical Crane Cloud Clusters.

- It provides a basic information from the `cluster_logs` model.

## Project Setup

Follow these steps to have a local running copy of the app.

### Clone The Repo

`git clone https://github.com/Group-BSE22-8/monitoring.git`

If `master` is not up to date, `git checkout develop`. However, note that code on develop could be having some minor issues to sort.

### Install PostgreSQL

Here's a great resource to check out:

[How To Install and Use PostgreSQL](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04)

If you have not yet, create a development database and call it `cranecloud`. If you already set up the backend from Crane Cloud, you should already have this setup.

### Create a Virtual Environment

create virtual enviroment called venv

Run `virtualenv venv`

### Activate the virtual environment

Run `. venv/bin/activate`

Make sure you have `pip` installed on your machine.

### Install the dependencies

```bash
pip install -r requirements.txt
```

### Create a .env file

Create a `.env` file (which defines the environment variables used) at the root of the app.

Add the following details, customizing as needed.

```bash
export FLASK_APP=server.py
export DATABASE_URI=postgresql:///flask_app_db
export FLASK_APP_SECRET=qY2i691SX2sEuZ7LUjY480RS48mw5qCeUiyV0i0vzmg
export FLASK_ENV=development
export FLASK_RUN_PORT=5000
export TEST_CLUSTERS='[
    {
        "name": "Cluster 1 name",
        "url": "http://127.0.0.1:5000"
    }
]'
export CLUSTERS='[{
    {
        "name": "Cluster 1 name",
        "url": "http://127.0.0.1:5000"
    }
}]'
```

The TEST_CLUSTERS variable will connect to the default flask application url: http://127.0.0.1:5000. This should ideally only be used for testing purposes and the actual clusters should be put inside the CLUSTERS variable for the production physical clusters to monitor.

### Run Database migrations

Run migrations for the database. This will create the tables for the models in the database .

`python manage.py db upgrade`

#### Note:
Do not run `python manage.py db migrate` because it will clear the tables in the database needed by the other parts of the Crane Cloud platform.

### Run Application

Run the application with this command

```bash
source .env
flask run
```

### Test the API

Through your browser go to link `localhost:<flask_port>/`.

### Activating logging of the cluster status every 5 seconds
There exists a shell script under the ````scipts``` folder called ```physicalClusterJob.sh``` that will handle the logging by running the ```flask scheduledlogging``` command. This command references a function ```clusterLogFunction``` from the ```physical_cluster_status.py``` controller. Modification of the logging functionality should be made to the above function.

Use the command ```nohup sh physicalClusterJob.sh &``` to run the shell script in the background. On running the command it will return it's process id.

### Stopping the logging of the cluster status every 5 seconds
With the process id returned above you can run ```kill -9 process_id``` and example of this could be ```kill -9 21457```. 

If you however do not have the process id or you lost it you can run the command ```ps aux | grep physicalClusterJob``` to return the process. The process id is the second value from the left next to the user's name.

### Checkout Application Api docs

Through your browser go to link `localhost:<flask_port>/apidocs`.
