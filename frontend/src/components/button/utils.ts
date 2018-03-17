import { ButtonVariant } from './types';

export const getBackgroundColor = (variant: ButtonVariant, hover: boolean) => {
  let result;

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

export const getTextColor = (variant: ButtonVariant, hover: boolean) => {
  let result;

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

export const getFontSize = (variant: ButtonVariant) => {
  let result;

  switch (variant) {
    case 'primary':
    default:
      result = 'body';
      break;
    case 'secondary':
      result = 'body';
      break;
  }
  return result;
};

export const getBorderColor = (variant: ButtonVariant) => {
  let result;

  switch (variant) {
    case 'primary':
    default:
      result = 'blue';
      break;
    case 'secondary':
      result = 'white';
      break;
  }
  return result;
};

export const getBorder = (variant: ButtonVariant, hover: boolean) => {
  let result;

  switch (variant) {
    case 'primary':
    default:
      result = 2;
      break;
    case 'secondary':
      result = 0;
      break;
  }
  return result;
};
