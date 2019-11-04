import { graphql } from "gatsby";
import marksy from "marksy";
import React, { createElement } from "react";

import { Article } from "../components/article";
import { PageQuery } from "../generated/graphql";

const compile = marksy({
  createElement,
});

export default ({ data }: { data: PageQuery }) => {
  const page = data.backend.page!;

  return (
    <Article
      hero={page.imageFile && { ...page.imageFile.childImageSharp! }}
      title={page.title}
    >
      {compile(page.content).tree}
    </Article>
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
