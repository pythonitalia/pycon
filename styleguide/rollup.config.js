import typescript from "rollup-plugin-typescript2";
import { terser } from "rollup-plugin-terser";
import commonjs from "@rollup/plugin-commonjs";
import pkg from "./package.json";
import copy from "rollup-plugin-copy";
import postcss from "rollup-plugin-postcss";
import ts from "typescript";

export default {
  input: "./src/index.ts",
  external: [
    ...Object.keys(pkg.dependencies || {}),
    ...Object.keys(pkg.peerDependencies || {}),
  ],
  output: [
    {
      file: `${pkg.module}`,
      format: "es",
      sourcemap: true,
    },
    {
      file: `${pkg.main}`,
      format: "cjs",
      sourcemap: true,
    },
  ],
  plugins: [
    commonjs(),
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
    postcss({
      config: {
        path: "./postcss.config.js",
      },
      extract: true,
      extensions: [".css"],
    }),
    terser({
      output: {
        comments: false,
      },
    }),
    copy({
      targets: [
        { src: "tailwind.config.js", dest: "dist" },
        { src: "postcss.config.js", dest: "dist" },
      ],
    }),
  ],
};
