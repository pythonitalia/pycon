import palx from 'palx';

// @ts-ignore
import ColorScheme from 'color-scheme';
// @ts-ignore
import tinycolor from 'tinycolor2';

import { theme as baseTheme } from '@hackclub/design-system';

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

const makeScale = (c: any) => {
  const method = c.isLight() ? 'darken' : 'lighten';

  return [
    c[method](4).toString(),
    c[method](8).toString(),
    c[method](12).toString(),
    c[method](16).toString(),
  ];
};

export const palette = palx(base);

export const colors = {
  primary: base,
  scale: makeScale(color),
  accent: accent.toString(),
  accentScale: makeScale(accent),
  success: palette.teal[5],
  info: palette.blue[5],
  warning: palette.orange[5],
  error: palette.red[7],
};

const theme = {
  ...baseTheme,
  colors,
};

export default theme;
