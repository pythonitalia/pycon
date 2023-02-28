/** @jsxRuntime classic */

/** @jsx jsx */
import { useState, useCallback } from "react";
import { FormattedMessage } from "react-intl";
import { Box, Heading, jsx } from "theme-ui";

import { Alert } from "~/components/alert";
import { Button } from "~/components/button/button";
import { Link } from "~/components/link";
import { Modal } from "~/components/modal";
import { Table } from "~/components/table";
import { useCurrentUser } from "~/helpers/use-current-user";
import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { useCurrentLanguage } from "~/locale/context";
import {
  AttendeeTicket,
  useUpdateTicketMutation,
  MyProfileDocument,
} from "~/types";

import { ProductState } from "../tickets-page/types";
import { QuestionsSection } from "./questions-section";

type Props = {
  tickets: AttendeeTicket[];
};

export const MyTickets = ({ tickets = [] }: Props) => {
  return null;
};
