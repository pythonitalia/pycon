import { queryPage } from "~/types";

const Page = async ({ params }) => {
  const slug = params.slug as string;
  const language = "en";

  const { data } = await queryPage({
    code: process.env.conferenceCode,
    language,
    slug,
  });

  console.log("data!", data);

  return <div>page</div>;
};

export default Page;
