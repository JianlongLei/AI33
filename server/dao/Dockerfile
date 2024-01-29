FROM bitnami/mongodb
LABEL authors="zyf"

#ENTRYPOINT ["top", "-b"]

RUN kubectl apply -f sever\dao\mongodb-configmap.yaml
RUN kubectl apply -f sever\dao\mongodb-secret.yaml
RUN kubectl apply -f sever\dao\mongodb-storage.yaml
RUN kubectl apply -f sever\dao\mongodb-deployment.yaml
RUN kubectl apply -f sever\dao\mongodb-service.yaml
# mongodb.conf

# Network-related settings
#bind_ip = 0.0.0.0
#port = 27017

# Storage-related settings
#dbpath = /data/db
