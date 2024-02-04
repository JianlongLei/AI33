# How to Run Web Application
## 1. run by k8s command
1. apply database
    ```BASH
    kubectl apply -f k8s\db\mongodb-configmap.yaml
    kubectl apply -f k8s\db\mongodb-secret.yaml
    kubectl apply -f k8s\db\mongodb-storage.yaml
    kubectl apply -f k8s\db\mongodb-deployment.yaml
    kubectl apply -f k8s\db\mongodb-service.yaml
    ```
2. apply backend
   ```BASH
   kubectl apply -f k8s\backend\backend-deployment.yaml
   kubectl apply -f k8s\backend\backend-service.yaml
   ```
3. apply frontend
    ```BASH
    kubectl apply -f k8s\app\configmap-app.yaml
    kubectl apply -f k8s\app\app-loadbalancer.yaml
    kubectl apply -f k8s\app\app-deployment.yaml
    kubectl apply -f k8s\app\app-secret.yaml
    ```
4. check the load balancer
    ```BASH
    kubectl get svc
    ```
   ![img.png](k8s-svc.png)
5. visit via EXTERNAL-IP:5000.
6. delete all k8s objects
```
kubectl delete secret mongodb-secret 
kubectl delete secret my-mongodb
kubectl delete secret webapp-registry-secret

kubectl delete configmap mongo-config-produce
kubectl delete configmap mongodb-config 
kubectl delete configmap server-address 

kubectl delete PersistentVolumeClaim mongo-produce
kubectl delete PersistentVolumeClaim mongodb-pvc 
kubectl delete PersistentVolumeClaim my-mongodb 

kubectl delete PersistentVolume mongodb-pv 
kubectl delete PersistentVolume pvc-6a9dd68a-1935-43ee-ad6a-fa804ecf39dc

kubectl delete deployment backend-deployment 
kubectl delete deployment mongodb-default 
kubectl delete deployment webapp-deployment

kubectl delete service backend-server 
kubectl delete service mongodb-service
kubectl delete service webapp-loadbalancer 
kubectl delete service webapp-service 
```
## Install via helm
1. run 
   `helm install sc-app ./sc_app`
