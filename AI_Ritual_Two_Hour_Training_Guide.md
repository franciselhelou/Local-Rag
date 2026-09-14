# AI Ritual Training Guide

## Building a Local RAG and Selecting the Right AI Opportunity

**Audience:** Mid-career professionals who use notebooks but are not software engineers.  
**Duration:** 120 minutes.  
**Format:** Instructor-led explanation, guided local demo, Colab comparison, and process-design exercise.  
**Primary message:** AI should be selected because it improves a defined process outcome—**speed, accuracy, efficiency, or a deliberate combination**—not because a particular model is fashionable.

> **Facilitation stance:** This is a practical literacy session, not a promise that every learner will become an AI engineer in two hours. Learners leave with a working, inspectable RAG example, a repeatable model-selection method, and a disciplined way to identify worthwhile AI opportunities.

## Learning objectives

At the end of the session, participants should be able to describe how a local RAG system retrieves evidence before generating an answer; identify the installation and trust requirements for a Windows-first, offline-after-preparation RAG setup; read a Hugging Face model card as a decision document rather than a catalogue entry; run the supplied local script or Colab notebook; and select among rules, classification, clustering, semantic search/RAG, and generative AI based on the business task and measurable outcome.

## Pre-session preparation

The local lab must be prepared **before** the live session. A download during a two-hour workshop risks consuming the practical time and obscuring the architecture. Ask learners to complete the pre-flight checklist 24–48 hours earlier. The instructor should also have a tested demonstration computer and the Colab notebook open on a GPU-enabled runtime.

| Item | Learner action before class | Why it matters |
| --- | --- | --- |
| Windows version | Confirm Windows 10 or later. | The selected local runtime’s Windows download page states this baseline requirement. [1] |
| Python | Install Python 3.11+ and confirm `py --version` in PowerShell. | The local script runs in a Python virtual environment. |
| Local runtime | Install Ollama, then run `ollama --version`. | It hosts the generator on the learner’s device. |
| Small generator | While online, run `ollama pull llama3.2:3b`. | The small model is downloaded once and then used locally. |
| Python packages | Create `.venv`, activate it, and run `pip install -r requirements.txt`. | This isolates workshop libraries from other work. |
| Embedding model | While online, run `python offline_rag.py --prepare`. | It caches the Hugging Face embedding model locally. |
| Verification | Build the supplied document index once, then run the supplied offline question. | It identifies installation issues before teaching starts. |
| Colab | Sign into a Google account and open the notebook. | The Colab comparison needs a temporary cloud runtime and model download. |

The supplied local guide includes copy-and-paste commands, an offline-mode check, and troubleshooting. It should be sent together with the session invitation, not introduced for the first time in the room.

## Two-hour run of show

| Time | Segment | Instructor approach | Learner output |
| --- | --- | --- | --- |
| 00:00–00:08 | **Start with the process, not the model** | Set the objectives. Ask participants to name one repeated decision, search task, or review queue in their work. Introduce the three value dimensions: speed, accuracy, and efficiency. | A candidate process written down in one sentence. |
| 00:08–00:20 | **What RAG changes** | Contrast a general model answering from learned patterns with RAG answering using retrieved local passages. Walk through the chain: documents → chunks → embeddings → retrieval → grounded prompt → answer with sources. | Participants can explain the role of retrieval. |
| 00:20–00:32 | **Local, private, and secure are different claims** | Explain the one-time online download versus offline operation after setup. State clearly that local does not automatically mean “100% secure.” Cover trusted software/model sources, licences, local device protection, document permission, and avoiding sensitive data in Colab. | A practical trust-boundary checklist. |
| 00:32–00:44 | **Windows components and their jobs** | Use the local script and a diagram to connect each component to a job: Ollama, small generator, embedding model, NumPy retrieval, PDF reader, and documents. Show where files live. | A component-to-function map. |
| 00:44–00:56 | **Hugging Face: select, do not browse blindly** | Tour a model page and model card. Explain task tags, intended use, language, licence, size/quantization, format/runtime compatibility, limitations, and evaluation. Introduce the 8 GB default configuration. | A completed mini model-card checklist. |
| 00:56–01:14 | **Guided local RAG run** | Build the saved index once from the fictional restaurant files, then run offline questions. First inspect retrieved chunks; only then read the answer. Change the question and demonstrate a question with no supporting evidence. If learner machines are ready, pair them for the same task. | A local answer with evidence labels and an observed abstention test. |
| 01:14–01:24 | **Why Colab changes capacity, not responsibility** | Open the companion notebook. Explain the larger 7B model, GPU requirement, 4-bit quantization, and public model download. Emphasise that the embedding/retrieval steps and evaluation discipline remain the same. | A clear local-versus-Colab comparison. |
| 01:24–01:42 | **Find the opportunity** | Teach the process-opportunity canvas and use a participant process as a live example. Define the current baseline and locate delay, error, and effort. | A one-page candidate problem statement. |
| 01:42–01:56 | **Choose the AI job** | Work through the restaurant-review case. Separate labels known in advance from themes not yet known. Show why Bag of Words is a representation/baseline, not the business task. | A justified technology choice and success metric. |
| 01:56–02:00 | **Commit to a small next experiment** | Each learner names one process, its metric, the proposed technology, a risk, and the next test. Close by collecting questions. | A 30-day experiment hypothesis. |

