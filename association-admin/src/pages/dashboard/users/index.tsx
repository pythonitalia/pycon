import Head from "next/head";

import { DashboardPageWrapper } from "~/components/dashboard-page-wrapper";
import { Loading } from "~/components/loading";
import { PageHeader } from "~/components/page-header";
import { UsersTable } from "~/components/users-table";

import { useUsersQuery } from "./users.generated";

const Users = () => {
  const [{ fetching, error, data }] = useUsersQuery();

  return (
    <>
      <Head>
        <title>Users</title>
      </Head>

      <DashboardPageWrapper>
        <PageHeader headingContent="Users" />

        <div className="mt-8 block">
          {fetching && <Loading />}
          {data && <UsersTable users={data.users} />}
        </div>
      </DashboardPageWrapper>
    </>
  );
};

export default Users;
