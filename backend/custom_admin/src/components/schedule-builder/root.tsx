import { Flex, Spinner } from "@radix-ui/themes";
import { Suspense } from "react";
import { Base } from "../shared/base";
import { DjangoAdminLayout } from "../shared/django-admin-layout";
import { useCurrentConference } from "../utils/conference";
import { AddItemModalProvider } from "./add-item-modal/context";
import { Calendar } from "./calendar";
import { PendingItemsBasket } from "./pending-items-basket";
import {
  useConferenceScheduleQuery,
  useConferenceScheduleSuspenseQuery,
} from "./schedule.generated";

export const ScheduleBuilderRoot = ({
  conferenceId,
  conferenceCode,
  breadcrumbs,
}) => {
  return (
    <Base
      args={{
        conferenceId,
        conferenceCode,
        breadcrumbs,
      }}
    >
      <AddItemModalProvider>
        <DjangoAdminLayout>
          <Suspense
            fallback={
              <Flex
                align="center"
                justify="center"
                width="100%"
                height="100%"
                position="absolute"
                top="0"
                left="0"
              >
                <Spinner size="3" />
              </Flex>
            }
          >
            <ScheduleBuilder />
          </Suspense>
        </DjangoAdminLayout>
      </AddItemModalProvider>
    </Base>
  );
};

const ScheduleBuilder = () => {
  const { conferenceCode } = useCurrentConference();
  const { error, data } = useConferenceScheduleSuspenseQuery({
    variables: {
      conferenceCode,
    },
  });

  const {
    conference: { days },
  } = data;

  if (error) {
    return (
      <h2>Something went wrong. Make sure you have the right permissions.</h2>
    );
  }

  return (
    <>
      {days.map((day) => (
        <Calendar key={day.id} day={day} />
      ))}
      <PendingItemsBasket />
    </>
  );
};
