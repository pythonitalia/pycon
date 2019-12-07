/** @jsx jsx */
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { MySubmissions } from "../../app/profile/my-submissions";
import { MetaTags } from "../meta-tags";
import { Cfp } from "./cfp";
import { Introduction } from "./introduction";

export const CFPPage = () => (
  <Fragment>
    <FormattedMessage id="cfp.pageTitle">
      {text => <MetaTags title={text} />}
    </FormattedMessage>

    <Introduction />

    <MySubmissions />

    <Cfp />
  </Fragment>
);
