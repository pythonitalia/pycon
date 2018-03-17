import React from 'react';
import { Box } from '../box';
import styled from '../../styled';
import { ButtonVariant } from './types';
import {
  getBackgroundColor,
  getFontSize,
  getBorderColor,
  getBorder,
  getTextColor
} from './utils';

const BaseButton = styled(Box.withComponent('button'))`
  transition: background-color ${props => props.theme.timings[0]}s ease-out,
    color ${props => props.theme.timings[0]}s ease-out;
  cursor: pointer;
  text-transform: uppercase;
  font-family: ${props => props.theme.fonts.button};
`;

type Props = {
  variant: ButtonVariant;
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
        borderColor={getBorderColor(this.props.variant)}
        border={getBorder(this.props.variant, false)}
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
