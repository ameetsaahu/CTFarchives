FROM ubuntu:21.04

RUN apt-get update && apt-get dist-upgrade -y && apt-get install socat -y && \
useradd -m vuln && \
apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

COPY chall flag.txt /home/vuln/

RUN chown -R root:vuln /home/vuln/ && chmod -R 750 /home/vuln/

EXPOSE 4446

USER vuln

CMD socat -T10 TCP-LISTEN:4446,reuseaddr,fork EXEC:/home/vuln/chall
