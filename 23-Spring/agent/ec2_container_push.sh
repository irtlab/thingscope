aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 040801773313.dkr.ecr.us-east-1.amazonaws.com
docker build -t thingscope .
docker tag thingscope:latest 040801773313.dkr.ecr.us-east-1.amazonaws.com/thingscope:latest
docker push 040801773313.dkr.ecr.us-east-1.amazonaws.com/thingscope:latest
aws ecs update-service --cluster thingscope-cluster --service thingscope --force-new-deployment --no-paginate --output text