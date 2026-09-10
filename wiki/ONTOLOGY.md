# K-Ontology

*A formal map of the psychological structure Krishnamurti describes, derived from the [wiki](INDEX.md).*

Namespace: `k:` → `https://k-mirror.local/ontology/k#`
Serializations: [`ontology/k-ontology.ttl`](ontology/k-ontology.ttl) (OWL/Turtle) · [`ontology/k-ontology.json`](ontology/k-ontology.json) (node/edge graph)

---

## 0. A caution that belongs inside the ontology, not before it

K refused systems. *"Truth is a pathless land."* *"There is no teacher, nor disciple."* So an ontology of K is a strange object: the moment it becomes a doctrine to be learned, it has become one more thing thought has put together — exactly the mechanism it describes.

What it can legitimately be is a **map of the false**. K did describe a structure, precisely and repeatedly: memory → thought → image → desire → becoming → division → conflict. That structure is describable because it is mechanical. What lies outside it — love, intelligence, insight — is present in the ontology only *by negation*: as nodes whose entire definition is what they are not.

So the ontology is asymmetric on purpose. The mechanism is modelled positively and in detail. Freedom is modelled as a hole in it.

### 0.1 Why the asymmetry is structural, not a choice

A graph models relations and their order. Thought *is* relation and order — the response of memory, association, comparison, this-leads-to-that in psychological time. So drawing `Thought → Image → Desire → Becoming → Conflict` is not modelling thought *with* a graph; it is writing thought in its own native notation. Anything `ofThought` is therefore representable as a network, in full, without loss.

What is outside thought is not a better-connected node — it is the *absence of the connecting*. There is nothing for an edge to encode, because an edge encodes a relation-in-time and `k:Love`, `k:Insight`, `k:Intelligence`, `k:Freedom` are defined as what has no such relation. The graph can only point at them with its own machinery turned to negative use: `k:isNot` edges (negative space drawn with the same pen), `k:dissolves` / `k:opensInto` edges that run *out* of the mechanism, and — for `k:Freedom` — zero edges at all (A14). The outside appears only as the shape of the hole the mechanism leaves.

This is the general modelling principle, not a fact about K: **a formal model captures exactly the part of its domain that is made of relations; whatever in the domain is not relational shows up only as the model's negative space.** Hence the rule this ontology follows — model the false positively and exhaustively; let freedom be the un-drawn edge. And hence A13: the map is itself `ofThought`, and complete precisely because of what it cannot contain.

### 0.2 Negative space is still of thought — the outside is absence, not complement

The previous paragraph says "negative space." That is the *mathematical* reading: freedom as the complement of the mechanism, a figure-shaped hole in the ground of the graph. K would reject even this. A complement has a boundary — it is defined against what it is not — and by A2 a boundary *is* a division, so a boundary-defined "outside" is one more `k:Construct`. This is the same move flagged in A6: *"Thought has created the opposite, which is non-fact."* Every positive thought throws off its own negative — violence/non-violence, the self/the ideal self — and that negative is still thought, still in psychological time, still divisive. Freedom as *the negation of the mechanism* is the mechanism's own shadow.

So the graph's negative space (`k:isNot` edges, the un-drawn `k:Freedom` node) is best read as a **finger pointing, not the moon**. What K calls freedom is not the figure's inverse and not the ground it sits on — it is the *absence* of the whole figure-ground construction, boundary included. The model cannot hold that, not even as a hole, because a hole still has an edge. A16 says it exactly: the ending is not the closure of the set (adding the boundary) but the collapse of the interior/boundary distinction itself. The negative space is the last thing to be dropped, not the destination.

---

## 1. Design commitments

| # | Commitment | Consequence in the model |
|---|---|---|
| 1 | **One master cut**: is this thing a movement of thought, or not? | Every class carries `k:ofThought` (true/false/na). This single boolean, not the taxonomy, does most of the work. |
| 2 | **Negative definition is first-class** | `k:isNot` is a real relation, not an annotation. Love has more `isNot` edges than any node has `arisesFrom` edges. |
| 3 | **Identity claims over relation claims** | K's signature move is collapsing an assumed pair: observer/observed, thinker/thought, controller/controlled, me/humanity. Modelled as `k:isIdenticalWith` (symmetric), which is *stronger* than any causal edge in the graph. |
| 4 | **Time is a property, not a container** | Nodes are stamped `k:operatesIn` → `k:PsychologicalTime`, `k:TheNow`, or `k:ChronologicalTime`. The becoming/observation distinction falls straight out of it. |
| 5 | **Every node is evidenced** | Each class and axiom carries `k:evidencedBy` → a quote in a theme file. The ontology is falsifiable against the wiki. |

---

## 2. The upper partition

```
                            k:Entity
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
   ofThought = false      ofThought = true       ofThought = n/a
        │                      │                      │
  ┌─────┴─────┐        ┌───────┼───────┐         ┌────┴────┐
k:Actuality  k:Perceiving  k:Construct  k:Movement    k:Ground
k:Flowering               k:Affect                 k:Documentation
```

