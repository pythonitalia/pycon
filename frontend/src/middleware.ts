import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

import { DEFAULT_LOCALE, VALID_LOCALES } from "~/locale/languages";

const PUBLIC_FILE = /\.(.*)$/;
const LOGIN_REDIRECT_URL = ["/cfp", "/grants"];

const handleLocale = (req: NextRequest) => {
  const locale = getLocale(
    req.cookies.has("pyconLocale")
      ? req.cookies.get("pyconLocale")!.value
      : null,
  );

  const url = req.nextUrl.clone();
  url.pathname = `${locale}${url.pathname}`;

  return NextResponse.redirect(url);
};

export function middleware(req: NextRequest) {
  const isLoggedIn = req.cookies.has("identity_v2");

  const shouldHandleLocale =
    !PUBLIC_FILE.test(req.nextUrl.pathname) &&
    !req.nextUrl.pathname.includes("/api/") &&
    !req.nextUrl.pathname.includes("/admin") &&
    !req.nextUrl.pathname.includes("/graphql") &&
    req.nextUrl.locale === "default";

  if (shouldHandleLocale) {
    return handleLocale(req);
  }

  if (LOGIN_REDIRECT_URL.includes(req.nextUrl.pathname) && !isLoggedIn) {
    const url = req.nextUrl.clone();
    url.search = `?next=${req.nextUrl.pathname}`;
    url.pathname = `/login`;
    return NextResponse.redirect(url);
  }

  return NextResponse.next();
}

const getLocale = (cookie: string): string => {
  if (cookie && VALID_LOCALES.findIndex((e) => e === cookie) !== -1) {
    return cookie;
  }

  return DEFAULT_LOCALE;
};

export const config = {
  matcher: "/:path*",
};
