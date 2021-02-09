import Head from "next/head";

import { Heading } from "~/components/heading";
import { Pill } from "~/components/pill";
import { Table } from "~/components/table";
import { User } from "~/helpers/types";

import { useUsersQuery } from "./users.generated";

const Users = () => {
  const [{ fetching, error, data }] = useUsersQuery();

  return (
    <>
      <Head>
        <title>Users</title>
      </Head>

      <div className="flex flex-col w-0 flex-1 overflow-hidden">
        <main
          className="flex-1 relative z-0 overflow-y-auto focus:outline-none"
          tabIndex={0}
        >
          <div className="border-b border-gray-200 px-6 py-4">
            <div className="flex-1 min-w-0">
              <Heading>Users</Heading>
            </div>
          </div>

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
                  "false",
                  item.isActive ? null : (
                    <Pill variant="warning">Not active</Pill>
                  ),
                ]}
                data={data.users}
                headers={["Email", "Name", "Is Associated?", ""]}
              />
            )}
          </div>
        </main>
      </div>
    </>
  );
};

export default Users;
