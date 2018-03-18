FROM node:9@sha256:59aff2d9898e2b3d35d7656bf57bf61c2dcaedac58b8c3934b8963904d27c437


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