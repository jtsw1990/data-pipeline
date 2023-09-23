# Glimpse

Glimpse is a data engineering project designed to:
- Read in latest news snippets from source API
- Combined and process text, metadata into a single input
- Call LLM API to generate a single paragraph prompt
- Use prompt to feed into image generation API
- Use social platform API to automatically generate content daily  

## System Components


## Project Architecture

![Project Architecture](/docs/project_architecture.png)

Components that are IaC:
- SNS topic set up
- SNS subcription add
- Pandas lambda layer

## Useful Links
- [Currents API Documentation](https://currentsapi.services/en/docs/)
- [AWS Console Login](https://ap-southeast-2.console.aws.amazon.com/console/home?region=ap-southeast-2#)
- [DALL-E Dashboard](https://labs.openai.com/collections)

## Project Goals

- Become a wizard in building infrastructure
- To know the right practices and tools to avoid running notebooks manually in datascience projects
- To be able to weigh options for different solutions given a specific stack and situation
- Have fun learning and hopefully build something cool along the way

## Optional Goals

- Get used to the standard git development process (TBD) which will help with work
- Create a personal project template that can be reused
- Add an element of content creation to this

