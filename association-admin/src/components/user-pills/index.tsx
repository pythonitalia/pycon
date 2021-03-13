import { Pill } from "~/components/pill";
import { Credential, User } from "~/helpers/types";

import { UserDataForTableFragment } from "../users-table/user-table.generated";

type Props = {
  user: UserDataForTableFragment;
};

export const UserPills: React.FC<Props> = ({ user }) => {
  const pills = [];

  if (!user.isActive) {
    pills.push(
      <Pill key="is-not-active" variant="warning">
        Not active
      </Pill>,
    );
  }

  if (user.isStaff) {
    pills.push(
      <Pill key="is-staff" variant="success">
        Staff
      </Pill>,
    );
  }

  if (true) {
    pills.push(
      <Pill key="is-associated" variant="success">
        Associated
      </Pill>,
    );
  }

  return <>{pills}</>;
};
