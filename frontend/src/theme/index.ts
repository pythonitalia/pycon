const breakpoints = ['40em', '52em', '64em'];

const colors = {
  text: '#333333',
  blue: '#0c67ff',

  grey: '#f4f4f4',
  white: '#ffffff'
};

const space = [0, 4, 8, 16, 32, 64, 128, 256, 512];

const fontSizes = {
  title1: 45.234335104,
  title2: 31.990336,
  title3: 22.624,
  body: 16
};

const lineHeights = {
  title1: 1.1,
  title2: 1.2,
  title3: 1.3,
  body: 1.4
};

const fontWeights = {
  normal: 500,
  bold: 700
};

const letterSpacings = {
  normal: 'normal',
  caps: '0.25em'
};

const radii = [0, 2, 4, 8];

const borders = [0, '1px solid', '2px solid'];

const shadows = [`0 1px 2px 0 ${colors.text}`, `0 1px 4px 0 ${colors.text}`];

const fonts = {
  title: 'Rubik',
  base: 'Roboto Mono',
  button: 'Rubik'
};

const timings = [0.15, 0.3];

export const theme = {
  breakpoints,
  colors,
  space,
  fontSizes,
  lineHeights,
  fontWeights,
  letterSpacings,
  radii,
  fonts,
  borders,
  shadows,
  timings
};

export type Theme = typeof theme;
