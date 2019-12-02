/** @jsx jsx */
import { Box } from "@theme-ui/components";
import { graphql } from "gatsby";
import { Fragment } from "react";
import { Helmet } from "react-helmet";
import { jsx } from "theme-ui";

import { Article } from "../../components/article";
import { PostQuery } from "../../generated/graphql";
import { compile } from "../../helpers/markdown";

type Props = {
  data: PostQuery;
  pageContext: {
    socialCard: string;
  };
};

export default ({ data, ...props }: Props) => {
  const post = data.backend.blogPost!;
  const socialCard = `${data.site!.siteMetadata!.siteUrl}${
    props.pageContext.socialCard
  }`;

  return (
    <Fragment>
      <Helmet
        meta={[
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
        ]}
      >
        <title>{post.title}</title>
      </Helmet>

      <Box sx={{ mx: "auto", px: 3, pt: 4, maxWidth: "container" }}>
        <Article
          hero={post.imageFile && { ...post.imageFile.childImageSharp! }}
          title={post.title}
        >
          {compile(post.content).tree}
        </Article>
      </Box>
    </Fragment>
  );
};

export const query = graphql`
  query Post($slug: String!, $language: String!) {
    site {
      siteMetadata {
        siteUrl
      }
    }

    backend {
      blogPost(slug: $slug) {
        title(language: $language)
        content(language: $language)
        excerpt(language: $language)
        image

        imageFile {
          childImageSharp {
            fluid(maxWidth: 1600) {
              ...GatsbyImageSharpFluid
            }
          }
        }
      }
    }
  }
`;
