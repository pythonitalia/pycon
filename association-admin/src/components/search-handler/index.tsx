import Head from "next/head";
import { useRouter } from "next/router";

import { DashboardPageWrapper } from "~/components/dashboard-page-wrapper";
import { Heading } from "~/components/heading";
import { Loading } from "~/components/loading";
import { PageHeader } from "~/components/page-header";
import { UsersTable } from "~/components/users-table";

import { useSearchQuery } from "./search.generated";

export const SearchHandler = () => {
  const { query } = useRouter();
  const searchQuery = query.q as string;
  const [{ fetching, data, error }] = useSearchQuery({
    variables: {
      query: searchQuery,
    },
    requestPolicy: "network-only",
  });

  return (
    <DashboardPageWrapper>
      <Head>
        <title>Search results</title>
      </Head>

      <PageHeader
        backTo="back"
        headingContent={`Search results for ${searchQuery}`}
      />

      {fetching && <Loading />}

      {!fetching && data.search.users && (
        <div className="my-4">
          <Heading className="mb-2 px-6">Users</Heading>
          {data.search.users.length > 0 ? (
            <UsersTable users={data.search.users} />
          ) : (
            <div className="-mt-3 px-6">No users found</div>
          )}
        </div>
      )}
    </DashboardPageWrapper>
  );
};
