import { Router } from "@reach/router";
import * as React from "react";

import { ProfileApp } from "../app/profile";
import { LoginForm } from "../components/login-form";
import { SignupForm } from "../components/signup-form";

export default () => (
  <Router>
    <ProfileApp path="/:lang/profile" />
    <LoginForm path="/:lang/login" />
    <SignupForm path="/:lang/signup" />
  </Router>
);
