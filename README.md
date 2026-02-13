# HousingAI ROI Calculator — Web App

A Flask-based interactive ROI calculator designed to be embedded in Trumpet.com micro sales rooms via iframe.

## Local Development

```bash
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000`

## Embedding in Trumpet.com

Use an iframe with optional query parameters:

```html
<iframe 
  src="https://your-domain.com/?org=Example%20Housing&embed=true" 
  width="100%" 
  height="800" 
  frameborder="0"
  style="border: none; border-radius: 12px;">
</iframe>
```

### Query Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `org` | Pre-fill organisation name | `?org=Acme%20Housing` |
| `embed` | Slim padding for iframe use | `?embed=true` |
| `theme` | Reserved for future theming | `?theme=light` |

## AWS Deployment Options

### Option A: AWS App Runner (Simplest)

1. Push code to a GitHub repository
2. Create an App Runner service pointing to the repo
3. App Runner auto-builds from the Dockerfile
4. Set port to 5000

### Option B: AWS ECS Fargate

```bash
# Build and push to ECR
aws ecr create-repository --repository-name housingai-roi
docker build -t housingai-roi .
docker tag housingai-roi:latest <account>.dkr.ecr.<region>.amazonaws.com/housingai-roi:latest
docker push <account>.dkr.ecr.<region>.amazonaws.com/housingai-roi:latest

# Deploy via ECS (use console or CloudFormation)
```

### Option C: AWS Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialise and deploy
eb init -p docker housingai-roi
eb create housingai-roi-prod
eb deploy
```

### Option D: AWS Lambda + API Gateway (Serverless)

Use `mangum` adapter:
```bash
pip install mangum
```
Add to `app.py`:
```python
from mangum import Mangum
handler = Mangum(app)
```

## Custom Domain & HTTPS

For Trumpet.com embedding, you'll need HTTPS. Options:
- **App Runner**: Built-in HTTPS with custom domain support
- **CloudFront**: Add in front of any deployment for CDN + HTTPS
- **ALB**: Application Load Balancer with ACM certificate

## Cost Estimate

This is a very lightweight app (static-like, no database). Expected AWS costs:
- **App Runner**: ~$5-10/month (auto-scales to zero when idle)
- **ECS Fargate**: ~$10-15/month (minimum task running)
- **Lambda**: ~$0-2/month (pay per request, essentially free at low volume)