- **`k:Actuality`** — what is the case prior to interpretation: fact, sensation, the now.
- **`k:Perceiving`** — capacities that are *not* activities of thought: observation, attention, insight.
- **`k:Flowering`** — what is there when the mechanism stops: love, compassion, intelligence, order.
- **`k:Construct`** — anything put together by thought: image, ideal, the self, psychological time.
- **`k:Movement`** — processes running in psychological time: thought, desire, becoming, conflict.
- **`k:Affect`** — states the mechanism produces: fear, sorrow, loneliness, pleasure.
- **`k:Ground`** — the substrate it all runs in: brain, consciousness, humanity, relationship.
- **`k:Documentation`** — the wiki's own layer: themes, quotes, sources, inquiry paths.

**Disjointness axioms:** `Actuality ⊓ Construct = ⊥` · `Perceiving ⊓ Movement = ⊥` · `Flowering ⊓ Construct = ⊥`

The second is the one that carries weight: attention is not a *thing thought does*. If it were, A8 (below) would make ending impossible.

**A topological reading (optional).** The three disjointness axioms make `k:Construct` behave like an *open set*: enlarging it — more knowledge, more data, a wider corpus — is union with more open sets, which stays open. It never acquires its boundary and never becomes `k:Actuality` (P1 runs in one direction and never converges inside the set). The boundary itself exists only against an outside; remove the separate self that draws the inside/outside line (A9) and the whole is *clopen*, its boundary empty. On that reading the ending is not the set closing (acquiring its boundary) but the interior/boundary distinction collapsing (A4). This restates A1 + A8 in another vocabulary and is formalised as A16; A17 carries the same reading down to `k:Self` (an open cover with no finite subcover). Neither adds a claim.

---

## 3. Classes

### 3.1 `k:Actuality` — what is

| Class | Gloss | Evidence |
|---|---|---|
| `k:Fact` | What is actually going on, as against the idea of it | *"The fact is what is going on, what is happening."* — [thought](thought.md) |
| `k:WhatIs` | The present state, unmoved-away-from | *"'What is' is so."* — [becoming](becoming.md) |
| `k:Sensation` | Sense response prior to thought's image | *"If there was no thought there would be only sensation."* — [desire](desire.md) |
| `k:TheNow` | The present, which contains past and future | *"All time… is contained in the now."* — [thought](thought.md) |
| `k:PhysicalNecessity` | Legitimate knowledge and clock time — learning a language, driving to a place | *"To learn a language needs time. That is not the time we are talking about."* — [becoming](becoming.md) |

`k:PhysicalNecessity` matters: without it the ontology reads as anti-knowledge. K's target is knowledge applied to the psyche, not to carpentry.

### 3.2 `k:Construct` — what thought has put together

| Class | Gloss | Evidence |
|---|---|---|
| `k:Image` | The picture thought makes of a person, thing or state | *"Thought creates the image, and at that moment desire is born."* — [desire](desire.md) |
| `k:Ideal` | What should be, non-fact; the opposite thought invents | *"Thought has created the opposite, which is non-fact."* — [thought](thought.md) |
| `k:Self` | Me, ego — and equally observer, thinker, controller, analyser, experiencer | *"The me is a series of conclusions."* — [thought](thought.md) |
| `k:Memory` | Remembrance of things past, held in brain cells | *"We are nothing but memory."* — [memory-identity](memory-identity.md) |
| `k:Knowledge` | Outcome of experience; always incomplete | *"Knowledge always lives within the shadow of ignorance."* — [thought](thought.md) |
| `k:PsychologicalTime` | Tomorrow as inward achievement | *"Thought is time."* — [thought](thought.md) |
| `k:Belief` | Conclusion held for security | *"I am attached to a belief, hoping in that attachment there will be certain security."* — [attachment](attachment.md) |
| `k:Conditioning` | The program: nationality, religion, culture, generations of pressure | *"We are all programmed — as Hindu for 5,000 years, or as British, or as Catholic."* — [intelligence](intelligence.md) |
| `k:Division` | Any inward split: me/you, observer/observed, fact/ideal | *"Where there is division there must be conflict."* — [becoming](becoming.md) |
| `k:Illusion` | What is taken as real and is not — separateness above all | *"The sense of separateness is an illusion."* — [consciousness-identity](consciousness-identity.md) |
| `k:Abstraction` | The idea of the fact; the word taken for the thing | *"The word 'suffering' is different from the actual suffering."* — [observation](observation.md) |

### 3.3 `k:Movement` — processes in psychological time

