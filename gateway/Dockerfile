FROM amazon/aws-lambda-nodejs:14 as build

RUN wget -qO- https://get.pnpm.io/install.sh | sh -

WORKDIR /app

ENV NODE_ENV=production

COPY package.json pnpm-lock.yaml ./

RUN pnpm install

COPY . .

RUN pnpm run tsc

FROM amazon/aws-lambda-nodejs:14

WORKDIR ${LAMBDA_TASK_ROOT}

COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/dist ./

# Copy some static files
COPY --from=build /app/internal-services/logout/schema.graphql ./internal-services/logout/schema.graphql

ENV NODE_ENV=production

CMD [ "handler.graphqlHandler" ]
