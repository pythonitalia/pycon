import {
  Page,
  Separator,
  LayoutContent,
} from "@python-italia/pycon-styleguide";
import React, { Fragment, useEffect } from "react";
import { FormattedMessage } from "react-intl";

import { HomepageHero } from "~/components/homepage-hero";
import { MetaTags } from "~/components/meta-tags";
import { useCurrentLanguage } from "~/locale/context";
import { GenericPage, useIndexPageQuery } from "~/types";

import { BlocksRenderer } from "../blocks-renderer";

type Props = {
  cycle: "day" | "night";
};

export const HomePagePageHandler = ({ cycle }: Props) => {
  const language = useCurrentLanguage();
  const {
    data: { cmsPage },
  } = useIndexPageQuery({
    variables: {
      code: process.env.conferenceCode,
      language,
    },
  });

  if (!cmsPage) {
    return null;
  }

  useEffect(() => {
    if (typeof window === "undefined") {
      return null;
    }
    const introSection = document.getElementById("homeIntroSection");
    setTimeout(() => {
      introSection.scrollIntoView({
        behavior: "smooth",
      });
    }, 5 * 1000);
  }, []);

  return (
    <Fragment>
      <FormattedMessage id="home.title">
        {(text) => <MetaTags title={text} />}
      </FormattedMessage>
      <HomepageHero cycle={cycle} />
      <LayoutContent showUntil="desktop">
        <Separator />
      </LayoutContent>

      <Page startSeparator={false}>
        <BlocksRenderer blocks={(cmsPage as GenericPage).body} />
      </Page>
    </Fragment>
  );
};
