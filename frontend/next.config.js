require("dotenv").config();
const webpack = require("webpack");
const path = require("path");
const { withSentryConfig } = require("@sentry/nextjs");

const {
  CONFERENCE_CODE,
  API_URL,
  API_TOKEN,
  NEXT_PUBLIC_SOCIAL_CARD_SERVICE,
  NEXT_PUBLIC_VERCEL_URL,
  API_URL_SERVER,
} = process.env;

module.exports = withSentryConfig({
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
      {
        source: "/discord",
        destination: "https://discord.gg/XAS3ZgRKDq",
        permanent: false,
      },
      {
        source: "/blog",
        destination: "/news",
        permanent: true,
      },
      {
        source: "/blog/:match*",
        destination: "/news/:match*",
        permanent: true,
      },
    ];
  },
  async rewrites() {
    return [
      {
        source: "/graphql",
        destination: API_URL_SERVER,
      },
    ];
  },
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
    domains: [
      "pastaporto-cdn.pycon.it",
      "cdn.pycon.it",
      "localhost",
      "pycon-backend",
    ],
  },
  webpack: (config, options) => {
    config.resolve.alias["~"] = path.resolve(__dirname) + "/src";

    config.plugins.push(
      new webpack.DefinePlugin({
        __DEV__: process.env.NODE_ENV !== "production",
      }),
    );

    return config;
  },
});
