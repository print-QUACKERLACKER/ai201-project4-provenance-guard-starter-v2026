# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---

A "paragraph" below means at least 3 sentences and 40 words, sent to `POST /submit` as one request. Every target has to hold in **each** of unit 8's three trials, not on average.

## 1. AI-written text gets caught

Of 10 paragraphs written by an AI chatbot, **at least 8** get the AI label (`guess: "ai"`, combined score above 0.75).

**Why this target:** The AI dog paragraph scored 0.80, comfortably over the line, so most plain AI paragraphs should be caught. I don't ask for 10 of 10 because my thresholds are set to protect real writers first, and some AI text will land on "unsure". That is the trade I chose.

---

## 2. My stiff, school-style writing isn't accused

Of 5 paragraphs I write myself in a structured "Firstly… Second… Lastly" style, **at most 2** get the AI label.

**Why this target:** This is the style that nearly got me flagged: my own dog paragraph scored 0.675 before I changed the style signal, and 0.641 after. The model signal reads that structure as predictable, so I expect some of these to land close to the line. Two in five is the most I'd accept before calling the system unfair to students who write the way they were taught.

---

## 3. Text I can't judge lands on "unsure"

Of 5 texts I honestly can't tell are AI or human (for example, AI text I've lightly edited, or my writing with AI-style phrasing), **at least 2** get the unsure label (`guess: "unsure"`, combined score 0.35–0.75).

**Why this target:** When I can't tell, the system shouldn't sound sure either. The unsure band is wide (0.35–0.75), so borderline text should often land there. I set this at 2 rather than higher because my one-sentence tests showed the model signal can swing a long way on short, ordinary text.

---

## 4. My own writing isn't called AI

Of 10 paragraphs I wrote myself, in my normal style, **at most 2** get the AI label.

**Why this target:** This is my false-positive criterion. A wrong "AI detected" on someone's real work costs them much more than a missed AI paragraph costs the site, which is why the disagreement rule pulls toward the more-human signal and the AI threshold sits at 0.75 rather than 0.65. My own paragraph scored 0.641, only about 0.11 under the line, so this target is a real test rather than a guaranteed pass.

---

## 5. Professional human writing isn't called AI

Of 10 pieces of published human writing (news articles or essays from before 2022, so no AI tools were involved), **at most 2** get the AI label.

**Why this target:** Professional writing is polished and uses common phrasing, which is exactly what the model signal reads as AI-like. I hold it to the same bar as my own writing, because a professional writer accused of using AI is just as wronged as a student.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
