import { gql } from "apollo-server";
import { readFileSync } from "fs";

require.extensions[".graphql"] = function (module, filename) {
  module.exports = gql(readFileSync(filename, "utf8"));
};
