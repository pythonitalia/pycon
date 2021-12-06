/* eslint import/first: "off", @typescript-eslint/ban-ts-comment: "off" */
import type { NextFetchEvent, NextRequest } from "next/server";
import { NextResponse } from "next/server";

import { getApolloClient } from "~/apollo/client";
import { DEFAULT_LOCALE } from "~/locale/languages";
import { queryScheduleDays } from "~/types";

export async function middleware(req: NextRequest, _ev: NextFetchEvent) {
  this.__DEV__ = false;
  // @ts-ignore
  global.__DEV__ = false;
  // @ts-ignore
  process.__DEV__ = false;

  const { pathname, locale } = req.nextUrl;
  const client = getApolloClient();
  const {
    data: {
      conference: { days },
    },
  } = await queryScheduleDays(client, {
    code: process.env.conferenceCode,
  });

  const firstDay = days[0].day;
  const language = locale === "default" ? DEFAULT_LOCALE : locale;

  // If we are landing on the /schedule page we want
  // to dynamically redirect the user to the first day of the schedule
  if (pathname === "/schedule") {
    return NextResponse.redirect(`/${language}/schedule/${firstDay}`);
  }

  return undefined;
}
