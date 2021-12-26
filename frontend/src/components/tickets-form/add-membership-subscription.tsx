/** @jsxRuntime classic */

/** @jsx jsx */
import { FormattedMessage } from "react-intl";
import { Box, jsx, Text } from "theme-ui";

import { CurrentUserQueryResult } from "~/types";

import { Button } from "../button/button";
import { useLoginState } from "../profile/hooks";

type Props = {
  me: CurrentUserQueryResult["data"]["me"];
  add: () => void;
  remove: () => void;
  added: boolean;
};

export const AddMembershipSubscription = ({
  me,
  add,
  remove,
  added,
}: Props) => {
  const [isLoggedIn] = useLoginState();

  const isPythonItaliaMember = me?.isPythonItaliaMember ?? false;
  const showAddRemoveButton = isLoggedIn ? !!me && !isPythonItaliaMember : true;

  return (
    <Box>
      {isLoggedIn && !me && (
        <Text
          sx={{
            textAlign: "center",
          }}
        >
          <FormattedMessage id="global.loading" />
        </Text>
      )}
      {isPythonItaliaMember && (
        <Text
          sx={{
            textAlign: "center",
          }}
        >
          <FormattedMessage id="order.userAlreadyMember" />
        </Text>
      )}

      {showAddRemoveButton && !added && (
        <Button onClick={add}>
          <FormattedMessage id="order.addMembership" />
        </Button>
      )}
      {showAddRemoveButton && added && (
        <Button onClick={remove}>
          <FormattedMessage id="order.removeMembership" />
        </Button>
      )}
    </Box>
  );
};
