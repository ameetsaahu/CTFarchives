FROM ubuntu:21.04

RUN /usr/sbin/useradd --no-create-home -u 1000 user
RUN apt-get update && apt-get install -y socat

COPY flag.txt /
# COPY rocket.c /home/user/
# COPY seccomp-bpf.h /home/user/
COPY rocket /home/user/

EXPOSE 1337

USER user

CMD socat \
      TCP-LISTEN:1337,reuseaddr,fork \
      EXEC:"/home/user/rocket"
