import type { NextFetchEvent, NextRequest } from "next/server";
import { NextResponse } from "next/server";

import { DEFAULT_LOCALE, VALID_LOCALES } from "~/locale/languages";

const PUBLIC_FILE = /\.(.*)$/;

export function middleware(req: NextRequest, _ev: NextFetchEvent) {
  const shouldHandleLocale =
    !PUBLIC_FILE.test(req.nextUrl.pathname) &&
    !req.nextUrl.pathname.includes("/api/") &&
    req.nextUrl.locale === "default";

  console.log("shouldHandleLocale", shouldHandleLocale);
  return shouldHandleLocale
    ? NextResponse.redirect(`/en${req.nextUrl.href}`)
    : undefined;

  // const { pathname } = req.nextUrl;
  // const locale = getLocale(req.cookies.pyconLocale);

  // if (pathname === "/") {
  //   return NextResponse.redirect(`/${locale}`);
  // }

  // return NextResponse.next();
}

// const getLocale = (cookie: string): string => {
//   if (cookie && VALID_LOCALES.findIndex((e) => e === cookie) !== -1) {
//     return cookie;
//   }

//   return DEFAULT_LOCALE;
// };
