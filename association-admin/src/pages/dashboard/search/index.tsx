import Head from "next/head";
import { useRouter } from "next/router";

import { Heading } from "~/components/heading";
import { PageHeader } from "~/components/page-header";
import { UsersTable } from "~/components/users-table";

import { useSearchQuery } from "./search.generated";

const SearchPage = () => {
  const { query } = useRouter();
  const searchQuery = query.q as string;
  const [{ fetching, data, error }] = useSearchQuery({
    variables: {
      query: searchQuery,
    },
    requestPolicy: "network-only",
  });

  return (
    <main
      className="flex-1 relative z-0 overflow-y-auto focus:outline-none"
      tabIndex={0}
    >
      <Head>
        <title>Search results</title>
      </Head>

      <PageHeader
        backTo="back"
        headingContent={`Search results for ${searchQuery}`}
      />

      {fetching && <div>Show loading</div>}

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
    </main>
  );
};

export default SearchPage;
