import { Button } from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

import { useExportBadgeScansMutation } from "~/types";

export const ExportBadgeScansButton = () => {
  const [exportBadges, { loading, error }] = useExportBadgeScansMutation({
    variables: {
      conferenceCode: process.env.conferenceCode,
    },
  });

  const handleExport = async () => {
    const data = await exportBadges();

    window.open(data.data.exportBadgeScans.url);
  };

  return (
    <div>
      <Button onClick={handleExport} disabled={loading}>
        {loading ? (
          <FormattedMessage id="profile.sponsorSection.loading" />
        ) : (
          <FormattedMessage id="profile.sponsorSection.badgeScansExport" />
        )}
      </Button>
    </div>
  );
};
