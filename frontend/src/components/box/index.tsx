import React from 'react';

import {
  space,
  width,
  fontSize,
  color,
  boxShadow,
  SpaceProps,
  WidthProps,
  FontSizeProps,
  ColorProps,
  BoxShadowProps,
  flexWrap,
  FlexWrapProps,
  flexDirection,
  FlexDirectionProps,
  flex,
  FlexProps,
  alignItems,
  AlignItemsProps,
  display,
  DisplayProps
} from 'styled-system';

import styled from '../../styled';

type BoxProps = SpaceProps &
  WidthProps &
  FontSizeProps &
  ColorProps &
  BoxShadowProps &
  FlexWrapProps &
  FlexDirectionProps &
  FlexProps &
  DisplayProps &
  AlignItemsProps;

export const Box: React.SFC<BoxProps> = styled('div')`
  ${space}
  ${width}
  ${fontSize}
  ${color}
  ${boxShadow}
  ${flexWrap}
  ${flexDirection}
  ${flex}
  ${display}
  ${alignItems}
`;
