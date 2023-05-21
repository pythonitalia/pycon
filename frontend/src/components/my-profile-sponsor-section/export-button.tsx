import { Button } from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

import { useExportBadgeScansMutation } from "~/types";

import { Alert } from "../alert";

export const ExportBadgeScansButton = () => {
  const [exportBadges, { loading, error }] = useExportBadgeScansMutation({
    variables: {
      conferenceCode: process.env.conferenceCode,
    },
  });

  const handleExport = async () => {
    const { data } = await exportBadges();

    const link = document.createElement("a");
    link.download = "badge_scans.csv";
    link.href = data.exportBadgeScans.url;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
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

      {error && (
        <Alert sx={{ mb: 4 }} variant="alert">
          <FormattedMessage
            id="global.tryAgain"
            values={{ error: error.message }}
          />
        </Alert>
      )}
    </div>
  );
};
