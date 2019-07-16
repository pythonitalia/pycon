import { Column, space } from "fannypack";
import React from "react";
import styled, { css } from "styled-components";
import { CustomColumnSideType, CustomColumnType } from "./types";

export const BaseCustomColumn: React.SFC<CustomColumnType> = Column;

const renderResponsiveClasses = (
  prop: {
    top?: CustomColumnSideType;
    bottom?: CustomColumnSideType;
    left?: CustomColumnSideType;
    right?: CustomColumnSideType;
  },
  property: "padding" | "margin",
) => {
  if (prop) {
    let assambled_style = "";
    for (const [key, element] of Object.entries(prop)) {
      // console.log(key, element);
      console.log(`${property}-${key}`);
      if (element) {
        assambled_style = `${assambled_style}
        ${property}-${key}: ${space(element.mobile, "major")}rem;
        @media only screen and (min-width: 1024px) {
          ${property}-${key}: ${space(element.desktop, "major")}rem;
        }
        `;
      }
    }
  }

  return css``;
};

export const CustomColumn = styled(BaseCustomColumn)`
  ${props => {
    const { responsivePadding, responsiveMargin } = props;
    let assembled_style = "";
    if (responsivePadding) {
      const stylePadding = renderResponsiveClasses(
        responsivePadding,
        "padding",
      );
      assembled_style = `${assembled_style} ${stylePadding}`;
    }
    if (responsiveMargin) {
      const styleMargin = renderResponsiveClasses(responsiveMargin, "margin");
      assembled_style = `${assembled_style} ${styleMargin}`;
    }
    return css`
      ${assembled_style}
    `;
    return css``;
  }}
`;
