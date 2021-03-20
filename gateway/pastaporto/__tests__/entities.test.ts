import { Credential, Pastaporto, UserInfo } from "../entities";
import { fetchUserInfo } from "../user-info";
import { decodeIdentity } from "../identity";

const mockedFetchUserInfo = fetchUserInfo as jest.Mock;
const mockedDecodeIdentity = decodeIdentity as jest.Mock;

jest.mock("../../config", () => ({
  PASTAPORTO_SECRET: "abc",
}));

jest.mock("../identity", () => ({
  decodeIdentity: jest.fn(() => ({
    sub: "10",
  })),
}));

jest.mock("../user-info", () => ({
  fetchUserInfo: jest.fn(),
}));

describe("Unauthenticated pastaporto", () => {
  test("Create unauthenticated pastaporto", () => {
    const unauthenticated = Pastaporto.unauthenticated();
    expect(unauthenticated.userInfo).toBeNull();
    expect(unauthenticated.credentials).toBeEmpty();
  });

  test("Sign unauthenticated pastaporto", () => {
    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-20 14:35:31Z").getTime());

    const unauthenticated = Pastaporto.unauthenticated();
    const emptyPastaportoToken =
      "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mbyI6bnVsbCwiY3JlZGVudGlhbHMiOltdLCJpYXQiOjE2MTYyNTA5MzEsImV4cCI6MTYxNjI1MDk5MSwiaXNzIjoiZ2F0ZXdheSJ9.gUKpCcphlVZI22nVSnzCZqPyBfELg3zm1w2ASP2lRqE";
    expect(unauthenticated.sign()).toBe(emptyPastaportoToken);
  });
});

describe("Pastaporto", () => {
  beforeEach(() => {
    mockedDecodeIdentity.mockClear();
    mockedFetchUserInfo.mockReset();
  });

  test("Create pastaporto from identity token", async () => {
    mockedFetchUserInfo.mockReturnValue({
      id: 10,
      email: "test@email.it",
      isStaff: false,
    });

    const pastaporto = await Pastaporto.fromIdentityToken("fake");

    expect(mockedDecodeIdentity).toBeCalledTimes(1);
    expect(mockedDecodeIdentity).toBeCalledWith("fake");

    expect(mockedFetchUserInfo).toBeCalledTimes(1);
    expect(mockedFetchUserInfo).toBeCalledWith("10");

    expect(pastaporto.userInfo).toStrictEqual(
      new UserInfo(10, "test@email.it", false),
    );
    expect(pastaporto.credentials).toStrictEqual([Credential.AUTHENTICATED]);
  });

  test("Create pastaporto from staff identity token", async () => {
    mockedFetchUserInfo.mockReturnValue({
      id: 10,
      email: "test@email.it",
      isStaff: true,
    });

    const pastaporto = await Pastaporto.fromIdentityToken("fake");

    expect(mockedFetchUserInfo).toBeCalledWith("10");

    expect(pastaporto.userInfo).toStrictEqual(
      new UserInfo(10, "test@email.it", true),
    );
    expect(pastaporto.credentials).toStrictEqual([
      Credential.AUTHENTICATED,
      Credential.STAFF,
    ]);
  });

  test("Sign authenticated pastaporto", () => {
    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-20 14:35:31Z").getTime());

    const pastaporto = new Pastaporto(new UserInfo(5, "test@email.it", false), [
      Credential.AUTHENTICATED,
    ]);

    const expectedToken =
      "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mbyI6eyJpZCI6NSwiZW1haWwiOiJ0ZXN0QGVtYWlsLml0IiwiaXNTdGFmZiI6ZmFsc2V9LCJjcmVkZW50aWFscyI6WyJhdXRoZW50aWNhdGVkIl0sImlhdCI6MTYxNjI1MDkzMSwiZXhwIjoxNjE2MjUwOTkxLCJpc3MiOiJnYXRld2F5In0.eYiHsYsqfGkfH31Yicxml8kUqE1BKk-XFNFUw_kWIQo";
    expect(pastaporto.sign()).toBe(expectedToken);
  });
});
