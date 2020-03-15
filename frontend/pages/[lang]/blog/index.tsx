/** @jsx jsx */
import { Box, Heading, Text } from "@theme-ui/components";
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { Link } from "~/components/link";
import { MetaTags } from "~/components/meta-tags";
import { useCurrentLanguage } from "~/locale/context";
import { useBlogIndexQuery } from "~/types";

export default () => {
  const language = useCurrentLanguage();

  const { data, loading, error } = useBlogIndexQuery({
    variables: {
      language,
    },
  });

  if (!data) {
    return null;
  }

  const posts = data.blogPosts;

  return (
    <Fragment>
      <MetaTags title="Blog" />

      <Box sx={{ mx: "auto", px: 3, pt: 4, maxWidth: "container" }}>
        {posts.map((post) => (
          <Box as="article" key={post.slug} sx={{ mb: 4, maxWidth: "600px" }}>
            <Heading sx={{ mb: 2 }}>
              <Link
                variant="heading"
                path={`/[lang]/blog/[slug]`}
                params={{ slug: post.slug }}
              >
                {post.title}
              </Link>
            </Heading>

            <Text sx={{ mb: 2 }}>{post.excerpt}</Text>

            <Link path={`/[lang]/blog/[slug]`} params={{ slug: post.slug }}>
              <FormattedMessage id="blog.readMore" />
            </Link>
          </Box>
        ))}
      </Box>
    </Fragment>
  );
};
