import { ClearAuthAction } from "../clear-auth-action";

jest.mock("../../config");
test("Clear auth action clears cookies", async () => {
  const context = {
    setCookies: [],
  };

  const action = new ClearAuthAction();
  await action.apply(context);

  expect(context.setCookies).toContainEqual({
    name: "identity",
    value: "",
    options: {
      httpOnly: true,
      maxAge: -1,
      path: "/",
      sameSite: "none",
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
      sameSite: "none",
      secure: false,
    },
  });
});
