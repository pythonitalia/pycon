const { API_URL, API_URL_SERVER, STRIPE_KEY, GRAPHQL_GATEWAY_URL } =
  process.env;

module.exports = {
  env: {
    API_URL: API_URL,
    API_URL_SERVER: API_URL_SERVER,
    STRIPE_KEY: STRIPE_KEY,
  },
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
  async rewrites() {
    return [
      {
        source: "/graphql",
        destination: GRAPHQL_GATEWAY_URL,
      },
    ];
  },
};
