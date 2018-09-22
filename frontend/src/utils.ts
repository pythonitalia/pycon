/**
 * Generates an array with numbers starting at `start` and ending at `end - 1`
 */
export const range = (start: number, end: number) => {
  return Array.from(Array(end - start).keys()).map(i => i + start);
};
