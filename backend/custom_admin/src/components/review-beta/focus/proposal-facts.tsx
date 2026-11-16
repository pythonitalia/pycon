import { Badge, Flex } from "@radix-ui/themes";
import type { ReviewProposalFragmentFragment } from "./focus-mode.generated";

const LANGUAGES: Record<string, { flag: string; name: string }> = {
  en: { flag: "🇬🇧", name: "English" },
  it: { flag: "🇮🇹", name: "Italiano" },
};

const TYPE_ICONS: Record<string, string> = {
  talk: "🎤",
  tutorial: "🛠️",
  workshop: "🛠️",
  keynote: "⭐",
};

type Props = { proposal: ReviewProposalFragmentFragment };

export const ProposalFacts = ({ proposal }: Props) => (
  <Flex gap="4" justify="between" align="start" wrap="wrap">
    <Flex gap="2" wrap="wrap" align="center">
      <Badge size="2" color="gray" variant="surface" className="capitalize">
        {TYPE_ICONS[proposal.type.toLowerCase()] ?? "📄"} {proposal.type}
      </Badge>
      <Badge size="2" color="gray" variant="surface">
        📶 {proposal.audienceLevel}
      </Badge>
      <Badge size="2" color="gray" variant="surface">
        ⏱ {proposal.duration} min
      </Badge>
      {proposal.languages.map((code) => (
        <Badge key={code} size="2" color="gray" variant="surface">
          {LANGUAGES[code]?.flag} {LANGUAGES[code]?.name ?? code}
        </Badge>
      ))}
    </Flex>
    <Flex gap="2" wrap="wrap" justify="end">
      {proposal.tags.map((tag) => (
        <Badge key={tag.id} size="2">
          {tag.name}
        </Badge>
      ))}
    </Flex>
  </Flex>
);
