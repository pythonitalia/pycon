import { Badge } from "~/components/badge";

const cmToPx = (cm: number) => cm * (96 / 2.54);

const CUT_SPACE_CM = 3;
// 13 - 3
const CUT_LINE_SIZE_CM = 0.3;
const CUT_LINE_SIZE_2_CM = 0.07;

export const CUT_LINE_SIZE_PX = cmToPx(CUT_LINE_SIZE_CM);
export const CUT_LINE_SIZE_2_PX = cmToPx(CUT_LINE_SIZE_2_CM);

const BADGE_WIDTH_CM = 8;
const BADGE_HEIGHT_CM = 12;

export const CUT_SPACE_PX = cmToPx(CUT_SPACE_CM);

export const BADGE_WIDTH_PX = cmToPx(BADGE_WIDTH_CM + CUT_SPACE_CM);
export const BADGE_HEIGHT_PX = cmToPx(BADGE_HEIGHT_CM + CUT_SPACE_CM);

export const BADGE_INSIDE_WIDTH_PX = BADGE_WIDTH_PX - CUT_SPACE_PX;
export const BADGE_INSIDE_HEIGHT_PX = BADGE_HEIGHT_PX - CUT_SPACE_PX;

const BadgePage = () => {
  return (
    <div className="grid grid-cols-2 gap-3">
      <PageBadge />
      <PageBadge />
    </div>
  );
};

const PageBadge = () => {
  return (
    <div
      style={{
        display: "flex",
        width: `${BADGE_WIDTH_PX}px`,
        height: `${BADGE_HEIGHT_PX}px`,
        fontFamily: '"GeneralSans-Variable"',
      }}
    >
      <Badge />
    </div>
  );
};

export default BadgePage;
