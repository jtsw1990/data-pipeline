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
- Create and branch off new issue
- Install all local dependencies in `requirements.txt` as well as setting up `serverless` locally
- Use `#%%` magic from vscode jupyter extension to run isolated lambda functions
- Replicate variables locally using sample files
- Run `ruff check . --fix` to highlight any linting issues
- Run `sls deploy` to push latest adjustments to AWS (Note the components not included in IAC above and apply accordingly)
- Run git workflow to push to feature branch
- Merge back into main

## Project Goals

- Become a wizard in building infrastructure
- To know the right practices and tools to avoid running notebooks manually in datascience projects
- To be able to weigh options for different solutions given a specific stack and situation
- Have fun learning and hopefully build something cool along the way

## Optional Goals

- Get used to the standard git development process (TBD) which will help with work
- Create a personal project template that can be reused
- Add an element of content creation to this

