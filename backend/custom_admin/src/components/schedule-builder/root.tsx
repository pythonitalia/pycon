import { Base } from "../shared/base";
import { DjangoAdminLayout } from "../shared/django-admin-layout";
import { AddItemModalProvider } from "./add-item-modal/context";
import { Calendar } from "./calendar";
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

  if (loading) {
    return "wait";
  }

  console.log("error", error);

  const {
    conferenceSchedule: { days },
  } = data;
  console.log("conferenceId", days);

  return (
    <DjangoAdminLayout
      breadcrumbs={[
        { label: "Conference", url: "/admin/conferences/conference" },
        { label: "Schedule Builder" },
      ]}
    >
      {days.map((day) => (
        <Calendar key={day.id} day={day} />
      ))}
    </DjangoAdminLayout>
  );
};
