from flask import Flask, render_template, request, url_for
from pymysql import connections
import os
import random
import argparse
import logging
import boto3
# Adding Kubernetes
from kubernetes import client, config


app = Flask(__name__)

DBHOST = os.environ.get("DBHOST")
DBUSER = os.environ.get("DBUSER") or "root"
DBPWD = os.environ.get("DBPWD")
DATABASE = os.environ.get("DATABASE") or "employees"
DBPORT = int(os.environ.get("DBPORT") or "3306")

#Logging
logging.basicConfig(level=logging.INFO)
# Loading Kubernetes configuration
config.load_incluster_config()
v1 = client.CoreV1Api()
configmap = v1.read_namespaced_config_map('app-config','final')
#background_image_location = configmap.data['background-image-location']
#s3bucket = configmap.data['s3-bucket']


##Extracting Information from ConfigMap

APP_NAME = os.environ.get('APP_NAME', 'MyApp')
#APP_BG_IMG_LOC = os.environ.get('APP_BG_IMG_LOC') or "background_image_loction"
#AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
#S3_BUCKET = os.environ.get('S3_BUCKET') or "s3bucket"
# Intialize s3 bucket
#s3 = boto3.client('s3', region_name=AWS_REGION)
# Get the ConfigMap Object
APP_BG_IMG_LOC = configmap.data.get('background-image-location', '')
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
S3_BUCKET = os.environ.get('S3_BUCKET') or "group7background"
name = configmap.data.get('name', '')
#db_pwd = configmap.data["DBPWD"]
db_host = configmap.data["DBHOST"]
s3 = boto3.client('s3', region_name=AWS_REGION)
# Get the URL of the background image from ConfigMap
if APP_BG_IMG_LOC and S3_BUCKET:
    local_image_path = 'static/background.png'
    try:
        s3.download_file(S3_BUCKET, APP_BG_IMG_LOC, local_image_path)
        logging.info('Background image downloaded from S3: s3://{}/{}'.format(S3_BUCKET,APP_BG_IMG_LOC))
    except Exception as e:
        logging.error('Failed to download background image from S3: {}'.format(str(e)))
        #s3.download_file(S3_BUCKET, APP_BG_IMG_LOC, local_image_path)
        #logging.info('Background image downloaded from S3: s3://{}/{}'.format(S3_BUCKET, APP_BG_IMG_LOC))
    #except Exception as e:
     #   logging.error('Failed to download background image from S3: {}'.format(str(e)))


# Get the MySQL DB username and password from K8s secrets
#v1 = client.CoreV1Api()
#username_secret = v1.read_namespaced_secret("my-secrets", "final")
#password_secret = v1.read_namespaced_secret("my-secrets", "final")

# Decode the secrets to get the username and password
#db_user = username_secret.data.get("username").decode()
#db_password = password_secret.data.get("password")

# Set the environment variable with your name from the ConfigMap
name = configmap.data.get("name")
os.environ['NAME'] = name

# Create a connection to the MySQL database
db_conn = connections.Connection(
    host= db_host,
    port= DBPORT,
    user= DBUSER,
    password= DBPWD, 
    db= DATABASE
)

output = {}
table = 'employee'

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('addemp.html', app_name=APP_NAME, background_image_path='/app/background.png',name=name)

@app.route("/about", methods=['GET','POST'])
def about():
    return render_template('about.html', app_name=APP_NAME, background_image_path=url_for("static", filename="background.png"), name=name)

    
@app.route("/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    primary_skill = request.form['primary_skill']
    location = request.form['location']

    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:
        cursor.execute(insert_sql,(emp_id, first_name, last_name, primary_skill, location))
        db_conn.commit()
        emp_name = "" + first_name + " " + last_name

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('addempoutput.html', name=emp_name, background=APP_BG_IMG)

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    return render_template("getemp.html", background=APP_BG_IMG)

@app.route("/fetchdata", methods=['GET','POST'])
def FetchData():
    emp_id = request.form['emp_id']

    output = {}
    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location from employee where emp_id=%s"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql,(emp_id))
        result = cursor.fetchone()

        # Add No Employee found form
        output["emp_id"] = result[0]
        output["first_name"] = result[1]
        output["last_name"] = result[2]
        output["primary_skills"] = result[3]
        output["location"] = result[4]
        
    except Exception as e:
        print(e)

    finally:
        cursor.close()

    return render_template("getempoutput.html", id=output["emp_id"], fname=output["first_name"],
                           lname=output["last_name"], interest=output["primary_skills"], location=output["location"],app_name=APP_NAME, background_image_path=local_image_path)

if __name__ == '__main__':
    
    # Check for Command Line Parameters for color
    parser = argparse.ArgumentParser()
    parser.add_argument('--color', required=False)
    args = parser.parse_args()

    

    app.run(host='0.0.0.0',port=81,debug=True)