## The local RAG explanation

A RAG system does not retrain a language model on an organisation’s documents. Instead, it retrieves relevant passages when a question is asked and passes those passages into the model’s working context. The answer is therefore constrained by a **current, inspectable evidence set**. This supports provenance and can reduce unsupported answers, but only when the source documents are relevant, the retrieval step finds them, and the model follows the instruction to remain grounded.

| Stage | Plain-language explanation | What can go wrong | Practical control |
| --- | --- | --- | --- |
| Documents | The approved source material, such as policies, manuals, or procedures. | Out-of-date, incomplete, or unauthorised content. | Assign ownership, refresh dates, access rules, and a small representative evaluation set. |
| Chunking | Documents are split into manageable passages while retaining source metadata. | A key condition is split away from its exception or context. | Review chunks; tune chunk length/overlap; preserve document/page reference. |
| Embeddings | A compact model turns each passage and question into numbers representing meaning. | English-only model used for multilingual text; semantically similar but wrong context retrieved. | Match the model to the language and test retrieval separately. |
| Retrieval | The system ranks passages most similar to the question. | Relevant evidence is absent from the top results. | Inspect top results, alter chunking, improve documents, add filters/reranking at scale. |
| Prompt | Retrieved evidence plus an instruction is supplied to the generator. | Instructions are weak, context is overloaded, or sources conflict. | Require citations, restrict the answer to sources, define abstention, keep context modest. |
| Generation | A local or cloud model writes the response. | Fluent but unsupported wording; inconsistent outputs. | Low temperature for factual use, evaluation, human review for consequential tasks. |

The local lab deliberately uses NumPy rather than a vector database. For a small classroom corpus, direct cosine similarity makes the mechanism visible and removes a Windows dependency. The script persists the resulting normalized vectors and source metadata in a local `rag_index` folder; it rebuilds only after a supported document changes. Hugging Face’s semantic-search material explains that embeddings can represent whole passages and can be compared to find semantically similar documents; it introduces FAISS for efficient search at a larger scale. [2] In production, a dedicated vector database becomes reasonable when corpus scale, metadata filtering, persistence, access control, or query throughput justifies the added complexity.

## Hugging Face and component selection

Hugging Face is a repository and documentation ecosystem for models, datasets, and related components. In this session, it is not presented as a source of “the best model.” It is where learners can find the **model card** that describes intended uses, limitations, datasets, evaluation results, and licence. [3] A model’s task tag helps establish what job it was made to perform, but the final selection still requires local testing with representative inputs.

