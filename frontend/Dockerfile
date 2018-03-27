FROM node:9@sha256:0b02160d1dc9d2afcdd17ab2c106884b656604f763fd905cbde51c31ecc7d795


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