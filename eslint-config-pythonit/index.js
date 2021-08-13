module.exports = {
  env: {
    browser: true,
    es6: true,
    node: true,
  },
  ignorePatterns: [
    "src/**/*.generated.ts",
    "src/generated",
    "next.config.js",
    "public/",
    "**/*.graphql",
    "src/types.tsx",
  ],
  parser: "@typescript-eslint/parser",
  extends: [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "prettier",
  ],
  plugins: ["simple-import-sort"],
  overrides: [
    {
      files: [
        "**/association-frontend/**/*.[jt]s?(x)",
        "**/frontend/**/*.[jt]s?(x)",
      ],
      extends: ["next", "next/core-web-vitals"],
    },
    {
      files: [
        "**/association-frontend/__tests__/**/*.[jt]s?(x)",
        "**/association-frontend/?(*.)+(spec|test).[jt]s?(x)",
        "**/frontend/__tests__/**/*.[jt]s?(x)",
        "**/frontend/?(*.)+(spec|test).[jt]s?(x)",
      ],
      extends: ["plugin:testing-library/react", "plugin:jest-dom/recommended"],
      plugins: ["testing-library", "jest-dom"],
    },
  ],
  rules: {
    "simple-import-sort/imports": "error",
    "simple-import-sort/exports": "error",
    "import/first": "error",
    "import/newline-after-import": "error",
    "import/no-duplicates": "error",
    "react-hooks/exhaustive-deps": "off",
    "prefer-const": "error",
    "react/no-unescaped-entities": "off",
    "no-eval": "error",
    "no-undef-init": "error",
    "@typescript-eslint/no-non-null-assertion": "off",
    "@typescript-eslint/no-explicit-any": "off",
    "@typescript-eslint/explicit-module-boundary-types": "off",
    "no-unused-vars": "off",
    "no-debugger": "error",
    "@next/next/no-img-element": "off",
    "@typescript-eslint/no-unused-vars": [
      "warn",
      {
        argsIgnorePattern: "^_",
        varsIgnorePattern: "^(_|jsx)",
        ignoreRestSiblings: true,
      },
    ],
  },
};
