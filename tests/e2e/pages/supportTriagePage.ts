import { expect, type Page } from '@playwright/test';

export class SupportTriagePage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async goto() {
    await this.page.goto('/');
    await expect(this.page.getByText('AI Support Decisioning Console')).toBeVisible();
  }

  async chooseScenario(label: string) {
    await this.page.getByLabel('Support scenario').click();
    await this.page.getByTestId('stSelectboxVirtualDropdown').getByText(label, { exact: true }).click();
  }

  async setCustomerMessage(message: string) {
    await this.page.getByLabel('Customer message').fill(message);
  }

  async runWorkflow() {
    await this.page.getByRole('button', { name: 'Run Workflow' }).click();
    await expect(this.page.getByText('System Details')).toBeVisible();
  }

  async openSystemDetail(name: 'Evidence' | 'Observability' | 'Guardrails' | 'Raw Audit Log') {
    await this.page.getByText(name, { exact: true }).first().click();
  }

  async runScenario(label: string, message: string) {
    await this.chooseScenario(label);
    await this.setCustomerMessage(message);
    await this.runWorkflow();
  }

  async expectDecision({
    intent,
    risk,
    decision,
    humanReview,
  }: {
    intent: string;
    risk: string;
    decision: string;
    humanReview: string;
  }) {
    await expect(this.page.getByText(intent, { exact: true }).first()).toBeVisible();
    await expect(this.page.getByText(risk, { exact: true }).first()).toBeVisible();
    await expect(this.page.getByText(decision, { exact: true }).first()).toBeVisible();
    await expect(this.page.getByText(humanReview, { exact: true }).first()).toBeVisible();
  }

  async expectEvidence(values: string[]) {
    await this.openSystemDetail('Evidence');

    for (const value of values) {
      await expect(this.page.getByText(value).first()).toBeVisible();
    }
  }

  async expectResponseFacts(values: string[]) {
    for (const value of values) {
      await expect(this.page.getByText(value).first()).toBeVisible();
    }
  }

  async expectProductionSignals() {
    await expect(this.page.getByText('Orchestration: LangGraph')).toBeVisible();

    await this.openSystemDetail('Observability');
    await expect(this.page.getByText('Trace ID')).toBeVisible();
    await expect(this.page.getByText('Intent mode:')).toBeVisible();
    await expect(this.page.getByText('Response mode:')).toBeVisible();
    await expect(this.page.getByText('Fallback used:', { exact: true })).toBeVisible();

    await this.openSystemDetail('Guardrails');
    await expect(this.page.getByText('Policy Guardrails')).toBeVisible();

    await this.openSystemDetail('Raw Audit Log');
    await expect(this.page.getByText('Readable audit timeline')).toBeVisible();
  }

  async expectNoInternalLanguageInCustomerResponse() {
    const response = this.page.locator('.response-card').first();

    await expect(response).not.toContainText(/JSON|API|agent|workflow/i);
  }
}
