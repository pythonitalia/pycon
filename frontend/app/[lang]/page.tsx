import { getApolloClient } from "~/apollo/sc-client";
import { BlocksRenderer } from "~/components/blocks-renderer";
import { queryIndexPage } from "~/types";

const Homepage = async ({ params: { lang } }) => {
  console.log("lang", lang);
  const client = getApolloClient();
  const { data } = await queryIndexPage(client, {
    language: "en",
    code: process.env.conferenceCode,
  });

  if (data?.cmsPage?.__typename === "SiteNotFoundError") {
    return null;
  }

  return <BlocksRenderer blocks={data?.cmsPage?.body} />;
};

export default Homepage;
