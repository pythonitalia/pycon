import React from 'react';
import { Box } from '../box';

const BaseCard = Box.withComponent('div');

type Props = {
  variant?: 'primary' | 'secondary';
};

export class Card extends React.Component<Props> {
  render() {
    return (
      <BaseCard
        borderRadius={8}
      >
        {this.props.children}
      </BaseCard>
    );
  }
}
