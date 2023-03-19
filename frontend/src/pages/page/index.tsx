import {
  Heading,
  Text,
  Spacer,
  Section,
  Container,
  MultiplePartsCard,
  CardPart,
} from "@python-italia/pycon-styleguide";
import { borderStyle } from "styled-system";

import Error from "next/error";
import { GetStaticProps } from "next/types";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { PageLoading } from "~/components/page-loading";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useWagtailPageQuery, TextSection as TextSectionType } from "~/types";

const TextSection = ({
  id,
  title,
  subtitle,
  body,
  illustration,
  accordions,
}: TextSectionType) => {
  return (
    <Section spacingSize="xl" illustration={illustration}>
      <Container noPadding center={false} size="small">
        <Heading size="display1">{title}</Heading>
        <Spacer size="medium" />
        <Heading size={2}> {subtitle}</Heading>
        <Text as="p" size={2} color="grey-900">
          <div dangerouslySetInnerHTML={{ __html: body }} />
        </Text>
      </Container>
      {accordions?.map((accordion) => (
        <MultiplePartsCard
          openByDefault={false}
          clickablePart="heading"
          expandTarget="content"
        >
          <CardPart contentAlign="left" id="heading">
            <Heading size={2}>{accordion.title}</Heading>
          </CardPart>
          <CardPart id="content" contentAlign="left" background="milk">
            <Text size={2}>{accordion.body}</Text>
          </CardPart>
        </MultiplePartsCard>
      ))}
    </Section>
  );
};

const COMPONENT_MAP = {
  TextSection: TextSection,
  CMSMap: TextSection,
  TextSectionWithAccordion: TextSection,
};

const CmsPage = () => {
  const { data, loading, error } = useWagtailPageQuery({
    variables: {
      hostname: process.env.conferenceCode,
      slug: "where",
      language: "en",
    },
  });
  console.log(data, loading, error);

  if (loading) {
    return <PageLoading titleId="global.loading" />;
  }

  if (!data || data.cmsPage.__typename === "SiteNotFoundError") {
    return <Error statusCode={404} />;
  }

  const { cmsPage: page } = data;

  if (!page) {
    return <Error statusCode={404} />;
  }

  return (
    <div>
      {page.body.map((block) => {
        const ReactComponent = COMPONENT_MAP[block.__typename];
        return <ReactComponent key={block.id} {...block} />;
      })}
    </div>
  );
};
export default CmsPage;

export const getStaticProps: GetStaticProps = async ({ locale, params }) => {
  const client = getApolloClient();

  await Promise.all([prefetchSharedQueries(client, locale)]);
  return addApolloState(client, {
    props: {},
  });
};
