# HousingAI ROI Calculator v2 — Persistent Storage Setup

## How It Works

- Each Trumpet.com sales room gets a unique ID (e.g. `698f4a67d5371271fbf24804`)
- Embed the calculator with: `https://your-domain.com/?id=698f4a67d5371271fbf24804`
- The prospect's inputs auto-save 1.5 seconds after they stop typing
- When they return, their inputs are automatically restored
- Without an `?id` parameter, it runs in preview mode (no saving)

## AWS Setup (3 steps)

### Step 1: Create DynamoDB Table

In the AWS Console → DynamoDB → Create table:

- **Table name**: `housingai-roi-calculator`
- **Partition key**: `calc_id` (String)
- **Table settings**: Use default settings (on-demand capacity)

That's it — no sort key, no indexes needed. On-demand pricing means you only pay per request (essentially free at your volume).

### Step 2: Grant App Runner Permission to DynamoDB

Your App Runner service needs an **instance role** with DynamoDB access.

1. Go to **IAM → Roles → Create role**
2. Trusted entity: **AWS Service → App Runner**
   - If App Runner isn't listed, choose "Custom trust policy" and use:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [{
       "Effect": "Allow",
       "Principal": { "Service": "tasks.apprunner.amazonaws.com" },
       "Action": "sts:AssumeRole"
     }]
   }
   ```
3. Attach this **inline policy** (or create a managed policy):
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [{
       "Effect": "Allow",
       "Action": [
         "dynamodb:GetItem",
         "dynamodb:PutItem"
       ],
       "Resource": "arn:aws:dynamodb:eu-west-2:YOUR_ACCOUNT_ID:table/housingai-roi-calculator"
     }]
   }
   ```
4. Name the role: `AppRunnerHousingAIROI`

Then in **App Runner → your service → Configuration → Security**:
- Set **Instance role** to `AppRunnerHousingAIROI`

### Step 3: Deploy the Updated Code

Push the updated code to your GitHub repo. App Runner will auto-deploy.

## Embedding in Trumpet.com

```html
<iframe
  src="https://your-domain.com/?id=UNIQUE_ID_PER_CUSTOMER&embed=true"
  width="100%"
  height="800"
  frameborder="0"
  style="border: none; border-radius: 12px;">
</iframe>
```

Use a different `id` for each Trumpet sales room / prospect. The ID from Trumpet's own room ID would work well — just needs to be unique per customer.

## Cost

- **DynamoDB on-demand**: Essentially free (you'd need millions of requests to hit $1/month)
- **App Runner**: Same as before (~$5-10/month)
