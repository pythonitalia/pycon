/* eslint-disable @typescript-eslint/ban-ts-comment */
import { USER_INFO_CACHE } from "~/components/profile/hooks";

export const updateOlarkFields = (newData: any = null) => {
  // @ts-ignore
  if (typeof window.olark === "undefined") {
    return;
  }

  if (newData) {
    // If we have new data from GraphQL
    // update our local cache
    // this allows us to send to Olark the user name and email
    // and since we don't always fetch the user data
    // we need to store it temporally so we can restore it if needed
    // In the future this data might be used for other stuff, like showing "Hi X"
    window.localStorage.setItem(
      USER_INFO_CACHE,
      JSON.stringify({
        email: newData.email,
        fullName: newData.fullName,
        name: newData.name,
        id: newData.id,
      }),
    );
  }

  // Empty object just so we can assume those props always exist
  // and we can force the json
  const defaultUser = {
    email: null,
    fullName: null,
    name: null,
    id: null,
  };

  let user;
  try {
    user =
      newData === null
        ? JSON.parse(window.localStorage.getItem(USER_INFO_CACHE))
        : newData;
  } catch (e) {
    console.log("Unable to restore user cache", e);
  }

  if (!user) {
    // if we can't restore the user somehow, or it is invalid from JSON or whatever
    // set a default empty user
    user = defaultUser;
  }

  // If we have something, replace the data
  // if some information is missing, the one from previous session might be used

  if (user.email) {
    // @ts-ignore
    window.olark("api.visitor.updateEmailAddress", {
      emailAddress: user.email,
    });
  }

  if (user.fullName || user.name) {
    // @ts-ignore
    window.olark("api.visitor.updateFullName", {
      fullName: user.fullName || user.name,
    });
  }

  if (user.id) {
    // @ts-ignore
    window.olark("api.visitor.updateCustomFields", {
      userId: user.id,
    });
  }
};
