const path = require("path");
const webpack = require("webpack");
const withSourceMaps = require("@zeit/next-source-maps");

module.exports = withSourceMaps({
  env: {
    API_URL: "https://pycon.it/graphql",
    conferenceCode: "pycon11",
  },

  webpack: (config) => {
    config.resolve.alias["~"] = path.resolve(__dirname) + "/src";
    return config;
  },
});
