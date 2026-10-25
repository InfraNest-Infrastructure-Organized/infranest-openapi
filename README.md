<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset=".github/assets/infranest-logo-dark.svg">
    <img alt="InfraNest" src=".github/assets/infranest-logo-light.svg" width="300">
  </picture>
</p>

<h1 align="center">infranest-openapi</h1>

<p align="center">
  <strong>The InfraNest API, described in OpenAPI 3, with Postman and Bruno collections.</strong><br>
  Import it into your API client, generate a client in your language, or hand it to an AI assistant.
</p>

<p align="center">
  <a href="https://github.com/InfraNest-Infrastructure-Organized/infranest-openapi/actions/workflows/update.yml"><img alt="Update" src="https://github.com/InfraNest-Infrastructure-Organized/infranest-openapi/actions/workflows/update.yml/badge.svg"></a>
  <a href="https://github.com/InfraNest-Infrastructure-Organized/infranest-openapi/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/InfraNest-Infrastructure-Organized/infranest-openapi/actions/workflows/ci.yml/badge.svg"></a>
  <img alt="OpenAPI 3" src="https://img.shields.io/badge/OpenAPI-3-6BA539">
  <img alt="Licence: Apache-2.0" src="https://img.shields.io/badge/licence-Apache--2.0-blue">
</p>

---

[InfraNest](https://infranest.io) keeps your domains, DNS, servers and monitoring in one place. This repository holds
the description of its public API — every endpoint an API token may call, the fields each takes, a recorded example
of each answer, the token scope it needs and the errors it can give — and ready-made collections for API clients.
It is copied here once a day from the [developer site](https://developers.infranest.io), which is built from the
same files.

| File | What it is |
|---|---|
| [`openapi.json`](openapi.json) | The OpenAPI 3 description of the public API. |
| [`postman/`](postman/) | A Postman collection, one folder per area, and an environment. |
| [`bruno/`](bruno/) | The same as a [Bruno](https://www.usebruno.com) collection: a folder of `.bru` files, with an environment. |
| [`.spectral.yaml`](.spectral.yaml) | The lint ruleset the description is checked with, here and in InfraNest's own CI. |

Only the public API is here. Anything else the InfraNest app does is deliberately left out, so nothing in this
repository is a promise the API does not keep. None of the files contains a token.

## Quick start

**Start in your sandbox.** It is a free test organization with sample data, and nothing you do there reaches a
provider or the internet. In the app, open **My account → Developer**, select **Create a sandbox**, and create a
token while you are in it: a **test token** (`…|in_test_…`). Then pick your tool.

### Postman

1. **Import** both files in [`postman/`](postman/).
2. Pick the **InfraNest** environment, and set `token` (a secret) and `organization_id` (your sandbox's ID).
3. Send **Account → Get the signed-in user** to check the token works.

### Bruno

1. Clone this repository, or download `infranest.bruno.zip` from the latest
   [release](https://github.com/InfraNest-Infrastructure-Organized/infranest-openapi/releases/latest) and unzip it.
2. In Bruno, **Open collection** and pick the [`bruno/`](bruno/) folder.
3. Pick the **InfraNest** environment and set `organization_id`. `token` is a secret: Bruno keeps its value on your
   machine, never in the files.

### Insomnia, Hoppscotch and others

Import [`openapi.json`](openapi.json) directly, then set the base URL to `https://api.infranest.io` and add your
token as a Bearer token.

### Generate a client

Use [openapi-generator](https://openapi-generator.tech) (Java, or through `npx`):

```sh
npx @openapitools/openapi-generator-cli generate -i openapi.json -g typescript-fetch -o clients/typescript
npx @openapitools/openapi-generator-cli generate -i openapi.json -g python -o clients/python
npx @openapitools/openapi-generator-cli generate -i openapi.json -g php -o clients/php
npx @openapitools/openapi-generator-cli generate -i openapi.json -g go -o clients/go
npx @openapitools/openapi-generator-cli generate -i openapi.json -g csharp -o clients/csharp
```

The client sends your token as a Bearer token. Each operation carries its scope (`x-infranest-scope`), whether a
token may call it when it changes data (`x-infranest-token-writable`), its area (`x-infranest-module`) and the error
codes it can answer (`x-infranest-errors`).

### Give it to an AI assistant

To have an assistant or coding agent write code against the API, point it at
[`llms.txt`](https://developers.infranest.io/llms.txt), the developer site's index for AI tools, or give it
`openapi.json` itself. To let an assistant *read your account* — "which monitors were down last night?" — connect it
to the [MCP server](https://developers.infranest.io/ai-assistants) instead; it only reads.

## Versions and changes

- InfraNest **adds** fields and endpoints without notice: write clients that ignore what they do not know.
- It never **removes or renames** a field, or changes what one means, without **six months' notice** in the
  [changelog](https://developers.infranest.io/changelog) ([RSS](https://developers.infranest.io/changelog.xml)).
- Error codes never change. See [Versioning and deprecation](https://developers.infranest.io/versioning).

Each change here is a [release](https://github.com/InfraNest-Infrastructure-Organized/infranest-openapi/releases) with
a dated tag, such as `v2026.11.02`, listing the operations added, removed and changed, and which collections
changed. Its assets are that day's description and collections. Pin a tag to build against a fixed description, and
select **Watch → Custom → Releases** to be told about every change.

## How it stays current

A [daily workflow](.github/workflows/update.yml) fetches what the developer site publishes. When anything changed it
lints the description, commits the files and publishes a release. [CI](.github/workflows/ci.yml) checks every
committed version: the description is valid OpenAPI 3 and passes the [Spectral](https://stoplight.io/open-source/spectral)
ruleset, and no collection carries a token. Nobody edits these files here by hand; a change to the API happens in
InfraNest and reaches this repository from there.

## Links

- [Developer site](https://developers.infranest.io): the [quickstart](https://developers.infranest.io/quickstart),
  the [API reference](https://developers.infranest.io/reference), [limits](https://developers.infranest.io/limits)
  and [errors](https://developers.infranest.io/errors)
- [Sandbox](https://developers.infranest.io/sandbox): a free organization to try everything safely
- [Use with Postman, Bruno or Insomnia](https://developers.infranest.io/api-clients)
- [MCP server](https://developers.infranest.io/ai-assistants): Claude, ChatGPT, Cursor and VS Code read your account
- [infranest-examples](https://github.com/InfraNest-Infrastructure-Organized/infranest-examples): ready-to-run scripts
- [infranest-action](https://github.com/InfraNest-Infrastructure-Organized/infranest-action): InfraNest in a GitHub Actions workflow
- [Service status](https://status.infranest.io)

## Use at your own risk

The files are provided "as is", under the [Apache License 2.0](LICENSE). A client or collection calls the real API
with your token: what it changes is your responsibility, and can cause costs at your providers (see
[Responsibility and costs](https://developers.infranest.io/responsibility-and-costs)). Your use of InfraNest is
governed by its [Terms of Service](https://infranest.io/terms).

Found a mistake? Please open an [issue](https://github.com/InfraNest-Infrastructure-Organized/infranest-openapi/issues).
For a security issue in InfraNest, see [infranest.io/security](https://infranest.io/security).

## Licence

[Apache License 2.0](LICENSE).
