import { Box, Button, Flex, Heading, Separator, Text } from "@radix-ui/themes";
import type { ReviewProposalFragmentFragment } from "./focus-mode.generated";
import { ProposalFacts } from "./proposal-facts";
import { Disclosure, SectionLabel } from "./section";

type Props = { proposal: ReviewProposalFragmentFragment };

export const ProposalPanel = ({ proposal }: Props) => {
  const languageVersions = (["en", "it"] as const).filter(
    (code) => proposal.title[code] !== null,
  );

  return (
    <Flex direction="column" gap="4">
      <ProposalFacts proposal={proposal} />

      {languageVersions.map((code, index) => (
        <Flex direction="column" gap="3" key={code}>
          {index > 0 && <Separator size="4" />}
          {languageVersions.length > 1 && (
            <Text size="1" color="gray" weight="bold">
              {code === "en" ? "ENGLISH" : "ITALIANO"}
            </Text>
          )}
          <Flex justify="between" align="start" gap="3">
            <Heading as="h2" size="7">
              {proposal.title[code]}
            </Heading>
            {index === 0 && (
              <Flex gap="4" flexShrink="0" pt="2">
                <Button asChild size="1" variant="ghost" color="gray">
                  <a
                    href={proposal.websiteUrl}
                    target="_blank"
                    rel="noreferrer"
                  >
                    Website ↗
                  </a>
                </Button>
                <Button asChild size="1" variant="ghost" color="gray">
                  <a href={proposal.adminUrl} target="_blank" rel="noreferrer">
                    Edit ↗
                  </a>
                </Button>
              </Flex>
            )}
          </Flex>
          <Separator size="4" />
          <Box>
            <SectionLabel>Elevator pitch</SectionLabel>
            <Html html={proposal.elevatorPitchHtml[code]} />
          </Box>
          <Separator size="4" />
          <Box>
            <SectionLabel>Abstract</SectionLabel>
            <Html html={proposal.abstractHtml[code]} />
          </Box>
        </Flex>
      ))}

      {proposal.notes && <Separator size="4" />}
      {proposal.notes && (
        <Disclosure
          summary={<SectionLabel inline>Notes from the author</SectionLabel>}
        >
          <Text
            as="p"
            size="2"
            mt="2"
            className="max-w-[70ch] whitespace-pre-wrap"
          >
            {proposal.notes}
          </Text>
        </Disclosure>
      )}
    </Flex>
  );
};

const Html = ({ html }: { html: string | null }) => (
  <Text
    as="div"
    size="3"
    className="max-w-[70ch] [&_a]:underline [&_ol]:list-decimal [&_ol]:pl-5 [&_ul]:list-disc [&_ul]:pl-5"
    dangerouslySetInnerHTML={{ __html: html ?? "" }}
  />
);
