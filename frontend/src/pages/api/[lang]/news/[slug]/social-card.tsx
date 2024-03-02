import { ImageResponse } from "@vercel/og";

import type { NextRequest } from "next/server";

import { createClient } from "~/apollo/create-client";
import { TitleSubtitleCard } from "~/components/social-card-images/title-subtitle-card";
import { queryNewsArticle } from "~/types";

export const config = {
  runtime: "edge",
  unstable_allowDynamic: ["/node_modules/**"],
};

const regularFont = fetch(
  new URL(
    "../../../../../social-card-font/GeneralSans-Regular.otf",
    import.meta.url,
  ),
).then((res) => res.arrayBuffer());
const semiBoldFont = fetch(
  new URL(
    "../../../../../social-card-font/GeneralSans-Semibold.otf",
    import.meta.url,
  ),
).then((res) => res.arrayBuffer());

const handler = async (req: NextRequest) => {
  const client = createClient();
  const { searchParams } = new URL(req.url);

  const language = searchParams.get("lang");
  const slug = searchParams.get("slug");

  const [
    regularFontData,
    semiBoldFontData,
    {
      data: { newsArticle },
    },
  ] = await Promise.all([
    regularFont,
    semiBoldFont,
    queryNewsArticle(client, {
      slug,
      language,
      hostname: process.env.cmsHostname,
    }),
  ]);

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
          data: semiBoldFontData,
          style: "normal",
          weight: 600,
        },
      ],
    },
  );
};

export default handler;
