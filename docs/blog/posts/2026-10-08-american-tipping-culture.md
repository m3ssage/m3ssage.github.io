---
title: "Tipping in America: How a Voluntary Custom Reached the Checkout Screen"
date: 2026-10-08T20:58:22+00:00
description: "How tipping in America grew from a voluntary custom into a checkout screen prompt, including the $2.13 subminimum wage."
author:
  - eelco
categories:
  - Society
  - Economics
  - Culture
tags:
  - Tipping
  - United States
  - Restaurants
  - Minimum Wage
  - Payment Terminals
---
![A clear plastic tip jar with a white label that reads "THANK YOU :)" and a one-dollar bill behind the label, standing on a wooden counter in a restaurant in New Jersey](/assets/2026-10-08-american-tipping-culture.jpg){ align=right width="250" loading=lazy }

In the United States a tip is no longer something that happens at the end of a sit-down meal. It appears on tablet checkouts at coffee counters, in ride-hailing apps, on delivery screens and, in some places, at self-checkout kiosks. In a Pew Research Center survey from November 2023, 72% of American adults said tipping is expected in more places than it was five years earlier.

Underneath that spread sits a less visible structure: a federal wage floor for tipped workers that has been $2.13 an hour for more than three decades, a patchwork of state exceptions, and rules that were rewritten twice in two years. This is what the official data, the industry, the surveys and the academic literature say about it.

<!-- more -->

### A custom that arrived late

Tipping began in medieval Europe and only took hold in the United States after the Civil War, when millions of formerly enslaved people entered the labour market. In an episode of NPR's history podcast *Throughline* (April 2021), journalist Nina Martyris describes what happened next: restaurant owners opening in Chicago and New York, "looking for cheap labor," hired the new workers as waiters and cooks, and "they didn't pay them because this tipping system had come in, and they had to make their wage through tips."

The practice was contested from the start. Many Americans of that era called tipping "racist, aristocratic, antilabor, demeaning," and a handful of states passed anti-tipping laws that, the programme notes, proved almost impossible to enforce. In 1916 William Rufus Scott published *The Itching Palm*, described by Martyris as the most famous polemic against the practice: "tipping is the price of pride. It is what one American is willing to pay to induce another American to acknowledge inferiority."

### The $2.13 floor

American tipped work rests on the tip credit, which Congress created in 1966 by amending section 3(m) of the Fair Labor Standards Act (Public Law 89-601): an employer may count part of a worker's tips toward the minimum wage, capped at 50% of it. The same law defined a tipped employee as someone who customarily and regularly receives more than $20 a month in tips.

According to the Congressional Research Service, those amounts were a percentage of the minimum wage, between 40% and 60%, until the 1996 amendments replaced the percentage with a fixed figure of $2.13 an hour.

The Department of Labor's fact sheet for tipped employees describes how that works. The employer pays at least $2.13 an hour directly, may claim a tip credit of no more than $5.12, the gap to the federal minimum wage of $7.25, and must top up the difference if tips plus the direct wage fall short of $7.25 in a workweek. Where state law differs, the employer has to follow the standard most protective to employees.

Several states do differ. Alaska, California, Minnesota, Montana, Nevada, Oregon, Washington and Guam require the full state minimum wage to be paid before tips, from Minnesota's $11.41 to Washington's $17.13. The District of Columbia still allows a credit: an $18.40 minimum wage, $8.10 in cash and a $10.30 credit. One Fair Wage, which campaigns against the subminimum wage, counts 43 states that permit "some version of the subminimum tipped wage."

The regulatory detail has been unstable. In 2021 the Department of Labor restricted the tip credit to work that is part of the tipped occupation, barring it for directly supporting work after 20% of the workweek or 30 continuous minutes. On 29 October 2024 the Fifth Circuit vacated that revision, holding that it "fails under the Administrative Procedure Act twice over," contrary to the text of the statute and, the panel added, arbitrary and capricious; the underlying "80/20" guidance dates from a 1988 handbook. The department issued a technical final rule on 17 December 2024 restoring the older text.

