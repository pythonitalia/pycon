import Head from "next/head";

import { DashboardPageWrapper } from "~/components/dashboard-page-wrapper";
import { Heading } from "~/components/heading";
import { PageHeader } from "~/components/page-header";
import { Table } from "~/components/table";
import { UserPills } from "~/components/user-pills";
import { UsersTable } from "~/components/users-table";
import { User } from "~/helpers/types";

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
          {data && <UsersTable users={data.users} />}
        </div>
      </DashboardPageWrapper>
    </>
  );
};

export default Users;
