import { useCountriesQuery } from "~/types";

const TOP_COUNTRIES = [
  "IT",
  "DE",
  "GB",
  "US",
  "PL",
  "CH",
  "NL",
  "BE",
  "NO",
  "FR",
];

const createOption = (item: { name: string; code: string }) => ({
  label: item.name,
  value: item.code,
  disabled: false,
});

const createOptions = (
  items: {
    name: string;
    code: string;
    disabled: boolean;
  }[],
) => [
  { label: "", value: "", disabled: true },
  ...items.slice(0, TOP_COUNTRIES.length).map(createOption),
  { label: "---------", value: "---", disabled: true },
  ...items.slice(TOP_COUNTRIES.length + 1).map(createOption),
];

export const useCountries = () => {
  const { data } = useCountriesQuery();

  if (!data) {
    return [];
  }

  const clonedCountries = [...data.countries];

  return createOptions(
    clonedCountries.sort((a, b) => {
      const aTopIndex = TOP_COUNTRIES.indexOf(a.code);
      const bTopIndex = TOP_COUNTRIES.indexOf(b.code);

      if (aTopIndex !== -1 && bTopIndex !== -1) {
        return aTopIndex - bTopIndex;
      }
      if (aTopIndex !== -1) return -1;
      if (bTopIndex !== -1) return 1;

      return a.name.localeCompare(b.name);
    }),
  );
};
