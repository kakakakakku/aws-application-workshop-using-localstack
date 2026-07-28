# Chapter 1: Set Up Your Workshop Environment

## Introduction

LocalStack is an AWS emulator that runs on your local machine or in CI environments. It supports 120+ AWS services[^1], and even the free **LocalStack v4.14.0** covers the most commonly used ones.

It also works well as an environment for learning AWS, so it is a great fit for beginners who **want to learn AWS but worry about accidental charges**!

See the [LocalStack website](https://www.localstack.cloud/) for details.

This workshop is a hands-on introduction to LocalStack. With LocalStack, you can develop AWS applications without creating an AWS account, integrate LocalStack into your unit tests, and ultimately improve both your development speed and quality.

I built this workshop hoping that more people will discover how useful LocalStack is.

Now, let's set up the environment for this workshop!

## GitHub Codespaces

To keep the setup effort as low as possible and give everyone an identical environment, this workshop uses [GitHub Codespaces](https://github.com/features/codespaces). GitHub Codespaces is an online **VS Code (Visual Studio Code)** environment tied to a GitHub repository.

Open this GitHub repository and press the `.` (dot) keyboard shortcut. GitHub Codespaces should launch automatically.

## LocalStack

First, set up LocalStack in GitHub Codespaces. There are several ways to use LocalStack — the [LocalStack CLI](https://docs.localstack.cloud/getting-started/installation/) (command-line tool), [LocalStack Desktop](https://docs.localstack.cloud/user-guide/tools/localstack-desktop/) (desktop app), and the [LocalStack Docker Extension](https://docs.localstack.cloud/user-guide/tools/localstack-docker-extension/) (Docker Desktop extension). In this workshop, we install the **LocalStack CLI** in GitHub Codespaces and use it to start LocalStack.

> [!WARNING]
> LocalStack changed its license in March 2026 and now requires account registration and an auth token. There is a Hobby plan for personal use, but commercial use requires a paid plan (Base or higher). This workshop uses **LocalStack v4.14.0** — the last version published as open source — so that you can use LocalStack without registering an account. You will see a warning when starting LocalStack, which is safe to ignore. For details about the license change, see the official blog post:
> https://blog.localstack.cloud/the-road-ahead-for-localstack/

To open a terminal, select `Terminal` → `New Terminal` from the menu (the three-line icon) on the left side of GitHub Codespaces. Then choose `Continue Working in GitHub Codespaces` → `2 cores, 8 GB RAM, 32 GB storage`. GitHub Codespaces is available on the GitHub Free plan.

See [About billing for GitHub Codespaces](https://docs.github.com/en/billing/managing-billing-for-github-codespaces/about-billing-for-github-codespaces) for details.

> [!NOTE]
> You can check your GitHub Codespaces usage on the [Billing summary](https://github.com/settings/billing/summary) page.

> [!NOTE]
> Right after startup, you will see a terminal showing a `👋 Welcome to Codespaces!` message. Wait a moment, and it will automatically switch to a new terminal without that message.

Then run the following commands. If `localstack status` finally shows **✔ running**, the LocalStack CLI setup and the LocalStack startup are complete. It is fine if the other fields, such as `id` and the date, differ.

```sh
$ curl --output localstack-cli-4.14.0-linux-amd64-onefile.tar.gz \
    --location https://github.com/localstack/localstack-cli/releases/download/v4.14.0/localstack-cli-4.14.0-linux-amd64-onefile.tar.gz
$ sudo tar xvzf localstack-cli-4.14.0-linux-*-onefile.tar.gz -C /usr/local/bin

$ localstack --version
LocalStack CLI 4.14.0

$ localstack start -d
$ localstack status
┌─────────────────┬───────────────────────────────────────────────────────┐
│ Runtime version │ 4.14.0                                                │
│ Docker image    │ tag: 4.14.0, id: 3ebc37595918, 📆 2026-02-26T10:27:36 │
│ Runtime status  │ ✔ running (name: "localstack-main", IP: 172.17.0.2)   │
└─────────────────┴───────────────────────────────────────────────────────┘
```

On macOS, you can also install the LocalStack CLI with Homebrew. The commands above are taken from the [installation documentation](https://docs.localstack.cloud/getting-started/installation/), which covers the details.

## AWS CLI

The AWS CLI is preinstalled in GitHub Codespaces. Run `aws configure` to set up access keys for LocalStack. As the `DUMMY` values suggest, placeholder values are perfectly fine.

```sh
$ aws configure
AWS Access Key ID [None]: DUMMY
AWS Secret Access Key [None]: DUMMY
Default region name [None]: us-east-1
Default output format [None]: json
```

## LocalStack Resource Browser

LocalStack has a feature called the [Resource Browser](https://docs.localstack.cloud/aws/capabilities/web-app/resource-browser/). Although its functionality and design differ from the AWS Management Console, it lets you inspect and operate the resources deployed to LocalStack.

> [!WARNING]
> Due to the license change, the Resource Browser is no longer available with LocalStack v4.14.0. This workshop therefore uses the AWS CLI for all resource verification.

## Resuming the Workshop Later

You can go through this workshop in one sitting, or a little bit every day. Here is how to resume the workshop on a different day after setting up the environment in Chapter 1.

To resume your existing GitHub Codespaces environment, open this GitHub repository and press the `,` (comma) keyboard shortcut, then select `Resume this codespace`.

Tools such as the LocalStack CLI remain installed in the environment, but the LocalStack process itself will have stopped. So the only step you need to run again is starting LocalStack:

```sh
$ localstack start -d
```

That's it for Chapter 1! ✋

**Next: [Chapter 2: Try LocalStack](02-hello-localstack.md)**

[^1]: Quoted from the "support for 120+ AWS services" statement on the LocalStack website.
