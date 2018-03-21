import React from 'react';
import { Box } from '../box';
import { getBackgroundColor } from './utils';
import styled from '../../styled';

const BaseCard = styled(Box.withComponent('div'))`
  width: ${props => props.theme.cardDimension[0]}px;
  height: ${props => props.theme.cardDimension[1]}px;
`;

export class Card extends React.Component {
  render() {
    return (
      <BaseCard
        borderRadius={16}
        bg={getBackgroundColor(false)}
      >
        {this.props.children}
      </BaseCard>
    );
  }
}