| Selection question | Local RAG choice | Larger Colab choice | Reasoning to teach |
| --- | --- | --- | --- |
| What job is being selected? | Generator and embedding model are separate jobs. | The same two jobs remain separate. | Do not use one general model indiscriminately when a smaller specialist can do retrieval. |
| Generator | `llama3.2:3b` through Ollama. | `Qwen/Qwen2.5-7B-Instruct` through Transformers. | The local model prioritises fit on constrained RAM; Colab exploits temporary GPU capacity. |
| Memory strategy | Small local model selected for constrained devices; close other applications. | 4-bit NF4 quantization on a CUDA GPU. | Quantization is a resource trade-off, not a quality guarantee. [4] |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2`. | The same model. | Compact 384-dimensional semantic embeddings make the retrieval step practical. [5] |
| Trust/licence | Verify publisher, licence, intended use, and download provenance. | Perform the same checks, plus cloud data approval. | “Free to download” does not equal “approved for every business use.” |
| Language | English practice corpus. | English practice corpus. | Select multilingual components if users or evidence are multilingual. |
| Evidence | Local documents remain authoritative. | Uploaded Colab documents are copied to a cloud runtime. | Capacity does not replace source quality or governance. |

> **Facilitator note:** Do not claim a precise RAM requirement or token speed for every 8 GB laptop. Operating system load, other programs, processor type, integrated graphics, context length, and model format all affect the experience. Frame this configuration as a deliberately small default, then point learners to Colab when a laptop cannot run it comfortably.

## Find AI opportunities: the process-opportunity canvas

Start with a process rather than with an AI solution. A candidate is strong when the inputs and outcome are observable, the volume or consequence is meaningful, a baseline can be measured, and someone owns the result. A process is weak when the desired outcome is vague, the evidence is inaccessible, an error would cause unacceptable harm without review, or a simpler non-AI change would solve the bottleneck.

| Canvas field | Questions to ask | Example: restaurant review flow |
| --- | --- | --- |
| Process and owner | What actually happens today? Who owns the outcome? | Reviews arrive on several platforms; the operations manager owns the response and weekly insights. |
| Trigger and volume | What starts the work? How often? Is demand variable? | New review received; 2,000 reviews per month with weekend spikes. |
| Decision or output | What must a person decide, classify, retrieve, draft, or execute? | Decide review topics and owner; draft a safe response; aggregate recurring themes. |
| Inputs and evidence | What information is available and permitted? | Review text, rating, channel, date, location, menu items, existing policy. |
| Current baseline | How long, how often wrong, how much rework, what cost? | 4.5 minutes per review; 36-hour assignment delay; 15% miscoded themes. |
| Desired change | Is the priority speed, accuracy, efficiency, or more than one? | Reduce time to owner and staff effort while retaining correct, auditable categorisation. |
| Error cost and risk | Who is harmed if it is wrong? What is the escalation route? | Allergy, discrimination, or potential safety review must route to a human immediately. |
| Measure and decision threshold | What test will prove value? What result warrants scale? | ≥90% agreed topic routing on a held-out set; median assignment time under 5 minutes; 50% less staff handling. |

The desired improvement must be made explicit. **Speed** means less elapsed time, such as time from review arrival to correct owner. **Accuracy** means a higher proportion of correct, complete, or well-grounded outcomes. **Efficiency** means more useful output per unit of staff time, cost, energy, or rework. One system can improve all three, but they can also conflict. For example, a large model may draft richer responses but be slower and more expensive; an automated router may increase speed but lower accuracy on ambiguous reviews unless it has a human-review threshold.

| Value dimension | Baseline metric | Example target | Guardrail |
| --- | --- | --- | --- |
| Speed | Median time to category/owner; total response lead time. | Route routine reviews within five minutes. | Do not delay priority safety or legal escalation. |
| Accuracy | Precision, recall, F1, human agreement, grounded-citation rate. | At least 90% agreement with an approved human label set. | Report performance by category, not only an average. |
| Efficiency | Staff minutes/review, cost/review, rework rate, cases/person-hour. | Reduce manual first-pass handling by 50%. | Include review and exception-handling time, not just model runtime. |

## Select the technology by the job

The phrase “use AI” hides several very different tasks. First define the output. Then choose the simplest technology that can meet the defined threshold and governance constraints. A robust workflow often combines approaches rather than declaring one universal winner.

| Business job | Best starting technology | When it fits | What it is not for |
| --- | --- | --- | --- |
| Apply a stable, explicit policy | Rules/workflow automation | Conditions, exceptions, and actions are known and rarely change. | Interpreting complex, ambiguous free text without reliable signals. |
| Assign known labels | Supervised classification | A fixed taxonomy exists and there are enough representative labelled examples. | Discovering themes nobody has defined yet. |
| Discover unknown themes | Clustering/topic discovery | The aim is exploration, segmentation, or taxonomy design; human interpretation is expected. | Stable operational categories without a human naming and QA step. |
| Match literal terms or use a transparent baseline | Bag of Words / TF-IDF features | Strong keyword signals, limited data, explainability needs, and a quick baseline. | Treating synonyms, negation, context, or nuanced meaning reliably. |
| Find semantically relevant knowledge | Embeddings + semantic search / RAG | The answer must be grounded in changing documents and show evidence. | Determining a fixed label when a simpler classifier is adequate. |
| Draft, summarise, extract flexible language, or handle long-tail ambiguity | Generative AI | Desired output is open-ended language, schema extraction, or flexible synthesis; evaluation and guardrails exist. | An unattended source of truth, especially in high-impact decisions. |
| Combine stable routing with flexible handling | Hybrid system | Most cases are repeatable but exceptions need language understanding or human judgment. | Avoiding process ownership or evaluation. |

## Case exercise: restaurant review categorisation

Frame the question precisely: “We receive thousands of customer reviews. We want to route them to the right owner, identify emerging themes, and reduce staff time without silently mishandling safety or discrimination complaints.” The word **categorisation** alone is not enough to select a technology. The correct choice depends on whether the categories are known and stable, whether labelled examples exist, and whether the output needs to be a label, a discovery insight, a factual answer, or a customer-facing draft.

| Option | Is it a good fit? | Why | Recommended role |
| --- | --- | --- | --- |
| Supervised classification | **Yes, for a stable taxonomy.** | If topics such as food quality, waiting time, hospitality, delivery, price/value, and allergy concern are defined and historical reviews have reliable labels, classification can route at scale. | Primary production router for high-volume, routine reviews, with confidence thresholds and human escalation. |
| Clustering | **Yes, for discovery—not final routing by itself.** | It groups similar reviews and can reveal new issues, such as a recurring packaging problem or a new menu complaint. The groups require people to interpret and name them. | Monthly theme discovery and early taxonomy design. Human analysts confirm what a cluster means. |
| Bag of Words / TF-IDF | **Useful baseline, not the business solution.** | It is a text representation and can support a lightweight classifier. It is fast and interpretable when words are reliable signals, but it does not truly understand synonymy, negation, or context. | Establish the simplest measurable benchmark; retain as a low-cost fallback for narrow keyword rules. |
| Generative AI | **Useful selectively, not automatically the first answer.** | It can label zero-/few-shot reviews, extract multiple aspects, explain a route, summarise themes, and draft response suggestions. It can also be variable, costlier, harder to evaluate, and prone to unsupported wording. | Bootstrap labels, handle long-tail/ambiguous cases, extract structured details, and assist humans under clear evaluation. |
| RAG | **Useful for response assistance, not the basic label alone.** | When a staff member needs the current refund, allergen, or service-recovery policy, RAG can retrieve approved policy text before generating a response. | Ground suggested public responses in the latest approved operating playbook. |

The recommended **hybrid design** is sequential. First, use clustering and human review to discover themes and agree a taxonomy. Next, produce a gold-standard labelled evaluation set. Then use a classifier for common known categories, with rules for obvious safety escalations. Send low-confidence, multi-topic, new-theme, safety, and reputationally sensitive cases to a human or a carefully tested generative AI assistant with human approval. Use RAG only where the output needs current policy evidence, such as drafting a response consistent with the restaurant’s refund or allergen guidance.

| Review text | Desired output | Appropriate initial route | Human role |
| --- | --- | --- | --- |
| “Wonderful food but we waited 45 minutes for the main course.” | `food_quality=positive`, `waiting_time=negative`; route waiting issue to front of house. | Multi-label classifier if trained; otherwise validated generative extraction. | Sample QA, resolve ambiguous multi-topic cases. |
| “I think the nut-free option may have touched another dish.” | Immediate safety escalation; no automated reassurance. | High-priority rule plus human workflow; RAG can retrieve the approved allergen process for the manager. | Mandatory immediate review. |
| “The new takeaway containers made the salad soggy.” | Potential emerging packaging theme. | Cluster with similar reviews; optionally generative summarisation after review. | Name/confirm theme and decide whether it becomes a stable class. |
| “Too expensive for what you get.” | `price_value=negative`; include in weekly trend. | Known-label classifier or transparent baseline. | Audit category quality and interpret trend alongside pricing changes. |

### Exercise instructions

Form groups of three. Give each group a process from one participant’s work or the restaurant-review case. In eight minutes, they should complete the canvas, choose the **primary task**, identify the simplest suitable technology, name the first metric, and define the cases that must remain with a person. In the debrief, do not ask “Which model would you use?” Ask instead: “What outcome improves, what evidence is available, how will we know, and what happens when the system is uncertain?”

## Evaluation and next steps

A pilot is not successful because an answer looks impressive. It is successful if it meets the pre-agreed threshold on representative cases while respecting the risk controls. Build a test set before scaling. Keep it separate from the examples used to design prompts or choose model settings. For RAG, assess retrieval relevance, factual support, citation/source correctness, abstention on unanswerable questions, and user usefulness. For categorisation, assess per-class precision and recall, confidence calibration, exception rate, and the time saved including human review.

The final commitment is a one-sentence experiment: **“For [process], we will use [technology] to improve [speed/accuracy/efficiency metric] from [baseline] to [target], while sending [risk/low-confidence cases] to [human owner].”** This statement prevents technology-first experimentation and supplies the basis for a 30-day pilot.

## References

[1]: https://ollama.com/download/windows "Ollama — Download for Windows"
[2]: https://huggingface.co/learn/llm-course/en/chapter5/6 "Hugging Face LLM Course — Semantic Search with FAISS"
[3]: https://huggingface.co/docs/hub/en/model-cards "Hugging Face — Model Cards"
[4]: https://huggingface.co/docs/transformers/quantization/bitsandbytes "Hugging Face — Bitsandbytes quantization"
[5]: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2 "Sentence Transformers — all-MiniLM-L6-v2 model card"
