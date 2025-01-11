import { Flex, RadioGroup, Text } from "@radix-ui/themes";

export const AlignOptions = ({ value, onChange, position }) => {
  return (
    <Flex gap="1" direction="column" justify="center">
      <Text as="label" size="2">
        Align
      </Text>
      <RadioGroup.Root
        onValueChange={onChange}
        value={value}
        defaultValue={`${position}-left`}
      >
        <Flex align="center" gap="2">
          <RadioGroup.Item value={`${position}-left`}>
            {position}-left
          </RadioGroup.Item>
          <RadioGroup.Item value={`${position}-center`}>
            {position}-center
          </RadioGroup.Item>
          <RadioGroup.Item value={`${position}-right`}>
            {position}-right
          </RadioGroup.Item>
        </Flex>
      </RadioGroup.Root>
    </Flex>
  );
};
