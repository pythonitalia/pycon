import {
  Heading,
  Text,
  Section,
  MultiplePartsCard,
  CardPart,
  Link,
  Grid,
} from "@python-italia/pycon-styleguide";
import { parseISO } from "date-fns";

import { createHref } from "~/components/link";
import { useCurrentLanguage } from "~/locale/context";
import { queryNewsGridSection, useNewsGridSectionQuery } from "~/types";

export const NewsGridSection = () => {
  const language = useCurrentLanguage();

  const { data } = useNewsGridSectionQuery({
    variables: {
      language,
      code: process.env.conferenceCode,
    },
  });

  const posts = data.newsArticles;

  return (
    <Section>
      <Grid cols={3}>
        {posts.map((post) => (
          <BlogPost key={post.id} post={post} language={language} />
        ))}
      </Grid>
    </Section>
  );
};

const BlogPost = ({ post, language }: { post: any; language: string }) => {
  const dateFormatter = new Intl.DateTimeFormat(language, {
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
            {dateFormatter.format(parseISO(post.published || post.publishedAt))}
          </Text>
        </CardPart>
        <CardPart fullHeight background="milk" contentAlign="left">
          <Heading size={4}>{post.title}</Heading>
        </CardPart>
      </MultiplePartsCard>
    </Link>
  );
};

NewsGridSection.dataFetching = (client, language) => {
  return [
    queryNewsGridSection(client, {
      code: process.env.conferenceCode,
      language,
    }),
  ];
};
