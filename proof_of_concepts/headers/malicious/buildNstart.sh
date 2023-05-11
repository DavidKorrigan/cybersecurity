docker stop header-poc-malicious-running
docker rm header-poc-malicious-running

docker build -t header-poc-malicious-app .
docker run -d --name header-poc-malicious-running header-poc-malicious-app