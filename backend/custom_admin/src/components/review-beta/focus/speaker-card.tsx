import {
  Avatar,
  Button,
  DataList,
  Flex,
  Heading,
  Link,
  Separator,
  Text,
} from "@radix-ui/themes";
import { useLayoutEffect, useRef, useState } from "react";
import { useArgs } from "../../shared/args";
import type { Screen } from "../types";
import { CollapsibleCard } from "./collapsible-card";
import type { ReviewProposalFragmentFragment } from "./focus-mode.generated";
import { SectionLabel } from "./section";

type Props = { speaker: ReviewProposalFragmentFragment["speaker"] };

export const SpeakerCard = ({ speaker }: Props) => {
  const { screens } = useArgs() as { screens: Screen[] };
  const focusUrl = screens.find((screen) => screen.id === "focus")?.url;
  const socialLinks = [
    ["Website", speaker.website],
    [
      "Twitter",
      speaker.twitterHandle && `https://twitter.com/${speaker.twitterHandle}`,
    ],
    [
      "Instagram",
      speaker.instagramHandle &&
        `https://instagram.com/${speaker.instagramHandle}`,
    ],
    ["LinkedIn", speaker.linkedinUrl],
    ["Facebook", speaker.facebookUrl],
  ].filter((social): social is [string, string] => Boolean(social[1]));
  const details = [speaker.gender, speaker.country].filter(Boolean).join(" · ");

  const facts: [string, React.ReactNode][] = [
    ["Speaking experience", speaker.speakerLevel],
    [
      "Previous talk",
      speaker.previousTalkVideo && (
        <Link
          href={speaker.previousTalkVideo}
          target="_blank"
          rel="noopener noreferrer"
        >
          Watch video
        </Link>
      ),
    ],
    [
      "Grant",
      speaker.grant ? (
        <Link href={speaker.grant.adminUrl} target="_blank">
          {speaker.grant.status}
        </Link>
      ) : (
        "Not requested"
      ),
    ],
  ].filter((fact): fact is [string, React.ReactNode] => Boolean(fact[1]));

  return (
    <CollapsibleCard
      summary={
        <Flex gap="3" align="center" justify="between" width="100%">
          <Flex gap="3" align="center">
            <Avatar
              size="4"
              radius="full"
              src={speaker.photoUrl ?? undefined}
              fallback={speaker.fullName.slice(0, 1)}
            />
            <Flex direction="column">
              <Heading as="h3" size="3">
                {speaker.fullName}
              </Heading>
              {details && (
                <Text size="1" color="gray">
                  {details}
                </Text>
              )}
            </Flex>
          </Flex>
          {speaker.participantAdminUrl && (
            <Button asChild size="1" variant="ghost" color="gray">
              <a
                href={speaker.participantAdminUrl}
                target="_blank"
                rel="noreferrer"
              >
                Edit ↗
              </a>
            </Button>
          )}
        </Flex>
      }
    >
      {speaker.bio && <Bio text={speaker.bio} />}

      {(socialLinks.length > 0 || speaker.mastodonHandle) && (
        <Flex gap="3" wrap="wrap" align="center">
          {socialLinks.map(([label, url]) => (
            <Link
              key={label}
              size="2"
              href={url}
              target="_blank"
              rel="noopener noreferrer"
            >
              {label}
            </Link>
          ))}
          {speaker.mastodonHandle && (
            <Text size="2" color="gray">
              Mastodon: {speaker.mastodonHandle}
            </Text>
          )}
        </Flex>
      )}

      <Separator size="4" />

      <DataList.Root size="2">
        {facts.map(([label, value]) => (
          <DataList.Item key={label}>
            <DataList.Label minWidth="140px">{label}</DataList.Label>
            <DataList.Value>{value}</DataList.Value>
          </DataList.Item>
        ))}
      </DataList.Root>

      <Separator size="4" />
      <Flex direction="column" gap="1">
        <SectionLabel>
          Proposals sent ·{" "}
          {speaker.maxProposals
            ? `${speaker.proposalsCount} of ${speaker.maxProposals}`
            : speaker.proposalsCount}
        </SectionLabel>
        {speaker.otherProposals.map((other) => (
          <Link
            key={other.id}
            size="2"
            href={`${focusUrl}?proposal=${other.id}`}
          >
            {other.title}
          </Link>
        ))}
      </Flex>
    </CollapsibleCard>
  );
};

const Bio = ({ text }: { text: string }) => {
  const ref = useRef<HTMLParagraphElement>(null);
  const [expanded, setExpanded] = useState(false);
  const [clamped, setClamped] = useState(false);

  useLayoutEffect(() => {
    const element = ref.current;
    if (element && !expanded) {
      setClamped(element.scrollHeight > element.clientHeight);
    }
  }, [expanded]);

  return (
    <Flex direction="column" align="start" gap="1">
      <Text
        ref={ref}
        as="p"
        size="2"
        color="gray"
        className={`whitespace-pre-wrap ${expanded ? "" : "line-clamp-4"}`}
      >
        {text}
      </Text>
      {(clamped || expanded) && (
        <Button
          size="1"
          variant="ghost"
          color="gray"
          onClick={() => setExpanded(!expanded)}
        >
          {expanded ? "Show less" : "Show more"}
        </Button>
      )}
    </Flex>
  );
};
