import { nanoid } from "nanoid";

import { test, expect } from "@playwright/test";
import { PYCON_FRONTEND_URL } from "../config";

test.describe("User register", async () => {
  test("with short password fails", async ({ page }) => {
    const email = `e2e-${nanoid()}-user@pythonit.it`;

    await page.goto(`${PYCON_FRONTEND_URL}/en/signup`);

    await page.fill("data-testid=email-input", email);
    await page.fill("data-testid=password-input", "a");
    await page.click("data-testid=signup-button");

    await new Promise((resolve) => {
      setTimeout(resolve, 5000);
    });

    await page.screenshot({ path: "aaa.png" });

    await expect(page).toHaveURL(/.*signup/);
    await expect(
      page.locator("data-testid=password-input-wrapper"),
    ).toContainText("ensure this value has at least 8 characters");
  });
});
