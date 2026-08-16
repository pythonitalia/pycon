import {
  CardPart,
  Grid,
  Heading,
  Link,
  MultiplePartsCard,
  Section,
  Text,
} from "@python-italia/pycon-styleguide";
import { parseISO } from "date-fns";

import { createHref } from "~/components/link";
import { queryNewsGridSection, useNewsGridSectionQuery } from "~/types";

export const NewsGridSection = () => {
  const { data } = useNewsGridSectionQuery({
    variables: {
      hostname: process.env.cmsHostname,
    },
  });

  const posts = data.newsArticles;

  return (
    <Section>
      <Grid cols={3}>
        {posts.map((post) => (
          <BlogPost key={post.id} post={post} />
        ))}
      </Grid>
    </Section>
  );
};

const BlogPost = ({ post }: { post: any }) => {
  const dateFormatter = new Intl.DateTimeFormat("en", {
    day: "2-digit",
    month: "long",
    year: "numeric",
  });

  return (
    <Link
      noLayout
      hoverColor="black"
      href={createHref({
        path: `/news/${post.slug}`,
      })}
    >
      <MultiplePartsCard>
        {post.publishedAt && (
          <CardPart
            rightSideIcon="arrow"
            rightSideIconSize="small"
            shrink={false}
            contentAlign="left"
          >
            <Text uppercase size="label3" weight="strong">
              {dateFormatter.format(parseISO(post.publishedAt))}
            </Text>
          </CardPart>
        )}
        <CardPart fullHeight background="milk" contentAlign="left">
          <Heading size={4}>{post.title}</Heading>
        </CardPart>
      </MultiplePartsCard>
    </Link>
  );
};

NewsGridSection.dataFetching = (client) => {
  return [
    queryNewsGridSection(client, {
      hostname: process.env.cmsHostname,
    }),
  ];
};
