import { buildFederatedSchema } from "@apollo/federation";

import { ClearAuthAction } from "../../actions/clear-auth-action";

// eslint-disable-next-line @typescript-eslint/no-var-requires
const typeDefs = require("./schema.graphql");

const resolvers = {
  Query: {
    logout: () => "👋",
  },
  Mutation: {
    async logout(_: any, __: any, context: any) {
      const action = new ClearAuthAction();
      await action.apply(context);
      return "ok";
    },
  },
};

export const schema = buildFederatedSchema([{ typeDefs, resolvers }]);
