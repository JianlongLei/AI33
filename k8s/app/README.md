# AI33


## How to run
First create server loadbalancer to get external ip address
```BASH
kubectl apply -f server-loadbalancer.yaml 
```
when external ip address of server is created,run below command to get ip,and fill the ip address in the app-deployment.yaml

```BASH
kubectl get svc server-access -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
```

set secret and configmap
```BASH
kubectl apply -f configmap-app.yaml 
kubectl apply -f app-secret.yaml 
```

deploy app
```BASH
 kubectl apply -f app-deployment.yaml
```

load balancer
```BASH
 kubectl apply -f app-loadbalancer.yaml
```
```BASH
kubectl get svc webapp-loadbalancer -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
```


