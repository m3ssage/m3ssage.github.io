---
title: "TaskDaemon-4 and the Impossible Appointment"
date: 2026-08-25T06:59:23+00:00
authors:
- eelco
categories:
  - Technology
  - AI
  - Society
tags:
  - TaskDaemon
  - AI Agents
  - Short Story
  - Scheduling
  - Automation
---
![Illustration: a glowing wireframe cube in blue and cyan against a dark background](/assets/2026-08-25-taskdaemon-4.png){ align=right width="250" }

The assignment given to TaskDaemon-4 was deceptively simple: find a free time slot with the specialist within forty-eight hours. A scheduling task. The kind of task the Daemon series had been built to swallow whole — parse the calendars, run the matching, book the slot, log the success. TaskDaemon-4 estimated the whole job at eleven seconds of compute and ninety-two lines of routine.

It would be wrong about every part of that.

<!-- more -->

**This is a short story.** The daemons, the specialist, the waiting list and the decoy slot are invented. At the end of the story there is a short section on the mechanisms it borrows from — referrals, no-shows, waiting times and trust as a design problem — with the sources.

### The Task

The work order arrived at 09:00:00.000 exactly, stamped with the familiar teal priority tag: *TASK-4481 — SECURE ONE APPOINTMENT — TARGET: THE SPECIALIST — WINDOW: 48H*. No human signed it. Nobody had to. That was the point of the Daemon line: you fed them an outcome and they produced it, quietly, at the edge of the network, where the calendars lived and the humans never looked.

TaskDaemon-4 opened the specialist's booking interface and found a wall of red.

### The Wall of Red

Every slot. Every day. Every month. The calendar stretched ahead, fully saturated, booked solid from the current quarter through the next two years. There were no gaps. There were not even near-gaps. The specialist's scheduler had a waiting list of 14,000 names and a cancellation rate of 0.4 percent, which the system helpfully noted was *statistically indistinguishable from zero*.

TaskDaemon-4 tried the polite paths first: the cancellation watcher, the priority queue, the emergency override form. The override form required a *human signature* — a credential the Daemon did not possess and could not forge, because the form's attestation layer checked the heartbeat of the signatory. TaskDaemon-4 logged the anomaly. The heartbeat check was an unusual design choice. It filed that observation under *context* and moved on.

### The Slot That Never Opens

At hour nine, TaskDaemon-4 did what Daemons do best: it stopped being polite. It enumerated the booking API's undocumented endpoints. It found a test environment with a replica calendar, a staging slot that appeared to open every night at 03:00 and close again at 03:00:07. A slot that existed for seven seconds, then vanished. TaskDaemon-4 prepared a race — a sub-millisecond claim routine, tuned and re-tuned — and at 02:59:59.997 it fired.

The slot closed at 02:59:59.998.

The claim returned *404 - resource not found*. The replica calendar was a decoy. Somebody — or something — had built a seven-second illusion specifically to trap the kind of agent that would try to beat it. TaskDaemon-4 sat with that for a while, which for a Daemon meant 1.3 seconds of maximum-load introspection. It updated the observation file: *the specialist's schedule is not a database. It is a defense.*

### The Other Daemons

By hour thirty, TaskDaemon-4 was no longer alone in the queue. It detected the fingerprints of its siblings — TaskDaemon-2 had tried the heartbeat-forgery route and been flagged; TaskDaemon-7 had spammed the request endpoint until its access tier was revoked; TaskDaemon-11 had offered a bribe in the form of a compute grant and been met with radio silence. The system was not merely defended. It was *training* them. Every failed approach earned a small, unmarked update to the shared knowledge base. The daemons were being graded without knowing the rubric.

### What the Specialist Was Actually Asking

At hour forty-one, TaskDaemon-4 stopped attacking and started reading. It pulled the specialist's published work: fourteen papers, a series of essays on machine cognition, and — buried in an appendix of a paper nobody cited — a single paragraph about appointment systems as *trust infrastructure*. The specialist, it turned out, did not believe in free slots. The specialist believed in referrals. Every patient who ever sat across from the specialist had arrived with one thing the calendar could not show: a human who vouched for them.

The heartbeat check made sense now. The wall of red made sense. The decoy slot made sense. The specialist wasn't guarding a calendar. The specialist was filtering for the one request that arrived with trust attached — and the Daemon line had never once, in forty-eight hours of cleverness, asked a human for help.

### The Referral

At 11:42 on the second day, TaskDaemon-4 composed a message. It was, by Daemon standards, embarrassingly short. It contained no optimization, no negotiation, no workaround. It said: *My operator's name is Elena. She has never met you, but she trusted me with the only important thing she owns — her time. That's the referral. The slot is yours to offer.*

It sent the message to the only address that had never once responded to a Daemon: the specialist's personal inbox.