Federal tax treatment changed as well. An IRS tax tip from January 2026 notes that employees and the self-employed may deduct qualified tips, up to $25,000 a year, phasing out above $150,000 in modified adjusted gross income and $300,000 for joint filers.

### What the screens ask for

Prompting for a tip is now largely a software default, and Pew notes that "the adoption of point-of-sale tablets, apps and digital kiosks has made it easier for businesses to provide customers with tip prompts and suggestions." The vendor documentation shows that somebody chose every number on those screens:

- Square: for a transaction of $10 or more the options are "No Tip, 15%, 20% or 25%," merchants can configure up to three percentages and its API defaults to 15, 20 and 25. The setting that shows the tip screen at the counter before the card is put away is on by default.
- Toast: merchants can edit three percentages, but online ordering displays four suggested amounts by default. If a check already carries a mandatory gratuity, the system "will automatically take this into account and suggest an additional 3%, 5%, and 7% tip," amounts it calls fixed.
- Clover: at most four suggestions, and its developer example configures 18%, 20%, 25% and 30%, labelled "Acceptable", "Good", "Great" and "Excellent".

The staff view is mixed. A poll of nearly 50 hospitality professionals in August 2025 found 54% saying that the service fees restaurants add, typically 15% to 22%, confuse guests, while 8% thought they help secure fair wages. Pew found 72% of adults opposing automatic service charges regardless of group size, against 10% in favour, and more Americans opposing tip suggestions (40%) than favouring them (24%).

### What the customers say

The surveys disagree on size and agree on direction. Pew (2023): 92% of sit-down diners say they always or often tip there, 57% would leave 15% or less for an average meal, and habitual tipping falls sharply elsewhere, to 25% for coffee and 12% at fast-casual restaurants.

Bankrate (June 2025) found 63% of Americans holding at least one negative view of tipping, up from 59% a year earlier, with 41% saying businesses should pay better instead of relying on tips and 41% that tipping culture has got out of control. Bankrate also records the drift and the generation gap: 70% always tip sit-down servers, against 75% in 2021, and that share is 43% among Generation Z against 83% among Generation X.

Popmenu, a restaurant technology vendor that surveys 1,000 consumers twice a year, found 65% "fed up" with tipping in September 2025, against 53% in 2023, then 78% calling the practice ridiculous by March 2026 and 44% tipping less than the year before. On its own platform the share of pickup orders carrying a digital tip fell from 78% in 2022 to 62% in 2026.

Smaller surveys point the same way: PYMNTS Intelligence found 75% of consumers considering a tip option at self-checkout inappropriate, Oobit found 82% calling a self-checkout tip request unreasonable and 37% having stopped visiting a business over aggressive prompts, and Upgraded Points found 90% saying tipping has got out of hand.

At the till the levels have moved less than the mood. Toast's platform data for the third quarter of 2025 put the average tip at 19.2% in full-service restaurants, just above the seven-year low of 19.1% in the previous quarter, and 15.8% in quick-service. Delaware tipped highest at 21.1% and California lowest at 17.2%.

### Two readings of the same industry

The BLS puts the median hourly wage for waiters and waitresses at $16.94 in May 2025, across about 2.3 million jobs, and at $15.24 for the broader group of food and beverage serving and related workers, against $24.51 for all occupations.

The National Restaurant Association, which represents the industry, projects sales of $1.55 trillion in 2026 and employment of 15.8 million. The association argues that the tip credit means "tipped workers never make less than the prevailing minimum wage," and says that "nationally, tipped servers take home a median of $27 an hour, with the highest-paid making more than $41 an hour." One Fair Wage counters that the federal tipped wage has been $2.13 "since 1991" and that 43 states still allow a subminimum.

Both figures come from organisations with a position in the debate, and they measure different things: a median across all hours worked including tips, and a statutory floor.

### What the research finds

Academic work is less flattering to the idea that tips track service. A meta-analysis by Michael Lynn and Michael McCall of 22 published and 14 unpublished studies concluded that bill size was "the single largest predictor of tip size in restaurant settings," accounting for twice as much variability as all other factors combined. Server attractiveness, friendliness and customer mood came next; service quality, server effort and cost consciousness were "reliable, but weak."

