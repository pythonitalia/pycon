module.exports = {
  async rewrites() {
    const API_URL = process.env.API_URL
      ? process.env.API_URL
      : "http://localhost:4001/graphql";

    return [
      {
        source: "/graphql",
        destination: API_URL,
      },
    ];
  },
};
