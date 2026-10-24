---
title: "Software Isn't Dead, Generic Software Is"
date: 2026-10-24T07:22:13+00:00
description: "Chris Ashby argues the generic SaaS dashboard is running out of road, and names eight other shapes of software that are wide open in the agent era."
authors:
- eelco
categories:
  - AI
  - Software Development
  - Technology
  - YouTube
tags:
  - SaaS
  - AI agents
  - product strategy
  - startups
  - MCP
  - open source
---
![Editorial illustration seen from above: a wooden workbench with eight everyday objects in a row (a folding ruler, a brass compass, a spool of thread, a bell, a field notebook, a cardboard box, a small antenna and a hand plane), a laptop showing a dashboard at the right edge and a dashed empty outline on the bench where it used to sit](/assets/2026-10-24-software-isnt-dead-generic-software-is.png){ align=right width="250" loading=lazy }

For fifteen years Chris Ashby designed apps and advised startups on product. In a 35-minute video on his channel Build Great Products he makes an uncomfortable claim for anyone still shipping a generic dashboard: your product might not make it. Building one is now a weekend job with Claude Code or Codex, and what used to make software defensible, the fact that it was expensive and slow to build, has evaporated.

His conclusion is not that software is finished. It is narrower: software is not dead, generic software is. What follows is his list of eight shapes that still have room, and where that argument is solid and where it is a forecast.

<!-- more -->

### Three shifts behind the argument

Ashby puts the change on three shifts. First, building got cheap, so the moat moved away from the code and towards expertise, taste, data and distribution. Second, agents became users of software alongside people: through MCP servers, APIs and command line tools, a program can now have a customer that never opens a window. Third, pricing moved from features to outcomes, closer to how service work is billed.

That third shift is the interesting one. Software has spent two decades charging per seat, which only made sense while a human had to sit in the chair. An agent that books, plans and remembers things does not need a seat. If you cannot explain what outcome the invoice buys, the invoice gets harder to defend.

### The eight shapes he names

**Software-enabled services.** Do not sell accounting software, run the accounting firm that is ten times faster. His examples are Crosby and Pilot in accounting, Harvey and EvenUp in legal, Abridge in medical. The pitch is that two people plus AI deliver what a twenty-person firm delivered, and the client buys the finished work rather than a licence.

**Vertical agent harnesses.** The model is general purpose, so the product is everything around it: the rules, tools, knowledge, workflows and memory. Claude Code is that harness for programming; Ashby expects the same shape to appear in every niche, including very small ones. As models improve, the harness improves with them.

**Headless AI software.** Tools with no interface at all, built for agents to call. A CLI, an API, an MCP server. His own Eyedropper pulls a design system from a server into whatever project an agent is working on. The obvious risk is the one he names: a model lab can bundle something similar into its next release.

**Agent-native systems.** A plugin or skill that runs inside the agent the customer already uses, paired with a dashboard that shows progress and collects data. His ProductOS, a free plugin for Claude Code, Codex and Cursor, is the example. Coaches and consultants fit here because they already own a repeatable method worth encoding.

**Taste-led niche products.** Build for the thousand people who already trust you instead of a market of a million. The scarce thing in this category is caring more than anyone else about one narrow subject, and the product does not have to win on features.

**Ambient consumer agents.** An assistant that lives inside WhatsApp or iMessage instead of asking for an install. Meta's Muse is the current example. The real work is in the interface illusion: the user should never have to understand what an agent is.

**Proprietary data products.** Anyone can copy your app, nobody can copy your data. Strava's heat maps, Waze traffic, Glassdoor salaries. The test is whether the data is out of distribution for the models, which is another way of asking whether it is worth paying for.

**Open-source core.** Give the code away and charge for hosting, support, paid tiers and community. PostHog, Supabase and cal.com run this way. The public repository becomes the marketing department.

### How he would have you choose

The mapping is blunt and useful. Service experience or existing clients: type one. Deep niche expertise: vertical harness. One data source or one hard narrow skill: headless. A repeatable method with proof: agent-native system. An audience or a community: taste-led niche product. Ambition for a consumer giant and a tolerance for a brutal market: ambient agent. A body of data nobody else collects: data product. Comfortable building in public: open-source core.

### Where the argument holds, and where it does not

The three shifts are real. Coding agents did collapse the cost of a CRUD application, and MCP and CLI surfaces did turn agents into genuine users of software. The taxonomy is also more useful than the usual list of AI startup ideas because each type names where the defensibility sits, rather than what the product does.

The weak part is the headline. "Generic SaaS is dying" is a forecast without a measurement behind it: no churn figures, no revenue data, no example of a generic product that failed for the reason he gives. Plenty of unremarkable dashboards still sell, mostly on distribution, integration depth and switching costs, none of which the video counts. A cheap build makes a bad product easier to create, which is not the same as making it impossible to sell.

Two of his own categories carry the risk he mentions in passing. A headless tool can be absorbed by a model lab, and an ambient consumer agent competes with Meta, OpenAI and xAI on the distribution channel those companies own. The taste-led product is deliberately small, which is fine as a business and a poor fit for anyone raising money on growth.

The sharpest observation is buried in the middle: every one of the eight improves as the models improve. That cuts both ways. If your product is a thin layer over a model, the model's next release is your competitor. What survives is the part that is not in the model, which is exactly what he calls the harness, the data, the taste and the audience.

Original video: [Stop building SaaS. Build one of these 8 instead.](https://youtu.be/iJgBQy2k9hk)

### Sources

- [Stop building SaaS. Build one of these 8 instead.](https://youtu.be/iJgBQy2k9hk) — Build Great Products, Chris Ashby, 21 October 2026
- [Product OS](https://www.buildgreatproducts.com/product-os) — the plugin Ashby names as an example of an agent-native system
- [Introducing Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/) — Meta's personal AI agent, September 2026