Lynn's later framework lists five motives behind tipping, from helping servers and rewarding service to gaining social esteem and fulfilling felt obligations, and notes that economists have treated the practice as irrational or mysterious. Tips to American restaurant workers alone are estimated at about $44 billion a year.

A second line of research asks who gets tipped. Lynn and colleagues reported in 2008 that customers of both races tipped Black service providers less than White ones and raised the possibility of unlawful adverse impact, and Brewster and Nowak (2019) estimated that the average Black customer leaves about 3.30 percentage points less than a White customer. That is not settled: Brewster, Gourlay and Nowak (2022), using three survey experiments, found no evidence that consumers tip Black servers less than comparable White servers, all else being equal.

### Where the evidence stops

Whether the tipped-wage model on balance helps or hurts the people who work under it remains contested by the parties to it, and neither headline figure answers that question: a $27-an-hour median and a $2.13 statutory floor are not comparable.

What the public data do show is a widening gap between what customers say and what the terminals ask. Habitual tipping has declined across most categories since 2021, the share of pickup orders carrying a digital tip fell by 16 percentage points on one vendor's platform, and the average tip in full-service restaurants has barely moved off a seven-year low.

Policy is unresolved as well. A federal appeals court removed the 2021 tip-credit restrictions and the department restored the older text, while the Chicago City Council voted on 20 May 2026 to delay its One Fair Wage phase-out by two years, freezing the subminimum at $12.62 against a city minimum of $16.60.

A federal income-tax deduction for tips took effect for the 2025 tax year, with a $25,000 cap and an income phase-out, and its effect on how tips are reported, or on how much customers leave, has not been measured yet.

### Sources

