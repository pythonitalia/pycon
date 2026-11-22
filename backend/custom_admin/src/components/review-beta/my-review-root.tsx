import { FocusMode } from "./focus/focus-mode";
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
      {screen === "focus" ? <FocusMode /> : <ScreenPlaceholder />}
    </ReviewBetaLayout>
  );
};
