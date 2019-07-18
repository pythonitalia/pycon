import React from "react";

import styled, { css } from "styled-components";
import { customTheme } from "../../config/theme";
import { ALLOWED_RESPONSIVE_COLUMN_PROPS } from "./const";
import { camelToKebabCase } from "./utils";

type ColumnWidthRange = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12;

export type ColumnWidthValuesType = {
  mobile: ColumnWidthRange;
  tabletPortrait: ColumnWidthRange;
  tabletLandscape: ColumnWidthRange;
  desktop: ColumnWidthRange;
};

type ColumnResponsiveValuesType = {
  mobile: number;
  tabletPortrait: number;
  tabletLandscape: number;
  desktop: number;
};

type AllowedResponsiveProps = typeof ALLOWED_RESPONSIVE_COLUMN_PROPS[number];

const createProperty = (prop: string, value: number) => {
  return prop === "col-width"
    ? `width: ${(value / 12) * 100}%;`
    : `${prop}: ${value}rem;`;
};

const responsiveStyle = (props: ColumnType) => {
  let assembledStyle = css``;
  Object.entries(props)
    .filter(
      ([key]) =>
        ALLOWED_RESPONSIVE_COLUMN_PROPS.indexOf(
          key as AllowedResponsiveProps,
        ) !== -1,
    )
    .map(([key, values]) => {
      const prop = camelToKebabCase(key);
      assembledStyle = css`${assembledStyle}${Object.entries(
        customTheme.breakPoints,
      ).map(([k, breakPointValue]) => {
        return css`
          @media (min-width: ${breakPointValue}) {
            ${createProperty(prop, values[k])}
          }
        `;
      })}`;
    });

  return assembledStyle;
};

type ColumnSpacingType = {
  colWidth?: ColumnWidthValuesType;
  marginTop?: ColumnResponsiveValuesType;
  marginBottom?: ColumnResponsiveValuesType;
  marginLeft?: ColumnResponsiveValuesType;
  marginRight?: ColumnResponsiveValuesType;
  paddingTop?: ColumnResponsiveValuesType;
  paddingBottom?: ColumnResponsiveValuesType;
  paddingLeft?: ColumnResponsiveValuesType;
  paddingRight?: ColumnResponsiveValuesType;
};

type ColumnType = React.FunctionComponent<ColumnSpacingType>;

const Wrapper = styled.div<ColumnType>`
  position: relative;
  padding: 0.5rem;
  ${props => {
    return responsiveStyle(props);
  }}
`;

export const Column: ColumnType = props => {
  return <Wrapper {...props}>{props.children}</Wrapper>;
};
