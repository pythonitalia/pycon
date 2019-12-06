/** @jsx jsx */
import { Box } from "@theme-ui/components";
import { graphql } from "gatsby";
import { Fragment } from "react";
import { jsx } from "theme-ui";

import { Article } from "../components/article";
import { MetaTags } from "../components/meta-tags";
import { PageQuery } from "../generated/graphql";
import { compile } from "../helpers/markdown";

export default ({ data }: { data: PageQuery }) => {
  const page = data.backend.page!;

  return (
    <Fragment>
      <MetaTags title={page.title} />

      <Box sx={{ mx: "auto", px: 3, maxWidth: "container" }}>
        <Article
          hero={page.imageFile && { ...page.imageFile.childImageSharp! }}
          title={page.title}
        >
          {compile(page.content).tree}
        </Article>
      </Box>
    </Fragment>
  );
};

export const query = graphql`
  query Page($slug: String!, $language: String!) {
    backend {
      page(slug: $slug) {
        title(language: $language)
        content(language: $language)
        image

        imageFile {
          childImageSharp {
            fluid(
              maxWidth: 1600
              maxHeight: 700
              fit: COVER
              cropFocus: ATTENTION
              duotone: { highlight: "#000000", shadow: "#000000", opacity: 20 }
            ) {
              ...GatsbyImageSharpFluid
            }
          }
        }
      }
    }
  }
`;
