module.exports = {
  async rewrites() {
    return [
      {
        source: "/graphql",
        destination: `http://localhost:4001/graphql`,
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
