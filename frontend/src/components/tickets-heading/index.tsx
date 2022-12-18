import { Container, Heading, Spacer } from "@python-italia/pycon-styleguide";

type Props = {
  children: React.ReactNode;
};

export const TicketsHeading = ({ children }: Props) => {
  return (
    <div>
      <Spacer size="xl" />
      <Container>
        <Heading size="display2">{children}</Heading>
      </Container>
      <Spacer size="xl" />
    </div>
  );
};
