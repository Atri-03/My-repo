Title: VWGSA AMS — GenAI Class 1
Filename suggested for PPTX: VWGSA_AMS_GenAI_Class1_VWGSA_AMS_Atri_Bandyopadhyay.pptx
Slide size: 16:9
Theme: Modern blue/teal gradient with subtle diagonal accents
Fonts: Headings — Segoe UI Semibold; Body — Segoe UI / Calibri
Notes: Use subtle professional animations (fade / wipe / zoom subtle), slide transitions (Fade or Push), and keep motion minimal for accessibility. Appendix slides are hidden by default.

---

Slide 1 — Title (Title Slide)
- Elements:
  - Title: "Introduction to Generative AI — Class 1"
  - Subtitle: "Foundations, Tools, and Practical Demos"
  - Placeholder: "Presenter: Atri Bandyopadhyay"
  - Placeholder: "Team: VWGSA AMS"
  - Placeholder: "replace-logo-here" (center-right or top-right)
  - Footer: Date / location (optional)
- Design notes:
  - Large title, teal-blue gradient background, white text, subtle geometric accent.
  - Use Segoe UI for title and Calibri for smaller text.
- Slide transition: Fade (duration 400ms)
- Animations: Title — Appear (0.5s), Subtitle — Fade in (0.6s), Placeholders — Appear on click (0.4s)
- Speaker notes:
  - Welcome the audience, quick intro to yourself and VWGSA AMS. Set expectations for 90-min session.
  - Mention interactive demos and appendix resources available.

---

Slide 2 — Agenda
- Bullet points:
  - Welcome & Objectives
  - What is Generative AI?
  - Key models & capabilities
  - Use-cases for VWGSA AMS
  - Demo & hands-on prompts
  - Ethics & safety considerations
  - Q&A and next steps
- Animations: Bullet points — Wipe (from left) staggered (0.3s each)
- Speaker notes:
  - Walk through agenda; estimate time per section.

---

Slide 3 — Learning Objectives
- List:
  - Understand generative AI fundamentals
  - Identify core model families (LLMs, Diffusion, etc.)
  - Run simple prompts & demos
  - Apply best practices for prompt design and evaluation
- Animations: Each objective Fade in sequentially
- Speaker notes: Clarify outcomes and what participants will be able to do by session end.

---

Slide 4 — What is Generative AI?
- Content:
  - Definition: Models that generate data (text, images, audio, code)
  - Examples of outputs and everyday uses
  - Distinction between discriminative vs generative models
- Visual: Two-column with a simple diagram showing inputs -> model -> outputs
- Animations: Diagram elements Zoom in slightly
- Speaker notes: Use accessible examples (auto-complete, image creation, code generation).

---

Slide 5 — Core Model Families
- Bullets:
  - Large Language Models (LLMs) — text generation, summarization
  - Text-to-Image / Diffusion Models — image generation
  - Text-to-Speech / Speech-to-Text
  - Multimodal models — combine modalities
- Quick table: strengths, typical latency, example providers (OpenAI, Hugging Face, Google, Stability AI)
- Speaker notes: Mention trade-offs: cost, latency, controllability

---

Slide 6 — How Generative Models Work (High-level)
- Content:
  - Training on large datasets, next-token prediction, diffusion steps
  - Conditioning and prompts
  - Fine-tuning vs prompting vs retrieval-augmented generation (RAG)
- Visual: simple flowchart
- Animations: Flowchart parts appear in sequence
- Speaker notes: Keep technical explanation high-level; avoid math-heavy details.

---

Slide 7 — Responsible AI & Safety Considerations
- Points:
  - Hallucinations & verification
  - Data privacy and PII
  - Bias and fairness
  - Access controls and monitoring
- Speaker notes: Provide quick mitigations: human-in-loop, RAG with sources, model selection.

---

