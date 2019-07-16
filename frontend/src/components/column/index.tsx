import React from "react";

import { Column, space } from "fannypack";
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
    let assembledStyle = "";
    for (const [key, element] of Object.entries(prop)) {
      if (element) {
        assembledStyle = `${assembledStyle}
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
    let assembledStyle = "";
    if (responsivePadding) {
      const stylePadding = renderResponsiveClasses(
        responsivePadding,
        "padding",
      );
      assembledStyle = `${assembledStyle} ${stylePadding}`;
    }
    if (responsiveMargin) {
      const styleMargin = renderResponsiveClasses(responsiveMargin, "margin");
      assembledStyle = `${assembledStyle} ${styleMargin}`;
    }
    return css`
      ${assembledStyle}
    `;
  }}
`;
