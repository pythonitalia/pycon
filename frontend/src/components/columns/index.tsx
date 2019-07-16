import { Columns } from "fannypack";
import React from "react";
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
    let assambled_style = ``;
    for (const [key, element] of Object.entries(prop)) {
      if (element) {
        assambled_style = `
          ${assambled_style}
          ${property}-${key}: ${element.mobile}rem;
          @media only screen and (min-width: 1024px) {
            ${property}-${key}: ${element.desktop}rem;
          }
        `;
        console.log(assambled_style);
      }
    }
    return `
      ${assambled_style}
    `;
  }

  return css``;
};

export const CustomColumns = styled(BaseCustomColumns)`
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
