FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -fy wget python3 python3-pip openjdk-11-jdk-headless

WORKDIR /src/app

COPY ./src .

RUN pip3 install -r requirements.txt

RUN chmod +x ./run.sh

RUN useradd n00b
USER n00b

CMD ["./run.sh"]


