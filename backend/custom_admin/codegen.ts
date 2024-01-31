import type { CodegenConfig } from "@graphql-codegen/cli";

const config: CodegenConfig = {
  overwrite: true,
  schema: "http://localhost:3002/admin/graphql",
  documents: ["src/**/*.graphql"],
  generates: {
    "src/types.ts": { plugins: ["typescript"] },
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
