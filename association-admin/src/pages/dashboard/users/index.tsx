import Head from "next/head";

import { Heading } from "~/components/heading";
import { PageHeader } from "~/components/page-header";
import { Table } from "~/components/table";
import { UserPills } from "~/components/user-pills";
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
          {data && (
            <Table<User>
              clickableItem={(item) => ({
                pathname: "/dashboard/users/[userid]",
                query: { userid: item.id },
              })}
              keyGetter={(item) => `${item.id}`}
              rowGetter={(item) => [
                item.email,
                item.fullname || item.name || "No name",
                <div className="-ml-2">
                  <UserPills user={item} />
                </div>,
              ]}
              data={data.users}
              headers={["Email", "Name", "Roles"]}
            />
          )}
        </div>
      </main>
    </>
  );
};

export default Users;
