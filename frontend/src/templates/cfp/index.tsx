/** @jsx jsx */
import { Fragment } from "react";
import { jsx } from "theme-ui";

import { CfpForm } from "../../components/cfp-form";

type Props = {
  pageContext: { language: string };
};

export default ({ pageContext }: Props) => (
  <Fragment>
    <CfpForm />
  </Fragment>
);