Slide 8 — VWGSA AMS Use-cases (Overview)
- Bullets with short descriptions:
  - Automating reports & summaries
  - Drafting customer communications
  - Code generation and automation
  - Data exploration & insights
  - Image assets for collateral
- Animations: Icons appear with each bullet
- Speaker notes: Invite participants to call out which use-cases are most relevant to them.

---

Slide 9 — Example: Automating Reports
- Before vs After layout
- Include metrics that can be auto-generated (charts, summaries)
- Speaker notes: Show sample prompt used to generate an executive summary, and discuss verification steps.

---

Slide 10 — Prompt Design Best Practices
- Tips:
  - Be explicit about role, format, constraints
  - Provide examples (few-shot)
  - Request step-by-step when needed
  - Use temperature and max tokens appropriately
- Visual: mini how-to box with prompt template
- Animations: Template typeset fades in
- Speaker notes: Walk through a live example prompt and show variations and outputs.

---

Slide 11 — Demonstration Plan (Live Demos)
- Bullets:
  - Short text prompt demos (LLM)
  - RAG example with knowledge base
  - Image generation prompt
  - Notebook / Colab run
- Speaker notes: Clarify which demos will be live and which will be pre-run (to manage time).

---

Slide 12 — Demo 1: LLM Prompting (Structure)
- Show prompt template and expected output
- Include short demo transcript
- Animation: Show prompt then reveal model output
- Speaker notes: Explain intent, expected failure modes, and debugging steps.

---

Slide 13 — Demo 2: RAG Example (Search + LLM)
- Architecture diagram: user query -> retriever -> context -> LLM
- Show sample results and citations
- Speaker notes: Emphasize citations and using a retrieval store (e.g., Elastic, Pinecone)

---

Slide 14 — Demo 3: Image Generation (Prompting)
- Show a before (prompt) and after (image) example; include alt text
- Tips for better image prompts (stylistic tags, aspect ratio)
- Speaker notes: Remind about license, asset rights, and appropriate content filtering.

---

Slide 15 — Demo 4: Notebook / Colab Snippet
- Show a compact Colab code snippet (see appendix for full snippet)
- Visual: Screenshot of notebook output (placeholder)
- Speaker notes: Walk through running the cell and what to expect.

---

Slide 16 — Evaluation & Metrics
- List metrics to track model outputs: accuracy, factuality, ROUGE, BLEU, human evaluation
- Operational metrics: latency, cost per call, throughput
- Speaker notes: Discuss A/B testing and continuous monitoring.

---

Slide 17 — Integration Patterns
- Patterns:
  - API-first (serverless functions)
  - Agent pattern (tooling + LLMs)
  - Batch vs online inference
- Small architecture diagrams
- Speaker notes: Cover pros/cons for each pattern and recommended starting points.

---

Slide 18 — Governance & CI/CD for Models
- Topics:
  - Versioning prompts and model configs
  - Automated tests for prompts
  - Access control and logging
- Speaker notes: Emphasize reproducibility and rollback strategies.

---

Slide 19 — Cost Management
- Tips:
  - Token budgeting, model selection, caching
  - Hybrid approach: small model for routine tasks, large for complex tasks
- Speaker notes: Share typical cost-saving measures and monitoring tips.

---

Slide 20 — Example Project Roadmap
- Phases:
  - Pilot (1–2 teams)
  - Scale (frameworks and libraries)
  - Hardening (SLOs, security)
- Timeline graphic (3–6 months)
- Speaker notes: Suggest KPIs to measure pilot success.

---

Slide 21 — Case Study / Success Story
- Short story showing impact (metrics before/after)
- Visual highlights and quote
- Speaker notes: Keep concise; tie to VWGSA AMS priorities.

---

Slide 22 — Q&A (Interactive)
- Placeholder for audience questions
- Add quick poll suggestions (raise hand, chat)
- Speaker notes: Encourage practical, work-related questions; capture follow-ups.

---

Slide 23 — Next Steps & Resources
- Links to docs, internal resources, sandbox access, and office hours
- Call to action: Sign up for hands-on labs
- Speaker notes: Provide contact details and next workshop dates.

