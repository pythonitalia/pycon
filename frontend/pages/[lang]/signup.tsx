import { Fragment } from "react";

import { MetaTags } from "~/components/meta-tags";
import { SignupForm } from "~/components/signup-form";

export const SignupPage = () => (
  <Fragment>
    <MetaTags title={"Signup"} />

    <SignupForm />
  </Fragment>
);

export default SignupPage;
