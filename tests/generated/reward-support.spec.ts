import { test, expect, Page } from '@playwright/test';

const BASE_URL = 'http://localhost:8502';

async function selectScenario(page: Page, label: RegExp) {
  await page.locator('[data-testid="stSelectbox"]').first().click();
  await page.locator('[data-testid="stSelectboxVirtualDropdown"]').getByText(label).click();
}

async function runWorkflow(page: Page) {
  await page.getByRole('button', { name: /Run AI Workflow/i }).click();
  await expect(page.locator('.response-card')).toBeVisible({ timeout: 30000 });
}

test.describe('AI Reward Support Workflow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(BASE_URL);
    await expect(page.getByText(/AI Reward Support Workflow/i).first()).toBeVisible({
      timeout: 20000,
    });
  });

  test('loads the main workflow UI', async ({ page }) => {
    await expect(page.getByText(/Intent Agent/i).first()).toBeVisible();
    await expect(page.getByText(/Router Agent/i).first()).toBeVisible();
    await expect(page.getByText(/Risk Agent/i).first()).toBeVisible();
    await expect(page.getByText(/Response Agent/i).first()).toBeVisible();

    await expect(page.locator('[data-testid="stSelectbox"]').first()).toBeVisible();
    await expect(page.getByLabel(/Customer message/i)).toBeVisible();
    await expect(page.getByRole('button', { name: /Run AI Workflow/i })).toBeVisible();
  });

  test('handles high risk balance deducted but voucher missing case', async ({ page }) => {
    await selectScenario(page, /High Risk/i);
    await runWorkflow(page);

    const response = await page.locator('.response-card').innerText();

    expect(response).toMatch(/balance|deduct/i);
    expect(response).toMatch(/voucher/i);
    expect(response).toMatch(/escalat|support/i);
  });

  test('handles medium risk expired campaign case', async ({ page }) => {
    await selectScenario(page, /Medium Risk/i);
    await runWorkflow(page);

    const response = await page.locator('.response-card').innerText();

    expect(response).toMatch(/campaign/i);
    expect(response).toMatch(/active|expired|redeem/i);
    expect(response).toMatch(/display|visible|balance/i);
  });

  test('handles low risk voucher already issued case', async ({ page }) => {
    await selectScenario(page, /Low Risk/i);
    await runWorkflow(page);

    const response = await page.locator('.response-card').innerText();

    expect(response).toMatch(/voucher/i);
    expect(response).toMatch(/issued|available|created/i);
    expect(response).toMatch(/My Rewards|email|inbox|spam/i);
  });
});
