import { Redirect } from "@reach/router";
import React, { Component } from "react";

import { useLoginState } from "../profile/hooks";

export const PrivateRoute = ({
  component: PrivateComponent,
  lang,
  ...rest
}: any) => {
  const [loggedIn, _] = useLoginState();
  const loginUrl = `${lang}/login`;

  if (!loggedIn) {
    return <Redirect to={loginUrl} noThrow={true} />;
  }

  return <PrivateComponent lang={lang} {...rest} />;
};
