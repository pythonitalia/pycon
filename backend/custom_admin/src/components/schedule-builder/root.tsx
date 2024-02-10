import { Base } from "../shared/base";
import { DjangoAdminLayout } from "../shared/django-admin-layout";
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
  const conferenceId = (window as any).conferenceId;
  const { error, loading, data } = useConferenceScheduleQuery({
    variables: {
      conferenceId,
    },
  });

  const {
    conferenceSchedule: { days },
  } = data ?? { conferenceSchedule: {} };

  return (
    <DjangoAdminLayout
      breadcrumbs={[
        { label: "Conference", url: "/admin/conferences/conference" },
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
