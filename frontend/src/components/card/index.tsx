import React from 'react';
import { Box } from '../box';
import { getBackgroundColor, getColor } from './utils';
import styled from '../../styled';

const BaseCard = styled(Box.withComponent('div'))`
  width: ${props => props.theme.cardDimension[0]}px;
  height: ${props => props.theme.cardDimension[1]}px;
  font-family: ${props => props.theme.fonts.card};
  box-shadow: ${props => props.theme.shadows[2]};

  position: relative;
  overflow: hidden;
`;

const CardBackground = styled.img`
  position: absolute;
  top: 0;
  left: 0;
  object-fit: cover;
  width: 100%;
  height: 100%;
`;

const CardContent = styled(Box.withComponent('div'))`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 2;
`;

type Props = {
  srcset?: string;
  sizes?: string;
  src?: string;
};

export class Card extends React.Component<Props> {
  render() {
    return (
      <BaseCard
        borderRadius={16}
        my={3}
        bg={getBackgroundColor(false)}
        color={getColor(false)}
      >
        <CardContent p={4}>{this.props.children}</CardContent>

        {(this.props.src || this.props.srcset) && (
          <CardBackground src={this.props.src} srcSet={this.props.srcset} />
        )}
      </BaseCard>
    );
  }
}
