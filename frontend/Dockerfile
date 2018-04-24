FROM node:9@sha256:bd7b9aaf77ab2ce1e83e7e79fc0969229214f9126ced222c64eab49dc0bdae90


RUN curl -o- -L https://yarnpkg.com/install.sh | bash

RUN mkdir /app

COPY ./package.json ./yarn.* /tmp/
WORKDIR /tmp
RUN yarn install
WORKDIR /app
RUN  ln -s /tmp/node_modules .
COPY . /app/

EXPOSE 3000 

 
ENTRYPOINT ["yarn"]
CMD ["start"]