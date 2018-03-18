FROM node:9


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