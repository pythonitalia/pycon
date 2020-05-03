require("dotenv").config();
const path = require("path");
const webpack = require("webpack");
const withSourceMaps = require("@zeit/next-source-maps");

module.exports = withSourceMaps({
  env: {
    API_URL: process.env.API_URL,
    conferenceCode: process.env.CONFERENCE_CODE,
  },

  webpack: (config) => {
    config.resolve.alias["~"] = path.resolve(__dirname) + "/src";
    return config;
  },
});
