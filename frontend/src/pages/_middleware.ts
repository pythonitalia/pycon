import type { NextFetchEvent, NextRequest } from "next/server";
import { NextResponse } from "next/server";

import { DEFAULT_LOCALE, VALID_LOCALES } from "~/locale/languages";

const PUBLIC_FILE = /\.(.*)$/;

export function middleware(req: NextRequest, _ev: NextFetchEvent) {
  const shouldHandleLocale =
    !PUBLIC_FILE.test(req.nextUrl.pathname) &&
    !req.nextUrl.pathname.includes("/api/") &&
    req.nextUrl.locale === "default";
  const locale = getLocale(req.cookies.pyconLocale);

  console.log("req.nextUrl.href =>", req.nextUrl.href, "req.nextUrl", req.nextUrl)
  return shouldHandleLocale
    ? NextResponse.redirect(`/${locale}${req.nextUrl.href}`)
    : undefined;
}

const getLocale = (cookie: string): string => {
  if (cookie && VALID_LOCALES.findIndex((e) => e === cookie) !== -1) {
    return cookie;
  }

  return DEFAULT_LOCALE;
};
