FROM amazon/aws-lambda-nodejs:14 as build

RUN npm install -g pnpm; \
    pnpm --version; \
    pnpm setup; \
    mkdir -p /usr/local/share/pnpm &&\
    export PNPM_HOME="/usr/local/share/pnpm" &&\
    export PATH="$PNPM_HOME:$PATH"; \
    pnpm bin -g

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

ENV NODE_ENV=production

CMD [ "handler.graphqlHandler" ]
