import type { NextFetchEvent, NextRequest } from "next/server";
import { NextResponse } from "next/server";

import { DEFAULT_LOCALE, VALID_LOCALES } from "~/locale/languages";

const PUBLIC_FILE = /\.(.*)$/;

export function middleware(req: NextRequest, _ev: NextFetchEvent) {
  const shouldHandleLocale =
    !PUBLIC_FILE.test(req.nextUrl.pathname) &&
    !req.nextUrl.pathname.includes("/api/") &&
    !req.nextUrl.pathname.includes("/admin") &&
    req.nextUrl.locale === "default";
  const locale = getLocale(req.cookies.pyconLocale);

  if (!shouldHandleLocale) {
    return undefined;
  }

  return NextResponse.redirect(
    `/${locale}${req.nextUrl.pathname.replace("/default", "")}`,
  );
}

const getLocale = (cookie: string): string => {
  if (cookie && VALID_LOCALES.findIndex((e) => e === cookie) !== -1) {
    return cookie;
  }

  return DEFAULT_LOCALE;
};
