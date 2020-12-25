require("dotenv").config();
const path = require("path");
const withSourceMaps = require("@zeit/next-source-maps");
const SentryWebpackPlugin = require("@sentry/webpack-plugin");

const {
  NEXT_PUBLIC_SENTRY_DSN: SENTRY_DSN,
  SENTRY_ORG,
  SENTRY_PROJECT,
  SENTRY_AUTH_TOKEN,
  NODE_ENV,
  VERCEL_GITHUB_COMMIT_SHA,
  CONFERENCE_CODE,
  API_URL,
  API_TOKEN,
} = process.env;

module.exports = withSourceMaps({
  serverRuntimeConfig: {
    API_TOKEN: API_TOKEN,
  },
  env: {
    API_URL: API_URL,
    conferenceCode: CONFERENCE_CODE || "pycon-demo",
    SENTRY_DSN: SENTRY_DSN || null,
  },
  i18n: {
    locales: ["en", "it"],
    defaultLocale: "en",
  },
  images: {
    domains: ["production-pycon-backend-media.s3.amazonaws.com"],
  },
  webpack: (config, options) => {
    config.resolve.alias["~"] = path.resolve(__dirname) + "/src";

    if (!options.isServer) {
      config.resolve.alias["@sentry/node"] = "@sentry/browser";
    }

    if (
      SENTRY_ORG &&
      SENTRY_PROJECT &&
      SENTRY_AUTH_TOKEN &&
      SENTRY_DSN &&
      NODE_ENV === "production"
    ) {
      config.plugins.push(
        new SentryWebpackPlugin({
          include: ".next",
          ignore: ["node_modules"],
          urlPrefix: "~/_next",
          release: VERCEL_GITHUB_COMMIT_SHA,
        }),
      );
    }

    return config;
  },
});
