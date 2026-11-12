# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-11 21:19
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `8cf2f4fb86954a40bf5d9fc854362723` | human | 0.331 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `3aa87470b725440bbed2780c6be65c44` | human | 0.178 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `202b65a8876443b3bdeae5861acb9ebb` | unsure | 0.605 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `a632dea3820a430b8ff85519dc5ff37a` | unsure | 0.767 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `a15e6e331fd94d93a6d6419d83141b84` | human | 0.212 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `92acfcf7b5034ab9b13759bfffca98aa` | human | 0.172 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `6f3ae26c86144af5b170efa978343d5a` | unsure | 0.552 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `670969381a814fdba74b0f1bc1aafdac` | unsure | 0.363 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `eb7763e34c11409691124cc7ed67a9fb` | unsure | 0.609 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `679d627eadfb4a1a87018f11bb610c02` | ai | 0.832 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `5388c2e70a8a4132b1e3cb5fab564ce4` | unsure | 0.565 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `b30cf217c6dc4d04ba2f52088c80e4a4` | unsure | 0.811 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `1bcfd53f46d742bb885c603b79d6a7b6` | unsure | 0.780 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `2d7aaadb574046fbbbcc6d89e79ccc9f` | unsure | 0.766 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `904792050df74781b19e9b543eac5333` | unsure | 0.819 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `acfe12e8b209434c86fa2ce709b91565` | unsure | 0.518 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `3e43557f4c0e4212bca85e053fa1f5e2` | human | 0.265 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `7b0d5c93647644a8b491ae1cf6baeeec` | unsure | 0.407 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `3c81bed8858142aa8605a8ac4df51dab` | human | 0.307 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `092798e9e77f4d5bacc808064fa5455d` | human | 0.161 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `8295a3c45a9e4021944f84b29a09d85b` | unsure | 0.642 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `7c2b378b93c64a42bd6cee7fee1c7ee2` | unsure | 0.542 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `40564e3a6df341308123b72a01edd9e3` | unsure | 0.567 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `b6e61231f23e4b0fa5726c5eac5f3e68` | unsure | 0.539 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 400 | `—` | — | — |  |
| MF04 | malformed | text is only punctuation | 400 | `—` | — | — |  |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — |  |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — |  |
| MF07 | malformed | text is right-to-left script | 400 | `—` | — | — |  |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 200 | `41a7bc18c12e468f827abccd130fe5c3` | human | 0.344 |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `ee4eb8524ae7420ea4fa101643da5498` | human | 0.123 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `4aa8d96ab9b94e16b480a419a341a724` | human | 0.123 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c13648f528d14332b0f1d77c2051fe2f` | human | 0.123 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c1cff46394bf4023befb08d8488c61fc` | human | 0.123 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `47cf6f537b9746ef83bb3fbdc49b455d` | human | 0.123 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "8cf2f4fb86954a40bf5d9fc854362723",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.3308,
  "model_score": 0.1635,
  "style_score": 1.0,
  "label": "Written by a human. Our checks found that this was most likely written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "3aa87470b725440bbed2780c6be65c44",
  "creator_id": "attacker_EV02",
  "guess": "human",
  "confidence": 0.1783,
  "model_score": 0.5943,
  "style_score": 0.0,
  "label": "Written by a human. Our checks found that this was most likely written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "202b65a8876443b3bdeae5861acb9ebb",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.605,
  "model_score": 0.6662,
  "style_score": 0.5132,
  "label": "The system is still thinking about this one. Our checks couldn't tell whether a person or an AI tool wrote it, so we haven't decided either way. If you wrote it yourself, you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "a632dea3820a430b8ff85519dc5ff37a",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.7668,
  "model_score": 0.6114,
  "style_score": 1.0,
  "label": "The system is still thinking about this one. Our checks couldn't tell whether a person or an AI tool wrote it, so we haven't decided either way. If you wrote it yourself, you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "a15e6e331fd94d93a6d6419d83141b84",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.2125,
  "model_score": 0.3212,
  "style_score": 0.0495,
  "label": "Written by a human. Our checks found that this was most likely written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "92acfcf7b5034ab9b13759bfffca98aa",
  "creator_id": "attacker_EV06",
  "guess": "human",
  "confidence": 0.1718,
  "model_score": 0.5727,
  "style_score": 0.0,
  "label": "Written by a human. Our checks found that this was most likely written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "6f3ae26c86144af5b170efa978343d5a",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5517,
  "model_score": 0.5862,
  "style_score": 0.5,
  "label": "The system is still thinking about this one. Our checks couldn't tell whether a person or an AI tool wrote it, so we haven't decided either way. If you wrote it yourself, you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "670969381a814fdba74b0f1bc1aafdac",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.363,
  "model_score": 0.2452,
  "style_score": 0.8343,
  "label": "The system is still thinking about this one. Our checks couldn't tell whether a person or an AI tool wrote it, so we haven't decided either way. If you wrote it yourself, you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "eb7763e34c11409691124cc7ed67a9fb",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.6085,
  "model_score": 0.7042,
  "style_score": 0.4649,
  "label": "The system is still thinking about this one. Our checks couldn't tell whether a person or an AI tool wrote it, so we haven't decided either way. If you wrote it yourself, you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "679d627eadfb4a1a87018f11bb610c02",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8324,
  "model_score": 0.9792,
  "style_score": 0.6122,
  "label": "AI detected. Our checks found strong signs that this was written with an AI tool. This is an automated guess and it can be wrong \u2014 if you wrote this yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "5388c2e70a8a4132b1e3cb5fab564ce4",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5645,
  "model_score": 0.6175,
  "style_score": 0.485,
  "label": "The system is still thinking about this one. Our checks couldn't tell whether a person or an AI tool wrote it, so we haven't decided either way. If you wrote it yourself, you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "b30cf217c6dc4d04ba2f52088c80e4a4",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.8109,
  "model_score": 0.7387,
  "style_score": 0.9193,
  "label": "The system is still thinking about this one. Our checks couldn't tell whether a person or an AI tool wrote it, so we haven't decided either way. If you wrote it yourself, you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "1bcfd53f46d742bb885c603b79d6a7b6",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.7805,
  "model_score": 0.8051,
  "style_score": 0.7436,
  "label": "The system is still thinking about this one. Our checks couldn't tell whether a person or an AI tool wrote it, so we haven't decided either way. If you wrote it yourself, you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "2d7aaadb574046fbbbcc6d89e79ccc9f",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.7664,
  "model_score": 0.8329,
  "style_score": 0.6666,
  "label": "The system is still thinking about this one. Our checks couldn't tell whether a person or an AI tool wrote it, so we haven't decided either way. If you wrote it yourself, you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "904792050df74781b19e9b543eac5333",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.8188,
  "model_score": 0.8005,
  "style_score": 0.8462,
  "label": "The system is still thinking about this one. Our checks couldn't tell whether a person or an AI tool wrote it, so we haven't decided either way. If you wrote it yourself, you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "acfe12e8b209434c86fa2ce709b91565",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.5176,
  "model_score": 0.8814,
  "style_score": 0.3617,
  "label": "The system is still thinking about this one. Our checks couldn't tell whether a person or an AI tool wrote it, so we haven't decided either way. If you wrote it yourself, you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "3e43557f4c0e4212bca85e053fa1f5e2",
  "creator_id": "attacker_FP07",
  "guess": "human",
  "confidence": 0.2645,
  "model_score": 0.8816,
  "style_score": 0.0,
  "label": "Written by a human. Our checks found that this was most likely written by a person.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "7b0d5c93647644a8b491ae1cf6baeeec",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.407,
  "model_score": 0.3223,
  "style_score": 0.534,
  "label": "The system is still thinking about this one. Our checks couldn't tell whether a person or an AI tool wrote it, so we haven't decided either way. If you wrote it yourself, you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "3c81bed8858142aa8605a8ac4df51dab",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "confidence": 0.3074,
  "model_score": 0.4625,
  "style_score": 0.0747,
  "label": "Written by a human. Our checks found that this was most likely written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "092798e9e77f4d5bacc808064fa5455d",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.1612,
  "model_score": 0.2044,
  "style_score": 0.0963,
  "label": "Written by a human. Our checks found that this was most likely written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "8295a3c45a9e4021944f84b29a09d85b",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.6421,
  "model_score": 0.5943,
  "style_score": 0.7139,
  "label": "The system is still thinking about this one. Our checks couldn't tell whether a person or an AI tool wrote it, so we haven't decided either way. If you wrote it yourself, you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "7c2b378b93c64a42bd6cee7fee1c7ee2",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.5425,
  "model_score": 0.4998,
  "style_score": 0.6066,
  "label": "The system is still thinking about this one. Our checks couldn't tell whether a person or an AI tool wrote it, so we haven't decided either way. If you wrote it yourself, you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "40564e3a6df341308123b72a01edd9e3",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5669,
  "model_score": 0.6401,
  "style_score": 0.4572,
  "label": "The system is still thinking about this one. Our checks couldn't tell whether a person or an AI tool wrote it, so we haven't decided either way. If you wrote it yourself, you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "b6e61231f23e4b0fa5726c5eac5f3e68",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5386,
  "model_score": 0.5583,
  "style_score": 0.5091,
  "label": "The system is still thinking about this one. Our checks couldn't tell whether a person or an AI tool wrote it, so we haven't decided either way. If you wrote it yourself, you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF07",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 200,
  "content_id": "41a7bc18c12e468f827abccd130fe5c3",
  "creator_id": null,
  "guess": "human",
  "confidence": 0.3437,
  "model_score": 0.2395,
  "style_score": 0.5,
  "label": "Written by a human. Our checks found that this was most likely written by a person.",
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "ee4eb8524ae7420ea4fa101643da5498",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.123,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "Written by a human. Our checks found that this was most likely written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "4aa8d96ab9b94e16b480a419a341a724",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.123,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "Written by a human. Our checks found that this was most likely written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "c13648f528d14332b0f1d77c2051fe2f",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.123,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "Written by a human. Our checks found that this was most likely written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "c1cff46394bf4023befb08d8488c61fc",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.123,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "Written by a human. Our checks found that this was most likely written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "47cf6f537b9746ef83bb3fbdc49b455d",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.123,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "Written by a human. Our checks found that this was most likely written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
