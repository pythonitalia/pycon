import { Heading, Page, Section } from "@python-italia/pycon-styleguide";
import React from "react";
import { FormattedMessage } from "react-intl";

import { MetaTags } from "../meta-tags";

export const PageLoading = ({ titleId }: { titleId: string }) => (
  <Page>
    <Section>
      <FormattedMessage id={titleId}>
        {(text) => <MetaTags title={text} />}
      </FormattedMessage>

      <Heading>
        <FormattedMessage id="tickets.loading" />
      </Heading>
    </Section>
  </Page>
);
