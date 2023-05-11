docker stop header-poc-running
docker rm header-poc-running

docker build -t header-poc-app .
docker run -d --name header-poc-running header-poc-app