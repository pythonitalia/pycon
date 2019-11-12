/** @jsx jsx */
import { Router } from "@reach/router";
import { Box } from "@theme-ui/components";
import { jsx } from "theme-ui";

import { PrivateRoute } from "../app/private-route/private-route";
import { ProfileApp } from "../app/profile";
import { LoginForm } from "../components/login-form";
import { SignupForm } from "../components/signup-form";

export default () => (
  <Box
    sx={{
      maxWidth: "container",
      mx: "auto",
    }}
  >
    <Router>
      <PrivateRoute path="/:lang/profile" component={ProfileApp} />
      <LoginForm path="/:lang/login" />
      <SignupForm path="/:lang/signup" />
    </Router>
  </Box>
);
