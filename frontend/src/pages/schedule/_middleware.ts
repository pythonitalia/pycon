import type { NextFetchEvent, NextRequest } from "next/server";
import { NextResponse } from "next/server";

import { getApolloClient } from "~/apollo/client";
import { queryScheduleDays } from "~/types";

export async function middleware(req: NextRequest, _ev: NextFetchEvent) {
  if (req.nextUrl.pathname !== "/schedule") {
    return undefined;
  }

  console.log("aee", fetch)

  // const client = getApolloClient();
  // console.log("a", client)
  // const out = await queryScheduleDays(client, {
  //   code: process.env.conferenceCode,
  // });
  // console.log("b", out)
  // const days = out.data.conference.days
  // console.log("c", days)
  // const firstDay = days[0].day;
  // console.log("d", firstDay)
  // return NextResponse.redirect(`/schedule/${firstDay}`);
  return undefined;
}
