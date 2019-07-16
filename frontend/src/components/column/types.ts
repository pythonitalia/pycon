import { ColumnProps } from "fannypack";

export type CustomColumnSideType = { desktop: number; mobile: number };
export type CustomColumnSidesType = {
  top?: CustomColumnSideType;
  bottom?: CustomColumnSideType;
  left?: CustomColumnSideType;
  right?: CustomColumnSideType;
};

export type CustomColumnType = ColumnProps & {
  responsivePadding?: CustomColumnSidesType;
  responsiveMargin?: CustomColumnSidesType;
};
