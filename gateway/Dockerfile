FROM amazon/aws-lambda-nodejs:14 as build

RUN npm install -g yarn

WORKDIR /app

ENV NODE_ENV=production

COPY package.json yarn.lock ./

RUN yarn install --prod

COPY . .

RUN yarn tsc

FROM amazon/aws-lambda-nodejs:14

WORKDIR ${LAMBDA_TASK_ROOT}

COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/dist ./

# Copy some static files
COPY --from=build /app/internal-services/logout/schema.graphql ./internal-services/logout/schema.graphql

ENV NODE_ENV=production
ENV VARIANT=default

CMD [ "handler.graphqlHandler" ]
