import withProps from 'recompose/withProps';

import { Box } from '../box';

const BaseLink = Box.withComponent('a').extend`
    text-decoration: none;
    color: inherit;
`;

export const Link = withProps({
  fontFamily: 'base',
  fontSize: 'body',
  lineHeight: 'body',
  px: 3,
  hover: {
    color: 'blue'
  }
})(BaseLink);
