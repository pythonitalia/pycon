module.exports = {
  future: {
    webpack5: true,
  },
  async rewrites() {
    const API_URL = process.env.API_URL
      ? process.env.API_URL
      : "http://localhost:4000/graphql";

    return [
      {
        source: "/graphql",
        destination: API_URL,
      },
    ];
  },
};
