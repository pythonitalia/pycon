module.exports = {
  async rewrites() {
    return [
      {
        source: "/graphql",
        destination: `http://localhost:8050/graphql`,
      },
    ];
  },
};
