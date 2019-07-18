import React from "react";

import styled from "styled-components";
import { customTheme } from "../../config/theme";
import { ALLOWED_RESPONSIVE_SPACING_PROPS } from "./const";
import { camelToKebabCase } from "./utils";

type RowResponsiveValuesType = {
  mobile: number;
  tabletPortrait: number;
  tabletLandscape: number;
  desktop: number;
};

type AllowedResponsiveSpacingProps = typeof ALLOWED_RESPONSIVE_SPACING_PROPS[number];

const responsiveStyle = (props: RowType) => {
  let assembledStyle = ``;
  Object.entries(props)
    .filter(
      ([key]) =>
        ALLOWED_RESPONSIVE_SPACING_PROPS.indexOf(
          key as AllowedResponsiveSpacingProps,
        ) !== -1,
    )
    .map(([key, values]) => {
      const prop = camelToKebabCase(key);
      assembledStyle = `
      ${assembledStyle}
      ${Object.entries(customTheme.breakPoints).map(([k, value]) => {
        console.log(value);

        return `
        @media (min-width: ${value}) {
          ${prop}: ${values[k]}rem;
        }
        `;
      })}
      `;
    });
  console.log(assembledStyle);
  return assembledStyle;
};

type RowSpacingType = {
  marginTop?: RowResponsiveValuesType;
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
  ${props => {
    return responsiveStyle(props);
    // console.log(props.marginBottom);
    // return ``;
  }}
`;

export const Row: RowType = props => {
  return <Wrapper {...props}>{props.children}</Wrapper>;
};
