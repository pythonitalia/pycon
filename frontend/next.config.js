require("dotenv").config();
const path = require("path");
const { withSentryConfig } = require("@sentry/nextjs");

const {
  SENTRY_ORG,
  SENTRY_PROJECT,
  SENTRY_AUTH_TOKEN,
  VERCEL_GITHUB_COMMIT_SHA,
  CONFERENCE_CODE,
  API_URL,
  API_TOKEN,
  VERCEL_ENV,
  NEXT_PUBLIC_SOCIAL_CARD_SERVICE,
  NEXT_PUBLIC_VERCEL_URL,
} = process.env;

const SentryWebpackPluginOptions = {
  silent: true,
  org: SENTRY_ORG,
  project: SENTRY_PROJECT,
  authToken: SENTRY_AUTH_TOKEN,
  release: VERCEL_GITHUB_COMMIT_SHA,
  dryRun: VERCEL_ENV !== "production",
};

module.exports = withSentryConfig(
  {
    serverRuntimeConfig: {
      API_TOKEN: API_TOKEN,
    },
    env: {
      API_URL: API_URL,
      conferenceCode: CONFERENCE_CODE || "pycon-demo",
      NEXT_PUBLIC_SOCIAL_CARD_SERVICE:
        NEXT_PUBLIC_SOCIAL_CARD_SERVICE ||
        "https://socialcards.python.it/api/card",
      NEXT_PUBLIC_SITE_URL: NEXT_PUBLIC_VERCEL_URL
        ? `https://${NEXT_PUBLIC_VERCEL_URL}/`
        : `http://localhost:3000/`,
    },
    images: {
      domains: ["production-pycon-backend-media.s3.amazonaws.com"],
    },
    webpack: (config) => {
      config.resolve.alias["~"] = path.resolve(__dirname) + "/src";
      return config;
    },
    eslint: {
      ignoreDuringBuilds: true,
    },
  },
  SentryWebpackPluginOptions,
);
