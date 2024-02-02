# MongoDB Database
To enable the database, you need to do followings:
1. pull the official mongodb image
    ```BASH
   docker pull mongo:latest
    ```
2. run a container
   ```BASH
   docker run -d -p 27017:27017 --name my-mongo-container mongo:latest
   ```
3. apply configurations
    ```BASH
   kubectl apply -f server\dao\mongodb-configmap.yaml
   kubectl apply -f server\dao\mongodb-secret.yaml
   kubectl apply -f server\dao\mongodb-storage.yaml
   kubectl apply -f server\dao\mongodb-deployment.yaml
   kubectl apply -f server\dao\mongodb-service.yaml
    ```