---

Slide 24 — Thank You / Contact
- Reiterate Presenter: Atri Bandyopadhyay and Team: VWGSA AMS
- Contact: email placeholder (e.g., atri@company.example)
- Social / slack channel link (if relevant)
- Speaker notes: Close session and invite feedback.

---

Hidden Appendix (hidden slides: set slide properties to Hidden)

Appendix A (Hidden Slide A1) — Demo Script: LLM Prompting
- Step-by-step script for running the text demo live
- Include exact prompts to copy/paste and expected verbiage to read aloud.
- Speaker notes: Keep timings (e.g., 2 min for prompt, 1 min to review)

Appendix B (Hidden Slide A2) — Ready-to-use Prompts (Text)
- Prompts grouped by use-case:
  - Executive summary: "You are a senior analyst. Summarize the following report in 4 bullet points..."
  - Code generation: "Write a Python function to ..." with required signature
  - Customer response template: "Draft a polite reply to a customer who..."
- Variants with temperature and max tokens suggestions

Appendix C (Hidden Slide A3) — Image Prompts
- Examples for marketing assets and diagrams
- Guidance: aspect ratio, stylistic tags, negative prompts

Appendix D (Hidden Slide A4) — Colab Snippets (Ready to run)
- Minimal Colab snippet for calling an LLM (pseudo-code / Python)

Example Colab snippet (Python)
```
# Install dependencies
!pip install -q openai transformers

# Example using OpenAI pseudo-client
from openai import OpenAI
client = OpenAI(api_key="YOUR_API_KEY")

prompt = "Summarize the following text in 3 bullets: <paste text here>"
resp = client.responses.create(model="gpt-4o-mini", input=prompt)
print(resp.output[0].content[0].text)
```

- Also include a small snippet for RAG using FAISS / Chroma:
```
# Pseudocode
from langchain import FAISS, OpenAI, RetrievalQA
# load embeddings, build index, query
```

Appendix E (Hidden Slide A5) — Instructor Checklist
- Before the session:
  - Verify projector / screen scaling (16:9)
  - Confirm internet access and demo environment
  - Prepare alternate screenshots if live demos fail
  - Print or have quick links to appendix resources
- During the session:
  - Timebox demos
  - Monitor chat & capture follow-ups
  - Encourage hands-on sign-ups

Appendix F (Hidden Slide A6) — Troubleshooting & FAQs
- Common issues and quick fixes (API keys, quota, image generation timeouts)
- Suggested answers to participant FAQs


Accessibility and deliverables notes
- Keep alt text on images, use high-contrast text, avoid long flashing animations.
- Provide an attendee handout (PDF) with key prompts and Colab links (can be generated from appendix content).

Animation & Transition Summary (for authoring in PowerPoint)
- Default slide transition: Fade (duration 400ms) with subtle sound off
- Heading animation: Appear (0.5s) with ease-out
- Fat content reveal: Wipe or Fade in staggered 0.25–0.4s
- Images: Subtle Zoom in 1.0x -> 1.03x on entry for emphasis
- Keep animations per slide <= 4 elements to maintain clarity

Authoring tips (to create the PPTX from this doc)
1. Create a 16:9 blank presentation and apply a master slide with the blue/teal gradient and Segoe UI/Calibri fonts.
2. Add the title slide as specified and set placeholders for presenter/team/logo.
3. Build each slide with the provided content; apply suggested animations via the Animations pane and Transitions pane.
4. Mark appendix slides as hidden (right-click > Hide Slide).

If you want, I can:
- Generate a downloadable PPTX here (best-effort, may lack complex animations and notes) and commit it instead.
- Or I can open a PR instead of committing directly to main.

---

End of file. If you need the actual .pptx binary generated and committed instead of this markdown, reply and I will attempt to create a best-effort .pptx and commit it to the same path you originally requested.
