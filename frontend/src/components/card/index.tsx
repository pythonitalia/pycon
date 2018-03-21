import React from 'react';
import { Box } from '../box';
import { getBackgroundColor, getColor } from './utils';
import styled from '../../styled';

const BaseCard = styled(Box.withComponent('div'))`
  width: ${props => props.theme.cardDimension[0]}px;
  height: ${props => props.theme.cardDimension[1]}px;
  font-family: ${props => props.theme.fonts.card};
  box-shadow: ${props => props.theme.shadows[2]};
`;

export class Card extends React.Component {
  render() {
    return (
      <BaseCard
        borderRadius={16}
        bg={getBackgroundColor(false)}
        px={24}
        py={16}
        color={getColor(false)}
      >
        {this.props.children}
      </BaseCard>
    );
  }
}
