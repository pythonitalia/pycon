import React from "react";

import { Columns } from "fannypack";
import styled, { css } from "styled-components";
import { CustomColumnSideType, CustomColumnsType } from "./types";

export const BaseCustomColumns: React.SFC<CustomColumnsType> = Columns;

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
    let assembledStyle = ``;
    for (const [key, element] of Object.entries(prop)) {
      if (element) {
        assembledStyle = `
          ${assembledStyle}
          ${property}-${key}: ${element.mobile}rem;
          @media only screen and (min-width: 1024px) {
            ${property}-${key}: ${element.desktop}rem;
          }
        `;
      }
    }
    return `
      ${assembledStyle}
    `;
  }

  return css``;
};

export const CustomColumns = styled(BaseCustomColumns)`
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