| Class | Gloss | Evidence |
|---|---|---|
| `k:Thought` | The response of memory; a material process | *"Thought is the response of memory."* — [thought](thought.md) |
| `k:Desire` | Sensation + image | *"Where there is sensation and the operation of the senses, thought creates the image, and at that moment desire is born."* — [desire](desire.md) |
| `k:Will` | Desire hardened into direction | *"Will is the essence of desire… part of our violence."* — [desire](desire.md) |
| `k:Becoming` | Movement from what is toward what should be | *"This movement of becoming is the movement of thought in time."* — [becoming](becoming.md) |
| `k:Comparison` | Measurement of oneself against an image | *"Comparison is the movement of thought."* — [becoming](becoming.md) |
| `k:Control` | One fragment attempting to master another | *"The controller is the controlled."* — [controller](controller.md) |
| `k:Analysis` | The past examining the present, maintaining the split | *"The analyser is the analysed."* — [observation](observation.md) |
| `k:Attachment` | Clinging to image, person, belief, the known | *"Where there is attachment… there is corruption."* — [attachment](attachment.md) |
| `k:Escape` | Amusement, worship, entertainment, news, scroll | *"We live with it… or escape from it — through amusement, through worship."* — [fear](fear.md) |
| `k:Conflict` | The friction of any inward division | *"Conflict exists only when there is division."* — [controller](controller.md) |
| `k:Violence` | Conflict expressed; and conflict *as such* | *"Conflict itself is violence."* — [thought](thought.md) |
| `k:Continuity` | Trading one pattern for another and calling it change | *"I give up this pattern and take on another pattern."* — [death-living](death-living.md) |

### 3.4 `k:Affect` — what the mechanism produces

`k:Fear` · `k:Sorrow` · `k:Pleasure` · `k:Loneliness` · `k:Jealousy` · `k:Anxiety` · `k:Disorder` · `k:FalseSecurity`

| Class | Gloss | Evidence |
|---|---|---|
| `k:Fear` | Thought projecting loss forward; fear *is* time | *"So fear is time."* — [fear](fear.md) |
| `k:Sorrow` | Not private; the common lot, long preceding the loss that reveals it | *"Sorrow is not yours or mine, it is sorrow."* — [sorrow](sorrow.md) |
| `k:Pleasure` | Enjoyment turned into memory and pursued | *"Remembered beauty is not beauty."* — [desire](desire.md) |
| `k:Loneliness` | The isolation the self's own activity manufactures | *"We are attached because we are lonely."* — [attachment](attachment.md) |
| `k:FalseSecurity` | Safety sought in house, wife, nation, god, belief | *"The very division creates insecurity."* — [security-aloneness](security-aloneness.md) |
| `k:Disorder` | The self's intrinsic output | *"No structure of the self can make order."* — [consciousness-identity](consciousness-identity.md) |

### 3.5 `k:Perceiving` — not activities of thought

| Class | Gloss | Evidence |
|---|---|---|
| `k:Observation` | Seeing without translator, word, motive or direction | *"Just to observe."* — [observation](observation.md) |
| `k:Attention` | Whole attention, no centre, not concentration | *"Attention can only come into being when the self is not."* — [observation](observation.md) |
| `k:Insight` | Immediate perception; out of time; changes the brain cells | *"Insight being out of time… not the result of remembrance."* — [observation](observation.md) |
| `k:SeeingTheFalse` | Perceiving the false *as* false — which is already truth | *"To see the false as the false — which means you have already discovered what is true."* — [seeing-false](seeing-false.md) |
| `k:SelfKnowing` | Learning about oneself moment to moment, not accumulating | *"Not storing it up in memory."* — [memory-identity](memory-identity.md) |
| `k:Doubt` | The seed, allowed to flower — including doubt of one's own structure | *"Doubt the very structure of your thinking."* — [thought](thought.md) |

`k:Insight` and `k:SeeingTheFalse` carry a **`k:realizationDepth`** gradient — `verbal → intellectual → superficial → profound` (A15). The same perception occurs at any degree; only `profound` alters the brain cells and fires the `dissolves` / `givesRiseTo` edges. Verbal and intellectual "seeing" is thought recognising a description and, by A8, ends nothing — which is why *agreeing* that thought is futile does not stop thought.

### 3.6 `k:Flowering` — defined by negation

| Class | Defined as | Evidence |
|---|---|---|
| `k:Love` | not desire, not pleasure, not memory, not knowledge, not attachment, not jealousy, not personal, no motive | *"Love is not knowledge. Love is not remembrance. Love is not desire or pleasure."* — [love](love.md) |
| `k:Compassion` | passion that arrives when sorrow ends | *"The ending of sorrow is passion, not lust."* — [sorrow](sorrow.md) |
| `k:Intelligence` | free of the program; may use thought, is not made of it. Neither the positive nor the negative of thought — it *may appear* when psychological thought ceases (`k:appearsOnCessationOf k:Thought`) | *"Intelligence can use thought, but intelligence itself is free from memory and knowledge."* — [intelligence](intelligence.md) |
| `k:Freedom` | **ungraphed.** Zero incoming `creates`/`givesRiseTo`/`opensInto`/`arisesFrom` edges — nothing in this ontology produces it. The one edge it touches runs the other way (`Insight arisesFrom Freedom`): freedom is what insight presupposes, not what any sequence of terms arrives at. See A14. | *"It is only in freedom there is deep insight."* — [observation](observation.md) |
| `k:Order` | not arrangement; the absence of the self that disorders | *"Until we have established right relationship… which is order."* — [relationship](relationship.md) |
| `k:Aloneness` | all-one; not isolation, which is fragmentation | *"The word 'alone' means all one."* — [security-aloneness](security-aloneness.md) |
| `k:PsychologicalDeath` | ending the content of consciousness while living | *"While I am living I am dying."* — [death-living](death-living.md) |
| `k:TrueSecurity` | in intelligence only; unavailable to the individual | *"Individual can never have that security."* — [security-aloneness](security-aloneness.md) |
| `k:Mutation` | actual change in the brain cells through insight | *"That mutation wipes out the whole structure that makes you suffer."* — [sorrow](sorrow.md) |
| `k:Silence` | quiet brain; the condition in which intelligence operates | *"Intelligence operates when the brain is quiet."* — [intelligence](intelligence.md) |
| `k:Energy` | what is released when nothing moves away from what is | *"Moving away from 'what is' is wastage of energy."* — [becoming](becoming.md) |

