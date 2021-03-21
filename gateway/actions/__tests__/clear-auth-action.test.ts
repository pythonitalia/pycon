import { ClearAuthAction } from "../clear-auth-action";

jest.mock("../../config", () => ({
  IS_DEV: true,
}));

test("Clear auth action clears cookies", async () => {
  const context = {
    setCookies: [],
  };

  const action = new ClearAuthAction({});
  await action.apply(context);

  expect(context.setCookies).toContainEqual({
    name: "identity",
    value: "",
    options: {
      httpOnly: true,
      maxAge: -1,
      path: "/",
      sameSite: true,
      secure: false,
    },
  });
  expect(context.setCookies).toContainEqual({
    name: "refreshIdentity",
    value: "",
    options: {
      httpOnly: true,
      maxAge: -1,
      path: "/",
      sameSite: true,
      secure: false,
    },
  });
});
