import { isToday } from "date-fns";

import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

import { DEFAULT_LOCALE, VALID_LOCALES } from "~/locale/languages";

import { getApolloClient } from "./apollo/client";
import { queryScheduleDays } from "./types";

const PUBLIC_FILE = /\.(.*)$/;
const LOGIN_REDIRECT_URL = ["/cfp", "/grants", "/voting"];

const handleLocale = (req: NextRequest) => {
  const locale = getLocale(
    req.cookies.has("pyconLocale")
      ? req.cookies.get("pyconLocale")!.value
      : null,
  );

  const url = req.nextUrl.clone();
  url.pathname = `${locale}${url.pathname}`;
  console.log("redirect to:", url);

  return NextResponse.redirect(url);
};

export async function middleware(req: NextRequest) {
  const isLoggedIn = req.cookies.has("identity_v2");
  const pathname = req.nextUrl.pathname;

  const shouldHandleLocale =
    !PUBLIC_FILE.test(pathname) &&
    !pathname.includes("/api/") &&
    !pathname.includes("/admin") &&
    !pathname.includes("/graphql") &&
    !pathname.includes("/_next/image") &&
    VALID_LOCALES.every(
      (locale) =>
        !pathname.startsWith(`/${locale}/`) && pathname !== `/${locale}`,
    );

  if (shouldHandleLocale) {
    console.log("pathname", pathname);
    return handleLocale(req);
  }

  if (LOGIN_REDIRECT_URL.includes(pathname) && !isLoggedIn) {
    const url = req.nextUrl.clone();
    url.search = `?next=${pathname}`;
    url.pathname = `/login`;
    return NextResponse.redirect(url);
  }

  if (req.nextUrl.pathname === "/schedule") {
    const url = req.nextUrl.clone();

    const {
      data: {
        conference: { days },
      },
    } = await queryScheduleDays(getApolloClient(), {
      code: process.env.conferenceCode,
    });
    const dateToOpen = days.find((day) => {
      const dayDate = new Date(day.day);
      return isToday(dayDate);
    });

    url.pathname = `/schedule/${dateToOpen?.day ?? days[0].day}`;
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
