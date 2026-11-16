import { ReviewBetaLayout, ScreenPlaceholder } from "./layout";

export const MyReviewRoot = ({
  reviewSessionId,
  conferenceId,
  screen,
  screens,
  breadcrumbs,
}) => {
  return (
    <ReviewBetaLayout
      args={{ reviewSessionId, conferenceId, screen, screens, breadcrumbs }}
    >
      <ScreenPlaceholder />
    </ReviewBetaLayout>
  );
};
