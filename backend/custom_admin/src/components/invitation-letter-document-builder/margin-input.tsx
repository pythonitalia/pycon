import { Flex, Grid, Text, TextField } from "@radix-ui/themes";

export const MarginInput = ({ value, onChange }) => {
  const margins = value?.split(" ") || ["", "", "", ""];

  const onChangeMargin = (
    index: number,
    e: React.ChangeEvent<HTMLInputElement>,
  ) => {
    const newValue = margins.slice();
    newValue[index] = e.target.value;
    onChange(newValue.join(" "));
  };

  const onKeyDownMargin = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.code === "Space") {
      event.preventDefault();
    }
  };

  return (
    <Flex gap="1" direction="column" justify="center">
      <Text as="label" size="2">
        Margin
      </Text>
      <Grid columns="repeat(4, 60px)" gap="2">
        {["top", "right", "bottom", "left"].map((label, i) => (
          <TextField.Root
            onKeyDown={onKeyDownMargin}
            key={i}
            value={margins[i] || ""}
            onChange={(e) => onChangeMargin(i, e)}
            placeholder={label}
          />
        ))}
      </Grid>
    </Flex>
  );
};
