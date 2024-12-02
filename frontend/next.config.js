require("dotenv").config();
const webpack = require("webpack");
const path = require("node:path");
const { withSentryConfig } = require("@sentry/nextjs");

const {
  CONFERENCE_CODE,
  API_URL,
  API_TOKEN,
  NEXT_PUBLIC_SOCIAL_CARD_SERVICE,
  NEXT_PUBLIC_VERCEL_URL,
  API_URL_SERVER,
  CMS_HOSTNAME,
  CMS_ADMIN_HOST = "admin.pycon.it",
} = process.env;

module.exports = withSentryConfig({
  output: "standalone",
  i18n: {
    locales: ["default", "en", "it"],
    defaultLocale: "default",
    localeDetection: false,
  },
  trailingSlash: false,
  cacheHandler:
    process.env.NODE_ENV === "production"
      ? require.resolve("./cache-handler.mjs")
      : undefined,
  cacheMaxMemorySize: 0,
  async headers() {
    return [
      {
        source: "/:path*",
        headers: [
          {
            key: "X-Frame-Options",
            value: "DENY",
          },
          {
            key: "Content-Security-Policy",
            value: `frame-ancestors ${CMS_ADMIN_HOST};`,
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
        source: "/cms-admin/:match*",
        destination: "https://admin.pycon.it/cms-admin/:match",
        permanent: false,
      },
      {
        source: "/discord",
        destination: "https://discord.gg/CPT8EQYrfs",
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
      {
        source: "/schedule/ical/:match*",
        destination: `${API_URL_SERVER}/schedule/user-schedule-favourites-calendar/:match*`,
        permanent: false,
      },
    ];
  },
  async rewrites() {
    const rewrites = [
      {
        source: "/graphql",
        destination: `${API_URL_SERVER}/graphql`,
      },
    ];

    if (API_URL_SERVER.includes("http://backend")) {
      rewrites.push({
        source: "/local_files_upload/:match*",
        destination: `${API_URL_SERVER}/local_files_upload/:match*`,
      });

      rewrites.push({
        source: "/media/:match*",
        destination: `${API_URL_SERVER}/media/:match*`,
      });
    }

    return rewrites;
  },
  serverRuntimeConfig: {
    API_TOKEN: API_TOKEN,
  },
  env: {
    API_URL: API_URL,
    conferenceCode: CONFERENCE_CODE || "pycon-demo",
    cmsHostname: CMS_HOSTNAME,
    NEXT_PUBLIC_SOCIAL_CARD_SERVICE:
      NEXT_PUBLIC_SOCIAL_CARD_SERVICE ||
      "https://socialcards.python.it/api/card",
    NEXT_PUBLIC_SITE_URL: NEXT_PUBLIC_VERCEL_URL
      ? `https://${NEXT_PUBLIC_VERCEL_URL}/`
      : "http://localhost:3000/",
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
    config.resolve.alias["~"] = `${path.resolve(__dirname)}/src`;

    config.plugins.push(
      new webpack.DefinePlugin({
        __DEV__: process.env.NODE_ENV !== "production",
      }),
    );

    return config;
  },
});
