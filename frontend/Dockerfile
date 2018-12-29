FROM node:10.14.2

RUN curl -o- -L https://yarnpkg.com/install.sh | sh

RUN mkdir /pycon_frontend

COPY ./package.json ./yarn.*

WORKDIR /tmp
RUN yarn install

WORKDIR /pycon_frontend

RUN mv /tmp/node_modules .
COPY . /pycon_frontend/

RUN yarn build

COPY dist/ /sites/pycon_frontend/
