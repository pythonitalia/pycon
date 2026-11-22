import { Text } from "@radix-ui/themes";

export const SectionLabel = ({
  children,
  inline = false,
}: {
  children: React.ReactNode;
  inline?: boolean;
}) => (
  <Text
    as={inline ? "span" : "p"}
    size="1"
    weight="bold"
    color="gray"
    mb={inline ? undefined : "1"}
    className="uppercase tracking-wider"
  >
    {children}
  </Text>
);

export const Disclosure = ({
  summary,
  children,
}: {
  summary: React.ReactNode;
  children: React.ReactNode;
}) => (
  <details className="group">
    <summary className="flex cursor-pointer list-none items-center gap-2 [&::-webkit-details-marker]:hidden">
      <span
        aria-hidden
        className="text-[var(--gray-11)] transition-transform group-open:rotate-90"
      >
        ▸
      </span>
      <div className="min-w-0 flex-1">{summary}</div>
    </summary>
    {children}
  </details>
);
