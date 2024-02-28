import {
  SnakeHead,
  SnakeTail,
} from "@python-italia/pycon-styleguide/illustrations";
import { ImageResponse } from "@vercel/og";

import type { NextRequest } from "next/server";

import { createClient } from "~/apollo/create-client";
import { TitleSubtitleCard } from "~/components/social-card-images/title-subtitle-card";
import { queryNewsArticle } from "~/types";

export const config = {
  runtime: "edge",
};

const regularFont = fetch(
  new URL(
    "../../../../../social-card-font/GeneralSans-Regular.otf",
    import.meta.url,
  ),
).then((res) => res.arrayBuffer());
const boldFont = fetch(
  new URL(
    "../../../../../social-card-font/GeneralSans-Bold.otf",
    import.meta.url,
  ),
).then((res) => res.arrayBuffer());

const handler = async (req: NextRequest) => {
  const regularFontData = await regularFont;
  const boldFontData = await boldFont;
  const client = createClient();
  const { searchParams } = new URL(req.url);

  const language = searchParams.get("lang");
  const slug = searchParams.get("slug");

  const {
    data: { newsArticle },
  } = await queryNewsArticle(client, {
    slug,
    language,
    hostname: process.env.cmsHostname,
  });

  const title = newsArticle?.title;
  const excerpt = newsArticle?.excerpt;

  return new ImageResponse(
    <TitleSubtitleCard title={title} subtitle={excerpt} />,
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
          data: boldFontData,
          style: "normal",
          weight: 700,
        },
      ],
    },
  );
};

export default handler;
