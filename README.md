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

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

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



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



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
