/** @jsxRuntime classic */

/** @jsx jsx */
import { Flex, Input, jsx } from "theme-ui";

import { Button } from "../button/button";

export const AddRemoveProduct = ({
  quantity,
  increase,
  decrease,
}: {
  quantity: number;
  decrease: () => void;
  increase: () => void;
}) => (
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
