import { Table, Pagination } from "~/components/table";
import { UserPills } from "~/components/user-pills";

import { UserDataForTableFragment } from "./user-table.generated";

type Props = {
  users: UserDataForTableFragment[];
  pagination?: Pagination;
};

export const UsersTable: React.FC<Props> = ({ users, pagination }) => (
  <Table<UserDataForTableFragment>
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
    data={users}
    headers={["Email", "Name", "Roles"]}
    pagination={pagination}
  />
);
