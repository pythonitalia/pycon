export const getBackgroundColor = (hover: boolean) => {
  let result;
  hover ? (result = 'white') : (result = 'blue');
  return result;
};
