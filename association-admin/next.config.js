module.exports = {
  async rewrites() {
    const GATEWAY_URL = process.env.GATEWAY_URL
      ? process.env.GATEWAY_URL
      : "http://localhost:4001/graphql";

    return [
      {
        source: "/graphql",
        destination: GATEWAY_URL,
      },
    ];
  },
  async redirects() {
    return [
      {
        source: "/dashboard",
        destination: "/dashboard/users",
        permanent: false,
      },
      {
        source: "/",
        destination: "/dashboard/users",
        permanent: false,
      },
    ];
  },
};
