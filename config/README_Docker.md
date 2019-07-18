# bmsdemo

In this repository you can find a demo to create a docker image based on ubuntu 
with python3.7, postgreSQL and nginx installed.

Use sudo in front of all docker commands if you are a non-root user. At [this link](https://docs.docker.com/install/linux/linux-postinstall/) 
you can find more info.
___


## Build docker image and run

Open a terminal and run this command to pull the image (x.x.x is the version number of the server, i.e. 1.0.0)

`docker pull dockerhubRepo/bmsdemo:x.x.x`


To create the docker image, Dockerfile must be in this folder

`docker build -t dockerhubRepo/bmsdemo:x.x.x . `


You can specify some arguments with --build-arg, inspect the Dockerfile to see the list of all args.
(e.g. use server_release version instead of x.x.x (e.g. RELEASE=7.1.5)):

`docker build --build-arg SERVER_RELEASE=x.x.x -t dockerhubRepo/bmsdemo:x.x.x . `


To create and start the container:

`sudo docker run -d --name bmsdemoContainer -p 80:80 dockerhubRepo/bmsdemo:x.x.x`


To create and start the container using the console (useful to try flat project, during development phase):
! /bin/sh overwrite cmd, so start manually your services/script

`sudo docker run -it --name bmsdemoContainer -p 80:80 dockerhubRepo/bmsdemo:x.x.x /bin/sh`


To start the container after the first run:

`docker start bmsdemoContainer`


To stop the container:

`docker stop bmsdemoContainer`
___


## Inspect and run commands

To inspect the container:

`docker inspect bmsdemoContainer`


To open bash (or running command) on running container:

`docker exec -i -t bmsdemoContainer bash`
___


## List containers/images

List running containers:

`docker ps`


List all containers:

`docker ps -a`


List all images:

`docker images`
___


## Delete Containers/images

Delete containers (use -v to delete also linked volumes):

`docker rm <ContainerID1> <ContainerID2> ...`


Delete images:

`docker rmi <ImageID1> <ImageID2> ...`


Delete all images:

`docker rmi $(docker images -q)`


Delete all containers:

`docker rm $(docker ps -a -q)`


Delete dangling images:

`docker rmi -f $(docker images -f "dangling=true" -q)`


Delete  
- all stopped containers,
- all networks not used by at least one container,
- all volumes not used by at least one container,
- all dangling images,
- all dangling build cache ,
- and with the option --volumes also unused volumes:
	
`docker system prune --volumes`
___


## Push on dockerhub

Push images on dockerhub (tagged during build if you follow this guide):
- Login: `docker login`
- Push: `docker push dockerhubRepo/bmsdemo`




