# Requesting a Bedrock quota increase

Use this when Bedrock calls fail with `ThrottlingException` because the account-level quota is 0 or below the AWS default. Self-service increases in Service Quotas are rejected in that case ("must provide a quota value greater than the default"), so you need a support case.

Service limit increase cases are free on the Basic support plan.

## 1. Check current vs default values

```bash
# Applied (your account)
aws service-quotas get-service-quota --service-code bedrock --region us-east-2 \
  --quota-code L-D2912E70 --query 'Quota.Value'

# AWS default
aws service-quotas get-aws-default-service-quota --service-code bedrock --region us-east-2 \
  --quota-code L-D2912E70 --query 'Quota.Value'
```

Find quota codes for other models:

```bash
aws service-quotas list-service-quotas --service-code bedrock --region us-east-2 \
  --query "Quotas[?contains(QuotaName,'Nova Lite')].[QuotaName,Value,QuotaCode]" --output table
```

## 2. Open the case

https://support.console.aws.amazon.com/support/home#/case/create?issueType=service-limit-increase

If the form doesn't preselect it, click **Create case** and choose **Looking for service quota increases**.

## 3. Fill in the form

- **Service:** Bedrock
- **Request 1:**
  - **Region:** US East (Ohio), `us-east-2`
  - **Quota:** Model invocation max tokens per day for Amazon Nova Micro (doubled for cross-region calls)
  - **New value:** `5760000000`
- Click **Add another request** for each extra quota:

| Quota | Code | New value (AWS default) |
|---|---|---|
| Model invocation max tokens per day for Amazon Nova Micro | `L-D2912E70` | 5,760,000,000 |
| Cross-region model inference requests per minute for Amazon Nova Micro | `L-3F110E0F` | 4,000 |
| Cross-region model inference tokens per minute for Amazon Nova Micro | `L-DC7FF66C` | 8,000,000 |

To cover more models, add them to the same case instead of opening one case per model.

## 4. Case description

Paste this:

```
My account's Amazon Bedrock quotas for Amazon Nova Micro in us-east-2 are set
to 0 at the account level, below the AWS defaults, so every Converse call returns
ThrottlingException ("Too many tokens per day"). Self-service increase is rejected
because it requires a value above the default. Please restore these quotas to the
default values:
- L-D2912E70 Model invocation max tokens per day: 0 -> 5,760,000,000
- L-3F110E0F Cross-region inference requests per minute: 0 -> 4,000
- L-DC7FF66C Cross-region inference tokens per minute: 0 -> 8,000,000

Use case: development and testing with the Converse API, low volume
(a few thousand requests per day).
```

## 5. Submit

Choose **Web** as the contact method, then click **Submit**.

## After submitting

- Track the case and reply to AWS: https://support.console.aws.amazon.com/support/home#/case/history
- A response usually takes 1 to a few business days. AWS may ask about your use case or want some billing history first.
- Make sure the account has a valid payment method.

Confirm the new value once AWS replies:

```bash
aws service-quotas get-service-quota --service-code bedrock --region us-east-2 \
  --quota-code L-D2912E70 --query 'Quota.Value'
```
