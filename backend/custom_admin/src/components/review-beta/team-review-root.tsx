import { ReviewBetaLayout, ScreenPlaceholder } from "./layout";

export const TeamReviewRoot = ({
  reviewSessionId,
  conferenceId,
  screen,
  screens,
  canDecide,
  breadcrumbs,
}) => {
  return (
    <ReviewBetaLayout
      args={{
        reviewSessionId,
        conferenceId,
        screen,
        screens,
        canDecide,
        breadcrumbs,
      }}
    >
      <ScreenPlaceholder />
    </ReviewBetaLayout>
  );
};
