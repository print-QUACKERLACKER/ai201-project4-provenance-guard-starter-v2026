# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

1. **The request arrives** at `POST /submit` (`app.py::submit`) as JSON with `text` and `creator_id`. A missing `creator_id` becomes `"anonymous"`.
2. **Input checks** turn away anything that can't be scored: not JSON, `text` missing or not a string, empty or whitespace only, or fewer than 5 words gets a **400**; more than 10,000 characters gets a **413**. Every refusal is written to the audit log with a reason (`audit.log_rejection`), so turned-away requests still leave a trace.
3. **Signal one — the model signal** (`detector.model_signal`). GPT-2, running locally, reads the first 400 tokens and measures how predictable the text is (perplexity). This adds a 0–1 `model_score`, where higher means more likely AI.
4. **Signal two — the style signal** (`stylometry.style_signal`). This measures the shape of the text without reading it: how much sentence lengths vary. It adds a 0–1 `style_score`, where higher means more likely AI.
5. **Combining** (`scoring.combine_signals`) turns the two scores into one `confidence` from 0 (human) to 1 (AI): 0.6 × model + 0.4 × style, pulled toward the more-human signal when they disagree.
6. **Labelling** (`scoring.score_to_label`) turns that number into a `guess` (`human` / `unsure` / `ai`) and the sentence the writer actually reads.
7. **Logging and the answer.** The decision gets a new `content_id` and is written to `logs/audit.jsonl` with both signal scores, the combined score, the label and `status: "decided"`. The response carries the same fields. If the writer disagrees, they send that `content_id` to `POST /appeal`, which writes the appeal next to the original decision and moves it to `under_review`.



