/** @jsx jsx */
import { useMutation } from "@apollo/react-hooks";
import { Box, Text } from "@theme-ui/components";
import React, { useCallback, useState } from "react";
import { jsx } from "theme-ui";

import { Star } from "../../components/icons/star";
import {
  UpdateMyFavoriteMutation,
  UpdateMyFavoriteMutationVariables,
} from "../../generated/graphql-backend";
import UPDATE_MY_FAVORITE from "./update-my-favorite.graphql";

type Props = {
  itemId: string;
  myInterested: boolean;
};

export const FavoriteToggle: React.SFC<Props> = ({
  itemId,
  myInterested,
  ...props
}) => {
  const [myFavorite, setMyFavorite] = useState(myInterested);

  const [
    updateMyFavorite,
    { loading: updatingMyFavorite, error, data },
  ] = useMutation<UpdateMyFavoriteMutation, UpdateMyFavoriteMutationVariables>(
    UPDATE_MY_FAVORITE,
  );

  const toggleMyInterest = useCallback(e => {
    e.preventDefault();
    e.stopPropagation();

    updateMyFavorite({
      variables: {
        itemId,
        myFavorite: !myFavorite,
      },
    });
    setMyFavorite(!myFavorite);
  }, []);

  if (updatingMyFavorite) {
    return <Text />;
  }
  return (
    <Box>
      <Text onClick={toggleMyInterest}>
        <Star active={myFavorite} />️
      </Text>
    </Box>
  );
};
