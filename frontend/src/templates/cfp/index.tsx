/** @jsx jsx */
import { Fragment } from "react";
import { jsx } from "theme-ui";

import { CfpForm } from "../../components/cfp-form";
import { Introduction } from "./introduction";

type Props = {
  pageContext: { language: string };
};

export default ({ pageContext }: Props) => (
  <Fragment>
    <Introduction />
    <CfpForm />
  </Fragment>
);