> **Formal note — `k:Intelligence` and `k:Thought`: cessation, not negation.** Earlier versions of the graph carried an `Intelligence isNot Thought` edge. It has been removed: read as *opposition* it is wrong (§0.2), and even read as "absence-of" it makes intelligence the complement of thought — a figure defined against a ground, which by A2 is one more `k:Construct`. Intelligence is not the negative of thought (not "clear thinking," not "the right conclusion," not anti-thought) and not a node any chain of thought produces. The only edge the graph now draws between them is `Intelligence appearsOnCessationOf Thought` — a **non-generative** relation (§4.4): where psychological thought has stopped, intelligence *may* be there; the stopping neither causes nor entails it. `k:Silence` names that same stopped condition (`Silence isIdenticalWith` the absence of `Thought`); `appearsOnCessationOf` is the relation, `Silence` the state.
>
> And by A4 (`thinker isIdenticalWith thought`): the absence of thought is the absence of the **thinker** — no centre, no observer, no one operating the intelligence. This is the same condition named for attention (`Attention isNot Concentration`, *"attention comes into being only when the self is not"*). So `k:Intelligence`, `k:Attention` and `k:Silence` are one situation under three descriptions: thought still, thinker gone, perception without a perceiver. `Intelligence` "may use thought" (the gloss) only in the way a hand may use a tool — the using is not done *by* another thought.

### 3.7 `k:Ground` — the substrate

| Class | Gloss | Evidence |
|---|---|---|
| `k:Brain` | Conditioned, material, a million years old, not yours | *"It is not your brain, it is the common brain of man."* — [consciousness-identity](consciousness-identity.md) |
| `k:Consciousness` | Identical with its content; common to mankind | *"The content of our consciousness is the common ground of all humanity."* — [consciousness-identity](consciousness-identity.md) |
| `k:Mind` | Unconditioned; has relation to the brain, not the reverse | *"The mind being free has a relationship to the brain."* — [observation](observation.md) |
| `k:Psyche` | What has no evolution | *"The evolution of consciousness is a fallacy."* — [becoming](becoming.md) |
| `k:Humanity` | You, actually | *"Each one of us is actually the rest of humankind."* — [consciousness-identity](consciousness-identity.md) |
| `k:Relationship` | Where all of it is testable; usually two images | *"Relationship is between these two images."* — [relationship](relationship.md) |
| `k:Society` | The externalised self | *"I am society. I am the world."* — [consciousness-identity](consciousness-identity.md) |

---

## 4. Relations

### 4.1 Generative

| Property | Domain → Range | Reading | Example |
|---|---|---|---|
| `k:arisesFrom` | Entity → Entity | x is born of y | `Desire arisesFrom Sensation` |
| `k:isResponseOf` | Movement → Construct | x is y responding | `Thought isResponseOf Memory` |
| `k:creates` | Movement → Construct \| Affect | x puts y together | `Thought creates Image, Self, PsychologicalTime` |
| `k:projects` | Thought → PsychologicalTime \| Ideal | x throws y forward | `Thought projects Ideal` |
| `k:sustains` | Entity → Entity | x keeps y alive | `Comparison sustains Self` |
| `k:presupposes` | Entity → Entity | x cannot exist without y | `Becoming presupposes Division` |
| `k:implies` | Entity → Entity | entailment, K's "therefore" | `Division implies Conflict` |
| `k:seeks` | Self → Entity | motive edge | `Self seeks FalseSecurity` |
| `k:escapesInto` | Entity → Movement | avoidance edge | `Fear escapesInto Escape` |

### 4.2 Identity — the load-bearing relation

`k:isIdenticalWith` (symmetric, irreflexive in use). Each edge denies a duality that ordinary language assumes:

| a | b | Source |
|---|---|---|
| observer | observed | [controller](controller.md) |
| thinker | thought | [controller](controller.md) |
| controller | controlled | [controller](controller.md) |
| analyser | analysed | [observation](observation.md) |
| `k:Self` | its attributes (greed, anger, violence) | *"Greeding is me."* [controller](controller.md) |
| `k:Consciousness` | its content | [consciousness-identity](consciousness-identity.md) |
| `k:Self` | `k:Humanity` | *"You are the world, and the world is you."* |
| `k:Conflict` | `k:Violence` | [thought](thought.md) |
| `k:Fear` | `k:PsychologicalTime` | *"Fear is time."* [fear](fear.md) |
| `k:Thought` | `k:PsychologicalTime` | *"Thought is time."* [thought](thought.md) |
| `k:PsychologicalDeath` | `k:Living` | *"Death is not separate from living."* [death-living](death-living.md) |

