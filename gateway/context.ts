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
  const pastaporto = await createPastaporto(identity);
  const context: ApolloContext = {
    setCookies: [],
    setHeaders: [],
    pastaporto,
    allHeaders,
    res,
  };
  return context;
};
