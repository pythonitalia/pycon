import React, { AnchorHTMLAttributes } from 'react';

import MaterialButton from '../../vendor/react-material/button';

import { ButtonVariant } from './types';

type Props = {
  variant?: ButtonVariant;
  children: React.ReactNode;
};

const button = (
  { variant, children, ...additionalProps }: Props,
  tagName: 'a' | 'button',
) => {
  return (
    <MaterialButton
      tagName={tagName}
      unelevated={variant === 'primary' ? true : false}
      outlined={variant === 'primary' ? false : true}
      {...additionalProps}
    >
      {children}
    </MaterialButton>
  );
};

type ButtonLinkProps = Props & AnchorHTMLAttributes<HTMLAnchorElement>;

export const Button: React.SFC<Props> = (props: Props) =>
  button(props, 'button');
export const ButtonLink: React.SFC<ButtonLinkProps> = (
  props: ButtonLinkProps,
) => button(props, 'a');

Button.defaultProps = {
  variant: 'primary',
};
ButtonLink.defaultProps = {
  variant: 'primary',
};
