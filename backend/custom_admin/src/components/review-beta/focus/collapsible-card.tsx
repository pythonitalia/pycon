import { Card, Flex } from "@radix-ui/themes";
import { Disclosure } from "./section";
import { useIsWide } from "./use-is-wide";

type Props = {
  summary: React.ReactNode;
  children: React.ReactNode;
};

export const CollapsibleCard = ({ summary, children }: Props) => {
  const isWide = useIsWide();

  if (isWide) {
    return (
      <Card>
        <Flex direction="column" gap="3">
          {summary}
          {children}
        </Flex>
      </Card>
    );
  }

  return (
    <Card>
      <Disclosure summary={summary}>
        <Flex direction="column" gap="3" mt="3">
          {children}
        </Flex>
      </Disclosure>
    </Card>
  );
};
