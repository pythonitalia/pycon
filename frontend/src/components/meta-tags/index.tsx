import { graphql, useStaticQuery } from "gatsby";
import React from "react";
import { Helmet } from "react-helmet";

import { useCurrentLanguage } from "../../context/language";
import messages from "../../locale";

type Props = {
  title?: string;
  description?: string;
  imageUrl?: string;
};

export const MetaTags: React.SFC<Props> = ({
  title,
  description,
  imageUrl,
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

  const socialCard = imageUrl || `${siteMetadata.siteUrl}/social/social.png`;
  const titleTemplate = messages[language].titleTemplate;
  description = description || messages[language].description;

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
      content: socialCard,
    },
    {
      name: "twitter:title",
      content: title,
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
