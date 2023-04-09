import type { CodegenConfig } from "@graphql-codegen/cli";

const config: CodegenConfig = {
  overwrite: true,
  schema: process.env.GRAPHQL_SCHEMA_URL || "http://localhost:4000/graphql",
  documents: ["src/**/*.graphql"],
  generates: {
    "src/": {
      preset: "near-operation-file",
      plugins: ["typescript-operations", "typescript-react-apollo"],
      presetConfig: {
        extension: ".generated.ts",
        baseTypesPath: "types.ts",
      },
    },
  },
};

export default config;
