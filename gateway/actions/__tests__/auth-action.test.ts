import { AuthAction, AuthActionPayload } from "../auth-action";

jest.mock("../../config");

test("Auth auction sets both identity and refresh cookies", async () => {
  const context = {
    setCookies: [],
  };
  const action = new AuthAction(new AuthActionPayload("1", 5));
  await action.apply(context);

  expect(context.setCookies).toBeArrayOfSize(2);
});

test("Auth auction with only set identity option", async () => {
  const context = {
    setCookies: [],
  };
  const action = new AuthAction(new AuthActionPayload("1", 5), {
    identityOnly: true,
  });
  await action.apply(context);

  expect(context.setCookies).toBeArrayOfSize(1);
});
