import cookie from "cookie";

import { createPastaporto } from "./pastaporto";
import { Pastaporto } from "./pastaporto/entities";
import { removeIdentityTokens } from "./pastaporto/identity";

export type ApolloContext = {
  setCookies?: any[];
  setHeaders?: any[];
  allHeaders?: any;
  pastaporto?: Pastaporto;
  res?: any;
};

export const createContext = async (
  allHeaders: any,
  cookiesHeader?: string,
) => {
  let cookies = null;
  if (cookiesHeader) {
    cookies = cookie.parse(cookiesHeader);
  }

  let identity = null;
  let refreshToken = null;

  const context: ApolloContext = {
    setCookies: [],
    setHeaders: [],
    allHeaders,
  };

  if (cookies) {
    identity = cookies["identity"];
    refreshToken = cookies["refreshIdentity"];
  }

  try {
    context.pastaporto = await createPastaporto(
      identity,
      context,
      refreshToken,
    );
  } catch (e) {
    console.log("Unable to create pastaporto, deleting identity tokens", e);
    removeIdentityTokens(context);

    context.pastaporto = Pastaporto.unauthenticated();
  }
  return context;
};
