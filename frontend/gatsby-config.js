const Sentry = require("@sentry/node");

const proxy = require("http-proxy-middleware");
require("dotenv").config({
  path: `.env`,
});

const API_URL = process.env.API_URL || "http://127.0.0.1:8000/graphql";
const API_TOKEN = process.env.API_TOKEN || "example-token";
const CONFERENCE_CODE = process.env.CONFERENCE_CODE || "pycon-demo";

Sentry.init({
  dsn: process.env.SENTRY_DSN || "",
  maxBreadcrumbs: 50,
  debug: true,
});

module.exports = {
  siteMetadata: {
    siteUrl: `https://www.pycon.it`,
  },
  developMiddleware: app => {
    app.use(
      "/graphql",
      proxy({
        target: API_URL.replace("/graphql", ""),
      }),
    );
    app.use(
      "/login/google/",
      proxy({
        target: API_URL.replace("/graphql", ""),
        pathRewrite: function(path, req) {
          return "/login/google-oauth2/";
        },
      }),
    );
    app.use(
      "/complete/google-oauth2/",
      proxy({
        target: API_URL.replace("/graphql", ""),
        pathRewrite: function(path, req) {
          return "/complete/google-oauth2/";
        },
      }),
    );
  },
  plugins: [
    `gatsby-plugin-netlify`,
    "gatsby-plugin-theme-ui",
    {
      resolve: "gatsby-source-pycon",
      options: {
        url: API_URL,
        conferenceCode: CONFERENCE_CODE,
        typeName: "BACKEND",
        fieldName: "backend",
        refetchInterval: 60,
        headers: {
          Authorization: `Token ${API_TOKEN}`,
        },
      },
    },
    {
      resolve: "gatsby-plugin-extract-schema",
      options: {
        dest: `${__dirname}/_schema.json`,
      },
    },
    {
      resolve: `gatsby-source-filesystem`,
      options: {
        path: `${__dirname}/content/assets`,
        name: `assets`,
      },
    },
    {
      resolve: `gatsby-transformer-remark`,
      options: {
        plugins: [
          {
            resolve: `gatsby-remark-images`,
            options: {
              maxWidth: 500,
            },
          },
          {
            resolve: `gatsby-remark-external-links`,
            options: {
              target: `_blank`,
              rel: `nofollow noopener noreferrer`,
            },
          },
          `gatsby-remark-responsive-iframe`,
        ],
      },
    },
    `gatsby-plugin-social-images`,
    `gatsby-plugin-typescript`,
    `gatsby-plugin-react-helmet`,
    `gatsby-transformer-sharp`,
    `gatsby-plugin-sharp`,
    {
      resolve: `gatsby-plugin-favicon`,
      options: {
        logo: "./static/logo.png",
        appName: "PyCon Italia",
        developerName: null,
        developerURL: null,
        dir: "auto",
        lang: "en-GB",
        background: "#fff",
        theme_color: "#fff",
        display: "standalone",
        orientation: "any",
        start_url: "/?homescreen=1",
        version: "1.0",

        icons: {
          android: true,
          appleIcon: true,
          appleStartup: true,
          coast: false,
          favicons: true,
          firefox: true,
          opengraph: false,
          twitter: false,
          yandex: false,
          windows: false,
        },
      },
    },
  ],
};
