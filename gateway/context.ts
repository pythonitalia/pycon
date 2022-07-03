import { IS_DEV } from "./config";
import cookie from "cookie";

import { createPastaporto } from "./pastaporto/create-pastaporto";

export type ApolloContext = {
  setCookies?: any[];
  setHeaders?: any[];
  allHeaders?: any;
  pastaporto: string | null;
  res?: any;
};

export const createContext = async ({
  allHeaders,
  cookiesHeader,
  res,
}: {
  allHeaders: any;
  cookiesHeader?: string;
  res: any;
}) => {
  let cookies = null;
  if (cookiesHeader) {
    cookies = cookie.parse(cookiesHeader);
  }

  const identity = cookies?.["identity_v2"] ?? null;
  let pastaporto = null;
  try {
    pastaporto = await createPastaporto(identity);
  } catch (e) {
    console.error("Error creating pastaporto.", e);
    res.cookie("identity_v2", "invalid", {
      httpOnly: true,
      maxAge: -1,
      path: "/",
      sameSite: "strict",
      secure: !IS_DEV,
    });
  }

  const context: ApolloContext = {
    setCookies: [],
    setHeaders: [],
    pastaporto,
    allHeaders,
    res,
  };
  return context;
};
