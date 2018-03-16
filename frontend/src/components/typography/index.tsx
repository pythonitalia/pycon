import React from 'react';
import { withTheme } from 'emotion-theming';
import withProps from 'recompose/withProps';

import { Theme } from '../../theme';

import {
  space,
  fontSize,
  color,
  lineHeight,
  LineHeightProps,
  SpaceProps,
  FontSizeProps,
  ColorProps,
  BoxShadowProps
} from 'styled-system';

import styled from '../../styled';

type TypographyProps = SpaceProps &
  FontSizeProps &
  LineHeightProps &
  ColorProps &
  BoxShadowProps;

const BaseTypography = styled<TypographyProps, 'h1'>('h1')`
  ${space}
  ${fontSize}
  ${lineHeight}
  ${color}
`;

interface TitleProps {
  level: 1 | 2 | 3 | 4 | 5 | 6;
  children: React.ReactNode;
}

// TODO spacing etc
const BaseTitle = ({
  theme,
  level,
  children
}: TitleProps & { theme: Theme }) => {
  // ugly, but works :)
  const tagName: keyof JSX.IntrinsicElements = `h${level}` as keyof JSX.IntrinsicElements;
  const name = `title${level}`;

  const X = BaseTypography.withComponent(tagName);

  return (
    <X fontSize={name} lineHeight={name}>
      {children}
    </X>
  );
};

export const Title = withTheme<TitleProps, Theme>(BaseTitle);

const BaseParagraph = withProps({
  fontSize: 'body',
  lineHeight: 'body'
})(BaseTypography.withComponent('p'));

export const Paragraph = withTheme<{}, Theme>(BaseParagraph);
