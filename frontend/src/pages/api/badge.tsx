import PDFDocument from "pdfkit";
import satori from "satori";
import SVGtoPDF from "svg-to-pdfkit";

import type { NextRequest } from "next/server";

import { Badge } from "~/components/badge";

import { BADGE_WIDTH_PX, BADGE_HEIGHT_PX } from "../badge";

export const config = {
  runtime: "edge",
};

const regularFont = fetch(
  new URL("../../social-card-font/GeneralSans-Regular.otf", import.meta.url),
).then((res) => res.arrayBuffer());
const semiBoldFont = fetch(
  new URL("../../social-card-font/GeneralSans-Semibold.otf", import.meta.url),
).then((res) => res.arrayBuffer());

const handler = async (req: NextRequest) => {
  const regularFontData = await regularFont;
  const semiBoldFontData = await semiBoldFont;

  const svg = await satori(
    <div
      style={{
        width: "100%",
        height: "100%",
        display: "flex",
        fontFamily: '"GeneralSans"',
      }}
    >
      <Badge />
    </div>,
    {
      debug: false,
      width: BADGE_WIDTH_PX,
      height: BADGE_HEIGHT_PX,
      fonts: [
        {
          name: "GeneralSans",
          data: regularFontData,
          style: "normal",
          weight: 400,
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

  const doc = new PDFDocument();
  doc.addPage({
    size: "A4",
  });
  SVGtoPDF(doc, svg, 0, 0);

  return new Response(svg);
};

export default handler;
