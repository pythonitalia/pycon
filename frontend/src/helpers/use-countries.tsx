import { useCountriesQuery } from "~/types";

const createOptions = (
  items: {
    name: string;
    code: string;
  }[],
) => [
  { label: "", value: "" },
  ...items.map((item) => ({ label: item.name, value: item.code })),
];

export const useCountries = () => {
  const { data } = useCountriesQuery();

  if (!data) {
    return [];
  }

  return createOptions(
    data.countries.sort((a, b) => (a.name > b.name ? 1 : -1)),
  );
};
