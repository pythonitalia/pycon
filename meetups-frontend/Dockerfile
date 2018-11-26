FROM node:9@sha256:e9311a4a7beacb1e655b459d1320931a87ccb69ece3bfa6444928c24173bb992


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