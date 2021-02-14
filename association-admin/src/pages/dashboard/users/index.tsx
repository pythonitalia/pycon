import Head from "next/head";

import { DashboardPageWrapper } from "~/components/dashboard-page-wrapper";
import { Loading } from "~/components/loading";
import { PageHeader } from "~/components/page-header";
import { UsersTable } from "~/components/users-table";
import { usePagination } from "~/hooks/use-pagination";

import { useUsersQuery } from "./users.generated";

const Users = () => {
  const { to, after, goNext, goBack } = usePagination();
  const [{ fetching, error, data }] = useUsersQuery({
    variables: {
      to,
      after,
    },
  });

  return (
    <>
      <Head>
        <title>Users</title>
      </Head>

      <DashboardPageWrapper>
        <PageHeader headingContent="Users" />

        <div className="mt-8 block">
          {data && (
            <UsersTable
              pagination={{
                totalCount: data.users.pageInfo.totalCount,
                after,
                to,
                hasMore: data.users.pageInfo.hasMore,
                goNext,
                goBack,
              }}
              users={data.users.items}
            />
          )}
        </div>
      </DashboardPageWrapper>
    </>
  );
};

export default Users;
