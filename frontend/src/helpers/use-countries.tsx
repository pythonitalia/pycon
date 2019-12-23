import { graphql, useStaticQuery } from "gatsby";

import { CountriesQuery } from "../generated/graphql";

const COUNTRIES_QUERY = graphql`
  query Countries {
    backend {
      countries {
        code
        name
      }
    }
  }
`;

const createOptions = (items: any[]) => [
  { label: "", value: "" },
  ...items.map(item => ({ label: item.name, value: item.id || item.code })),
];

export const useCountries = () => {
  const {
    backend: { countries },
  } = useStaticQuery<CountriesQuery>(COUNTRIES_QUERY);

  return createOptions(countries.sort((a, b) => (a.name > b.name ? 1 : -1)));
};
