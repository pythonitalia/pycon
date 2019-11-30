import { Location, Redirect } from "@reach/router";
import React from "react";

import { useLoginState } from "../profile/hooks";

export const PrivateRoute = ({
  component: PrivateComponent,
  lang,
  ...rest
}: any) => {
  const [loggedIn, _] = useLoginState();
  const loginUrl = `${lang}/login`;

  if (!loggedIn) {
    return (
      <Location>
        {({ location }) => (
          <Redirect
            to={loginUrl}
            noThrow={true}
            state={{ next: location.pathname }}
          />
        )}
      </Location>
    );
  }

  return <PrivateComponent lang={lang} {...rest} />;
};
