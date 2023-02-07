/** @type {import('tailwindcss').Config} */
// eslint-disable-next-line @typescript-eslint/no-var-requires
const { tailwindConfig } = require("@python-italia/pycon-styleguide");

module.exports = {
  ...tailwindConfig,
  content: [
    "./src/**/*.{js,ts,jsx,tsx}",
    "./node_modules/@python-italia/pycon-styleguide/**/*.{js,ts,jsx,tsx}",
  ],
};
