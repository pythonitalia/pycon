import { Heading } from "~/components/heading";
import { Table } from "~/components/table";

const Users = () => (
  <>
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
          <Table
            clickableItem={(item) => ({
              pathname: "/dashboard/users/[userid]",
              query: { userid: 1 },
            })}
            keyGetter={(item) => item[0]}
            rowGetter={(item) => ["marco@test.it", "Marco Acierno", "true"]}
            data={[{}, {}, {}]}
            headers={["Email", "Fullname", "Is Associated?"]}
          />
        </div>
      </main>
    </div>
  </>
);

export default Users;
