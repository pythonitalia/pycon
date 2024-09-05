import { Text } from "@python-italia/pycon-styleguide";

export const Title = ({ children }: { children: React.ReactNode }) => (
  <Text size="label3" uppercase weight="strong">
    {children}
  </Text>
);
