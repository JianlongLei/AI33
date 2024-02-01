# AI33


## How to run
First install uvicorn
```BASH
pip install "uvicorn[standard]"
```
Run main
```BASH
uvicorn main:app --reload
```
Check the API doc at:  http://127.0.0.1:8000/docs
or  http://127.0.0.1:8000/redoc

Build and run docker

Build server image
```BASH
docker build -t ai33_server .
```
run database docker container
```BASH
docker run -d `
    -p 27017:27017 `
    --name ai33-mongo `
    --network mongodb `
    -v mongo-data:/data/db `
    -e MONGODB_INITDB_ROOT_USERNAME=ai33 `
    -e MONGODB_INITDB_ROOT_PASSWORD=a_strong_password `
    mongo:latest
```
run server docker container

```BASH
docker run -d `
    -p 8000:8000 `
    --name ai33-server `
    --network mongodb `
    -e MONGO_DB=AI33_IMAGE `
    -e MONGO_URL=mongodb://mongodb:27017 `
    -e MONGO_USER=ai33 `
    -e MONGO_PASSWORD=a_strong_password `
    ai33_server
```
In Linux:
