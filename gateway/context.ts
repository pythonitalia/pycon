import cookie from "cookie";
import { removeIdentityTokens } from "./pastaporto/identity";
import { createPastaporto } from "./pastaporto";

export const createContext = async (cookiesHeader?: string) => {
  let cookies = null;
  if (cookiesHeader) {
    cookies = cookie.parse(cookiesHeader);
  }

  let identity = null;
  let refreshToken = null;

  const context: { [key: string]: any } = {
    setCookies: new Array(),
    setHeaders: new Array(),
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
  }
  return context;
};
