import { Box } from "@radix-ui/themes";

export const Spacer = ({
  size = 3,
}: {
  size?: number;
}) => <Box height={`var(--space-${size})`} />;
