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
import { queryBlogIndex, useBlogIndexQuery } from "~/types";

export const NewsGridSection = () => {
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
    <Section>
      <Grid cols={3}>
        {posts.map((post) => (
          <Link
            noLayout
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
              <CardPart fullHeight background="milk" contentAlign="left">
                <Heading size={4}>{post.title}</Heading>
              </CardPart>
            </MultiplePartsCard>
          </Link>
        ))}
      </Grid>
    </Section>
  );
};

NewsGridSection.dataFetching = (client, language) => {
  return [
    queryBlogIndex(client, {
      language,
    }),
  ];
};
