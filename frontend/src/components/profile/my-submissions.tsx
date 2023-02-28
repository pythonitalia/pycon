/** @jsxRuntime classic */

/** @jsx jsx */
import { FormattedMessage } from "react-intl";
import { Box, Heading, jsx } from "theme-ui";

import { Alert } from "~/components/alert";
import { Link } from "~/components/link";
import { Table } from "~/components/table";
import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { useCurrentLanguage } from "~/locale/context";
import { useMySubmissionsQuery } from "~/types";

type Props = {
  className?: string;
};

export const MySubmissions = ({ className }: Props) => {
  return null;
};
