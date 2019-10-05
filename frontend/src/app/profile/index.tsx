import { useQuery } from "@apollo/react-hooks";
import * as React from "react";

import { MyProfileQuery } from "../../generated/graphql-backend";
import MY_PROFILE_QUERY from "./profile.graphql";

export const ProfileApp = () => {
  const { loading, error, data: profileData } = useQuery<MyProfileQuery>(
    MY_PROFILE_QUERY,
  );

  if (error) {
    throw new Error(`Unable to fetch profile, ${error}`);
  }

  return (
    <>
      <h1>My profile</h1>

      {loading && "Loading..."}
      {!loading && (
        <dl>
          <dt>email</dt>
          <dd>{profileData!.me.email}</dd>
        </dl>
      )}
    </>
  );
};
