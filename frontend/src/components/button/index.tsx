import React from 'react';
import { Box } from '../box';

const BaseButton = Box.withComponent('button');

type Props = {
  variant?: 'primary' | 'secondary';
};

export class Button extends React.Component<Props> {
  render() {
    return (
      <BaseButton
        px={3}
        py={2}
        borderRadius={100}
        bg={getBackgroundColor(this.props.variant)}
        color={getTextColor(this.props.variant)}
        fontSize={getFontSize(this.props.variant)}
      >
        Hello
      </BaseButton>
    );
  }
}

const getBackgroundColor = (variant: Props['variant']) => {
  switch (variant) {
    case 'primary':
    default:
      return 'blue';
    case 'secondary':
      return 'grey';
  }
};

const getTextColor = (variant: Props['variant']) => {
  switch (variant) {
    case 'primary':
    default:
      return 'white';
    case 'secondary':
      return 'blue';
  }
};

const getFontSize = (variant: Props['variant']) => {
  switch (variant) {
    case 'primary':
    default:
      return 'body';
    case 'secondary':
      return 'body';
  }
};
