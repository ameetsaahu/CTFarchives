FROM python:buster
RUN apt-get -qqy update && \
    apt-get -qqy --no-install-recommends install \
    xdg-utils xfce4 xvfb && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/*
RUN pip install flask

COPY server.py /
RUN echo '#!/bin/sh\necho flag{flag}' > /proof_uuid.sh
RUN chmod 555 /server.py /proof_*.sh

RUN useradd infant --create-home
USER infant

WORKDIR /tmp
ENV BROWSER wget
ENV XDG_CURRENT_DESKTOP XFCE
ENV H_SITEKEY hCaptcha_sitekey_fix_it_yourself
ENV H_SECRET hCaptcha_secret_fix_it_yourself
ENV DISPLAY :88
CMD ["sh","-c","rm -f .X99-lock & Xvfb :88 -screen 0 640x400x8 -nolisten tcp & python3 /server.py"] 