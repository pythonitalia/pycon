import { Base } from "../shared/base";
import { DjangoAdminLayout } from "../shared/django-admin-layout";
import { useCurrentConference } from "../utils/conference";
import { AddItemModalProvider } from "./add-item-modal/context";
import { Calendar } from "./calendar";
import { PendingItemsBasket } from "./pending-items-basket";
import { useConferenceScheduleQuery } from "./schedule.generated";

export const ScheduleBuilderRoot = () => {
  return (
    <Base>
      <AddItemModalProvider>
        <ScheduleBuilder />
      </AddItemModalProvider>
    </Base>
  );
};

const ScheduleBuilder = () => {
  const { conferenceCode, conferenceId, conferenceRepr } =
    useCurrentConference();
  const { error, loading, data } = useConferenceScheduleQuery({
    variables: {
      conferenceCode,
    },
  });

  const {
    conference: { days },
  } = data ?? { conference: {} };

  return (
    <DjangoAdminLayout
      breadcrumbs={[
        { label: "Conferences", url: "/admin/conferences" },
        { label: "Conferences", url: "/admin/conferences/conference" },
        {
          label: conferenceRepr,
          url: `/admin/conferences/conference/${conferenceId}`,
        },
        { label: "Schedule Builder" },
      ]}
    >
      {loading && <h2>Please wait</h2>}
      {!loading && error && (
        <h2>Something went wrong. Make sure you have the right permissions.</h2>
      )}
      {!loading && (
        <>
          {days.map((day) => (
            <Calendar key={day.id} day={day} />
          ))}
          <PendingItemsBasket />
        </>
      )}
    </DjangoAdminLayout>
  );
};
