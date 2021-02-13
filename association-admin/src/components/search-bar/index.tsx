import { SearchOutline } from "heroicons-react";

import { useIsOnLogin } from "~/hooks/use-is-on-login";

import { Input, Variant } from "../input";

export const SearchBar = () => {
  const isOnLogin = useIsOnLogin();

  if (isOnLogin) {
    return null;
  }

  return (
    <div className="h-14">
      <Input
        icon={SearchOutline}
        type="text"
        name="search"
        id="search"
        placeholder="Search..."
        variant={Variant.Search}
      />
    </div>
  );
};
