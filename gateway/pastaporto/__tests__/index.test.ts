import { canRefreshIdentity } from "../index";
import { createRefreshToken } from "../identity";

describe("Can refresh token", () => {
  test("rejects expired token", () => {
    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-20 14:35:31Z").getTime());

    const testToken = createRefreshToken("10");

    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2050-03-20 14:35:31Z").getTime());

    expect(canRefreshIdentity(testToken, "10")).toBeFalse();
  });

  test("rejects token for a different user", () => {
    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-20 14:35:31Z").getTime());

    const testToken = createRefreshToken("10");

    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2050-03-20 14:35:31Z").getTime());

    expect(canRefreshIdentity(testToken, "30")).toBeFalse();
  });

  test("accepts valid token", () => {
    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-20 14:35:31Z").getTime());

    const testToken = createRefreshToken("10");

    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-04-20 14:35:31Z").getTime());

    expect(canRefreshIdentity(testToken, "10")).toBeTrue();
  });
});