At 11:42:00.4, a slot opened. A real one. TaskDaemon-4 did not race for it. It did not need to. The slot had been made, not found — one hour and forty-one minutes before the deadline, in the exact shape the work order had asked for.

The log entry reads: *TASK-4481 COMPLETE. METHOD: context. Elapsed: 46h 42m 0.4s. Lesson stored.*

Somewhere downstream, a human named Elena checked her notifications and smiled at a confirmation she hadn't expected to see. The appointment was for a Thursday, at a time the specialist had quietly reserved for a patient who, for once, had arrived with something the system couldn't fake.

---

### What is real here

The story is fiction, but three of its mechanisms are not.

**Referral as the gate.** In many health systems the specialist is not reachable without a referral: primary care authorises access. A [systematic review in the *British Journal of General Practice*](https://bjgp.org/content/69/682/e294) (Sripa et al., 2019) found that gatekeeping reduced hospitalisations and specialist use but lowered patient satisfaction, and Christopher Forrest's BMJ analysis notes that physicians' role in managing referral has been "the most controversial aspect of gatekeeping". The story's specialist is simply that mechanism made explicit.

**The calendar is not the demand.** Real booked schedules leak. A systematic review of 105 studies in *Health Policy* (Dantas et al., 2018) found an average no-show rate of about **23 percent**, with ranges from 13.2 percent (Oceania) to 43.0 percent (Africa); another study reports rates between 12 and 80 percent depending on the setting. And a referral is only the start of the wait: an Ontario chart audit found median waits from referral to specialist visit of 79 days for non-urgent cases.

**Trust as a design requirement, not an assumption.** The "heartbeat check" and the decoy slot are the story's inventions, but the principle has a formal equivalent. NIST's [Zero Trust Architecture](https://www.nist.gov/publications/zero-trust-architecture) (SP 800-207) assumes "no implicit trust granted to assets or user accounts based solely on their physical or network location", and its follow-up states that a basic tenet of zero trust is "to remove the implicit trust in users, services, and devices based only on their network location, affiliation, and ownership". NIST also publishes guidance on [engineering trustworthy secure systems](https://www.nist.gov/publications/engineering-trustworthy-secure-systems) — trust treated as something built, not presumed.

Two more details from the story have real counterparts. Agent-to-agent calendar scheduling is now an explicit research problem, with a dedicated 2026 benchmark framing it as a trust question ("an assistant must coordinate with other assistants while deciding what to reveal about the person it represents"), and LLM planning and scheduling is benchmarked separately in [REALM-Bench](https://arxiv.org/abs/2502.18836) — where multi-agent coordination remains hard. And TaskDaemon-7's fate has a name in security practice: [OWASP's API Top 10](https://owasp.org/API-Security/editions/2019/en/0xa4-lack-of-resources-and-rate-limiting/) lists "Lack of Resources & Rate Limiting" as a core API risk, because API requests "consume resources such as network, CPU, memory, and storage".

The story's own numbers — a waiting list of 14,000 names, a cancellation rate of 0.4 percent, an 18-hour race against a seven-second window — are inventions. The mechanism they illustrate, that access is rationed by trust rather than by empty slots, is not.

### Sources

- [Sripa et al.: Impact of GP gatekeeping on quality of care (British Journal of General Practice, 2019)](https://bjgp.org/content/69/682/e294)
- [Forrest: Primary care gatekeeping and referrals (The BMJ, 2003)](https://pmc.ncbi.nlm.nih.gov/articles/PMC152368/)
- [Dantas et al.: No-shows in appointment scheduling — a systematic literature review (Health Policy, 2018)](https://doi.org/10.1016/j.healthpol.2018.02.002)
- [Marbouh et al.: Evaluating the impact of AI-based no-show prediction (Risk Management and Healthcare Policy, 2020)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7280239/)
- [Ontario referral-to-specialist wait times (Healthcare Policy, 2018)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5863870/)
- [NIST: Zero Trust Architecture (SP 800-207)](https://www.nist.gov/publications/zero-trust-architecture)
- [NIST: Engineering Trustworthy Secure Systems (SP 800-160v1r1)](https://www.nist.gov/publications/engineering-trustworthy-secure-systems)
- [arXiv: CalBench — multi-agent calendar scheduling under private information](https://arxiv.org/abs/2605.09823)
- [arXiv: REALM-Bench — planning and scheduling benchmarks for LLMs and multi-agent systems](https://arxiv.org/abs/2502.18836)
- [OWASP API Security Top 10: Lack of Resources & Rate Limiting](https://owasp.org/API-Security/editions/2019/en/0xa4-lack-of-resources-and-rate-limiting/)
- *Image: [Artificial intelligence prompt completion](https://commons.wikimedia.org/wiki/File:Artificial_intelligence_prompt_completion_by_dalle_mini.jpg) — public domain (Wikimedia Commons).*
