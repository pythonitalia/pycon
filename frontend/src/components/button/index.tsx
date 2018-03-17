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
        bg={getBackgroundColor(this.props.variant, false)}
        color={getTextColor(this.props.variant, false)}
        fontSize={getFontSize(this.props.variant)}
        borderColor = {getBorderColor(this.props.variant)}
        hover={{
          backgroundColor: getBackgroundColor(this.props.variant, true),
          color: getTextColor(this.props.variant, true)
        }}
      >
        {this.props.children}
      </BaseButton>
    );
  }
}

const getBackgroundColor = (variant: Props['variant'], hover: boolean) => {
  let result = undefined;
  switch (variant) {
    case 'primary':
    default:
      hover ? (result = 'white') : (result = 'blue');
      break;
    case 'secondary':
      hover ? (result = 'white') : (result = 'grey');
      break;
  }
  return result;
};

const getTextColor = (variant: Props['variant'], hover: boolean) => {
  let result = undefined;
  switch (variant) {
    case 'primary':
    default:
      hover ? (result = 'blue') : (result = 'white');
      break;
    case 'secondary':
      hover ? (result = 'grey') : (result = 'white');
      break;
  }
  return result;
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

const getBorderColor = (variant: Props['variant']) => {
  switch (variant) {
    case 'primary':
    default:
      return 'blue';
    case 'secondary':
      return 'white';
  }
};
