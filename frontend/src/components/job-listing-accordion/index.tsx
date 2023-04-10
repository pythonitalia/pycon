import {
  CardPart,
  MultiplePartsCard,
  Heading,
  HorizontalStack,
  Spacer,
  Text,
  Link,
} from "@python-italia/pycon-styleguide";
import React from "react";
import { FormattedMessage } from "react-intl";

import Image from "next/image";
import { useRouter } from "next/router";

import { useCurrentLanguage } from "~/locale/context";
import { JobListing } from "~/types";

import { createHref } from "../link";

export const JobListingAccordion = ({ job }: { job: JobListing }) => {
  const language = useCurrentLanguage();
  const { push, replace, pathname } = useRouter();
  const url = `/jobs/${job.id}`;

  const onOpenJob = (e: React.MouseEvent<HTMLAnchorElement, MouseEvent>) => {
    e.preventDefault();
    const func = pathname === "/jobs/[id]" ? replace : push;
    func("/jobs/[id]", url, {
      locale: language,
    });
  };

  return (
    <li>
      <Link
        onClick={onOpenJob}
        noHover={true}
        href={createHref({
          path: url,
          locale: language,
        })}
      >
        <MultiplePartsCard>
          <CardPart size="small" contentAlign="left">
            <HorizontalStack alignItems="center" gap="small">
              <img
                width={48}
                height={48}
                alt={`${job.company}'s logo`}
                src={job.companyLogo}
                loading="lazy"
                className="border border-black aspect-square object-scale-down bg-white p-[0.1rem]"
              />
              <Heading size={5}>{job.title}</Heading>
            </HorizontalStack>
          </CardPart>
          <CardPart size="small" contentAlign="left" background="milk">
            <Text size={2}>{job.company}</Text>
          </CardPart>
          <CardPart
            rightSideIcon="arrow"
            rightSideIconSize="small"
            size="small"
            contentAlign="left"
            background="milk"
          >
            <Text weight="strong" uppercase size="label4">
              <FormattedMessage id="jobboard.discoverMore" />
            </Text>
          </CardPart>
        </MultiplePartsCard>
        <Spacer size="small" />
      </Link>
    </li>
  );
};
