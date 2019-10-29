import { useLoginState } from "../profile/hooks";
import React, { Component } from "react"
import { Redirect } from "@reach/router";


export const PrivateRoute = ({component: Component, location, lang, ...rest}: any) => {
  const [loggedIn, _] = useLoginState(false);
  const loginUrl = `${lang}/login`;

  if (!loggedIn && !location.pathname.includes("login")) {
    return <Redirect to={loginUrl} noThrow={true} />;
  }

  return <Component {...rest} />
};