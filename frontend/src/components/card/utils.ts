export const getBackgroundColor = (hover: boolean) => {
  let result;
  hover ? (result = 'white') : (result = 'blue');
  return result;
};

export const getColor = (hover: boolean) => {
  let result;
  hover ? (result = 'white') : (result = 'white');
  return result;
};
