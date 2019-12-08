/** @jsx jsx */
import { Router } from "@reach/router";
import { Box, Button, Checkbox, Input, Label } from "@theme-ui/components";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { InputWrapper } from "../input-wrapper";

export const HotelForm = () => {
  const x = 1;

  return (
    <Box>
      <InputWrapper
        errors={["error"]}
        isRequired={true}
        label={
          <FormattedMessage id="profile.name">
            {msg => <b>{msg}</b>}
          </FormattedMessage>
        }
      >
        <Input type="number" />
      </InputWrapper>
    </Box>
  );
};
