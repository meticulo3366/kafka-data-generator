Credit to [Aiven tutorial](https://aiven.io/developer/teach-yourself-apache-kafka-and-python-with-a-jupyter-notebook) for the guide on their pizza generator that inspired this one.

# Docker Build Help
Commands used when building.

docker build -t kafka-data-generator:0.x -f ./Dockerfile ./

docker login --username stuzanne
docker tag kafka-data-generator:0.x stuzanne/kafka-data-generator:0.x
docker push stuzanne/kafka-data-generator:0.x

docker tag stuzanne/kafka-data-generator:0.x stuzanne/kafka-data-generator:latest
docker push stuzanne/kafka-data-generator:latest
