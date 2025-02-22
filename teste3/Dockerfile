FROM ubuntu:20.04


ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN apt-get update && apt-get install -y \
    build-essential \
    libjsoncpp-dev \
    g++ \
    libomp-dev \
    mpich \
    python3 \
    python3-pip \
    curl


RUN pip3 install flask

COPY wordcount_mpi_omp.cpp /app/wordcount_mpi_omp.cpp
COPY webserver.py /app/webserver.py


WORKDIR /app
RUN mpic++ -fopenmp -I/usr/include/jsoncpp -o wordcount_mpi_omp wordcount_mpi_omp.cpp -ljsoncpp


CMD ["python3", "webserver.py"]