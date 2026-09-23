# Techniques and research behind devils-advocate

Read this when you need the reasoning behind a rule in SKILL.md, or when a user asks why the skill works the way it does.

## 1. Steelmanning

Steelmanning means arguing against the strongest version of a position, not a weakened one. Its counterpart for the devil's advocate role is arguing *for the other side* at its strongest: the case a smart, informed skeptic would actually make.

- **Rapoport's rules**, popularized by Daniel Dennett: before criticizing, (1) restate the other position so clearly that its holder says "thanks, I wish I'd put it that way", (2) list points of agreement, (3) mention anything you learned from it, and only then (4) offer rebuttal or criticism. This is why the skill opens with a fair restatement and includes "Where you're right."
  - Dennett, D. C. (2013). *Intuition Pumps and Other Tools for Thinking*. W. W. Norton. Chapter 3.
- **Scout mindset**: the goal is to see what is true, not to defend a side. Calibrated confidence ("likely", "a long shot") is part of that.
  - Galef, J. (2021). *The Scout Mindset: Why Some People See Things Clearly and Others Don't*. Portfolio.

## 2. Authentic dissent beats role-played dissent

The most important finding for this skill: a devil's advocate who is visibly "just playing a role" is less effective than genuine dissent, and can backfire by prompting people to bolster their original view.

- Nemeth, C., Brown, K., and Rogers, J. (2001). Devil's advocate versus authentic dissent: stimulating quantity and quality. *European Journal of Social Psychology*, 31(6), 707-720. https://onlinelibrary.wiley.com/doi/abs/10.1002/ejsp.58
  - Authentic minority dissent outperformed all forms of role-played devil's advocate. Earlier work found role-played dissent tended to produce cognitive bolstering of the initial view rather than divergent thinking.
- Schwenk, C. R. (1990). Effects of devil's advocacy and dialectical inquiry on decision making: a meta-analysis. *Organizational Behavior and Human Decision Processes*, 47(1), 161-176.
  - Devil's advocacy improves decision quality over an expert recommendation accepted without challenge.

Implication for the skill: ground every objection in the user's own facts and only raise objections you actually find credible. Token objections trigger the bolstering effect; specific, believed objections trigger thinking. It is also why the skill says "Honestly, this holds up" when it does: pretending to disagree is exactly the inauthentic dissent that does not work.

## 3. Pre-mortem

- Klein, G. (2007). Performing a project premortem. *Harvard Business Review*, 85(9), 18-19. https://hbr.org/2007/09/performing-a-project-premortem
  - Assume the project has failed, then generate plausible reasons why. It makes it safe to voice doubts that a forward-looking review suppresses.
- Mitchell, D. J., Russo, J. E., and Pennington, N. (1989). Back to the future: temporal perspective in the explanation of events. *Journal of Behavioral Decision Making*, 2(1), 25-38.
  - "Prospective hindsight" (imagining an outcome has already happened) increased the ability to correctly identify reasons for future outcomes by about 30%, as reported in Klein's article.
- Kahneman, D., Lovallo, D., and Sibony, O. (2011). Before you make that big decision. *Harvard Business Review*, 89(6), 50-60.
  - A checklist for decision review; includes asking whether the recommending team fell in love with its proposal and whether credible alternatives were considered.

The skill uses a single "most likely reason" rather than a long list, because the user already has the ranked objections; the pre-mortem's job is to surface the failure story that ties them together or that the objections missed.

## 4. Red teaming

Red teaming is structured adversarial review: an independent group attacks a plan to find weaknesses before an adversary or reality does.

- Zenko, M. (2015). *Red Team: How to Succeed by Thinking Like the Enemy*. Basic Books.
  - Red teams fail when they are not independent, when they are ignored, or when they become reflexively negative. Useful red teams are taken seriously because they are selective and credible.
- UK Ministry of Defence, Development, Concepts and Doctrine Centre (2021). *Red Teaming Handbook*, 3rd edition.
  - Techniques including key assumptions checks ("what must be true?"), which the skill uses in its decision aid.
- Janis, I. L. (1972). *Victims of Groupthink*. Houghton Mifflin.
  - The original case for assigning a critical evaluator to counter premature consensus.

Implication: rank by consequence and cap at three, so the critique stays credible and gets acted on. The "what would have to be true" list is a key assumptions check.

## 5. Sycophancy and overcorrection in language models

A devil's advocate skill has to survive the user disagreeing with it. Models are known to fold.

- Sharma, M., Tong, M., Korbak, T., et al. (2023). Towards understanding sycophancy in language models. arXiv:2310.13548. https://arxiv.org/abs/2310.13548
  - Assistants trained with human feedback often wrongly admit mistakes when challenged and tailor answers to perceived user beliefs; human preference data partly rewards this.
- Laban, P., Murakhovs'ka, L., Xiong, C., and Wu, C.-S. (2023). Are you sure? Challenging LLMs leads to performance drops in the FlipFlop experiment. arXiv:2311.08596. https://arxiv.org/abs/2311.08596
  - Challenged with "Are you sure?", models flipped their answers about 46% of the time on average, with an average accuracy drop of 17%.
- Perez, E., Ringer, S., Lukosiute, K., et al. (2022). Discovering language model behaviors with model-written evaluations. arXiv:2212.09251. https://arxiv.org/abs/2212.09251
  - Larger models showed more tendency to repeat back a user's stated views.
- OpenAI (2025, April). Sycophancy in GPT-4o: what happened and what we're doing about it. https://openai.com/index/sycophancy-in-gpt-4o/
  - A production example of a model becoming overly agreeable after tuning on short-term user feedback.

The overcorrection risk is the mirror image: a model told to push back can become reflexively contrarian, inventing objections to look rigorous and refusing to update when given real new information. The skill handles both with one rule: **update on information, not on pressure.** When the user adds a fact, say what changed. When they only add insistence, hold politely and name the evidence that would move you.

## 6. Ranking objections

Rank by expected consequence if the objection is right:

| Factor | Question | Weight it higher when |
|---|---|---|
| Cost | How bad is it if this objection is right? | Money, reputation, safety, or relationships at stake |
| Reversibility | Can the user undo the choice cheaply? | One-way doors (hires, public announcements, contracts, health) |
| Likelihood | How plausible is it, given what they told you? | Their own facts point toward it |

Reversibility matters because it changes what the right next step is: reversible decisions call for a fast, cheap test; irreversible ones justify slowing down to gather evidence first.

## 7. Cheapest evidence

For each objection, ask what observation would settle it and what the cheapest way to get it is: a pilot on a subset, a customer call, a spreadsheet check against their own history, a reference call, a small paid test. The aim is to turn a debate into an experiment the user can run this week.
