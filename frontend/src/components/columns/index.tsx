import React from "react";

import { Columns } from "fannypack";
import styled, { css, CSSObject, SimpleInterpolation } from "styled-components";

export type CustomColumnSideType = { desktop: number; mobile: number };
export type CustomColumnSidesType = {
  top?: CustomColumnSideType;
  bottom?: CustomColumnSideType;
  left?: CustomColumnSideType;
  right?: CustomColumnSideType;
};

const camelToKebabCase = (str: string) =>
  str.replace(/[A-Z]/g, letter => `-${letter.toLowerCase()}`);

type ResponsiveValue = {
  desktop: number;
  mobile: number;
};

export const media = {
  desktop: (
    first: CSSObject | TemplateStringsArray,
    ...interpolations: SimpleInterpolation[]
  ) => {
    return css`
      @media (min-width: 1024px) {
        ${css(first, ...interpolations)}
      }
    `;
  },
};

const responsiveStyle = (
  cssProp: keyof React.CSSProperties,
  values: ResponsiveValue,
) => {
  const prop = camelToKebabCase(cssProp);

  console.log(prop);
  return css`
    ${prop}: ${values.mobile}rem;

    ${media.desktop`
      ${prop}: ${values.desktop}rem;
    `}
  `;
};

export type ResponsiveProps = {
  marginTop?: ResponsiveValue;
  marginBottom?: ResponsiveValue;
  marginLeft?: ResponsiveValue;
  marginRight?: ResponsiveValue;
  paddingTop?: ResponsiveValue;
  paddingBottom?: ResponsiveValue;
  paddingLeft?: ResponsiveValue;
  paddingRight?: ResponsiveValue;
};

export const responsiveSpacing = (props: ResponsiveProps) => css`
  ${Object.entries(props).map(
    ([key, value]) =>
      value && responsiveStyle(key as keyof ResponsiveProps, value),
  )}
`;

export type CustomColumnsType = ResponsiveProps;
export const BaseCustomColumns = Columns as React.SFC<CustomColumnsType>;

export const CustomColumns = styled(BaseCustomColumns)`
  ${props => responsiveSpacing(props)}
`;
