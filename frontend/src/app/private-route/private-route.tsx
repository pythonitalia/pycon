import { useLoginState } from "../profile/hooks";
import React, { Component } from "react"
import { Redirect } from "@reach/router";


export const PrivateRoute = ({component: Component, lang, ...rest}: any) => {
  const [loggedIn, _] = useLoginState(false);
  const loginUrl = `${lang}/login`;

  if (!loggedIn) {
    return <Redirect to={loginUrl} noThrow={true} />;
  }

  return <Component {...rest} />
};