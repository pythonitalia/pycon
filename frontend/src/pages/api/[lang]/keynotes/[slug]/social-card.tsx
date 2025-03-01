import { ImageResponse } from "@vercel/og";

import type { NextRequest } from "next/server";

import { createClient } from "~/apollo/create-client";
import { TitleSubtitleCard } from "~/components/social-card-images/title-subtitle-card";
import { queryTalk } from "~/types";

export const config = {
  runtime: "edge",
  unstable_allowDynamic: ["/node_modules/.pnpm/**"],
};

export const handler = async (req: NextRequest) => {
  const regularFont = fetch(
    new URL(
      "./social-card-font/GeneralSans-Regular.otf",
      req.url.substring(0, req.url.lastIndexOf("/api")),
    ),
  ).then((res) => res.arrayBuffer());
  const semiBoldFont = fetch(
    new URL(
      "./social-card-font/GeneralSans-Semibold.otf",
      req.url.substring(0, req.url.lastIndexOf("/api")),
    ),
  ).then((res) => res.arrayBuffer());

  const [regularFontData, semiBoldFontData] = await Promise.all([
    regularFont,
    semiBoldFont,
  ]);
  const client = createClient();
  const { searchParams } = new URL(req.url);

  const language = searchParams.get("lang");
  const slug = searchParams.get("slug");

  const {
    data: { conference },
  } = await queryTalk(client, {
    slug,
    language,
    code: process.env.conferenceCode,
  });
  const talk = conference?.talk;

  const title = talk.title;
  const speakers = talk.speakers.map((speaker) => speaker.fullName).join(", ");

  return new ImageResponse(
    <TitleSubtitleCard title={title} subtitle={speakers} tag="keynote" />,
    {
      width: 1200,
      height: 630,
      fonts: [
        {
          name: "GeneralSans",
          data: regularFontData,
          style: "normal",
          weight: 500,
        },
        {
          name: "GeneralSans",
          data: semiBoldFontData,
          style: "normal",
          weight: 600,
        },
      ],
    },
  );
};

export default handler;
