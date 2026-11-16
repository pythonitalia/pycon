import { Heading, Text } from "@radix-ui/themes";
import { useArgs } from "../shared/args";
import { Base } from "../shared/base";
import { DjangoAdminLayout } from "../shared/django-admin-layout";
import { useAdminTheme } from "../shared/use-admin-theme";
import { ReviewBetaNav } from "./nav";
import type { Screen } from "./types";

type Props = {
  args: Record<string, any>;
  children: React.ReactNode;
};

export const ReviewBetaLayout = ({ args, children }: Props) => {
  const appearance = useAdminTheme();

  return (
    <Base appearance={appearance} args={args}>
      <DjangoAdminLayout>
        <ReviewBetaNav />
        {children}
      </DjangoAdminLayout>
    </Base>
  );
};

export const ScreenPlaceholder = () => {
  const { screens, screen: currentScreen } = useArgs() as {
    screens: Screen[];
    screen: string;
  };
  const screen = screens.find((item) => item.id === currentScreen);

  return (
    <div>
      <Heading as="h2" size="5" mb="2">
        {screen?.title}
      </Heading>
      <Text color="gray">Coming soon.</Text>
    </div>
  );
};
