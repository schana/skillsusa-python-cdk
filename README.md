# Sneks Infrastructure

### Prerequisites

1. (GD) Buy domain from Google domains
2. (GD) Set website forward from `<domain>` to `www.<domain>`
3. (AWS) Create certificate in Certificate Manager
4. (GD) Add CNAME records from Certificate Manager
5. (AWS) Set SSM parameter `certificate-arn` with the certificate arn

### Deploy steps

1. Deploy infrastructure

   ```
   # Ensure docker is running
   cdk deploy
   ```

2. (GD) Update DNS to CloudFront by adding CNAME record
   `www.<domain>` to `<cloudfront domain>.`, note the trailing `.`. The domain
   can be found in the CloudFormation outputs
3. Update `app/sneks/src/aws-config.js` with the CloudFormation outputs
4. Build website

   ```
   cd apps/sneks
   npm install
   npm run build
   ```

5. Deploy website with `cdk deploy`