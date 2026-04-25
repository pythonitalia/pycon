import React from "react";
import { Text } from "./text";

export default {
  title: "Text",
};

export const Primary = () => (
  <>
    <Text as="p" size={1}>
      Text Size 1 🐎
    </Text>
    <Text as="p" size={1} weight="strong">
      Text Weight Strong 1 🐙
    </Text>

    <Text as="p" size={2}>
      Text Size 2 🐈
    </Text>
    <Text as="p" size={2} weight="strong">
      Text Weight Strong 2 🐙
    </Text>

    <Text as="p" size={3}>
      Text Size 3 🐠
    </Text>
    <Text as="p" size={3} weight="strong">
      Text Weight Strong 3 🐙
    </Text>
  </>
);