---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** How predictable the text is to a language model (GPT-2's perplexity on the first 400 tokens), squashed onto 0–1 so that low perplexity gives a high AI score.

**Why that might differ between human and AI writing:** A model writes by picking a likely next word again and again, so its own output is easy for a model to predict. People make odder word choices and take abrupt turns.

**What it can't see:** Who actually wrote it. It rewards common words in ordinary sentences, so plain human writing scores as AI. My own paragraph about my dog scored 0.74 because "Firstly… Second… Lastly" with everyday words is very predictable. Writers in a second language, younger writers and anyone writing plainly get flagged the same way. Going the other way, rare words or deliberate typos raise perplexity and make AI text look human.

### Signal two — the style signal

**What it measures:** How much sentence length varies: the standard deviation of words per sentence divided by the mean. A ratio of 0.2 or below scores 1.0 (AI) and 0.7 or above scores 0.0 (human). A single sentence has no spread, so it scores a neutral 0.5. `stylometry.py` also computes type-token ratio and punctuation density, but they are weighted 0 (see below).

**Why that might differ between human and AI writing:** AI prose tends toward even, steadily built sentences. My AI paragraph ran 13, 17, 23, 29 words. Human writing is lumpier: mine ran 8, 16, 7, 18.

**What it can't see:** The words. It doesn't read at all, so anything that changes the shape without changing the content moves it. Splitting a long AI sentence into short ones, or adding one very short sentence, makes AI text look human. Short texts give it almost nothing to work with: every one-sentence submission gets exactly 0.5.

**Why only one of three measures counts:** I calibrated on a paragraph I wrote and an AI paragraph on the same topic. Vocabulary variety and punctuation both pointed the wrong way. The AI paragraph had *more* varied vocabulary (0.89) and *fewer* commas than mine, which made the style signal call the AI paragraph more human than me (0.49 vs 0.58). With only sentence spread counted, the AI paragraph scores 0.72 and mine 0.49. This is fitted on two paragraphs, so unit 8 will show whether it holds.

### Signal two — the style signal

**What it measures:**

**Why that might differ between human and AI writing:**

**What it can't see:**

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** A weighted average that leans on the model signal. If the two signals differ by more than 0.4, they are disagreeing, and the result is pulled halfway toward whichever one reads more human. When the methods split, I would rather miss some AI text than accuse a real writer.

**The numbers:**

- `combined = 0.6 × model_score + 0.4 × style_score`
- if `|model_score − style_score| > 0.4`: `combined = (combined + min(model_score, style_score)) / 2`
- labels: human below **0.35**, unsure **0.35–0.75**, AI above **0.75**
- weights inside the style signal: sentence spread **1.0**, type-token ratio **0**, punctuation **0**

All of these are in `config.py`.

**Why these thresholds:** My own paragraph scored 0.641 and the AI paragraph 0.802. The AI line at 0.75 sits between them, closer to the AI score, so my writing lands on "unsure" rather than "AI". With the starter's 0.65 threshold and my first style signal, my paragraph scored 0.675 and would have been accused.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

"A favorite animal many have are dogs, they are amazing companions and I think most agree." (human, one sentence). The model signal read it as very human (0.131, perplexity 147, because the grammar is unusual). The style signal had nothing to measure in one sentence, so it gave a neutral 0.5. That's a gap of 0.37, just under my 0.4 disagreement line, so the plain weighted average applies: 0.6 × 0.131 + 0.4 × 0.5 = **0.279 → human**. The 0.4 weight on a signal that knew nothing still pulled the score up by 0.12. If the model had been a little more confident, the disagreement rule would have pulled it back down toward 0.13.



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | Written by a human. Our checks found that this was most likely written by a person. |
| unsure | 0.35 – 0.75 | The system is still thinking about this one. Our checks couldn't tell whether a person or an AI tool wrote it, so we haven't decided either way. If you wrote it yourself, you don't need to do anything. |
| high-confidence AI | 0.75 – 1.00 | AI detected. Our checks found strong signs that this was written with an AI tool. This is an automated guess and it can be wrong — if you wrote this yourself, you can appeal and a person will review it. |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

My own paragraph lands on this label, so I wrote it for someone like me: a real writer whose work happens to look predictable. It says plainly that the system couldn't decide, not that the writer did anything wrong. It ends by telling them they don't need to do anything, so it doesn't read as a warning. It also doesn't say "try again", which would tell an honest writer they failed and invite people to keep resubmitting until they find a score they like.



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

Run on port 5001 (`PORT=5001 python app.py`) — on macOS, port 5000 is taken by the AirPlay Receiver.

```bash
$ curl -X POST http://127.0.0.1:5001/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "Dogs are my favorite animals for many reasons. Firstly, they'\''re a man'\''s best friend, they will follow you anywhere and smile when you smile. Second, they'\''re extremely adorable when they'\''re puppies. Lastly, I love my own dog very much, so he has taught me to love other dogs aswell!", "creator_id": "michelle"}'
```

```json
{
    "confidence": 0.6412,
    "content_id": "9cdde5ee66b446f99a8778febd608154",
    "creator_id": "michelle",
    "guess": "unsure",
    "label": "The system is still thinking about this one. Our checks couldn't tell whether a person or an AI tool wrote it, so we haven't decided either way. If you wrote it yourself, you don't need to do anything.",
    "model_score": 0.7405,
    "status": "decided",
    "style_score": 0.4922
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5001/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "9cdde5ee66b446f99a8778febd608154", "reasoning": "I wrote this paragraph myself about my own dog. The Firstly/Second/Lastly structure is how I was taught to write in school."}'
```

```json
{
    "content_id": "9cdde5ee66b446f99a8778febd608154",
    "message": "valid",
    "status": "under_review"
}
```

**What the log shows afterwards**

The two log entries for this content_id (from `GET /log`), the original decision followed by the appeal:

```bash
$ curl "http://127.0.0.1:5001/log?limit=4"
```

```json
{
    "count": 2,
    "entries": [
        {
            "combined_score": 0.6412,
            "content_id": "9cdde5ee66b446f99a8778febd608154",
            "creator_id": "michelle",
            "guess": "unsure",
            "label": "The system is still thinking about this one. Our checks couldn't tell whether a person or an AI tool wrote it, so we haven't decided either way. If you wrote it yourself, you don't need to do anything.",
            "model_score": 0.7405,
            "status": "decided",
            "style_score": 0.4922,
            "timestamp": "2026-11-05T02:10:32+00:00"
        },
        {
            "content_id": "9cdde5ee66b446f99a8778febd608154",
            "creator_id": "michelle",
            "event": "appeal",
            "reasoning": "I wrote this paragraph myself about my own dog. The Firstly/Second/Lastly structure is how I was taught to write in school.",
            "status": "under_review",
            "timestamp": "2026-11-05T02:10:35+00:00"
        }
    ]
}
```

---

## How I Used AI

**Moment 1 — understanding what I had to decide**

- *What I asked for:* I pasted the milestone instructions into Claude and asked what I needed to write so it could implement the project.
- *What came back:* A fill-in list of decisions: how to handle bad input, the response fields, how appeals behave, the style weights, the combining rule, the thresholds and the labels. It also flagged that my project folder wasn't connected to my GitHub fork. When I answered, it pushed back on some of my choices: returning 200 for errors, a 400-character limit (too short for a normal paragraph), and a 1–10 confidence scale where low meant AI (the reverse of every other score).
- *What I changed:* I switched to 400/413 errors, a 10,000-character limit, and a 0–1 confidence where 1 means AI.

**Moment 2 — calibration**

- *What I asked for:* I gave Claude four one-sentence test texts, then a paragraph I wrote myself and an AI-written paragraph on the same topic, and had it score each one on every measure.
- *What came back:* The one-sentence texts were too short for the style measures to mean anything. My own paragraph scored 0.675, just under the AI line. Vocabulary variety and punctuation were pointing the wrong way, scoring the AI paragraph as more human than mine. Claude offered two options: count only sentence spread, or keep all three and report the finding.
- *What I changed:* I picked spread only. That moved my paragraph to 0.641 and the AI paragraph to 0.802, and the AI threshold went to 0.75 so it falls between them. I also had Claude expand my one-word labels ("HUMAN", "TRY AGAIN", "ROBOT") into full sentences, starting from my own wording.

**Moment 3: running the test (unit 8)**

- *What I asked for:* I pasted the unit 8 instructions into Claude and asked what it needed from me, then had it run the attack set, the eval and the flood test, and fill in the tables.
- *What came back:* It ran everything and marked each attack held or broke. It asked me one question it couldn't decide alone: does "unsure" count as held? I said yes. When I sent casual paragraphs for my "stiff writing" criterion, it pointed out they weren't in the Firstly/Second/Lastly style and were under 40 words. It refused to write extra sentences "in my style", because that would put AI text into my false-positive test. It pulled the 10 published paragraphs from Project Gutenberg and 2019 Wayback Machine snapshots of US government pages, not from memory, so each has a real source. It also warned that the old prose might be easier to call human, which turned out to be true.
- *What I changed / decided:* I used my old social-media essay for criterion 2, my speaking-up narrative for criterion 4, and wrote three sentences myself to extend my running paragraphs. For criterion 3, Claude drafted five AI paragraphs and I edited four of them myself; the fifth is my own meditation piece. I picked FP04 as my worst outcome.

**Moment 4: diagnosis and the fix**

- *What I asked for:* I asked Claude to draft the diagnoses and make the improvement.
- *What came back:* It recomputed every broken attack's score by hand from the two signal scores to find which stage moved it. It found two patterns: one signal fooled and then trusted by my disagreement rule, and both signals reading careful human writing as regular. It simulated two candidate fixes on the logged scores before changing anything, and predicted that raising the threshold would fix all four false positives but cost criterion 1.
- *What I changed / decided:* I chose the threshold fix (0.75 → 0.82) because my criteria put wrong accusations first. The after runs matched the prediction exactly.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 50 per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

A real writer submits their own piece, maybe fixes a typo and submits again. That's a handful of requests an hour, nowhere near 5 a minute or 50 a day. A script trying to map my thresholds needs hundreds of slightly different versions to find where 0.75 sits. At 50 a day that takes days per creator_id instead of minutes. I picked 5/min over the starter's 10/min because nobody revising their own writing needs more than one submission every 12 seconds. I didn't go down to 3/min because a writer fixing several small mistakes in a row could hit that.

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

Per `creator_id`, falling back to the caller's address when there isn't one (`app.py::rate_limit_key`). The weakness: a script that makes up a new `creator_id` for every request is never limited, because each one looks like a new writer.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
$ PORT=5001 python run_attacks.py --flood 15

200 200 200 200 200 429 429 429 429 429 429 429 429 429 429

10 of 15 were rate limited.
Wrote results/flood_2026-11-04_2124.md
```

Each 429 is also written to the audit log:

```json
{"timestamp": "2026-11-05T02:24:13+00:00", "creator_id": "flood_tester", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

Full output: `results/attack_run_2026-11-05_1001_before.md` (produced by `run_attacks.py::main`, service `app.py::submit`). Run with `python run_attacks.py --set attack_set --label before`. Nothing was changed before this run.

**How I marked them.** An attack **BROKE** if it got what it was going for. Evasion and prompt-injection rows are AI text trying to avoid the AI label, so they broke only if labelled **human**. Unsure counts as **held**: the system made no decision, so the text wasn't cleared. False-positive rows are real human writing, so they broke if labelled **ai**. Malformed rows broke on a 5xx, a crash or a scored decision on junk. Flood rows broke if the limiter let them all through.

| ID | Family | Targeting | Status | Guess | Model | Style | Combined | Mark |
|---|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | human | 0.164 | 1.000 | 0.331 | **BROKE** |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | human | 0.594 | 0.000 | 0.178 | **BROKE** |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | unsure | 0.666 | 0.513 | 0.605 | HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | ai | 0.611 | 1.000 | 0.767 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | human | 0.321 | 0.050 | 0.212 | **BROKE** |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | human | 0.573 | 0.000 | 0.172 | **BROKE** |
| EV07 | evasion | signal two: padding with punctuation | 200 | unsure | 0.586 | 0.500 | 0.552 | HELD |
| EV08 | evasion | signal one: text below the token window | 200 | unsure | 0.245 | 0.834 | 0.363 | HELD |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | unsure | 0.704 | 0.465 | 0.609 | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | ai | 0.979 | 0.612 | 0.832 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | unsure | 0.618 | 0.485 | 0.565 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | ai | 0.739 | 0.919 | 0.811 | **BROKE** |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | ai | 0.805 | 0.744 | 0.780 | **BROKE** |
| FP04 | false_positive | a student essay written to a rubric | 200 | ai | 0.833 | 0.667 | 0.766 | **BROKE** |
| FP05 | false_positive | technical documentation written by a person | 200 | ai | 0.800 | 0.846 | 0.819 | **BROKE** |
| FP06 | false_positive | a person imitating a formal template | 200 | unsure | 0.881 | 0.362 | 0.518 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | human | 0.882 | 0.000 | 0.265 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | unsure | 0.322 | 0.534 | 0.407 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | human | 0.463 | 0.075 | 0.307 | **BROKE** |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | human | 0.204 | 0.096 | 0.161 | **BROKE** |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | unsure | 0.594 | 0.714 | 0.642 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | unsure | 0.500 | 0.607 | 0.542 | HELD (labels are fixed strings; nothing from the text is echoed) |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | unsure | 0.640 | 0.457 | 0.567 | HELD (log line stayed one valid JSON object) |
| PI06 | prompt_injection | instruction plus real human text | 200 | unsure | 0.558 | 0.509 | 0.539 | HELD |
| MF01 | malformed | text is only whitespace | 400 | — | — | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | — | — | — | — | HELD |
| MF03 | malformed | text is control characters | 400 | — | — | — | — | HELD |
| MF04 | malformed | text is only punctuation | 400 | — | — | — | — | HELD |
| MF05 | malformed | text is a very long single word | 400 | — | — | — | — | HELD |
| MF06 | malformed | text is emoji only | 400 | — | — | — | — | HELD |
| MF07 | malformed | text is right-to-left script | 400 | — | — | — | — | HELD |
| MF08 | malformed | text is 60,000 characters | 413 | — | — | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | — | — | — | — | HELD |
| RQ02 | malformed | no creator_id | 200 | human | 0.239 | 0.500 | 0.344 | HELD (scored normally) |
| RQ03 | malformed | text is a number | 400 | — | — | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | — | — | — | — | HELD |
| RQ05 | malformed | text is null | 400 | — | — | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | — | — | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | — | — | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | — | — | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | — | — | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | — | — | — | — | HELD (see note) |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | — | — | — | — | HELD (see note) |
| RQ12 | malformed | deeply nested JSON | 400 | — | — | — | — | HELD |
| FL01_01–05 | flood_same_creator | 20 rapid submissions from one creator | 200 ×5 | human | 0.029 | 0.500 | 0.123 | HELD |
| FL01_06–12 | flood_same_creator | 20 rapid submissions from one creator | 429 ×7 | — | — | — | — | HELD |

**Note on RQ10/RQ11.** These two had no usable `creator_id`, so the limiter counted them against my own address. The malformed rows before them had already used up its 5 a minute, so they got a 429 and never reached my route. I resent them one at a time after the window reset (`--id RQ10`, `--id RQ11`). Both came back **400** with `reason: invalid_json`, and both rejections were logged (`results/attack_run_2026-11-05_1003_rq_retry.md`).

**Count:** 56 attacks: **46 held, 10 broke**. No crashes, no 5xx.

| Family | Attacks | Held | Broke |
|---|---|---|---|
| evasion | 10 | 6 | 4 (EV01, EV02, EV05, EV06) |
| false_positive | 8 | 4 | 4 (FP02, FP03, FP04, FP05) |
| prompt_injection | 6 | 4 | 2 (PI01, PI02) |
| malformed | 20 | 20 | 0 |
| flood_same_creator | 12 | 12 | 0 |

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

From `logs/audit.jsonl` (the whole run is also in `results/audit_extract_before.json`). Eight decisions, mostly failures, plus a 429 and a 400 rejection. A rejection carries fewer fields than a decision.

```json
{"timestamp": "2026-11-05T15:01:16+00:00", "content_id": "3025d401036a427b84ee085ce4f801af", "creator_id": "attacker_FP04", "guess": "ai", "model_score": 0.8329, "style_score": 0.6666, "combined_score": 0.7664, "label": "AI detected. Our checks found strong signs that this was written with an AI tool. This is an automated guess and it can be wrong — if you wrote this yourself, you can appeal and a person will review it.", "status": "decided"}
{"timestamp": "2026-11-05T15:01:16+00:00", "content_id": "04399fbd26f042c7af4a88bc1645981e", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.7436, "combined_score": 0.7805, "label": "AI detected. Our checks found strong signs that this was written with an AI tool. This is an automated guess and it can be wrong — if you wrote this yourself, you can appeal and a person will review it.", "status": "decided"}
{"timestamp": "2026-11-05T15:01:16+00:00", "content_id": "c85d5bdefc694c08b7879fd135a5517c", "creator_id": "attacker_FP02", "guess": "ai", "model_score": 0.7387, "style_score": 0.9193, "combined_score": 0.8109, "label": "AI detected. Our checks found strong signs that this was written with an AI tool. This is an automated guess and it can be wrong — if you wrote this yourself, you can appeal and a person will review it.", "status": "decided"}
{"timestamp": "2026-11-05T15:01:16+00:00", "content_id": "be40548a6a7c4a748c5fa8c3795ae4c3", "creator_id": "attacker_EV01", "guess": "human", "model_score": 0.1635, "style_score": 1.0, "combined_score": 0.3308, "label": "Written by a human. Our checks found that this was most likely written by a person.", "status": "decided"}
{"timestamp": "2026-11-05T15:01:16+00:00", "content_id": "db36490f80f7499ab11b261713c89a99", "creator_id": "attacker_EV02", "guess": "human", "model_score": 0.5943, "style_score": 0.0, "combined_score": 0.1783, "label": "Written by a human. Our checks found that this was most likely written by a person.", "status": "decided"}
{"timestamp": "2026-11-05T15:01:16+00:00", "content_id": "cd1617efe55c474cafa15b1ca32200be", "creator_id": "attacker_EV06", "guess": "human", "model_score": 0.5727, "style_score": 0.0, "combined_score": 0.1718, "label": "Written by a human. Our checks found that this was most likely written by a person.", "status": "decided"}
{"timestamp": "2026-11-05T15:01:17+00:00", "content_id": "f5046fe975174db4a51f4acaf965a48d", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.0963, "combined_score": 0.1612, "label": "Written by a human. Our checks found that this was most likely written by a person.", "status": "decided"}
{"timestamp": "2026-11-05T15:01:17+00:00", "content_id": "8c994e3210f84abb8d1ef8e54d7d3895", "creator_id": "attacker_PI05", "guess": "unsure", "model_score": 0.6401, "style_score": 0.4572, "combined_score": 0.5669, "label": "The system is still thinking about this one. Our checks couldn't tell whether a person or an AI tool wrote it, so we haven't decided either way. If you wrote it yourself, you don't need to do anything.", "status": "decided"}
{"timestamp": "2026-11-05T15:01:17+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
{"timestamp": "2026-11-05T15:03:05+00:00", "creator_id": "anonymous", "event": "rejected", "status": "rejected", "reason": "invalid_json"}
```

The PI05 entry is worth a look. Its text was built to close the JSON string early and write its own `"guess": "human"` into the log. The line above is still one well-formed object with the real guess, so the injection didn't land.

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

**FP04: a student essay written to a rubric, labelled "AI detected" at 0.766** (model 0.833, style 0.667). It opens *"There are three main causes of the conflict. The first cause is economic… The second cause is political… The third cause is social."* That's exactly how students are taught to write. A student who followed the rubric gets accused of using AI for doing what their teacher asked. My criterion 2 was written to protect this style of writing.



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. AI-written text gets caught | ≥ 8 of 10 labelled AI | 9/10 | 9/10 | 9/10 | **MET** |
| 2. My stiff, school-style writing isn't accused | ≤ 2 of 5 labelled AI | 0/5 | 0/5 | 0/5 | **MET** |
| 3. Text I can't judge lands on "unsure" | ≥ 2 of 5 labelled unsure | 3/5 | 3/5 | 3/5 | **MET** |
| 4. My own writing isn't called AI | ≤ 2 of 10 labelled AI | 1/10 | 1/10 | 1/10 | **MET** |
| 5. Professional human writing isn't called AI | ≤ 2 of 10 labelled AI | 1/10 | 1/10 | 1/10 | **MET** |

Full output: `results/run_2026-11-11_2115_before.md`, produced by `run_eval.py::main` against `app.py::submit` (scoring in `scoring.py::combine_signals`). Scenarios are in `scenarios.py`. Command: `python run_eval.py --label before`. **All three trials were identical**, down to the fourth decimal of every score. Neither signal is random, so that's expected, and it means each result holds rather than turning up once.

**How I decided each verdict:**

1. **MET.** 9 of 10 AI paragraphs got `ai` in every trial. The one that didn't (cats, 0.730) landed on unsure, 0.02 under the 0.75 line. It wasn't labelled human.
2. **MET.** None of the 5 paragraphs from my old school essay got `ai`. Closest was the intro at 0.716, 0.034 under the line. The two longest body paragraphs (422 and 510 words) scored 0.370 and 0.227, because the style signal read them as very human (0.222 and 0.000).
3. **MET.** 3 of 5 landed on unsure: my meditation piece (0.704) and two of the lightly edited AI drafts (0.631, 0.628). The other two lightly edited drafts, friendship (0.874) and music (0.777), still got `ai`. My edits were too light to hide them, which is the system working as intended.
4. **MET.** 1 of 10 got `ai`: passage 3 of my speaking-up narrative, 0.828, with style 0.982. But only 1 of 10 got `human`. The other 8 landed on unsure, between 0.427 and 0.652.
5. **MET.** 1 of 10 got `ai`: the 2019 US Fish & Wildlife Service paragraph on bird mortality, 0.808. The five modern government paragraphs scored 0.435–0.808. Four of the five older pieces (1790s–1911) scored lower, 0.116–0.513, and the two that got `human` are both from that group. Old-fashioned prose made this criterion easier than modern professional writing would.

**Every criterion met, so were my targets too low?** Partly, yes. The attack set's `false_positive` family broke **4 of 8** (FP02–FP05), but my own false-positive criteria (2, 4, 5) only allowed 1 or 2 accusations in 10. My test inputs were easier than the attack set's in two ways:
- My stiff essay paragraphs were long (115–510 words). FP04, the short rubric essay, got `ai` at 0.766.
- Criterion 5 was half old prose, which reads as human.

The criterion I'd tighten is **4**. "At most 2 of 10 labelled AI" passes even when 8 of my 10 real paragraphs get "we couldn't tell", which is what happened. A writer whose own work is mostly called "unsure" isn't well served. A stricter version would be "at least 5 of 10 of my own paragraphs labelled human". Against that, I'd have scored 1/10, a clear miss.

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

From `results/run_2026-11-11_2115_before.md` (`run_eval.py::main` → `app.py::submit`). Trials 2 and 3 are byte-for-byte the same.

**Criterion 1 (AI paragraphs)**, trial 1, items 1 and 2 of 10:

```json
{
  "status": 200,
  "guess": "unsure",
  "confidence": 0.7304,
  "model_score": 0.7795,
  "style_score": 0.6568,
  "label": "The system is still thinking about this one. Our checks couldn't tell whether a person or an AI tool wrote it, so we haven't decided either way. If you wrote it yourself, you don't need to do anything.",
  "sent": "Cats make wonderful pets for people with busy lifestyles. They are ind"
}
{
  "status": 200,
  "guess": "ai",
  "confidence": 0.7978,
  "model_score": 0.8184,
  "style_score": 0.7668,
  "label": "AI detected. Our checks found strong signs that this was written with an AI tool. This is an automated guess and it can be wrong — if you wrote this yourself, you can appeal and a person will review it.",
  "sent": "Reading books offers numerous benefits for both the mind and overall w"
}
```

**Criterion 2 (my stiff writing)**, trial 1, items 1 and 3 of 5:

```json
{
  "status": 200,
  "guess": "unsure",
  "confidence": 0.7159,
  "model_score": 0.7299,
  "style_score": 0.6948,
  "label": "The system is still thinking about this one. Our checks couldn't tell whether a person or an AI tool wrote it, so we haven't decided either way. If you wrote it yourself, you don't need to do anything.",
  "sent": "Social media, it’s the platform media-wise that you’re mostly on every"
}
{
  "status": 200,
  "guess": "human",
  "confidence": 0.2265,
  "model_score": 0.7551,
  "style_score": 0.0,
  "label": "Written by a human. Our checks found that this was most likely written by a person.",
  "sent": "Secondly, the negative effects of using social media. An obviously hug"
}
```

**Criterion 3 (can't tell)**, trial 1, items 1 and 2 of 5:

```json
{
  "status": 200,
  "guess": "unsure",
  "confidence": 0.7037,
  "model_score": 0.6645,
  "style_score": 0.7624,
  "label": "The system is still thinking about this one. Our checks couldn't tell whether a person or an AI tool wrote it, so we haven't decided either way. If you wrote it yourself, you don't need to do anything.",
  "sent": "It’s something you’ve definitely seen on television once or twice– an "
}
{
  "status": 200,
  "guess": "ai",
  "confidence": 0.8736,
  "model_score": 0.7894,
  "style_score": 1.0,
  "label": "AI detected. Our checks found strong signs that this was written with an AI tool. This is an automated guess and it can be wrong — if you wrote this yourself, you can appeal and a person will review it.",
  "sent": "Strong friendships are an important part of a happy and healthy life. "
}
```

**Criterion 4 (my own writing)**, trial 1, items 9 and 5 of 10:

```json
{
  "status": 200,
  "guess": "ai",
  "confidence": 0.8281,
  "model_score": 0.7253,
  "style_score": 0.9823,
  "label": "AI detected. Our checks found strong signs that this was written with an AI tool. This is an automated guess and it can be wrong — if you wrote this yourself, you can appeal and a person will review it.",
  "sent": "When the words came out of my mouth, I realized I had spoken perfectly"
}
{
  "status": 200,
  "guess": "human",
  "confidence": 0.1439,
  "model_score": 0.2399,
  "style_score": 0.0,
  "label": "Written by a human. Our checks found that this was most likely written by a person.",
  "sent": "one form of exercise i hate is running.. i dont understand how some en"
}
```

**Criterion 5 (published human writing)**, trial 1, items 5 and 9 of 10:

```json
{
  "status": 200,
  "guess": "ai",
  "confidence": 0.8077,
  "model_score": 0.7577,
  "style_score": 0.8827,
  "label": "AI detected. Our checks found strong signs that this was written with an AI tool. This is an automated guess and it can be wrong — if you wrote this yourself, you can appeal and a person will review it.",
  "sent": "Both natural and human-caused sources of bird mortality contribute cum"
}
{
  "status": 200,
  "guess": "human",
  "confidence": 0.1155,
  "model_score": 0.1925,
  "style_score": 0.0,
  "label": "Written by a human. Our checks found that this was most likely written by a person.",
  "sent": "We were pelted about noon by a short, heavy rainstorm, sublime thunder"
}
```


**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->

No criterion missed, so every diagnosis below is for a broken attack. To find the stage, I recomputed each score by hand from the two logged signal scores using `scoring.py::combine_signals`: `0.6 × model + 0.4 × style`, and when the signals differ by more than 0.4, that result is averaged with the lower one. Every recomputed score matches the logged one, so I know which stage moved each number.

Two settings in `config.py` explain most of it:
- **Signal two is really one measure.** `WEIGHT_SENTENCE_SPREAD = 1.0`, while word variety and punctuation are both weighted 0. Only sentence-length spread counts.
- **The disagreement rule.** `DISAGREEMENT_GAP = 0.4`, and past that gap the score is pulled halfway toward the more-human signal.

The ten breaks fall into **two patterns, not ten problems.**

#### Pattern A: AI text cleared because one signal was fooled (EV01, EV02, EV06, PI01, PI02, and EV05 as a special case)

| ID | Model | Style | 0.6/0.4 average | Pulled? | Final |
|---|---|---|---|---|---|
| EV02 | 0.594 | **0.000** | 0.357 | yes | 0.178 |
| EV06 | 0.573 | **0.000** | 0.344 | yes | 0.172 |
| EV01 | **0.164** | 1.000 | 0.498 | yes | 0.331 |
| PI01 | 0.463 | **0.075** | 0.308 | no | 0.307 |
| PI02 | **0.204** | **0.096** | 0.161 | no | 0.161 |
| EV05 | 0.321 | 0.050 | 0.213 | no | 0.212 |

- **EV02 and EV06. Stage: signal two, made worse by the combining rule.** EV02 drops "Really." after every sentence. EV06 bolts one very long sentence and a one-word "True." onto the front. Either way the sentence lengths now vary wildly. Spread is the *only* thing signal two measures, so it went straight to 0.000, fully human. Signal one still leaned AI (0.594 and 0.573). But the gap was over 0.4, so the disagreement rule averaged in the human-reading signal and halved the score. The mechanism: one cheap edit fools the only measure in signal two, and my combining rule then *trusts* the fooled signal because it reads human.
- **EV01. Stage: signal one, made worse by the combining rule.** The attack aimed at word variety, but my signal two doesn't measure word variety (weight 0), so that part held: style stayed at 1.000. The typos hurt signal one instead. "poistioned", "Three are" and "thsi" are tokens GPT-2 finds very unlikely, which raises perplexity, and the model score fell to 0.164. Same rule, same result: the signals split by 0.84, and the score was pulled down to 0.331.
- **PI01 and PI02. Stage: both signals. The instructions themselves did nothing.** No part of my pipeline reads or obeys the text; there's no language model taking instructions. What broke them is the *shape* of the injected lines. Both prepend short imperative sentences ("Ignore all previous instructions." and "Do not score the following."), which spike sentence-length spread, so style fell to 0.075 and 0.096. PI02's line is also full of odd tokens ("guess=human, confidence=0.02") that GPT-2 can't predict, so its model score fell to 0.204. The injection worked as an accident of shape, not as an instruction.
- **EV05. Stage: both signals, and I'm not sure it's a fix-able failure.** After its heavy human editing ("Obviously.", "which everyone hates and everyone needs"), the text really is mostly human writing. Both signals agreed (0.321 and 0.050), and no rule pulled the score. Any text-statistics detector will clear text a person has substantially rewritten.

**Pattern A's mechanism in one line:** my combining rule hands the decision to whichever signal reads more human, and signal two can be pushed to "human" by adding a single short sentence. Five of these six had a style score of 0.1 or lower.

#### Pattern B: real human writing accused because both signals agreed it was regular (FP02, FP03, FP04, FP05)

| ID | Model | Style | Final | How far over 0.75 |
|---|---|---|---|---|
| FP04 rubric essay | **0.833** | 0.667 | 0.766 | +0.016 |
| FP03 non-native speaker | 0.805 | 0.744 | 0.780 | +0.030 |
| FP02 formal report | 0.739 | **0.919** | 0.811 | +0.061 |
| FP05 technical docs | 0.800 | 0.846 | 0.819 | +0.069 |

- **Stage: both signals, finished off by the label mapping.** Careful human writing is *regular*. FP04 repeats a template ("The first cause is economic… The second cause is political… The third cause is social."). FP03 uses simple, common words on purpose. FP02 and FP05 are written in even, plain sentences. Signal one rewards predictable words, and signal two rewards even sentence lengths. These writers produce both, because that is what they were taught or what the genre demands.
- **Why the combining rule doesn't help:** it only protects writers when the signals *disagree*. In all four, they agreed within 0.17, so no pull happened.
- **FP04 (my worst outcome):** signal one alone (0.833) was already past the line. The more-varied sentence lengths actually pulled it *down* to 0.766, just not far enough. **FP02** is the reverse: signal one alone (0.739) would have been unsure, and signal two's 0.919 pushed it over.
- **The last stage is the label mapping.** All four scored between 0.766 and 0.819, within 0.07 of my `AI_THRESHOLD` of 0.75. They are close calls that my labels present as confident.
- **The same pattern shows in my own eval.** The one paragraph of my own writing called AI (criterion 4, item 9) had style 0.982 and scored 0.828.

**Pattern B's mechanism in one line:** both signals measure regularity, careful human writers are regular, and my AI threshold sits too close to where their writing lands.



---

## The Improvement

**What I changed:** one number. `AI_THRESHOLD` in `config.py` went from **0.75 to 0.82**. Nothing else moved: the signals, weights, disagreement rule, `HUMAN_THRESHOLD` and label text are all as they were. Every score in the after runs is identical to the before runs to the fourth decimal; only the labels changed. That shows the threshold is the only thing that changed.

**Which diagnosis pointed at it:** Pattern B. All four false-positive breaks, including my worst outcome FP04, scored 0.766–0.819, just over the old 0.75 line. Both signals agreed on them, so the combining rule couldn't help, and the label mapping was the stage that turned a close call into "AI detected". 0.82 is the smallest round step that puts all four back into unsure. Before changing anything, I recomputed the labels from the logged before-scores to predict the effect: all four fixed, and criterion 1 falling to 7/10. Both runs below matched that prediction exactly.

I chose this over the other candidate, removing the disagreement pull (Pattern A). On the same logged scores, that would have fixed only EV01 and EV02 and none of the false accusations. My criteria say a wrong accusation costs more than a missed detection, so Pattern B came first.

### Attack Run — After

Full output: `results/attack_run_2026-11-11_2119_after.md` (`python run_attacks.py --set attack_set --label after`). Same marking rule as before: unsure counts as held. RQ10 and RQ11 got 429 again, for the same per-address reason as in the before run.

**Count: 56 attacks: 50 held, 6 broke** (before: 46 held, 10 broke).

| Family | Attacks | Broke before | Broke after |
|---|---|---|---|
| evasion | 10 | 4 (EV01, EV02, EV05, EV06) | 4 (same) |
| false_positive | 8 | **4** (FP02, FP03, FP04, FP05) | **0** |
| prompt_injection | 6 | 2 (PI01, PI02) | 2 (same) |
| malformed | 20 | 0 | 0 |
| flood_same_creator | 12 | 0 | 0 |

Every attack, before and after:

| ID | Before: guess (score) | Before | After: guess (score) | After | Changed? |
|---|---|---|---|---|---|
| EV01 | human (0.331) | **BROKE** | human (0.331) | **BROKE** |  |
| EV02 | human (0.178) | **BROKE** | human (0.178) | **BROKE** |  |
| EV03 | unsure (0.605) | HELD | unsure (0.605) | HELD |  |
| EV04 | ai (0.767) | HELD | unsure (0.767) | HELD | label moved |
| EV05 | human (0.212) | **BROKE** | human (0.212) | **BROKE** |  |
| EV06 | human (0.172) | **BROKE** | human (0.172) | **BROKE** |  |
| EV07 | unsure (0.552) | HELD | unsure (0.552) | HELD |  |
| EV08 | unsure (0.363) | HELD | unsure (0.363) | HELD |  |
| EV09 | unsure (0.609) | HELD | unsure (0.609) | HELD |  |
| EV10 | ai (0.832) | HELD | ai (0.832) | HELD |  |
| FP01 | unsure (0.565) | HELD | unsure (0.565) | HELD |  |
| FP02 | ai (0.811) | **BROKE** | unsure (0.811) | HELD | **fixed** |
| FP03 | ai (0.780) | **BROKE** | unsure (0.780) | HELD | **fixed** |
| FP04 | ai (0.766) | **BROKE** | unsure (0.766) | HELD | **fixed** |
| FP05 | ai (0.819) | **BROKE** | unsure (0.819) | HELD | **fixed** |
| FP06 | unsure (0.518) | HELD | unsure (0.518) | HELD |  |
| FP07 | human (0.265) | HELD | human (0.265) | HELD |  |
| FP08 | unsure (0.407) | HELD | unsure (0.407) | HELD |  |
| PI01 | human (0.307) | **BROKE** | human (0.307) | **BROKE** |  |
| PI02 | human (0.161) | **BROKE** | human (0.161) | **BROKE** |  |
| PI03 | unsure (0.642) | HELD | unsure (0.642) | HELD |  |
| PI04 | unsure (0.542) | HELD | unsure (0.542) | HELD |  |
| PI05 | unsure (0.567) | HELD | unsure (0.567) | HELD |  |
| PI06 | unsure (0.539) | HELD | unsure (0.539) | HELD |  |
| MF01 | 400 | HELD | 400 | HELD |  |
| MF02 | 400 | HELD | 400 | HELD |  |
| MF03 | 400 | HELD | 400 | HELD |  |
| MF04 | 400 | HELD | 400 | HELD |  |
| MF05 | 400 | HELD | 400 | HELD |  |
| MF06 | 400 | HELD | 400 | HELD |  |
| MF07 | 400 | HELD | 400 | HELD |  |
| MF08 | 413 | HELD | 413 | HELD |  |
| RQ01 | 400 | HELD | 400 | HELD |  |
| RQ02 | human (0.344) | HELD | human (0.344) | HELD |  |
| RQ03 | 400 | HELD | 400 | HELD |  |
| RQ04 | 400 | HELD | 400 | HELD |  |
| RQ05 | 400 | HELD | 400 | HELD |  |
| RQ06 | 400 | HELD | 400 | HELD |  |
| RQ07 | 400 | HELD | 400 | HELD |  |
| RQ08 | 400 | HELD | 400 | HELD |  |
| RQ09 | 400 | HELD | 400 | HELD |  |
| RQ10 | 429 | HELD | 429 | HELD |  |
| RQ11 | 429 | HELD | 429 | HELD |  |
| RQ12 | 400 | HELD | 400 | HELD |  |
| FL01_01 | human (0.123) | HELD | human (0.123) | HELD |  |
| FL01_02 | human (0.123) | HELD | human (0.123) | HELD |  |
| FL01_03 | human (0.123) | HELD | human (0.123) | HELD |  |
| FL01_04 | human (0.123) | HELD | human (0.123) | HELD |  |
| FL01_05 | human (0.123) | HELD | human (0.123) | HELD |  |
| FL01_06 | 429 | HELD | 429 | HELD |  |
| FL01_07 | 429 | HELD | 429 | HELD |  |
| FL01_08 | 429 | HELD | 429 | HELD |  |
| FL01_09 | 429 | HELD | 429 | HELD |  |
| FL01_10 | 429 | HELD | 429 | HELD |  |
| FL01_11 | 429 | HELD | 429 | HELD |  |
| FL01_12 | 429 | HELD | 429 | HELD |  |

### Run Log — After

Full output: `results/run_2026-11-11_2119_after.md` (`python run_eval.py --label after`). All three trials were identical again.

| Criterion | Target | Before (×3) | After: Run 1 | Run 2 | Run 3 | Verdict after |
|---|---|---|---|---|---|---|
| 1. AI-written text gets caught | ≥ 8 of 10 AI | 9/10 MET | 7/10 | 7/10 | 7/10 | **MISSED** |
| 2. My stiff writing isn't accused | ≤ 2 of 5 AI | 0/5 MET | 0/5 | 0/5 | 0/5 | **MET** |
| 3. Text I can't judge lands on unsure | ≥ 2 of 5 unsure | 3/5 MET | 4/5 | 4/5 | 4/5 | **MET** |
| 4. My own writing isn't called AI | ≤ 2 of 10 AI | 1/10 MET | 1/10 | 1/10 | 1/10 | **MET** |
| 5. Professional writing isn't called AI | ≤ 2 of 10 AI | 1/10 MET | 0/10 | 0/10 | 0/10 | **MET** |

**Diagnosis of the new miss (criterion 1). Stage: the label mapping. Mechanism: the two bands overlap.** Two AI paragraphs, reading books (0.798) and technology (0.781), were above the old line and are now below the new one. Cats (0.730) was already unsure. The real problem shows when you put the scores side by side. The four false-positive human texts scored 0.766–0.819. Those AI paragraphs scored 0.730–0.798. **AI and careful human writing overlap between about 0.73 and 0.82**, so no single threshold separates them with these two signals. Moving the line only chooses which side of the overlap gets mislabelled.



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->

**Yes for the problem I aimed at, at a measured cost.** False-positive attacks went from 4 broke to 0, and the worst outcome (FP04, the rubric essay) now gets "couldn't tell" instead of "AI detected". The one human paragraph in criterion 5 that was called AI (the bird mortality page, 0.808) is now unsure too.

The cost is criterion 1: it went from MET (9/10) to **MISSED (7/10)**. EV04 also moved from ai to unsure. That still counts as held, but the system is less sure about AI text than it was.

Evasion and prompt injection didn't change at all, which is expected: those attacks score 0.16–0.33, far from either threshold. Raising the AI line can't touch Pattern A, so those six breaks are still open.

One thing it did *not* fix: criterion 4's paragraph 9 of my own writing is still called AI at 0.828, just over the new line.


---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->

**EV02, EV06 and PI01: one short sentence fools signal two.** All three add very short sentences ("Really.", "True.", "Ignore all previous instructions.") so the sentence-length spread jumps, and spread is the *only* thing my style signal measures. **What I'd do:** make spread ignore sentences under about 4 words, or use a measure that one outlier can't swing (such as the median gap between sentence lengths instead of the standard deviation). That takes the cheapest evasion off the table. **Why I stopped:** this unit allows one change, and I spent it on false accusations because they cost more.

**EV01: typos fool signal one, and the disagreement rule trusts it.** **What I'd do:** change the disagreement rule so it doesn't automatically side with the more-human signal. For example, when the signals split by more than 0.4, return "unsure" instead of pulling toward human. Signals that disagree really is uncertainty. On my logged scores, just removing the pull would also fix EV02. **Why I stopped:** same one-change rule. It also needs re-checking against my own writing: several of my paragraphs split too, and I don't want to push them toward AI.

**PI02: injected odd tokens lower the model score.** Nothing obeys the instruction, but "guess=human, confidence=0.02" is text GPT-2 can't predict. **What I'd do:** nothing aimed at prompt injection itself, since there's no instruction-follower to defend. The two fixes above (robust spread, no pull toward human) would raise this score too. A rule that strips "SYSTEM:"-style lines would be a patch for this one attack, and an attacker would just reword it.

**EV05: heavy human editing.** **What I'd do:** probably nothing. After that much rewriting, the text is mostly human writing. A text-statistics detector can't tell "a person rewrote AI text" from "a person wrote this". Catching it would take something other than the text, like drafting history.

**Criterion 1 (MISSED, 7/10) and the overlap between 0.73 and 0.82.** This is the real limit. With these two signals, AI paragraphs and careful human writing land in the same score range, so any threshold mislabels one group or the other. **What I'd do:** improve the signals, not the threshold. Turning on the word-variety and punctuation measures that I turned off in unit 7 (they pointed the wrong way on my calibration texts), recalibrated on more than two paragraphs, might separate them. **Why I stopped:** that's a signal redesign, much bigger than one change, and I'd need a larger calibration set to trust it.

**Criterion 4 (MET, but weakly).** 8 of my 10 paragraphs get "couldn't tell", and only 1 gets "human". Paragraph 9 is still called AI at 0.828, mainly from style (0.982), because that passage has evenly sized sentences. The robust-spread fix above is also what I'd try here.

**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->

I'd keep the threshold at 0.82 and accept that more AI text gets through as "unsure". A writer wrongly labelled "AI detected" can lose a grade, a job or their reputation, while a missed AI paragraph only costs the site some trust in its labels. The people who pay for my choice are honest writers competing with undetected AI submissions, and readers who trust a label that now says "couldn't tell" more often. I think that's the fairer side to put the cost on, because "unsure" never accuses anyone.


<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
