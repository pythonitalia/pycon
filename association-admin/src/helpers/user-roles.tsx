import { Pill } from "~/components/pill";

import { Credential, User } from "./types";

export const getUserRolesAsPills = (user: User) => {
  const pills = [];

  if (!user.isActive) {
    pills.push(
      <Pill key="is-not-active" variant="warning">
        Not active
      </Pill>,
    );
  }

  if (user.credentials.includes(Credential.Staff)) {
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

  return pills;
};
