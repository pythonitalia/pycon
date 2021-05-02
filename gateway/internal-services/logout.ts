import { buildFederatedSchema } from "@apollo/federation";
import { gql } from "apollo-server";

import { ClearAuthAction } from "../actions/clear-auth-action";

const typeDefs = gql`
  type Query {
    logout: String!
  }

  type Mutation {
    logout: String
  }
`;

const resolvers = {
  Mutation: {
    async logout(_: any, __: any, context: any) {
      const action = new ClearAuthAction();
      await action.apply(context);
      return "ok";
    },
  },
};

export const schema = buildFederatedSchema([{ typeDefs, resolvers }]);
