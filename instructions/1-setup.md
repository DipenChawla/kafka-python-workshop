# Kafka Python Workshop

1. Install Docker ([Mac](https://docs.docker.com/docker-for-mac/install/), [Windows](https://docs.docker.com/docker-for-windows/install/), [Linux](https://docs.docker.com/engine/install/)) on your system.

    * Mac/Windows only: in Docker’s advanced settings, increase the memory dedicated to Docker to at least 8GB.

    * Clone the repository here :

    ```
    https://github.com/DipenChawla/kafka-python-workshop/tree/main
    ```

    * Test your docker memory settings

    ```
    docker system info | grep Memory 
    ```

      _Should return a value greater than 8GB - if not, the Kafka stack will probably not work._

    * Smoke test your Docker environment, by running : 

        docker run -p 8080:8080 hello-world

      You should see: 

          $  docker run -p 8080:8080 hello-world
          Unable to find image 'hello-world:latest' locally
          latest: Pulling from library/hello-world
          d1725b59e92d: Pull complete
          Digest: sha256:0add3ace90ecb4adbf7777e9aacf18357296e799f81cabc9fde470971e499788
          Status: Downloaded newer image for hello-world:latest

          Hello from Docker!
          This message shows that your installation appears to be working correctly.
          [...]

    * Run docker-compose in detached mode. This will setup a local Kafka broker, a Zookeeper node and a few important peripherals that will be a part of later exercises.

    ```
    docker-compose up -d
    ```
    