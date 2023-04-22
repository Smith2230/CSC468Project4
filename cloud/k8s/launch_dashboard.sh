#!/bin/bash

kubectl apply -f k8s_dash/dashboard-insecure.yaml
kubectl apply -f k8s_dash/socat.yaml
kubectl patch service kubernetes-dashboard -n kubernetes-dashboard --type='json' --patch='[{"op": "replace", "path": "/spec/ports/0/nodePort", "value":30082}]'
sleep 5
kubectl get svc --namespace=kubernetes-dashboard