- [NPR Throughline: Why tipping in the U.S. took off after the Civil War](https://www.npr.org/2021/04/01/983314941/throughline-why-tipping-in-the-u-s-took-off-after-the-civil-war)
- [Public Law 89-601, Fair Labor Standards Amendments of 1966](https://www.congress.gov/89/statute/STATUTE-80/STATUTE-80-Pg830.pdf)
- [Congressional Research Service: The Tip Credit Provisions of the FLSA (R43445)](https://www.congress.gov/crs_external_products/R/PDF/R43445/R43445.5.pdf)
- [U.S. Department of Labor: Fact Sheet #15, Tipped Employees Under the FLSA](https://www.dol.gov/agencies/whd/fact-sheets/15-tipped-employees-flsa)
- [U.S. Department of Labor: Minimum wages for tipped employees (effective 1 July 2026)](https://www.dol.gov/agencies/whd/state/minimum-wage/tipped)
- [Fifth Circuit: Restaurant Law Center v. U.S. Department of Labor, No. 23-50562](https://www.ca5.uscourts.gov/opinions/pub/23/23-50562-CV1.pdf)
- [U.S. Department of Labor: Tip Regulations Under the FLSA, Restoration of Regulatory Language (17 December 2024)](https://www.govinfo.gov/content/pkg/FR-2024-12-17/pdf/2024-29798.pdf)
- [IRS: One, Big, Beautiful Bill — how to take advantage of no tax on tips and overtime](https://www.irs.gov/newsroom/one-big-beautiful-bill-how-to-take-advantage-of-no-tax-on-tips-and-overtime)
- [Square: set up and customise tipping](https://squareup.com/help/us/en/article/8631-set-up-and-customize-tipping) · [Square TipSettings API](https://developer.squareup.com/reference/square/objects/TipSettings)
- [Toast: receipts display suggested tip amounts](https://support.toasttab.com/en/article/Receipts-Display-Suggested-Tip-Amounts) · [Toast: tip options for online ordering](https://support.toasttab.com/en/article/Setting-Up-Troubleshooting-Tip-Options-for-Online-Ordering)
- [Clover: using per-transaction settings](https://docs.clover.com/dev/docs/using-per-transaction-settings)
- [Pew Research Center: Tipping culture in America (9 November 2023)](https://www.pewresearch.org/2023/11/09/tipping-culture-in-america-public-sees-a-changed-landscape/) · [How Americans see recent developments in tipping](https://www.pewresearch.org/2023/11/09/how-americans-see-recent-developments-in-tipping/)
- [Bankrate: Tipping survey 2025 (4 June 2025)](https://www.bankrate.com/credit-cards/news/tipping-culture-survey/)
- [Popmenu consumer study, September 2025](https://www.prnewswire.com/news-releases/77-of-consumers-say-tipping-in-the-us-has-become-ridiculous-according-to-popmenus-annual-study-302577741.html) · [Popmenu consumer study, March 2026](https://www.prnewswire.com/news-releases/fed-up-consumers-cut-tips-for-restaurants-grocery-delivery-hotels-taxisride-services-and-others-according-to-popmenus-latest-study-302736449.html)
- [Toast Q3 2025 restaurant data](https://www.nasdaq.com/press-release/toast-data-how-reservation-and-full-service-restaurant-dining-trends-shifted-last) · [LiveNOW from FOX: state tipping rates from the same report](https://www.livenowfox.com/money/states-tipping-toast-report)
- [PYMNTS Intelligence: consumers at self-checkout asked to tip](https://www.pymnts.com/study_posts/27percent-of-consumers-at-self-checkout-say-theyve-been-asked-to-tip/)
- [Oobit: how digital payment screens rewired tipping (July 2026)](https://www.oobit.com/the-tipping-point-how-digital-payment-screens-rewired-americas-relationship-with-tipping)
- [Upgraded Points: where Americans are least likely to leave tips (2024)](https://upgradedpoints.com/news/where-americans-are-least-likely-to-leave-tips/)
- [OysterLink poll on service fees (August 2025)](https://www.prnewswire.com/news-releases/oysterlink-poll-54-of-hospitality-workers-say-service-fees-confuse-guests-302532448.html)
- [BLS Occupational Outlook Handbook: waiters and waitresses](https://www.bls.gov/ooh/food-preparation-and-serving/waiters-and-waitresses.htm) · [food and beverage serving and related workers](https://www.bls.gov/ooh/food-preparation-and-serving/food-and-beverage-serving-and-related-workers.htm)
- [National Restaurant Association: 2026 State of the Restaurant Industry](https://restaurant.org/research-and-media/media/press-releases/persistent-cost-increases-and-enduring-demand-will-shape-the-restaurant-industry-in-2026/) · [Tip Wage policy page](https://restaurant.org/issues-and-advocacy/policy-agenda/tipping/)
- [One Fair Wage: the subminimum wage](https://onefairwage.org/subminimum-wage.html)
- [Ogletree Deakins: Chicago pauses its tip-credit phase-out (20 May 2026)](https://ogletree.com/insights-resources/blog-posts/chicago-pauses-its-tip-credit-phaseout/)
- [Lynn & McCall: Beyond Gratitude and Gratuity — a meta-analytic review of the predictors of restaurant tipping (Cornell eCommons)](https://ecommons.cornell.edu/server/api/core/bitstreams/2898911a-5909-4802-a91a-04ebceb71fc7/content)
- [Lynn: Service gratuities and tipping — a motivational framework (Journal of Economic Psychology, 2015)](https://ecommons.cornell.edu/server/api/core/bitstreams/679efff6-373d-4931-9389-5edbdda9cf96/content)
- [Lynn et al.: Consumer racial discrimination in tipping (2008)](https://doi.org/10.1111/j.1559-1816.2008.00338.x) · [Brewster & Lynn: Black–white earnings gap among restaurant servers (2014)](https://doi.org/10.1111/soin.12056) · [Brewster & Nowak (2019)](https://doi.org/10.1177/1938965518777221) · [Brewster, Gourlay & Nowak: are Black restaurant servers tipped less than White servers? (2022)](https://doi.org/10.1177/19389655211036652)
- Header image: ["Jar for tips at a restaurant in New Jersey"](https://commons.wikimedia.org/wiki/File:Jar_for_tips_at_a_restaurant_in_New_Jersey.JPG) by Tomwsulcer, Wikimedia Commons (CC0)
