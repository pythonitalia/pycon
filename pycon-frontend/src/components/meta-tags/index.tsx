import Head from "next/head";
import React from "react";

import { useCurrentUrl } from "~/helpers/use-url";
import messages from "~/locale";
import { useCurrentLanguage } from "~/locale/context";

type Props = {
  title?: React.ReactNode | string | null;
  description?: string;
  useDefaultSocialCard?: boolean;
};

export const MetaTags: React.SFC<Props> = ({
  title,
  description,
  useDefaultSocialCard = true,
  children,
}) => {
  const language = useCurrentLanguage();
  const { host, path } = useCurrentUrl();
  const socialCard = useDefaultSocialCard
    ? `${host}/api/social/en`
    : `${host}/api/social${path}`;

  const titleTemplate = messages[language].titleTemplate;

  description = description || messages[language].description;

  const titleContent = titleTemplate.replace(
    "%s",
    title ? title.toString() : "",
  );

  return (
    <Head>
      <title>{titleTemplate.replace("%s", title.toString())}</title>

      <meta name="title" content={titleContent} />
      <meta name="description" content={description} />

      <meta property="og:type" content="website" />
      <meta property="og:title" content={titleContent} />
      <meta property="og:description" content={description} />
      <meta property="og:image" content={socialCard} />

      <meta property="twitter:card" content="summary_large_image" />
      <meta property="twitter:title" content={titleContent} />
      <meta property="twitter:description" content={description} />
      <meta property="twitter:image" content={socialCard} />

      {children}
    </Head>
  );
};
