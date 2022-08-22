import { FormattedMessage } from "react-intl";
import { Text } from "theme-ui";

type Props = {
  length: number;
  maxLength: number;
};

export const CharsCounter = ({ length, maxLength }: Props) =>
  maxLength ? (
    <Text
      variant="labelDescription"
      as="p"
      color={length >= maxLength ? "red" : "black"}
    >
      <FormattedMessage
        id="textarea.charsCount"
        values={{
          length,
          maxLength,
        }}
      />
    </Text>
  ) : null;
