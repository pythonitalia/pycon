/** @jsxRuntime classic */

/** @jsx jsx */
import { FormattedMessage } from "react-intl";

import { CurrentUserQueryResult } from "~/types"
import { Box, jsx, Text } from "theme-ui";
import { Button } from "../button/button";


type Props = {
  me: CurrentUserQueryResult["data"]["me"];
  add: () => {};
  remove: () => {};
  added: boolean;
}

export const AddMembershipSubscription = ({ me, add, remove, added }: Props) => {
  const isPythonItaliaMember = me?.isPythonItaliaMember
  console.log("added", added)
  return <Box>
      {isPythonItaliaMember && <Text sx={{
            textAlign: 'center'
          }}>
            <FormattedMessage id="order.userAlreadyMember" />
          </Text>
}

{!isPythonItaliaMember && !added && <Button onClick={add}>
  <FormattedMessage id="order.addMembership" /></Button>}
{!isPythonItaliaMember && added && <Button onClick={remove}>
<FormattedMessage id="order.removeMembership" /></Button>}
  </Box>;
}
