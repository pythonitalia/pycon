export const getCountryLabel = (
  countries: { label: string; value: string; disabled: boolean }[],
  value: string,
): string | undefined => {
  const country = countries.find((country) => country.value === value);
  return country ? country.label : undefined;
};
