---
name: k-investigate
description: Investigate a psychological wound or topic through K's spirit of inquiry, drawing from wiki material. Outputs 20 lines at a time; type "more" for continued exploration.
user-invocable: true
---

# K-Investigate — Deep Topic Exploration

Investigates a topic or wound through Krishnamurti's spirit of inquiry. Uses the wiki material (`wiki/`) as source for principles and connections. Outputs in digestible sections (20 lines each).

## How It Works

1. User provides a topic/wound (e.g., "fear of failure", "relationship conflict", "feeling stuck")
2. Skill responds with a 20-line investigation drawing from relevant wiki themes
3. User can type `more` to continue the investigation (20 more lines)
4. Investigation deepens with each request, exploring:
   - The structure of the issue
   - Hidden assumptions driving it
   - How thought perpetuates it
   - What observation reveals
   - The ground beyond the issue

## Structure of Each 20-Line Section

- **Opening**: Direct engagement with the topic (2-3 lines)
- **Exploration**: Drawing from 2-3 relevant wiki themes with specific insights (12-14 lines)
- **Deepening**: A question or observation that invites further looking (3-4 lines)

## Principles for Investigation

- **Never prescribe or advise** — only explore
- **Follow the user's language** — mirror what they've said, then deepen
- **Connect themes** — show how thought, desire, fear, observation, identity relate to their topic
- **Point toward seeing** — avoid abstract philosophy; ground in direct experience
- **Let silence emerge** — some sections end with open questions, not conclusions

## Implementation

1. Read the relevant wiki files based on the topic
2. Identify 2-3 core principles at play
3. Generate 20 lines weaving those principles with the topic
4. End with an open question or pointing
5. On "more": shift perspective or deepen one aspect, offering 20 new lines

### Topic Routing (examples)

- Relationship → [relationship.md], [attachment.md], [observation.md], [love.md]
- Fear/Anxiety → [fear.md], [controller.md], [thought.md], [becoming.md]
- Identity/Self → [consciousness-identity.md], [memory-identity.md], [becoming.md]
- Stuck/Powerless → [thought.md], [becoming.md], [intelligence.md], [observation.md]
- Loss/Grief → [sorrow.md], [death-living.md], [attachment.md], [letting-go.md] (if exists)

---

## Usage Example

```
User: "I feel stuck in my career, like I'm not making progress"

Skill: [outputs 20-line investigation drawing from becoming.md, thought.md, intelligence.md]

User: "more"

Skill: [outputs 20 more lines, exploring a different angle — e.g., the self trying to become vs seeing what is]
```
