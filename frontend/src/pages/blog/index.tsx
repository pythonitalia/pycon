import {
  Heading,
  Text,
  Page,
  Section,
  MultiplePartsCard,
  CardPart,
  Link,
  Grid,
} from "@python-italia/pycon-styleguide";
import { parseISO } from "date-fns";
import { FormattedMessage } from "react-intl";

import { GetStaticProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { createHref } from "~/components/link";
import { MetaTags } from "~/components/meta-tags";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useCurrentLanguage } from "~/locale/context";
import { queryBlogIndex, useBlogIndexQuery } from "~/types";

export const BlogPage = () => {
  const language = useCurrentLanguage();
  const dateFormatter = new Intl.DateTimeFormat(language, {
    day: "2-digit",
    month: "long",
    year: "numeric",
  });

  const { data } = useBlogIndexQuery({
    variables: {
      language,
    },
  });

  const posts = data.blogPosts;

  return (
    <Page endSeparator={false}>
      <FormattedMessage id="blog.title">
        {(text) => <MetaTags title={text} />}
      </FormattedMessage>

      <Section>
        <Heading size="display1">Blog</Heading>
      </Section>
      <Section>
        <Grid cols={3}>
          {posts.map((post) => (
            <Link
              hoverColor="black"
              href={createHref({
                path: `/blog/${post.slug}`,
                locale: language,
              })}
            >
              <MultiplePartsCard>
                <CardPart
                  rightSideIcon="arrow"
                  rightSideIconSize="small"
                  shrink={false}
                  contentAlign="left"
                >
                  <Text uppercase size="label3" weight="strong">
                    {dateFormatter.format(parseISO(post.published))}
                  </Text>
                </CardPart>
                <CardPart fullHeight noBg contentAlign="left">
                  <Heading size={4}>{post.title}</Heading>
                </CardPart>
              </MultiplePartsCard>
            </Link>
          ))}
        </Grid>
      </Section>
    </Page>
  );
};

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await Promise.all([
    prefetchSharedQueries(client, locale),
    queryBlogIndex(client, {
      language: locale,
    }),
  ]);

  return addApolloState(client, {
    props: {},
  });
};

export default BlogPage;
