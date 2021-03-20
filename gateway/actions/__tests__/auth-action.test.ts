import { AuthAction } from "../auth-action";

test("Auth auction sets both identity and refresh cookies", async () => {
  const context = {
    setCookies: [],
  };
  const action = new AuthAction({ id: "1" });
  await action.apply(context);

  expect(context.setCookies).toBeArrayOfSize(2);
});

test("Auth auction with only set identity option", async () => {
  const context = {
    setCookies: [],
  };
  const action = new AuthAction({ id: "1" }, { identityOnly: true });
  await action.apply(context);

  expect(context.setCookies).toBeArrayOfSize(1);
});
