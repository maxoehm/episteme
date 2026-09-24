# Constrained Decoding and Structured Outputs

## The Problem Statement

The construction of a Knowledge Graph from scientific literature requires extracting highly structured data (nodes,
edges, properties) suitable for programmatic insertion into a graph database like Neo4j. Traditionally, this is achieved
by instructing Large Language Models (LLMs) to output data in structured formats like JSON. However, recent research
reveals a fundamental tension between enforcing strict structural compliance and preserving an LLM's capacity for
complex reasoning.

To formalize the problem, constrained decoding can be mathematically described as generating a sequence of tokens where
each token is restricted to a predefined structure. As defined by the Hasso Plattner Institute (2025, p. 1075), if we
generate a sequence \(x = [x_1, x_2, \dots, x_{|x|}]\), each token \(x_i\) must follow a predefined structure \(S\). The
decoding process filters the model's normal next-token distribution to create a restricted set of valid tokens, \(C_i\),
excluding any tokens that would violate \(S\). Formally, the probability \(p (x_i | x_{<i}, S) = 0\) for any token \(x_i
\notin C_i\).

While this algorithm successfully enforces compliance (Deutsch et al., 2019), it carries hidden costs. Tam et al. (2024)
observed a "significant decline in LLMs' reasoning abilities under format restrictions," noting that overly restrictive
schemas hinder reasoning-intensive tasks.

### Hypothesis on the Underlying Causes of Degradation

The performance degradation under constrained decoding, particularly in instruction-tuned models, seems to stem from a
conflict between their learned objectives and structural enforcement. The Hasso Plattner Institute (2025) identifies a "
probability gap": instruction tuning biases models toward generating explanatory, natural language constructs (e.g.,
Chain-of-Thought). When constrained decoding blocks these preferred, high-probability tokens to enforce syntax, it
forces the model into lower-probability distributions of structured alternatives. This disrupts the model's learned
patterns for executing complex instructions effectively.

## Key Observations and Considerations

### 1. Task Dependency and the JSON-mode Gap

The impact of structured formats is highly task-dependent. Studies utilizing "JSON-mode" (a common method for enforcing
valid JSON syntax) highlight a stark divergence. Tam et al. (2024) found that JSON-mode improves performance on
classification tasks by restricting the possible answer space, thereby reducing errors in answer selection. In contrast,
on reasoning-intensive tasks, JSON-mode frequently fails to adhere to logical ordering (e.g., forcing the answer before
the reasoning), causing large drops in final performance. The Hasso Plattner Institute (2025) corroborates this, arguing
that classification stability arises because the model is merely selecting among predefined answers—an inherently
constrained task—whereas reasoning requires unconstrained generation.

### 2. Implementation via Guided Decoding

To enforce these constraints in practice, developers rely on guided decoding frameworks. Tools and libraries such as
`guidance`, `xgrammar`, `outlines`, and `llama.cpp` interface directly with the inference engine to manipulate the token
distribution in real-time to match a JSON Schema (Geng et al., 2025). While these tools guarantee schema compliance,
they are the direct mechanisms that introduce the aforementioned distributional shifts and tokenization ambiguities.

### 3. Prompting Strategies: Hard vs. Soft Prompting

When controlling models for structured extraction, the prompting methodology is critical (Liang et al.):

* **Hard Prompting:** Relies on discrete text instructions. It is highly sensitive to exact word choice, where minor
  changes significantly alter generation quality. Techniques like *AutoPrompt* attempt to optimize this by using
  gradient-based search methods to automatically discover optimal trigger words that maximize task performance without
  requiring full model fine-tuning.
* **Soft Prompting:** Uses continuous, trainable vector embeddings instead of discrete words. This allows for more
  flexible, fine-grained control and is highly effective for complex, multi-faceted tasks, although it suffers from
  lower interpretability and requires an initial tuning phase.

### 4. The Impact of Structured Input

While structured output can hinder reasoning, structured *input* can be highly beneficial. Narvekar et al. (2025) found
a clear preference for JSON format as an input context across models, with smaller models (which have limited capacity
and context windows) benefiting the most significantly from structured input compared to unstructured text or YAML.

### 5. Evaluation Challenges in Knowledge Graphs

Evaluating the extraction of Knowledge Graphs is notoriously difficult. Sérasset et al. (2026) note that relying on
automatic metrics like Triple F1 systematically underestimates extraction quality, as models often predict textually
valid triples that are absent from incomplete gold annotations.

## Methodological Approaches to Formatting

To bridge the gap between reasoning and structured output, several approaches have emerged:

* **NL-to-Format (Two-Step):** Instructing the LLM to answer in natural language first, then instructing it to convert
  the response into the target schema. This decouples content generation from format adherence (Tam et al., 2024).
* **In-Writing (Unified Framework):** A hybrid approach where unconstrained reasoning occurs first, and structured
  decoding is only applied after a specific "trigger token" is generated, explicitly decoupling the two phases in a
  single call (Nguyen et al., 2026).

## Strategic Aspects for System Design

Based on the literature, the following aspects must be considered when designing an LLM-based graph extraction pipeline:

1. **Decouple Reasoning from Mapping:** Avoid forcing the model to reason *while* generating JSON. Leverage NL-to-Format
   or Trigger-based hybrid approaches.
2. **Leverage Classification:** Use constrained decoding frameworks (`guidance`, `xgrammar`) where the task is primarily
   classifying pre-identified relationships into the target schema.
3. **Format Context as JSON:** Provide existing graph context or memory to the LLM in JSON format, especially when
   utilizing smaller, lower-capacity open-source models.

## References

* Deutsch, D., Upadhyay, S., & Roth, D. (2019). A General-Purpose Algorithm for Constrained Sequential Inference.
  *Proceedings of the 23rd Conference on Computational Natural Language Learning (CoNLL)*.
* Geng, S., et al. (2025). JSONSchemaBench: A Rigorous Benchmark of Structured Outputs for Language Models. *arXiv
  preprint arXiv:2501.10868*.
* Hasso Plattner Institute, Germany, et al. (2025). The Hidden Cost of Structure: How Constrained Decoding Affects
  Language Model Performance. *The 15th International Conference on Recent Advances in Natural Language Processing RANLP
  2025*.
* Liang, X., et al. Controllable Text Generation for Large Language Models: A Survey.
* Narvekar, A., Mukherjee, T., & Tanuwijaya, J. (2025). Evaluating the Impact of Input Format on LLM Performance: JSON
  vs. YAML vs. Text. *2025 IEEE International Conference on Future Machine Learning and Data Science (FMLDS)*.
* Nguyen, N. T. H., et al. (2026). Thinking Before Constraining: A Unified Decoding Framework for Large Language Models.
  *arXiv preprint arXiv:2601.07525*.
* Sérasset, G., et al. (2026). Knowledge Graphs and Large Language Models Workshop 2026 (KG-LLM) @ LREC 2026: workshop
  proceedings.
* Tam, Z. R., et al. (2024). Let Me Speak Freely? A Study on the Impact of Format Restrictions on Performance of Large
  Language Models. *arXiv preprint arXiv:2408.02442*.
