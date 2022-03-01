import type { NextFetchEvent, NextRequest } from "next/server";
import { NextResponse } from "next/server";

import { getApolloClient } from "~/apollo/client";
import { queryScheduleDays } from "~/types";

export async function middleware(req: NextRequest, _ev: NextFetchEvent) {
  if (req.nextUrl.pathname === "/schedule") {
    const client = getApolloClient();
    const {
      data: {
        conference: { days },
      },
    } = await queryScheduleDays(client, {
      code: process.env.conferenceCode,
    });
    const firstDay = days[0].day;
    return NextResponse.redirect(`/schedule/${firstDay}`);
  }
}
