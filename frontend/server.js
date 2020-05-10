/* eslint-disable no-console */
const express = require("express");
const next = require("next");

require("dotenv").config();

const devProxy = {
  "/graphql": {
    target: process.env.API_URL,
    pathRewrite: { "^/graphql": "" },
    changeOrigin: true,
  },
};

const port = parseInt(process.env.PORT, 10) || 3000;
const env = process.env.NODE_ENV;
const dev = env !== "production";
const app = next({
  dir: ".",
  dev,
});

const handle = app.getRequestHandler();

app
  .prepare()
  .then(() => {
    const server = express();

    // Set up the proxy.
    if (dev && devProxy) {
      const { createProxyMiddleware } = require("http-proxy-middleware");

      Object.keys(devProxy).forEach(function (context) {
        server.use(createProxyMiddleware(context, devProxy[context]));
      });
    }

    // social cards handler
    // server.all(/social\.png$/, socialCardHandler);

    // Default catch-all handler to allow Next.js to handle all other routes
    server.all("*", (req, res) => handle(req, res));

    server.listen(port, (err) => {
      if (err) {
        throw err;
      }
      console.log(`> Ready on port ${port} [${env}]`);
    });
  })
  .catch((err) => {
    console.log("An error occurred, unable to start the server");
    console.log(err);
  });
