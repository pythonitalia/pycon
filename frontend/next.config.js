require("dotenv").config();
const path = require("path");
const webpack = require("webpack");
const withSourceMaps = require("@zeit/next-source-maps");

module.exports = withSourceMaps({
  serverRuntimeConfig: {
    API_TOKEN: process.env.API_TOKEN,
  },
  env: {
    API_URL: process.env.API_URL,
    conferenceCode: process.env.CONFERENCE_CODE || "pycon-demo",
    SENTRY_DSN: process.env.SENTRY_DSN || null,
  },
  images: {
    domains: ['production-pycon-backend-media.s3.amazonaws.com'],
  },
  webpack: (config) => {
    config.resolve.alias["~"] = path.resolve(__dirname) + "/src";
    return config;
  },
});
