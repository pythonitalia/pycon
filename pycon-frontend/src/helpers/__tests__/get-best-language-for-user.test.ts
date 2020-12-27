import { getBestLanguageForUser } from "../get-best-language-for-user";

test.each`
  header                                    | expected
  ${"it"}                                   | ${"it"}
  ${"en"}                                   | ${"en"}
  ${"it-IT;q=0.8, it;q=0.5, en-US;q=0.3"}   | ${"it"}
  ${"en, it-IT;q=0.8,it;q=0.5,en-US;q=0.3"} | ${"en"}
  ${"da, en-GB;q=0.8, en;q=0.7"}            | ${"en"}
  ${"*, en-GB;q=0.8, en;q=0.7"}             | ${"en"}
  ${"*"}                                    | ${"en"}
`(
  "uses language $expected when the accept-language is $header",
  ({ header, expected }) => {
    expect(getBestLanguageForUser(header)).toBe(expected);
  },
);

test("uses en as default language when using an unkown accept-language", () => {
  expect(getBestLanguageForUser("fr-CH, fr;q=0.9, de;q=0.7, *;q=0.5")).toBe(
    "en",
  );
});

test("uses en as default language for empty accept-language", () => {
  expect(getBestLanguageForUser("")).toBe("en");
});
