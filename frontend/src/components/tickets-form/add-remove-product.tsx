/** @jsx jsx */
import { Flex, Input } from "@theme-ui/components";
import { jsx } from "theme-ui";

import { Button } from "../button/button";

export const AddRemoveProduct: React.SFC<{
  quantity: number;
  decrease: () => void;
  increase: () => void;
}> = ({ quantity, increase, decrease }) => (
  <Flex sx={{ justifyContent: "space-between" }}>
    <Button onClick={decrease} variant="minus">
      -
    </Button>
    <Input
      defaultValue={0}
      value={quantity}
      min={0}
      disabled={true}
      sx={{
        width: [100, 50],
        height: 50,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        p: 0,
      }}
    />
    <Button onClick={increase} variant="plus">
      +
    </Button>
  </Flex>
);