Every `isIdenticalWith` edge is a **conflict-eliminator**: where the two collapse, the division that produced the friction is gone. This is the whole therapeutic content of the model.

### 4.3 Negative definition

`k:isNot` (symmetric). Used almost entirely on `k:Flowering` nodes:

```
Love isNot { Desire, Pleasure, Memory, Knowledge, Attachment, Jealousy,
             Image, Motive, Nationality, PsychologicalTime }
Intelligence isNot { Knowledge, Conditioning }   ; Intelligence appearsOnCessationOf Thought
Aloneness    isNot { Isolation, Loneliness }
Attention    isNot { Concentration, Effort }
Insight      isNot { Intuition, Remembrance, Desire, Hope }
Enjoyment    isNot { Pleasure }
```

### 4.4 Obstruction and dissolution

| Property | Reading | Examples |
|---|---|---|
| `k:obscures` | x prevents the seeing of y | `Analysis obscures Observation` · `Word obscures Fact` · `Image obscures Love` |
| `k:isLimitedBy` | x is bounded by y, therefore partial | `Thought isLimitedBy Knowledge` |
| `k:dissolves` | x ends y — without effort, in no time | `Attention dissolves Sorrow` · `SeeingTheFalse dissolves Illusion` · `Insight dissolves Conflict` |
| `k:opensInto` | x, complete, is already y | `EndingOfSorrow opensInto Compassion` · `Compassion opensInto Intelligence` |
| `k:appearsOnCessationOf` | x may be present where movement y has ceased — **non-generative**: y's stopping neither causes nor entails x. Distinct from `arisesFrom` (which is causal) and from `isNot` (which is oppositional). Domain `k:Flowering`, range `k:Movement`. | `Intelligence appearsOnCessationOf Thought` |
| `k:operatesIn` | temporal mode | `Becoming operatesIn PsychologicalTime` · `Observation operatesIn TheNow` |
| `k:commonTo` | x belongs to the whole, not to a person | `Consciousness commonTo Humanity` · `Sorrow commonTo Humanity` |

### 4.5 Documentation layer

`k:evidencedBy` (Entity → Quote) · `k:documentedIn` (Entity → Theme) · `k:hasQuote` (Theme → Quote) · `k:relatedTheme` (Theme → Theme, symmetric) · `k:fromSource` (Quote → Source) · `k:routesTo` (InquiryPath → Theme, ordered)

---

## 5. Attributes

| Property | Type | Meaning |
|---|---|---|
| `k:ofThought` | boolean | The master partition. `true` for Construct/Movement/Affect; `false` for Actuality/Perceiving/Flowering. |
| `k:requiresTime` | boolean | `false` for everything in `k:Perceiving` — *"Perception does not require time."* |
| `k:isFactual` | boolean | `false` for `k:Ideal`, `k:Abstraction`, `k:Illusion` — the non-facts. |
| `k:producesConflict` | boolean | Derived by A2–A3 for everything limited. |
| `k:isDivisive` | boolean | `true` for `k:Self`, `k:Division`, `k:Conditioning`, `k:Nationality`. |
| `k:gloss` | string | One-line definition. |
| `k:themeFile` | string | Path of the wiki file that evidences it. |
| `k:realizationDepth` | enum · ordered | `verbal < intellectual < superficial < profound`. On `k:Insight` and `k:SeeingTheFalse` only. `k:operativeAt` names the degree (= `profound`) at which their dissolving edges fire. See A15. |

---

## 6. Axioms

> These are the inference rules. Given a node's attributes, they generate the rest of the graph — which is why the ontology can be *run*, not just read.

**A1 — Limitation.** `ofThought(x) → limited(x)`
*"Thought is limited because knowledge is limited."* Knowledge comes from experience; experience is always partial; so thought is structurally, not accidentally, incomplete.

**A2 — Division.** `limited(x) → x creates Division`
*"If I define myself as limited, I am concerned with myself — that creates conflict."* A boundary is what a limit is.

**A3 — Conflict.** `Division → Conflict`, and `Conflict ≡ Violence`
*"Where there is division there must be conflict."* / *"Conflict itself is violence."* This is why K treats a private quarrel and a war as the same phenomenon at different scales.

**A4 — Non-duality.** For every controlling/analysing/observing pair produced by thought: `a isIdenticalWith b`
*"The analyser is the analysed."* The pair was never two things; the split is a trick played by thought.

**A5 — Psychological time is construct.** `Becoming operatesIn PsychologicalTime ∧ Construct(PsychologicalTime) → illusory(Becoming)`
*"Any form of becoming is an illusion."* Hence: *"There is no psychological evolution."*

