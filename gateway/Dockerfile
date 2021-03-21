FROM amazon/aws-lambda-nodejs:14 as build

RUN npm install -g yarn

WORKDIR /app

ENV NODE_ENV=production

COPY package.json yarn.lock ./

RUN yarn install

COPY . .

RUN yarn tsc

FROM amazon/aws-lambda-nodejs:14

WORKDIR ${LAMBDA_TASK_ROOT}

COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/dist ./

ENV NODE_ENV=production
ENV VARIANT=default

CMD [ "handler.graphqlHandler" ]
