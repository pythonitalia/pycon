/* eslint import/first: "off", @typescript-eslint/ban-ts-comment: "off", @typescript-eslint/no-var-requires: "off" */
import type { NextFetchEvent, NextRequest } from "next/server";
import { NextResponse } from "next/server";

import { DEFAULT_LOCALE } from "~/locale/languages";
import { queryScheduleDays } from "~/types";

const __ = "__";
const GLOBAL_KEY = [__, __].join("DEV");

export async function middleware(req: NextRequest, _ev: NextFetchEvent) {
  this.__DEV__ = false;
  // @ts-ignore
  global.__DEV__ = false;
  // @ts-ignore
  (global as any)[GLOBAL_KEY] = false
  // @ts-ignore
  process.__DEV__ = false;

  // @ts-ignore
  const { getApolloClient } = require("../../apollo/client")

  console.log("a")
  const { pathname, locale } = req.nextUrl;
  console.log("b")

  const client = getApolloClient();
  console.log("c")
  const {
    data: {
      conference: { days },
    },
  } = await queryScheduleDays(client, {
    code: process.env.conferenceCode,
  });
  console.log("d")

  // const firstDay = days[0].day;
  // const language = locale === "default" ? DEFAULT_LOCALE : locale;

  // If we are landing on the /schedule page we want
  // to dynamically redirect the user to the first day of the schedule
  // if (pathname === "/schedule") {
  //   return NextResponse.redirect(`/${language}/schedule/${firstDay}`);
  // }

  return undefined;
}
