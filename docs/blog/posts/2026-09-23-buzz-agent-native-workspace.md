---
title: "Buzz: Block's Agent-Native Workspace, Explained"
date: 2026-09-23T12:51:52+00:00
author:
  - eelco
categories:
  - YouTube
  - Technology
  - AI
  - Developer Tools
  - Productivity
tags:
  - Buzz
  - Block
  - AI Agents
  - Nostr
  - Slack
---
![An illustration of AI agents sitting as equal members inside a shared team chat workspace](/assets/2026-09-23-buzz-agent-native-workspace.png){ align=right width="250" }

Slack changed how teams talk. Buzz, the open-source workspace Block released in July, bets that the next change is about *who is in the room*: not only your colleagues, but their agents — as members with names, identities and channel access rather than as a bot bolted on through an integration. It is being called a Slack killer, and the interesting part is not the chat window.

<!-- more -->

### Agents as teammates, not add-ons

In a tour on Greg Isenberg's podcast, Vinny walks through Buzz as it ships today: each agent is a normal participant in a channel, and the *harness* underneath it is swappable. One agent can run on Claude Code, the next on Codex, Goose or opencode — and because the conversation lives in the workspace, your context travels with you when you switch. Given how quickly tooling changes, that is the feature that removes the fear of betting on the wrong assistant.

Because Git is wired in, agents create projects, feature branches and their own worktrees, so several of them can work in parallel without touching the checkout on your laptop. Voice huddles work too: bring an agent into a call and it keeps the context of the channel.

### The open-protocol bet

Buzz is built on Nostr, an open protocol for signed messages and portable identities, and it is self-hostable: the server holds channels, search, automation and Git hosting. Block's framing is that people, agents, repos and decisions share one signed room instead of your team's memory living inside someone else's SaaS.

That is the argument Vinny keeps returning to: context is the raw material that makes models useful, so who owns it matters. Buzz can also run local models and share that compute with teammates, which means a small team can start without a cloud bill — or a vendor deciding what happens to its data.

### What it does today, and where it is rough

The demo is the convincing part. From a chat message, an agent scaffolded a small CRM app with the Wasp full-stack framework and deployed it to Railway; a second project pipes daily tweet stats into a channel through a public API, and the agent then analyses that data in place instead of you exporting it into a browser tab. Existing skills and global config from other harnesses carry over.

It is also clearly early-preview software. Workflows and recurring tasks did not land reliably in the tour, and the honest summary is that Buzz is a glimpse of work with more agent teammates than human ones — close, not finished. The full walkthrough, including the demos and the setup tips, is worth watching.

### Sources

- [Jack Dorsey's Buzz: Clearly Explained (and how to use it) — Greg Isenberg](https://youtu.be/_jGSgzBkzrY)
- [Block Engineering Blog: Buzz!](https://engineering.block.xyz/blog/buzz)
- [Block: Introducing Buzz — where humans and agents work together](https://block.xyz/inside/introducing-buzz-where-humans-and-agents-work-together)
- [GitHub: block/buzz](https://github.com/block/buzz)
