import { Text } from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

type Props = {
  length: number;
  maxLength: number;
};

export const CharsCounter = ({ length, maxLength }: Props) =>
  maxLength ? (
    <Text size="label2" as="p" color={length >= maxLength ? "red" : "black"}>
      <FormattedMessage
        id="textarea.charsCount"
        values={{
          length,
          maxLength,
        }}
      />
    </Text>
  ) : null;
