module.exports = {
  async rewrites() {
    return [
      {
        source: "/graphql",
        destination: `http://localhost:8050/admin-api`,
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
    ];
  },
};
