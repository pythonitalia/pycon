import getConfig from "next/config";

const { publicRuntimeConfig } = getConfig();

export const STRIPE_KEY = publicRuntimeConfig.stripeKey;
export const API_URL = publicRuntimeConfig.apiUrl;
