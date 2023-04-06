# Install the required MySQL package

sudo apt-get update -y
sudo apt-get install mysql-client -y

# Running application locally
pip3 install -r requirements.txt
sudo python3 app.py
# Building and running 2 tier web application locally
### Building mysql docker image 
```docker build -t my_db -f Dockerfile_mysql . ```

### Building application docker image 
```docker build -t my_app -f Dockerfile . ```

# Create a new network
docker network create  -d bridge --subnet 182.18.0.1/24 --gateway  182.18.0.1 new-network

docker network ls


#Creating first contianer and adding it to newtwork [new-network]

docker run -d -e MYSQL_ROOT_PASSWORD=pw --network new-network my_db

# Running mysql
```docker run -d -e MYSQL_ROOT_PASSWORD=pw my_db```

#Run docker ps to retrieve container ID and confirm docker is running
#run docker exec -it to confirm database is running in the container
-docker exec -it [container_id] /bin/bash
-login with DBPWD= pw
-use employee; [name of table created]
select * from employee; [This open a table and shows database running]
exit container

#create app container

# Get the IP of the database[msql container] and export it as DBHOST variable
```docker inspect <container_id>```


### Example when running DB runs as a docker container and app is running locally
```
export DBHOST=<container_id>
export DBPORT=3307
```
### Example when running DB runs as a docker container and app is running locally
```
export DBHOST=<container_id>
export DBPORT=3306
```
```
export DBUSER=root
export DATABASE=employees
export DBPWD=pw
export APP_COLOR=blue
```
### Run the application, make sure it is visible in the browser add network
```docker run -p 8080:8080  -e DBHOST=$DBHOST -e DBPORT=$DBPORT -e  DBUSER=$DBUSER -e DBPWD=$DBPWD  my_app```
docker run -p 8080:8080 -e DBHOST=$DBHOST -e DBPORT=$DBPORT -e DBUSER=$DBUSER -e DBPWD=$DBPWD -e APP_COLOR=red --network new-netwrk my_app

#open security group in ec2 console to add inbound rules in sg to allow connection on port 8080

create 3 container on port 8081 to 8083 adding newtork
docker run --name blue_ct -d -p 8081:8080 -e DBHOST=$DBHOST -e DBPORT=$DBPORT -e DBUSER=$DBUSER -e DBPWD=$DBPWD -e APP_COLOR=blue --network new-network my_app
docker run --name green_ct -d -p 8082:8080 -e DBHOST=$DBHOST -e DBPORT=$DBPORT -e DBUSER=$DBUSER -e DBPWD=$DBPWD -e APP_COLOR=green --network new-network my_app
docker run --name lime_ct -d -p 8083:8080 -e DBHOST=$DBHOST -e DBPORT=$DBPORT -e DBUSER=$DBUSER -e DBPWD=$DBPWD -e APP_COLOR=lime --network new-network my_app

#confirm dockers are running
docker ps

#open security group in ec2 console to add inbound rules to allow connection on port 8081.8082,8083

#deploy ec2 instance 
#login into ec2 instance [ssh -i [keyname public ip]
-run chmod 7000 keyname
#install docker and update docker
- sudo yum update -y
- sudo yum install docker -y
#start docker
-sudo systemctl start docker
-sudo systemctl start docker (check docker status)
docker ps
sudo usermod -a -G docker ec2-user [adding ec2 to docker groupto eliminate sudo before docker]
docker ps

#aws configure
aws configure [adding aws deatils from CLI i.e aws_access_key_id, aws_secret_access_key,  Region=us-east-1, format= Json]
-add aws_session_token [vi ~/.aws/credentials]

# Create a new network
docker network create  -d bridge --subnet 182.18.0.1/24 --gateway  182.18.0.1 new-network

docker network ls

#pull image
-docker pull [image url database]
docker pull [image url webapp]
run docker images [to check id]
#create contianer
docker run -d -e MYSQL_ROOT_PASSWORD=pw --network new-network [mysql id] and tag

#verify docker is running 
docker exec -t [cantainer id/bin/bash]

-login with DBPWD= pw
-use employee; [name of table created]
select * from employee; [This open a table and shows database running]
exit container

### Example when running DB runs as a docker container and app is running locally
```
export DBHOST=<container_id>
export DBPORT=3306
```
```
export DBUSER=root
export DATABASE=employees
export DBPWD=pw
export APP_COLOR=blue

#after creating container
docker ps to get container id
#login into one of the containers
#run some dependencies

-apt-get update -y
apt-get install iputils-ping

now ping conatainer [blue or ping]

ping lime