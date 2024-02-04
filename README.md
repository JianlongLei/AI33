#  Software Containerization Project -group33
***
This is a project repository for the group 33 of Software Containerization. The project includes frontend, server and database.
Here is the pipeline of how to set up:
1. build image of frontend, server and database
2. using image to containerize the application
3. deploy the project on Google cloud
## Project Structure
The project contains three parts, frontend, server and database. 
### Frontend
Based on Flask, including user interface, access control and communicate with server.
### Server
Including generating image, communicating with db and frontend
### Database
Using Mongodb for store and manage data.
## Docker
Frontend, backend, and database are all built using Docker to create images
```BASH
docker build -t <image name> -f <Dockerfile name> .
```
## Kubernetes on Google Cloud 
The whole project has already been deployed on google cloud successfully. 
Using helm to install, uninstall and upgrade.