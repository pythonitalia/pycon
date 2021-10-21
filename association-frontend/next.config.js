module.exports = {
  publicRuntimeConfig: {
    stripeKey: process.env.STRIPE_KEY,
    apiUrl: process.env.API_URL ?? "http://localhost:4000/graphql",
  },
};
