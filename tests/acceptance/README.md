# Acceptance spec: the post is live and renders

One artifact that is both specification and validation. The scenarios are written in the language of the
problem (a reader opens a post), not in the language of the solution — no plugin, no MkDocs internals, no
implementation filenames. This means the site can be built differently without changing this spec, and a
scenario can only turn red if the reader is missing something.

## Running

```bash
python3 tests/acceptance/publicatie.py                    # the newest post
python3 tests/acceptance/publicatie.py --post docs/blog/posts/<post>.md
python3 tests/acceptance/publicatie.py --json             # machine-readable
python3 tests/acceptance/publicatie.py --site file:///tmp/kopie   # offline against a copy
python3 tests/acceptance/rood_bewijs.py                   # proves the spec can fail
```

Exit **0** = green, **1** = at least one scenario red, **2** = could not run (no sitemap, no posts).
A scenario that cannot assess itself (page unreachable) counts as **red**, not gray.

## The four layers

| Layer | In this file | What it does |
|---|---|---|
| testcases | `scenario_*` | Given/When/Then, one property per scenario |
| DSL | `resolve`, `header_image`, `rendered_header`, `article_images` | domain operations: "the page is this post", "the header image renders" |
| protocol-drivers | `fetch`, `sitemap_paths`, `frontmatter` | talk to the real site and the real repo |
| system under test | `https://pages.bommel.xyz` | MkDocs + GitHub Pages |

The URL comes from `sitemap.xml`, not from the filename: the slug is a property of the plugin, and a spec
that reimplements the plugin breaks as soon as the plugin changes.

## The three scenarios, and what each uniquely catches

1. **The page is this post** — the sitemap has a page under the post's date and the `<h1>` is the title
   frontmatter. Catches: not deployed, a failed build, a wrong slug, a page showing a different post.
2. **The header image renders** — directly under the `<h1>`, with the path from the markdown, `width="250"`
   and in the lightbox wrapper. Catches: the dependency regression from `CONSTRAINTS.md` (`selectolax`
   1.0.1 made the `<img>` disappear), a missing width attribute (image renders page-wide), a converted
   path.
3. **Every image in the post content loads** — per `src` in the article area an actual GET: status 200,
   content-type `image/*` and not empty. Catches: a renamed or not-uploaded asset, a truncated file.
   Scenario 2 cannot reach this: the `<img>` tag can be perfect while the file returns 404.

What the spec **does not** cover: whether the text is correct (that's `blog-axi` plus the readability
pass), whether the index shows the post (it shows 10 posts per page, so an index check would turn red
for the wrong reason), and whether the post is politically neutral (Jev gate in `blog-axi`).

## The red proof

`rood_bewijs.py` fetches the latest page, plants three real faults in a throwaway copy and demands that the
spec fails exactly the right scenario:

| case | mutation | expected |
|---|---|---|
| green | none | exit 0, 3× PASS |
| a | lightbox wrapper and `width` removed | exit 1, scenario 2 red |
| b | asset file removed | exit 1, scenario 3 red |
| c | post not in the sitemap | exit 1, scenario 1 red (2 and 3 cannot assess anything) |

Exit 0 means: the spec is able to catch a wrong answer. Without this step, a green spec is a wish. Run it
after every change to the spec itself.

## Contract change

The scenarios and their thresholds are the contract. Anyone who changes them because a post does not pass
them weakens the spec to turn green — exactly what `CONSTRAINTS.md` forbids. Adjusting an expectation
(an extra scenario, a stricter threshold) is a decision for the owner, with the reason in the commit.