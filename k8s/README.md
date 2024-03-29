# How to Run Web Application
## run by k8s command
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
kubectl delete secret webapp-registry-secret

kubectl delete configmap mongodb-config 
kubectl delete configmap server-address 

kubectl delete PersistentVolumeClaim mongodb-pvc 
kubectl delete PersistentVolume mongodb-pv 

kubectl delete deployment backend-deployment 
kubectl delete deployment mongodb-deployment 
kubectl delete deployment webapp-deployment

kubectl delete service backend-service 
kubectl delete service mongodb-service
kubectl delete service webapp-loadbalancer 
kubectl delete service webapp-service 
```
## Install via helm chart
1. run `helm install sc-app ./sc_app` to install
2. run `helm uninstall sc-app` to uninstall
3. upgrade: 

## Using RBAC Authorization
1. apply roles, service account and role blinding
   ```
   kubectl apply -f k8s\security\admin-role.yaml
   kubectl apply -f k8s\security\reader-role.yaml
   kubectl apply -f k8s\security\editor-role.yaml
   
   kubectl apply -f k8s\security\admin-serviceaccount.yaml
   kubectl apply -f k8s\security\rolebinding.yaml
   kubectl apply -f k8s\security\user-rolebinding.yaml
   ```
2. 
