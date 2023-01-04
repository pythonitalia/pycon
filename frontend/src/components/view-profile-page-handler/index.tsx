import { useCurrentLanguage } from "~/locale/context";
import { useMyProfileQuery } from "~/types";

import { MyProfile } from "../profile/my-profile";

export const ViewProfilePageHandler = () => {
  const language = useCurrentLanguage();

  const { data: profileData } = useMyProfileQuery({
    variables: {
      conference: process.env.conferenceCode,
      language: language,
    },
  });

  return (
    <div>
      <MyProfile profile={profileData} />
    </div>
  );
};
