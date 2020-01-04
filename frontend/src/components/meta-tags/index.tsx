import { graphql, useStaticQuery } from "gatsby";
import React from "react";
import { Helmet } from "react-helmet";

import { useCurrentLanguage } from "../../context/language";
import messages from "../../locale";

type Props = {
  title?: React.ReactNode | string | null;
  description?: string;
  imageUrl?: string;
  twitterImageUrl?: string;
};

export const MetaTags: React.SFC<Props> = ({
  title,
  description,
  imageUrl,
  twitterImageUrl,
  children,
}) => {
  const {
    site: { siteMetadata },
  } = useStaticQuery(graphql`
    {
      site {
        siteMetadata {
          siteUrl
        }
      }
    }
  `);

  const language = useCurrentLanguage();

  let socialCard = imageUrl || `/social/social.png`;
  let socialCardTwitter = twitterImageUrl || `/social-twitter/social.png`;
  const titleTemplate = messages[language].titleTemplate;
  description = description || messages[language].description;

  if (!socialCard.startsWith("http")) {
    socialCard = `${siteMetadata.siteUrl}${socialCard}`;
  }
  if (!socialCardTwitter.startsWith("http")) {
    socialCardTwitter = `${siteMetadata.siteUrl}${socialCard}`;
  }

  const meta = [
    {
      name: "twitter:card",
      content: "summary_large_image",
    },
    {
      property: "og:image",
      content: socialCard,
    },
    {
      name: "twitter:image",
      content: socialCardTwitter,
    },
    {
      name: "twitter:title",
      content: title as string,
    },
    {
      name: "twitter:description",
      content: description,
    },
  ];

  return (
    <Helmet titleTemplate={titleTemplate} meta={meta}>
      {title && <title>{title}</title>}

      {children}
    </Helmet>
  );
};
