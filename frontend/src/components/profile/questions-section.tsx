/** @jsxRuntime classic */

/** @jsx jsx */
import React, { FormEvent, useCallback, useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { Box, Heading, Input, jsx, Select } from "theme-ui";

import { InputWrapper } from "~/components/input-wrapper";
import { TicketItem } from "~/types";

import { Button } from "../button/button";
import { SelectedProducts } from "../tickets-page/types";

type Props = {
  tickets: TicketItem[];
  selectedProducts: SelectedProducts;
  onNextStep: () => void;
  nextStepMessageId?: string;
  nextStepLoading?: boolean;
  updateQuestionAnswer: (data: {
    id: string;
    index: number;
    question: string;
    answer: string;
  }) => void;
  updateTicketInfo: (data: {
    id: string;
    index: number;
    key: string;
    value: string;
  }) => void;
  showHeading?: boolean;
};

export const QuestionsSection = ({
  tickets,
  selectedProducts,
  onNextStep,
  updateQuestionAnswer,
  updateTicketInfo,
  nextStepMessageId = "order.nextStep",
  showHeading = true,
  nextStepLoading = false,
}: Props) => {
  return null;
};
