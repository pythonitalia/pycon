import Head from "next/head";

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

      <main
        className="flex-1 relative z-0 overflow-y-auto focus:outline-none"
        tabIndex={0}
      >
        <PageHeader headingContent="Users" />

        <div className="mt-8 block">
          {data && <UsersTable users={data.users} />}
        </div>
      </main>
    </>
  );
};

export default Users;
