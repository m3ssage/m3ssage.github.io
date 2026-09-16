---
title: "The Real Lesson of Firstmate: In the Age of Agents, Build the Tools That Fit You"
date: 2026-09-16T06:00:43+00:00
author:
  - eelco
categories:
  - Artificial Intelligence
  - Developer Tools
  - Software Development
  - Open Source
  - YouTube
tags:
  - Firstmate
  - Kun Chen
  - Coding Agents
  - Agent Distro
  - CLI
  - Workflow Automation
---
![Pixelated photograph of a ship's crew on deck, circa 1904](../../assets/2026-09-16-firstmate-agent-distro.jpg){ align=right width="250" loading=lazy }

An L8 principal engineer at Meta quits his job — and instead of launching a startup or raising a fund, he spends a year building wrappers. He wraps the GitHub CLI, Chrome DevTools, Git worktrees and code validation, and writes a tool called `gnhf` — "goodnight, have fun" — that babysits his coding agents while he sleeps. Stitched together, they became Firstmate, an open-source project that hit 3,000 stars in two months. But in this video, Hal Shin argues that the tool is not the interesting part: the real lesson is what its author understood about building for yourself in the age of AI agents.

<!-- more -->

### What Firstmate Actually Is

The tagline is "talk to one agent and ship with a crew." You talk to a single agent — the Firstmate — and it runs a fleet: spawning workers into their own terminal windows, giving each a clean Git worktree, supervising them, and handing back finished pull requests. You are the captain; the theme is nautical all the way down.

The surprising part is what it *isn't*. There is no binary, no installer, no server. You clone the repo, `cd` into it, launch Claude Code or Codex, and that's it — the repo itself is the product. Kun Chen calls it an **agent distro**, and inside the clone you find an `AGENTS.md` operating contract of 562 lines, 20 skill manifests and 140 helper scripts (almost all plain bash) doing the deterministic work, plus five hard rules — the orchestrator is read-only, only the "crewmates" touch code, and no pull request is ever merged without the captain's approval.

### The Stack Underneath

Firstmate turns out to be the top layer of one person's entire personal stack: eight repositories sharing the "-axi" suffix, a reference to **Agent Experience Interface** — a set of principles built on the idea that *the end user is an AI agent*, and that CLIs therefore deserve a different design. Alongside it sit `treehouse` for worktree management and a validation pipeline called `no-mistakes` that has more stars than Firstmate itself.

### The Four Principles You Can Steal

1. **Wrap the CLIs you already use, shaped to your use case.** The author's `gh-axi` produces roughly 35% fewer bytes than the official GitHub CLI's JSON output for the same data — a contract designed for his workflow.
2. **When the CLI you need doesn't exist, build it.** He needed his agents to manage Cloudflare DNS and there was no good CLI, so he wrote one — small, personal and useful. Crucially, agent-facing tools should fail in a way that teaches recovery, not just "element not found."
3. **Verify the output instead of babysitting every tool call.** A proper validation pipeline is what makes giving agents real autonomy safe.
4. **Create systems.** The hard part of automation isn't building it — it's remembering it. Document your conventions, keep one source of truth, and make your tools reusable: with ten tools and ten conventions you have a hundred things to remember.

### And the Honest Catch

Adopting someone else's personal stack means inheriting their personal choices — Firstmate, for instance, ships no releases at all, so you take whatever is on main that day. That is exactly why the video's conclusion is not "install this" but "learn from this": take the parts you like, leave the rest, and rebuild your own. As the author puts it, this code is cheap — the whole point is to experiment, and nobody is around to judge.

If you build with coding agents, the full 23-minute breakdown is worth your time — especially the `-axi` design principles and the validation pipeline, which are the parts most people skip.

### Sources

- Original video: [The hidden truth inside Firstmate AI — Hal Shin](https://www.youtube.com/watch?v=TlmTypTQFj8)
- [Firstmate on GitHub (kunchenguid/firstmate)](https://github.com/kunchenguid/firstmate)
- [SudoAll: Talk to One Agent, Ship With a Crew — An L8 Principal's Agentic Engineering Stack](https://sudoall.com/talk-to-one-agent-first-mate-agentic-stack/)
- [Kun Chen on the 3,000-star milestone](https://substack.com/@kunchenguid/note/c-311919739)
- [Image: Crew of the sailing ship TAMAR, ca. 1904 — Wikimedia Commons (Public domain), pixelated](https://commons.wikimedia.org/wiki/File:Crew_of_the_three-masted_sailing_ship_TAMAR,_Puget_Sound_port,_Washington,_ca_1904_(HESTER_65).jpeg)