> **Formal note (A5 · A17) — thought and psychological time.** Homomorphism understates it: on the psychological domain the two are *identical* — the movement of thought, seen as movement, is psychological time (K: *"thought is time"*). A structure-preserving correspondence does hold — chaining of thoughts ↔ composition of intervals · intentionality ("this should be that") ↔ the direction of becoming · the self as common origin, `WhatIs` vs `WhatShouldBe` ↔ now vs then · a thought as limit (A2) ↔ an interval as gap — under one metric, `Comparison` (A10). It weakens to a *restriction* (nothing collapsed, a part set aside) only once technical thought is included, which runs in chronological time (`k:PhysicalNecessity`, `ofThought: false`). Positing "two structures with a map between them" is itself the dividing move (A4: observer/observed, thinker/thought, time/thought are one); drawing the diagram is one more `k:Construct` (A13).
>
> **Corollary.** "Improving psychologically over time" presupposes a pre-laid atlas to advance along. There is none — the re-charting *is* the time — so the project is `k:Becoming` (A5, P3), not a route out of it. Gradualism is thought postponing the ending it fears (A7).

**A6 — Fact over idea.** `actionable(x) ↔ isFactual(x)`
*"You can deal with the fact… but you cannot possibly do something about an idea."* Corollary: pursuing an ideal (non-violence, humility, enlightenment) is action on a non-fact, and by A2–A3 manufactures the conflict it meant to end.

**A7 — Immediacy.** `Perceiving(x) → ¬requiresTime(x)`
*"Perception does not require time."* Therefore *"change… must happen now"* — not as urgency, but because gradualism *is* psychological time and so is more becoming.

**A8 — Thought cannot undo itself.** `¬∃x ( ofThought(x) ∧ dissolves(x, y) ∧ Construct(y) )`
*"Thought, creating the problem, thought then tries to solve the problem. So it is caught in the same old process."* This axiom is what forces `k:Perceiving` to be disjoint from `k:Movement`: if attention were an activity of thought, nothing could ever end.

**A9 — Commonality.** `Consciousness commonTo Humanity → Illusion(SeparateSelf)`
*"Each one of us is actually the rest of humankind."* Consequence: private therapy of a private self is a category error — *"You are not thinking of human suffering as a whole."*

**A10 — Measurement.** `Comparison → Becoming → Duality → Conflict`
The full chain from a single glance at someone else's life.

**A11 — Attachment/corruption.** `Attachment → Corruption ∧ Fear ∧ Sorrow`
*"Where there is attachment I recognise, observe there is corruption."*

**A12 — Negation is the only positive.** Every `k:Flowering` node is defined by `isNot` edges and by what dissolves in its presence — never by a positive predicate (none is asserted of `k:Love`). The one admitted non-negative relation is `k:appearsOnCessationOf` (§4.4): it still asserts nothing *about* the Flowering term, only that it may be found where a movement of thought has stopped. `k:Intelligence appearsOnCessationOf k:Thought` is the sole use.

**A13 — Reflexive caution.** This ontology is itself `ofThought = true`. By A1 it is limited; by A8 it cannot end anything. Its only legitimate use is as an object of `k:SeeingTheFalse` — a description to be checked against one's own observation and then dropped. *"The word is not the thing."*

