import { test } from '@playwright/test';
import { SupportTriagePage } from './pages/supportTriagePage';

test.describe('AI Support Triage Console', () => {
  test('routes high-risk voucher inconsistency to human review', async ({ page }) => {
    const app = new SupportTriagePage(page);

    await app.goto();
    await app.runScenario(
      'High Risk — Balance deducted, voucher missing',
      'My balance was deducted but my flight voucher was not created.',
    );

    await app.expectDecision({
      intent: 'Reward Issue',
      risk: 'High',
      decision: 'Escalate To Human',
      humanReview: 'Required',
    });
    await app.expectEvidence([
      'balance api, voucher api',
      'balance deducted, voucher missing',
      'pending_review',
      'reward_support_review',
    ]);
    await app.expectResponseFacts([
      'balance was deducted',
      'flight voucher was not created',
      'support specialist',
    ]);
    await app.expectProductionSignals();
    await app.expectNoInternalLanguageInCustomerResponse();
  });

  test('flags visible but inactive campaign issue for review', async ({ page }) => {
    const app = new SupportTriagePage(page);

    await app.goto();
    await app.runScenario(
      'Medium Risk — Expired campaign still visible',
      'I can still see the flight voucher campaign, but I can’t redeem it.',
    );

    await app.expectDecision({
      intent: 'Campaign Issue',
      risk: 'Medium',
      decision: 'Flag For Review',
      humanReview: 'Not required',
    });
    await app.expectEvidence([
      'campaign api',
      'campaign visible, campaign inactive',
    ]);
    await app.expectResponseFacts([
      'visible in the app',
      'no longer active',
      'flagged it for review',
    ]);
    await app.expectProductionSignals();
    await app.expectNoInternalLanguageInCustomerResponse();
  });

  test('auto responds when voucher already exists', async ({ page }) => {
    const app = new SupportTriagePage(page);

    await app.goto();
    await app.runScenario(
      'Low Risk — Voucher already issued',
      'I redeemed a $500 flight voucher, but I can’t find it.',
    );

    await app.expectDecision({
      intent: 'Reward Issue',
      risk: 'Low',
      decision: 'Auto Respond',
      humanReview: 'Not required',
    });
    await app.expectEvidence([
      'balance api, voucher api',
      'voucher found',
    ]);
    await app.expectResponseFacts([
      'flight voucher has already been issued',
      'My Rewards',
      'registered email',
    ]);
    await app.expectProductionSignals();
    await app.expectNoInternalLanguageInCustomerResponse();
  });
});
