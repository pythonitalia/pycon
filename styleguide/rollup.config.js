import commonjs from "@rollup/plugin-commonjs";
import styles from "rollup-plugin-styles";
import { terser } from "rollup-plugin-terser";
import typescript from "rollup-plugin-typescript2";
import ts from "typescript";
import pkg from "./package.json";

const assetFileNames = (assetInfo) => {
  if (assetInfo.name === "index.css") {
    return "index.css"
  }

  if (assetInfo.name === "custom.css") {
    return "custom-style.css";
  }

  if (assetInfo.name === "config-parts.js") {
    return "config-parts.js";
  }

  return "assets/[name]-[hash][extname]";
}

const plugins = [
  commonjs(),
  styles({
    url: {
      hash: "[name]-[hash][extname]",
    },
    mode: "extract",
    config: { path: "./postcss.config.js" },
  }),
  terser({
    output: {
      comments: false,
    },
  }),
];

const external = [
  ...Object.keys(pkg.dependencies || {}),
  ...Object.keys(pkg.peerDependencies || {}),
];

export default [
  {
    input: './src/custom.css',
    output: [
        {
          file: `dist/custom.js`,
          format: 'es',
          sourcemap: false,
          assetFileNames,
        }
    ],
    plugins: [
      styles({
        url: {
          hash: "[name]-[hash][extname]",
        },
        mode: "extract",
        config: { path: "./postcss.config.js" },
      }),
    ],
  },
  {
    input: "./src/index.ts",
    external,
    output: [
      {
        file: `${pkg.module}`,
        format: "es",
        sourcemap: true,
        assetFileNames,
      },
      {
        file: `${pkg.main}`,
        format: "cjs",
        sourcemap: true,
        assetFileNames,
      },
    ],
    plugins: [
      typescript({
        typescript: ts,
        tsconfig: "tsconfig.json",
        tsconfigDefaults: {
          exclude: [
            "**/*.spec.ts",
            "**/*.test.ts",
            "**/*.stories.ts",
            "**/*.spec.tsx",
            "**/*.test.tsx",
            "**/*.stories.tsx",
            "node_modules",
            "bower_components",
            "jspm_packages",
            "dist",
          ],
          compilerOptions: {
            sourceMap: true,
            declaration: true,
          },
        },
      }),
      ...plugins,
    ],
  },
  {
    input: "./src/icons/index.ts",
    external,
    output: [
      {
        file: `dist/icons/index.esm.js`,
        format: "es",
        sourcemap: true,
        assetFileNames,
      },
      {
        file: `dist/icons/index.js`,
        format: "cjs",
        sourcemap: true,
        assetFileNames,
      },
    ],
    plugins: [
      typescript({
        typescript: ts,
        tsconfig: "tsconfig.json",
        tsconfigOverride: {
          include: ["./src/icons"],
        },
        tsconfigDefaults: {
          exclude: [
            "**/*.spec.ts",
            "**/*.test.ts",
            "**/*.stories.ts",
            "**/*.spec.tsx",
            "**/*.test.tsx",
            "**/*.stories.tsx",
            "node_modules",
            "bower_components",
            "jspm_packages",
            "dist",
          ],
          compilerOptions: {
            sourceMap: true,
            declaration: true,
          },
        },
      }),
      ...plugins,
    ],
  },
  {
    input: "./src/illustrations/index.ts",
    external,
    output: [
      {
        file: `dist/illustrations/index.esm.js`,
        format: "es",
        sourcemap: true,
        assetFileNames,
      },
      {
        file: `dist/illustrations/index.js`,
        format: "cjs",
        sourcemap: true,
        assetFileNames,
      },
    ],
    plugins: [
      typescript({
        typescript: ts,
        tsconfig: "tsconfig.json",
        tsconfigOverride: {
          include: ["./src/illustrations"],
        },
        tsconfigDefaults: {
          exclude: [
            "**/*.spec.ts",
            "**/*.test.ts",
            "**/*.stories.ts",
            "**/*.spec.tsx",
            "**/*.test.tsx",
            "**/*.stories.tsx",
            "node_modules",
            "bower_components",
            "jspm_packages",
            "dist",
          ],
          compilerOptions: {
            sourceMap: true,
            declaration: true,
          },
        },
      }),
      ...plugins,
    ],
  },
];
