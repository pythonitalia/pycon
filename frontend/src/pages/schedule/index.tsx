import Head from "next/head";
import { useRouter } from "next/router";

export const SchedulePage = () => {
  const { replace } = useRouter();

  // TODO Replace with _middleware
  if (typeof window !== "undefined") {
    replace("/schedule/2022-06-02");
  }
  return (
    <Head>
      <meta name="robots" content="noindex, nofollow" />
    </Head>
  );
};

export default SchedulePage;
