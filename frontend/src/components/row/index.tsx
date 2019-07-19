import React from "react";

import styled, { css } from "styled-components";
import { customTheme } from "../../config/theme";
import { ALLOWED_RESPONSIVE_ROW_PROPS } from "./const";
import { camelToKebabCase } from "./utils";

type RowResponsiveValuesType = {
  mobile: number;
  tabletPortrait: number;
  tabletLandscape: number;
  desktop: number;
};

type RowResponsiveValuesWidthType = {
  mobile: number;
  tabletPortrait: number;
  tabletLandscape: number;
  desktop: number;
};

type AllowedResponsiveProps = typeof ALLOWED_RESPONSIVE_ROW_PROPS[number];

const createProperty = (prop: string, value: number) => {
  return prop === "justify-content"
    ? `${prop}: ${value};`
    : `${prop}: ${value}rem;`;
};

const responsiveStyle = (props: RowType) => {
  let assembledStyle = css``;
  Object.entries(props)
    .filter(
      ([key]) =>
        ALLOWED_RESPONSIVE_ROW_PROPS.indexOf(key as AllowedResponsiveProps) !==
        -1,
    )
    .map(([key, values]) => {
      const prop = camelToKebabCase(key);
      assembledStyle = css`
        ${assembledStyle}
        ${Object.entries(customTheme.breakPoints).map(([k, value]) => {
          return `@media (min-width: ${value}) {
          ${prop}: ${values[k]}rem;
        }`;
        })}
      `;
    });

  return assembledStyle;
};

type RowSpacingType = {
  marginTop?: RowResponsiveValuesWidthType;
  marginBottom?: RowResponsiveValuesType;
  marginLeft?: RowResponsiveValuesType;
  marginRight?: RowResponsiveValuesType;
  paddingTop?: RowResponsiveValuesType;
  paddingBottom?: RowResponsiveValuesType;
  paddingLeft?: RowResponsiveValuesType;
  paddingRight?: RowResponsiveValuesType;
};

type RowType = React.FunctionComponent<RowSpacingType>;

const Wrapper = styled.div<RowType>`
  display: flex;
  position: relative;
  flex-wrap: wrap;
  ${props => {
    return responsiveStyle(props);
  }}
`;

export const Row: RowType = props => {
  return <Wrapper {...props}>{props.children}</Wrapper>;
};
