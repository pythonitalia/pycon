import palx from 'palx';

// @ts-ignore
import ColorScheme from 'color-scheme';
// @ts-ignore
import tinycolor from 'tinycolor2';

import { theme as baseTheme } from '@hackclub/design-system';

const baseColors = [
  '#07077a',
  '#311B92',
  '#0D47A1',
  '#F57F17',
  '#BF360C',
  '#263238',
];

const base = '#94052c';

const scm = new ColorScheme();
scm
  .from_hex(base.replace('#', ''))
  .scheme('triade')
  .distance(0.1)
  .add_complement(false)
  .variation('pastel')
  .web_safe(true);

const schema = scm.colors();

const color = tinycolor(base);
const accent = tinycolor(`#${schema[4]}`);

const makeScale = (c: any) => [
  c.lighten(4).toString(),
  c.lighten(8).toString(),
  c.lighten(12).toString(),
  c.lighten(16).toString(),
];

export const palette = palx(base);

export const grays = {
  darker: '#121217',
  dark: '#17171d',
  black: palette.black,
  slate: palette.gray[8],
  silver: palette.gray[7],
  smoke: palette.gray[2],
  snow: palette.gray[0],
  white: '#ffffff',
};

export const brand = {
  primary: base,
  scale: makeScale(color),
  accent: accent.toString(),
  accentScale: makeScale(accent),
  success: palette.teal[5],
  info: palette.blue[5],
  warning: palette.orange[5],
  error: palette.red[7],
  muted: grays.silver,
};

export const colors = {
  ...brand,
  ...grays,
  ...palette,
};

const theme = {
  ...baseTheme,
  colors,
};

export default theme;
