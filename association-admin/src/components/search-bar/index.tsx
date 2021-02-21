import { SearchOutline } from "heroicons-react";
import { useCallback } from "react";
import { useFormState } from "react-use-form-state";

import { useRouter } from "next/router";

import { useIsOnLogin } from "~/hooks/use-is-on-login";

import { Input, InputVariant } from "../input";

type Form = {
  query: string;
};

export const SearchBar = () => {
  const isOnLogin = useIsOnLogin();
  const { push } = useRouter();
  const [formState, { search }] = useFormState<Form>();

  const submitSearch = useCallback(
    (e: React.FormEvent) => {
      e.preventDefault();
      const query = formState.values.query;

      if (!query) {
        return;
      }

      push({
        pathname: "/dashboard/search",
        query: {
          q: formState.values.query,
        },
      });
    },
    [formState.values],
  );

  if (isOnLogin) {
    return null;
  }

  return (
    <form onSubmit={submitSearch} className="h-14">
      <Input
        icon={SearchOutline}
        type="text"
        name="search"
        id="search"
        placeholder="Search..."
        variant={InputVariant.Search}
        {...search("query")}
      />
    </form>
  );
};
