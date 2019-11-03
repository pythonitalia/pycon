import { Router } from "@reach/router";
import React from "react";

import { PrivateRoute } from "../app/private-route/private-route";
import { ProfileApp } from "../app/profile";
import { LoginForm } from "../components/login-form";
import { SignupForm } from "../components/signup-form";

export default () => (
  <Router>
    <PrivateRoute path="/:lang/profile" component={ProfileApp} />
    <LoginForm path="/:lang/login" />
    <SignupForm path="/:lang/signup" />
  </Router>
);
