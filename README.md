# bedrock-runtime

Small playground for calling Amazon Bedrock models (Amazon Nova) from the AWS CLI and Python.

## Prerequisites

- AWS CLI v2, configured with credentials (`aws configure`)
- Python 3.9+
- Bedrock quotas above 0 for the model you call (see [Troubleshooting](#troubleshooting))

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

While the venv is active, `python` refers to the venv interpreter. Without activating it, run `.venv/bin/python`.

## Usage

### AWS CLI

```bash
aws bedrock-runtime converse \
  --region us-east-2 \
  --model-id us.amazon.nova-micro-v1:0 \
  --messages '[{
    "role": "user",
    "content": [{"text": "Say hello in one short sentence."}]
  }]'
```

### Python

```bash
python main.py
```

## Troubleshooting

### `ThrottlingException: Too many tokens per day`

This usually means the account-level Bedrock quota for the model is **0**, not that you used up a daily budget. Waiting does not fix it.

Check the applied values:

```bash
aws service-quotas list-service-quotas --service-code bedrock --region us-east-2 \
  --query "Quotas[?contains(QuotaName,'Nova Micro')].[QuotaName,Value,QuotaCode]" --output table
```

Compare one with the AWS default:

```bash
aws service-quotas get-aws-default-service-quota --service-code bedrock \
  --region us-east-2 --quota-code L-D2912E70 --query 'Quota.Value'
```

If the applied value is below the default, a self-service increase is rejected ("must provide a quota value greater than the default"). In that case, open a support case asking AWS to restore the default values. Step-by-step guide: [QUOTA_INCREASE.md](QUOTA_INCREASE.md).

- Create a case: https://support.console.aws.amazon.com/support/home#/case/create?issueType=service-limit-increase
- Case history: https://support.console.aws.amazon.com/support/home#/case/history

Nova Micro quota codes in `us-east-2`:

| Quota | Code | AWS default |
|---|---|---|
| Model invocation max tokens per day | `L-D2912E70` | 5,760,000,000 |
| Cross-region inference requests per minute | `L-3F110E0F` | 4,000 |
| Cross-region inference tokens per minute | `L-DC7FF66C` | 8,000,000 |

To list every model that has a daily token quota above 0 (empty output means none):

```bash
aws service-quotas list-service-quotas --service-code bedrock --region us-east-2 \
  --query "Quotas[?contains(QuotaName,'tokens per day') && Value>\`0\`].[QuotaName,Value]" --output table
```

## Useful links

- Bedrock model catalog (us-east-2): https://us-east-2.console.aws.amazon.com/bedrock/home?region=us-east-2#/model-catalog
- Bedrock quotas (us-east-2): https://us-east-2.console.aws.amazon.com/servicequotas/home/services/bedrock/quotas
- Supported models by region: https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html
