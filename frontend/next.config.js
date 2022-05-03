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
  NEXT_PUBLIC_SOCIAL_CARD_SERVICE,
  NEXT_PUBLIC_VERCEL_URL,
  GRAPHQL_GATEWAY_URL,
} = process.env;

module.exports = withSourceMaps({
  i18n: {
    locales: ["default", "en", "it"],
    defaultLocale: "default",
    localeDetection: false,
  },
  trailingSlash: false,
  async headers() {
    return [
      {
        source: "/:path*",
        headers: [
          {
            key: "X-Frame-Options",
            value: "DENY",
          },
        ],
      },
    ];
  },
  async redirects() {
    return [
      {
        source: "/admin/:match*",
        destination: "https://admin.pycon.it/admin/:match",
        permanent: false,
      },
    ];
  },
  async rewrites() {
    return [
      {
        source: "/graphql",
        destination: GRAPHQL_GATEWAY_URL,
      },
    ];
  },
  serverRuntimeConfig: {
    API_TOKEN: API_TOKEN,
  },
  env: {
    API_URL: API_URL,
    conferenceCode: CONFERENCE_CODE || "pycon-demo",
    SENTRY_DSN: SENTRY_DSN || null,
    NEXT_PUBLIC_SOCIAL_CARD_SERVICE:
      NEXT_PUBLIC_SOCIAL_CARD_SERVICE ||
      "https://socialcards.python.it/api/card",
    NEXT_PUBLIC_SITE_URL: NEXT_PUBLIC_VERCEL_URL
      ? `https://${NEXT_PUBLIC_VERCEL_URL}/`
      : `http://localhost:3000/`,
  },
  images: {
    domains: [
      "pastaporto-cdn.pycon.it",
      "cdn.pycon.it",
      "localhost",
      "pycon-backend",
    ],
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
