import clsx from "clsx";
import { getStyleClassesTextColor } from "../colors-utils";
import { getStyleClassesForHeading } from "../heading/heading";
import { getStyleClassesForTextSize } from "../text/text";

const createProseStyle = (element, ...style) => {
  const classes = style.join(" ").split(" ");
  return classes.reduce((acc, curr) => {
    acc = `${acc} prose-${element}:${curr}`;
    return acc;
  }, "");
};

const SIZE_1_P_PROSE_STYLES = createProseStyle(
  "p",
  getStyleClassesForTextSize(1),
  getStyleClassesTextColor("grey-900")
);

const SIZE_1_LI_PROSE_STYLES = createProseStyle(
  "li",
  getStyleClassesForTextSize(1),
  getStyleClassesTextColor("grey-900")
);

const SIZE_2_P_PROSE_STYLES = createProseStyle(
  "p",
  getStyleClassesForTextSize(2),
  getStyleClassesTextColor("grey-900")
);

const SIZE_2_LI_PROSE_STYLES = createProseStyle(
  "li",
  getStyleClassesForTextSize(2),
  getStyleClassesTextColor("grey-900")
);

const H2_PROSE_STYLES = createProseStyle(
  "h2",
  getStyleClassesForHeading(2),
  getStyleClassesTextColor("grey-900")
);

const H3_PROSE_STYLES = createProseStyle(
  "h3",
  getStyleClassesForHeading(3),
  getStyleClassesTextColor("grey-900")
);

const H4_PROSE_STYLES = createProseStyle(
  "h4",
  getStyleClassesForHeading(4),
  getStyleClassesTextColor("grey-900")
);

export const ALL_PROSE_STYLES_SIZE_1 = clsx(
  SIZE_1_P_PROSE_STYLES,
  SIZE_1_LI_PROSE_STYLES
);

export const ALL_PROSE_STYLES_SIZE_2 = clsx(
  SIZE_2_P_PROSE_STYLES,
  SIZE_2_LI_PROSE_STYLES
);

export const ALL_H_STYLES = clsx(
  H2_PROSE_STYLES,
  H3_PROSE_STYLES,
  H4_PROSE_STYLES
);
