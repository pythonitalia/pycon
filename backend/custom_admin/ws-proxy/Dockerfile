FROM openresty/openresty:focal

RUN apt-get update -y

RUN apt-get install -y python3 python3-pip

RUN pip3 install websockets

COPY . .

CMD ["/run.sh"]
