<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset=".github/assets/infranest-logo-dark.svg">
    <img alt="InfraNest" src=".github/assets/infranest-logo-light.svg" width="300">
  </picture>
</p>

<h1 align="center">infranest-openapi</h1>

<p align="center">
  <strong>The InfraNest API, described in OpenAPI 3.</strong><br>
  Generate a client, feed it to your AI tools, or watch this repository to hear about every change.
</p>

<p align="center">
  <a href="https://github.com/InfraNest-Infrastructure-Organized/infranest-openapi/actions/workflows/update.yml"><img alt="Update" src="https://github.com/InfraNest-Infrastructure-Organized/infranest-openapi/actions/workflows/update.yml/badge.svg"></a>
  <img alt="OpenAPI 3" src="https://img.shields.io/badge/OpenAPI-3-6BA539">
  <img alt="Licence: Apache-2.0" src="https://img.shields.io/badge/licence-Apache--2.0-blue">
</p>

---

[`openapi.json`](openapi.json) describes every endpoint of the [InfraNest](https://infranest.io) public API: the
paths, the fields each request takes, a recorded example of each answer, which token scope it needs, and the error
format. It is the same file the [API reference](https://developers.infranest.io/reference) is built from, copied
here once a day from [developers.infranest.io/openapi.json](https://developers.infranest.io/openapi.json).

Only the public API is in it: what an API token may do. Anything else the InfraNest app does is deliberately left
out, so nothing here is a promise the API does not keep.

## Use it

**Generate a client** in your language with any OpenAPI generator, for example:

```sh
npx @openapitools/openapi-generator-cli generate -i openapi.json -g python -o infranest-client
```

**Give it to an AI tool or agent.** It is a complete, machine-readable description: every operation has a plain
summary, its scope (`x-infranest-scope`), whether it changes data (`x-infranest-token-writable`), the module it
belongs to (`x-infranest-module`) and an example answer.

**Pin a version.** Each change is a [release](https://github.com/InfraNest-Infrastructure-Organized/infranest-openapi/releases)
with a dated tag, such as `v2026.11.02`. Use a tag's `openapi.json` to build against a fixed description.

## Hear about changes

Select **Watch → Custom → Releases** at the top of this page. Every release lists the operations that were added,
removed or changed. InfraNest adds fields and endpoints without notice and gives six months' notice before it removes
or renames anything; see the [changelog](https://developers.infranest.io/changelog).

## How it stays current

A [daily workflow](.github/workflows/update.yml) fetches the published description. When it has changed, the
workflow commits the new file and publishes a release with a summary of the differences. Nobody edits
`openapi.json` here by hand: a change to the API happens in InfraNest, and reaches this repository from there.

## Start safely

Try calls in your free **sandbox** first: a test organization with sample data, where nothing reaches a provider or
the internet. See the [sandbox guide](https://developers.infranest.io/sandbox), and the ready-to-run scripts in
[infranest-examples](https://github.com/InfraNest-Infrastructure-Organized/infranest-examples).

## Use at your own risk

The description is provided "as is", under the [Apache License 2.0](LICENSE). A client generated from it calls the
real API with your token: what it changes is your responsibility, and can cause costs at your providers (see
[Responsibility and costs](https://developers.infranest.io/responsibility-and-costs)). Your use of InfraNest is
governed by its [Terms of Service](https://infranest.io/terms).

## Links

- [Developer documentation](https://developers.infranest.io) and the [API reference](https://developers.infranest.io/reference)
- [Errors](https://developers.infranest.io/errors): every error code, with what to do about it
- [infranest-examples](https://github.com/InfraNest-Infrastructure-Organized/infranest-examples): ready-to-run scripts
- [infranest-action](https://github.com/InfraNest-Infrastructure-Organized/infranest-action): InfraNest in a GitHub Actions workflow
- [Service status](https://status.infranest.io)

Found a mistake in the description? Please open an [issue](https://github.com/InfraNest-Infrastructure-Organized/infranest-openapi/issues).
For a security issue in InfraNest, see [infranest.io/security](https://infranest.io/security).

## Licence

[Apache License 2.0](LICENSE).
