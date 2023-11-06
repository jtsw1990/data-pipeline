# Glimpse

Glimpse is a data engineering project designed to:
- Read in latest news snippets from source API
- Combined and process text, metadata into a single input
- Call LLM API to generate a single paragraph prompt
- Use prompt to feed into image generation API
- Use social platform API to automatically generate content daily  

## System Components

#### External APIs
- [Currents API](https://currentsapi.services/en)
- [Openai](https://openai.com/blog/openai-api)

#### AWS Ecosystem
- [Serverless](https://app.serverless.com/)
- [IAM](https://us-east-1.console.aws.amazon.com/iam/home?region=ap-southeast-2#)
- [S3](https://s3.console.aws.amazon.com/s3/buckets?region=ap-southeast-2&region=ap-southeast-2)
- [Lambda](https://ap-southeast-2.console.aws.amazon.com/lambda/home?region=ap-southeast-2)
- [SNS](https://ap-southeast-2.console.aws.amazon.com/sns/v3/home?region=ap-southeast-2#/)
- [CloudWatch](https://ap-southeast-2.console.aws.amazon.com/cloudwatch/home?region=ap-southeast-2#home:)

#### Social Media
- [Project Email](mailto:glimpse.feed@gmail.com)
- [Project Instagram](https://www.instagram.com/glimpse.feed/)

## Project Architecture

![Project Architecture](/docs/glimpse-architecture-diagram-v3.png)


Components that are **not** IaC:
- Updating of AWS credentials/IAM user
- SNS topic set up + subscriptions
- Pandas lambda layer
- OpenAI lambda layer
- Creation of environment variables for content create lambda
- Posting of content

## Useful Links
- [Currents API Documentation](https://currentsapi.services/en/docs/)
- [AWS Console Login](https://ap-southeast-2.console.aws.amazon.com/console/home?region=ap-southeast-2#)
- [DALL-E Dashboard](https://labs.openai.com/collections)


## Development Workflow
1.  Create and branch off new issue
2. Install all local dependencies in `requirements.txt` as well as setting up `serverless` locally
3. Use `#%%` magic from vscode jupyter extension to run isolated lambda functions
4. Replicate variables locally using sample files
5. To test, upload a sample `raw_feed.json` from local into [glimpse-landing-dev](https://s3.console.aws.amazon.com/s3/buckets/glimpse-landing-dev?region=ap-southeast-2&tab=objects) through the AWS console. This should kick off the pipeline automatically
6. If everything runs correctly, an email should be sent to `jtsw1990@gmail.com` with the content feed
7. If not, review the [logs](https://ap-southeast-2.console.aws.amazon.com/cloudwatch/home?region=ap-southeast-2#home:), check each lambda's latest timestamp to identify error messages
8. Delete the `raw_feed.json` from [glimpse-landing-dev](https://s3.console.aws.amazon.com/s3/buckets/glimpse-landing-dev?region=ap-southeast-2&tab=objects) and `feature.json` from [glimpse-feature-store](https://s3.console.aws.amazon.com/s3/buckets/glimpse-feature-store?region=ap-southeast-2&tab=objects) if applicable to keep things clean
9. Repeat steps `3-8` until tests run as expected 
10. Run `ruff check . --fix` to highlight any linting issues
11. Run `sls deploy` to push latest adjustments to AWS (Note the components not included in IAC above and apply accordingly)
12. Run git workflow to push to feature branch
13. Merge back into main

## Project Goals

- Become a wizard in building infrastructure
- To know the right practices and tools to avoid running notebooks manually in datascience projects
- To be able to weigh options for different solutions given a specific stack and situation
- Have fun learning and hopefully build something cool along the way

## Optional Goals

- Get used to the standard git development process (TBD) which will help with work
- Create a personal project template that can be reused
- Add an element of content creation to this

