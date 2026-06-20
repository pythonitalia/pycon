import { isToday } from "date-fns";

import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

import { getApolloClient } from "./apollo/client";
import { queryScheduleDays } from "./types";

const LOGIN_REDIRECT_URL = ["/cfp", "/grants", "/voting"];

export async function middleware(req: NextRequest) {
  const isLoggedIn = req.cookies.has("pythonitalia_sessionid");

  if (LOGIN_REDIRECT_URL.includes(req.nextUrl.pathname) && !isLoggedIn) {
    const url = req.nextUrl.clone();
    url.search = `?next=${req.nextUrl.pathname}`;
    url.pathname = "/login";
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

export const config = {
  matcher: "/:path*",
};