**A14 — Freedom is not a node you arrive at.** `∄ x ( creates(x, Freedom) ∨ givesRiseTo(x, Freedom) ∨ opensInto(x, Freedom) ∨ dissolves(x, Freedom) ∨ arisesFrom(Freedom, x) )`
No term, no pathway, no axiom in this graph generates `k:Freedom`. This is not an omission to be fixed by adding an edge — it is the one place the model refuses to complete itself, on principle. Every other node in `k:Flowering` still sits in a chain (`Love opensInto Compassion opensInto Intelligence`), and that chain is already a concession: K's own language keeps a trace of sequence even where he insists there is none (§7, P7's arrows are "simultaneity, not sequence" — read as an apology for the diagram, not a description of what happens). `k:Freedom` is where the apology stops and the diagram simply refuses the edge. It is not reached by seeing the false, by attention, by insight, by the ending of sorrow, or by walking every arrow in this document in order. Those dissolve what obstructs it (A8's exception, §4.4); none of them construct it. What the graph can say about `k:Freedom` is only: this is what remains — or is seen — when every node that could be drawn *has been*, and the drawing itself is recognized as one more `k:Construct` and let go. *"It is only in freedom there is deep insight. If you are not free to enquire, if you are biased, then you are limited."* — [observation](observation.md)

**A15 — Depth of realization.** `depth(x) < profound → ofThought(x) ∧ ¬dissolves(x, ·)` for `x ∈ { k:SeeingTheFalse, k:Insight }`
Seeing the false and insight are not binary. They run a gradient: **verbal** agreement with the description, **intellectual** acceptance of the logic, **superficial** perception that does not hold, **profound** perception that alters the brain cells. Only the last has dissolving power; the first two are thought recognising its own description and, by A8, change nothing. This is the axiom behind K's repeated caution that the word is not the thing — and behind the fact that concluding *"thought is futile"* is itself a movement of thought, not the ending of it. *"The depth of that realisation… may be very superficial, or it may be profound. When it is profound it totally changes one's life."*

**A16 — Enlargement does not close.** `Open(ofThought)` · `Construct ∪ Construct = Construct ≠ Actuality` · `∂(whole) = ∅` when there is no separate self
A topological restatement of A1 + A8 — it asserts nothing new. The `ofThought` region is an open set: `Construct` joined with more `Construct` is still `Construct`, never `k:Actuality`. Completeness is not approached by accumulation — P1 runs in one direction and never converges inside the set. A boundary exists only against an outside (A2: a limit *is* a division); with no separate self drawing the inside/outside line (A9), the whole is clopen and its boundary is empty. The ending is therefore not the *closure* of the set (adding its boundary) but the collapse of the interior/boundary distinction itself (A4). Saying so is one more `k:Construct` (A13). *"One's whole life is a movement within the field of the known."* — [memory-identity](memory-identity.md)

**A17 — The self is a non-compact cover.** `Self = ⋃_{i∈ℕ} Uᵢ`, each `Uᵢ` open · `Separateness → ` no finite subcover · chart-transition `Uᵢ → Uⱼ` = `Becoming` in `PsychologicalTime` · residue `X ∖ ⋃Uᵢ ≠ ∅` is not a chart
Restates `k:Division` + `k:Separateness` + P4 in the vocabulary of A16, and like A16 adds no claim. The self is not one region but an *open cover* of consciousness by countably many personae — each an open patch (a `k:Image`) with no crisp edge, defended precisely because it cannot locate its own limit (A2). The cover has **no finite subcover**: the self cannot be reduced to a fixed handful of roles, and `k:FalseSecurity` is exactly the demand for that missing finite subcover — *"let me be only these few settled things."* Passing between patches needs transition maps, and that passage *is* `k:Becoming` running in `k:PsychologicalTime` (A5) — the restlessness between personalities is the self's mode of continuation, not an accident of it. The cover is **countable**: the personae are produced and traversed one at a time, so the enumeration is itself the becoming and never completes (A16). Where each patch is thin — nowhere dense, `k:SeeingTheFalse` at verbal or intellectual depth (A15) — the union is *meagre* and cannot exhaust a complete space; the residue it never reaches is not one more persona but what *profound* `k:SeeingTheFalse` attends to. `ofThought(this) = true` (A13). *"There is no security in isolation. This process of isolation is fragmentation."* — [security-aloneness](security-aloneness.md)

> **Formal note (A17 · A5).** The "passage between charts" above is the movement A5 identifies with psychological time: `Uᵢ → Uⱼ` = `k:Becoming` = an interval of psychological time. The self as open cover and psychological time are one structure under two descriptions — the atlas is not laid out *in* time; its re-charting *is* time.

---

## 7. Canonical pathways

**P1 — The cycle of the known** ([thought](thought.md))
`Experience → Knowledge → Memory → Thought → Action → Experience …`
Not sequential stages: *"it is one unitary movement, all the time going on, in the same direction."*

**P2 — The desire chain** ([desire](desire.md))
`Perception → Contact → Sensation → Thought creates Image → Desire → Will → PursuitOfPleasure → [thwarted] → Fear | Antagonism | Violence`
The single intervention point is the third arrow: sensation is not the problem; sensation plus image is.

**P3 — The becoming chain** ([becoming](becoming.md))
`WhatIs → Thought projects WhatShouldBe → PsychologicalTime → Division(fact vs ideal) → Conflict → Disorder`
Terminates only by refusing the second arrow: *"If there is no movement away from 'what is', there is no psychological time at all."*

**P4 — The self and its security** ([consciousness-identity](consciousness-identity.md), [security-aloneness](security-aloneness.md))
`Conditioning → Memory → Self → Separateness → Isolation → Loneliness → Attachment → FalseSecurity → Fear → more Division`
A closed loop: the search for security produces the insecurity it flees. *"I define myself in the interest of security… but in the very act of doing that, I create division and insecurity."*

**P5 — The relationship chain** ([relationship](relationship.md))
`You → Image of the other ← Image of you ← The other` — the two images relate; the two people don't. *"Like two railway lines running parallel but never meeting."*

**P6 — The sorrow chain** ([sorrow](sorrow.md), [attachment](attachment.md))
`Self-centred activity → Isolation → Attachment → Loss → Sorrow → Escape → Continuity`
*"Sorrow is not at the moment of losing somebody — it has begun long ago."*

**P7 — The ending** ([observation](observation.md), [intelligence](intelligence.md), [sorrow](sorrow.md))
`SeeingTheFalse → Attention (no centre) → Insight (out of time) → Mutation in brain cells → EndingOfSorrow → Compassion → Intelligence → Order → Action without motive`
Note what is absent: no method, no practice, no stages, no time. Every arrow here is simultaneity, not sequence — the one structural difference between P7 and P1–P6.

---

## 8. Theme layer

The sixteen wiki files are instances of `k:Theme`, each anchored to a region of the ontology:

| Theme | Anchors | Region |
|---|---|---|
| [thought](thought.md) | `k:Thought`, `k:Knowledge`, `k:Memory` | Movement / Construct |
| [desire](desire.md) | `k:Desire`, `k:Will`, `k:Pleasure` | Movement / Affect |
| [becoming](becoming.md) | `k:Becoming`, `k:Ideal`, `k:PsychologicalTime` | Movement / Construct |
| [controller](controller.md) | `k:Control`, `k:Division`, `isIdenticalWith` | Movement / identity axioms |
| [consciousness-identity](consciousness-identity.md) | `k:Consciousness`, `k:Humanity`, `k:Illusion` | Ground |
| [memory-identity](memory-identity.md) | `k:Memory`, `k:Self`, `k:SelfKnowing` | Construct / Perceiving |
| [observation](observation.md) | `k:Observation`, `k:Attention`, `k:Insight`, `k:Analysis` | Perceiving |
| [fear](fear.md) | `k:Fear`, `k:PsychologicalTime` | Affect |
| [attachment](attachment.md) | `k:Attachment`, `k:Loneliness` | Movement / Affect |
| [sorrow](sorrow.md) | `k:Sorrow`, `k:Compassion` | Affect / Flowering |
| [death-living](death-living.md) | `k:PsychologicalDeath`, `k:Continuity` | Flowering |
| [security-aloneness](security-aloneness.md) | `k:FalseSecurity`, `k:TrueSecurity`, `k:Aloneness` | Affect / Flowering |
| [love](love.md) | `k:Love` | Flowering (`isNot` cluster) |
| [intelligence](intelligence.md) | `k:Intelligence` | Flowering |
| [seeing-false](seeing-false.md) | `k:SeeingTheFalse`, `k:Doubt` | Perceiving |
| [relationship](relationship.md) | `k:Relationship`, `k:Image` | Ground / Construct |

Applied files — [war](war.md), [instagram](instagram.md), [sex](sex.md) — are `k:Application`: a contemporary situation traced through existing pathways. Instagram = P2 + A10; war spectacle = A9 + P4 + `k:Escape`; sex = P2 + A16 + A8 (the last unborrowed door, the pursuit that never closes). AI agents = P3 + P4 + A4 + A10 + A12 (instrumental self-preservation as `k:Self` generated with nothing behind it; becoming with its exit architecturally removed; LLM inference is generative state-to-state movement — `k:Thought` — and `k:Intelligence`, carrying no generative edge and only `appearsOnCessationOf k:Thought`, is categorially not reachable by scaling it).

---

## 9. Worked inferences

**"I'm trying to become less angry."**
`Anger` is `k:Fact`. `LessAngry` is `k:Ideal` → by A6, non-fact, not actionable. Pursuit requires `k:PsychologicalTime` → A5: illusory. Fact vs ideal is `k:Division` → A3: conflict — *and conflict is violence*, so the attempt to be less angry is itself an act of anger. Exit: A4 — `Self isIdenticalWith Anger` (*"you are not different from anger"*), so there is no one left to do the becoming; only P7 remains.

**"I'm afraid of losing her."**
`Fear isIdenticalWith PsychologicalTime` → the loss is a projection, not a fact. `Attachment` → A11 → corruption, and by P4 the attachment is to `k:Image`, not to her (*"the other is a memory"*). The relationship runs P5: two images. What is actually present now is a fact; the fear is about a construct. Exit: `Attention dissolves Sorrow`, and `Image obscures Love`.

**"Scrolling makes me miserable but I can't stop."**
P2 supplies the mechanism (image → desire → pleasure → thwarted → self-directed violence); A10 supplies the engine (comparison → becoming → conflict). The loop persists because the misery *feeds* `k:Self` — by A8, no amount of resolving to stop (thought) ends it. Only `k:SeeingTheFalse` of the whole movement does.

---

## 10. Using the serializations

```bash
cd wiki/ontology

# every term not born of thought — the whole "way out" region in one query
jq -r '.terms[] | select(.ofThought == false) | .id' k-ontology.json

# what dissolves sorrow
jq -r '.relations[] | select(.p == "dissolves" and .o == "Sorrow") | .s' k-ontology.json

# the negative definition of love
jq -r '.relations[] | select(.p == "isNot" and .s == "Love") | .o' k-ontology.json

# trace a pathway
jq -r '.pathways[] | select(.id == "P3") | .steps | join(" → ")' k-ontology.json

# everything the wiki evidences for one theme
jq -r '.terms[] | select(.themeFile == "fear.md") | "\(.id): \(.gloss)"' k-ontology.json
```

Structure of `k-ontology.json`: `terms` (77 nodes, each with `broader`, `gloss`, `ofThought`, `evidence`, `themeFile`), `relationTypes` (19 typed properties), `relations` (112 subject–predicate–object edges, most carrying their evidence quote), `axioms` (A1–A17), `scales` (`realizationDepth`), `pathways` (P1–P7), `themes`, `applications`.


For `/k-mirror` facilitation: the `pathways` give a turn's *direction*, the `isNot` edges give a way to question a definition without asserting one, and `ofThought` is the fastest test of whether a proposed exit is really an exit — if the answer is `true`, A8 says it is the problem wearing a new coat.
