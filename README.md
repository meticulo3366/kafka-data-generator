# kafka-data-generator
A data generator into Kafka.

A simple app for producing sample data into Kafka on three topics, `customers`, `products` and `pizza-orders`. A supporting docker-compose in this repo, includes a local Kafka and UI to see into Kafka.

# Get Started

Run `docker compose up -d` and navigate to [localhost:8080](http://localhost:8080) to see the Kafka topic with pizza order data using the Conduktor UI.

![viewMessage](/images/view-message.png)
*Messages produced, seen in the Conduktor UI*

![consumer-page](/images/consumer-page.png)
*An example message, seen in the Conduktor UI*

## Docker compose architecture
![simple-architecture](/images/kafka-data-generator-architecture.png)

# Changing configuration of the app

The configuration can be changed by setting environment variables.

| Name                      | Default                           | Description                                                                                             |
| ------------------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `KAFKA_BOOTSTRAP_SERVERS` | `localhost:19092`                 | The bootstrap server(s) for your Kafka cluster.                                                         |
| `MAX_BATCHES`             | 500                               | The max batches of 3 messages (1 for each of the 3 topics) to produce, stops the producer once reached. |
| `MESSAGE_DELAY_SECONDS`   | 2                                 | The wait time between producing messages, in seconds.                                                   |
| `TOPICS`                  | `customers,pizza-orders,products` | Customise which of the 3 topics to use, e.g. if you only want to produce to pizza-orders then set this. |

The app is published on [Dockerhub](https://hub.docker.com/r/stuzanne/kafka-data-generator).
