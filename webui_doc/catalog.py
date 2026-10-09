"""Static editorial catalogue for the 19 authored web chapters.

The site deliberately has no CMS or post model.  Copy, sequence and visual
metadata live here, while Django only resolves a known chapter slug.
"""

DRIVE = "https://docs.google.com/document/d/{}/edit"


def chapter(number, slug, title, subtitle, category, intro, summary, headline,
            source_id, modules, outcomes, practice):
    return {
        "number": number,
        "slug": slug,
        "title": title,
        "subtitle": subtitle,
        "category": category,
        "intro": intro,
        "summary": summary,
        "headline": headline,
        "heading": tuple(headline.rstrip(".").split("|", 1)) if "|" in headline else (headline, ""),
        "cover": f"imgs/{number}-cover.svg" if int(number) >= 5 else f"imgs/{number}-image-{ {'00': 1, '01': 2, '02': 1, '03': 0, '04': 2}[number] }.webp",
        "source": DRIVE.format(source_id),
        "modules": [{"id": f"{number}-{i + 1}", "title": item[0], "copy": item[1], "signal": item[2]} for i, item in enumerate(modules)],
        "sections": [{"id": f"{number}-{i + 1}", "title": item[0]} for i, item in enumerate(modules)],
        "outcomes": outcomes,
        "practice": practice,
    }


CHAPTERS = (
    chapter("00", "roadmap-architecture", "Roadmap & Architecture", "The complete map before the first setting.", "Foundations", "See the platform as connected layers: interface, model providers, knowledge, tools and operations. That map prevents configuration by guesswork.", "A working mental model for the system you are about to build.", "The map before|the journey.", "16izJPTwF1fuq9cQM_XMdsZSrhmxl071hX0U65bn1_1I", [
        ("Open WebUI is the control plane", "It is the layer where people choose models, keep conversations, attach knowledge, manage access and coordinate actions. It is not the model runtime, vector database or every external service by itself.", "Keep responsibilities separate."),
        ("Follow one message", "A prompt travels from browser to Open WebUI, then gathers instructions, retrieved evidence and tool definitions before reaching a provider. The response may return directly or trigger a controlled action loop.", "Trace the request path."),
        ("The building blocks", "Models generate language. Knowledge supplies evidence. Tools perform actions. Functions and connectors change how the system behaves. Each block answers a different problem, so add one only when the problem exists.", "Context is not capability."),
        ("The Zero to Hero path", "Start with interface and installation, learn models and RAG, then add tools, agents, automation, APIs and production operations. The sequence narrows uncertainty before complexity arrives.", "Foundations → build."),
        ("Security is a boundary map", "Application permissions matter, but so do provider keys, Docker volumes, the host, networks and external services. A secure platform makes those boundaries explicit from day one.", "Trust has layers."),
    ], ["Explain where inference happens and where it does not.", "Draw the path of a message through your own setup.", "Name the boundary that protects each secret."], ("Sketch your intended platform", "Write down one model provider, one knowledge source and one action you may add later. Label which component owns each responsibility.")),

    chapter("01", "what-is-open-webui", "What Is Open WebUI?", "Interface, concepts and the first useful mental models.", "Interface", "Learn the interface by responsibility rather than by the current location of each control. The layout can change; the four surfaces remain useful.", "A practical tour of Chat, Workspace, Settings and Admin.", "Get to know|your cockpit.", "1Q4IyA08vCqVPZquHU7N27UwD38sGMoopQI3dVNoUQ9U", [
        ("Four surfaces, four jobs", "Chat is daily work. Workspace stores reusable components. Settings belong to a person. Admin controls the shared instance. When a setting feels hard to find, ask which responsibility it serves.", "Find features by job."),
        ("Chat carries more than a prompt", "A conversation can include the selected model, instructions, attachments, retrieved sources, tools and history. The model picker chooses an engine or reusable preset, not merely a brand name.", "Every answer has context."),
        ("Workspace makes work repeatable", "Models, Knowledge, Prompts, Skills and Tools package intent into components others can use. A Workspace Model can combine a base model with instructions and approved capabilities.", "Build once, reuse carefully."),
        ("Settings versus Admin", "Personal preferences shape one user experience. Admin settings set global policy, connections and access. Treat an instance-wide toggle as operational change, not as a personal experiment.", "Scope changes risk."),
        ("First-session discipline", "Confirm a simple chat works before you upload documents or attach tools. Then inspect the sidebar and each Workspace area without changing it. A known baseline makes later diagnosis much faster.", "Prove the baseline."),
    ], ["Locate the four core surfaces.", "Describe what a Workspace Model adds to a base model.", "Distinguish a personal preference from an instance policy."], ("Run a clean first chat", "Open a new chat, choose one familiar model and ask a short question. Verify the response before changing any other setting.")),

    chapter("02", "installation", "Installing Open WebUI Properly", "Docker, persistence, networking and safe updates.", "Deployment", "A durable setup starts by separating the replaceable application from its data, model runtime and network. Docker Compose makes that separation readable and repeatable.", "Build a home for your AI that you can update and recover.", "Build a home|for your AI.", "1kGfWoed-O3vArREEMfAbvPTnu5ZZ4NbfqUU8CqccccA", [
        ("Containers are replaceable; data is not", "The Open WebUI image can be recreated at any time. Its data directory cannot. Persist it in a named volume or carefully protected host path, and include it in your backup plan.", "State needs a home."),
        ("Compose is the maintainable baseline", "A Compose file records image versions, ports, volumes and environment variables in one reviewable place. It turns a working command into an installation another person can understand and reproduce.", "Configuration is documentation."),
        ("Networking is part of the design", "A container cannot reach a host service by assuming localhost means the physical machine. Use service names on a Docker network, or a host gateway deliberately, and test the exact route Open WebUI uses.", "Name the network path."),
        ("GPU use has two owners", "Open WebUI serves the interface; Ollama or another provider performs inference. Giving a GPU to the web interface does not automatically accelerate the model runtime.", "The runtime owns inference."),
        ("Update as a small release", "Back up persistent data, pin or record the version, pull the image, restart, inspect logs and test one real chat. An update is complete only when the original use case still works.", "Backup → update → verify."),
    ], ["Explain why the data directory must persist.", "Read a Compose file and identify its durable state.", "Test connectivity from the application to a model provider."], ("Make your deployment note", "Record the image tag, data volume, provider address and the command you would use to inspect logs. This is the beginning of an operations runbook.")),

    chapter("03", "local-llms", "Understanding Local LLMs", "Parameters, quantization, VRAM, context and model families.", "Models", "Model names become useful once you can separate parameter count, quantization, format, context and hardware budget. A model that starts is not automatically a model that fits the task.", "Choose a local model with evidence instead of folklore.", "Understand|your local LLMs.", "1yKY0e58TG10PJax0xIS734Zqw6xNlC_YabpVIhzWoLk", [
        ("Tokens and parameters", "Tokens are the units a model reads and emits. Parameters are learned weights that shape capability. More parameters can improve quality, but they also increase memory, loading time and the cost of each generated token.", "Size changes trade-offs."),
        ("Quantization changes storage precision", "Q4, Q5, Q6 and Q8 describe compressed representations of weights. Lower precision often reduces memory pressure; higher precision may preserve more quality. Test the task you actually care about rather than assuming a universal winner.", "Format and precision differ."),
        ("VRAM, RAM and disk solve different problems", "Disk stores a model at rest. RAM helps the host and any CPU-offloaded layers. VRAM keeps active weights and the KV cache close to the GPU. A system can have plenty of disk yet remain slow.", "Fit is not enough."),
        ("Context consumes a KV cache", "A larger context lets the model see more tokens, but the memory used for attention state grows with it. Treat context length as a real resource budget, especially with RAG or long coding sessions.", "Budget the conversation."),
        ("Select by workload", "General chat, coding, reasoning, vision, embeddings and tool calling reward different model properties. Begin with a modest model that fits cleanly, run representative prompts and keep notes on quality and latency.", "Measure your use case."),
    ], ["Read the important parts of a local model name.", "Estimate why context length affects VRAM.", "Choose an evaluation prompt for one model category."], ("Create a model scorecard", "For one candidate model, record its size, quantization, context target, first-token latency and one quality observation from a real task.")),

    chapter("04", "configuring-models", "Choosing & Configuring Models", "System prompts, context, sampling, presets and practical evaluation.", "Configuration", "A useful assistant begins with a defined job. Prompts, sampling and context are levers for that job; presets preserve a configuration you can explain and repeat.", "Turn a capable model into an assistant with a clear role.", "Make it|your assistant.", "1GeacwD5gkRp5jFnqJzrLcPJXjE61riqXWEPLRYumSuM", [
        ("Choose for the task, not the leaderboard", "Ask whether you need chat, code, reasoning, vision, embeddings or tool calling. Then consider quality, latency, privacy, context and hardware. Fame is not a specification.", "The task sets the bar."),
        ("Keep configuration layers clear", "Provider defaults, model runtime settings, Workspace Models and per-chat overrides can all influence output. Know where a value is set before you try to tune it.", "Find the source of truth."),
        ("Context is a working budget", "The system prompt, chat history, retrieved chunks and tool schemas compete for a finite window. Give the model relevant evidence, then remove noise before adding more text.", "Useful context beats more context."),
        ("Sampling controls variation", "Temperature and related controls influence how predictably the next token is chosen. Start with defaults, change one variable at a time and tie every adjustment to an observed failure mode.", "Tune with a hypothesis."),
        ("Presets make quality repeatable", "A Workspace Model can package a base model, a short system prompt, chosen parameters and approved knowledge or tools. Treat it as a product surface with a name, intended user and acceptance test.", "Save the reasoning, not just values."),
    ], ["Write five questions before downloading a model.", "Identify the settings layer that owns a behaviour.", "Turn a tested configuration into a reusable preset."], ("Build a narrow assistant", "Create a preset for one job, write a short instruction, leave sampling near the baseline and test it against three examples you can judge.")),

    chapter("05", "administration-security", "Administration & Security", "Users, roles, groups, permissions and safe defaults.", "Governance", "Administration asks a simple but demanding question: what can each person do, and why? Build from restrictive defaults toward explicit, reviewable grants.", "Design access that stays understandable as the instance grows.", "Give access|with intention.", "1vciRJJTXGEH8d52ayMm_aW1MBjNbvBOYbe2Xy6_0ueg", [
        ("Roles establish broad trust", "Admin, User and Pending are high-level classifications. Admin is a maintenance role with wide reach; it should not be the shortcut for granting a useful feature to a normal user.", "Role is not a feature bundle."),
        ("Permissions are additive", "Effective access is the union of global defaults and every group grant. A disabled toggle in one group does not deny a permission granted elsewhere, so design with positive grants rather than imagined exceptions.", "There is no magical deny."),
        ("Groups scale policy", "Groups bundle capabilities and can receive read or write access to specific resources. They let a team manage a role once instead of editing every person, while keeping resource visibility separate from feature access.", "Permission and grant differ."),
        ("Defaults shape experience, not always policy", "A selected model or interface default may be overridden by a user. If a rule must hold, use the relevant access control and validate the effective result with the platform's preview tools.", "A default is not a lock."),
        ("Tools are a trust boundary", "Creating or importing server-side tools can run powerful code and access backend resources. Limit authoring privileges, review code and protect provider credentials, the host and data volume as separate boundaries.", "Capability can equal server trust."),
    ], ["Explain why removing one group toggle may not remove access.", "Separate model visibility from functional permission.", "Name two controls that should stay conservative by default."], ("Design a three-group policy", "Sketch Global Defaults, a Creators group and a small Tool Admins group. For every permission, state why it is granted and where it comes from.")),

    chapter("06", "knowledge-rag", "Knowledge & RAG from Zero", "Documents, chunks, embeddings, retrieval and reranking.", "Knowledge", "Retrieval-augmented generation is an evidence pipeline. Good answers depend first on whether the right passage was extracted, indexed and supplied to the model.", "Build a trustworthy path from documents to grounded answers.", "Give answers|evidence.", "1Qsx5lETnXLg4z_gw3PSrMhSZnRwxknBQ6Nxs7SDV1gI", [
        ("RAG solves a knowledge boundary", "A model cannot reliably know your private or changing documents. RAG retrieves selected passages at question time, then gives the model those passages as context for a grounded response.", "Retrieval precedes generation."),
        ("Extraction comes before retrieval", "A PDF, DOCX or image must become usable text before chunking can work. Inspect extracted text early; an OCR or parser failure cannot be repaired by a better embedding model.", "Check the source text."),
        ("Chunking creates searchable units", "Chunks should preserve enough local meaning to answer a question without being so large that irrelevant material dominates the context. Headings, overlap and document structure are practical levers.", "Boundaries affect recall."),
        ("Embeddings and vector search", "Embeddings place text and questions in a shared numeric space. A vector database stores those representations with text and metadata, then retrieves nearby candidates when a new question arrives.", "Meaning becomes coordinates."),
        ("Retrieval can be refined", "Hybrid search adds exact-term matching; reranking revisits candidates with a stronger relevance model. Use these stages when plain similarity returns plausible but not useful evidence.", "Inspect sources, then tune."),
    ], ["Describe the pipeline from upload to answer.", "Recognise whether a failure is extraction, retrieval or generation.", "Choose one known-answer question for evaluation."], ("Run a document baseline", "Upload one small document, confirm the extracted text, ask a question whose answer you can locate manually and inspect the retrieved sources.")),

    chapter("07", "advanced-rag", "Advanced RAG", "Chunking strategy, hybrid search, reranking and production evaluation.", "Knowledge", "Advanced RAG begins when you inspect evidence systematically. The aim is not an answer that sounds confident; it is a repeatable system that retrieves the right support.", "Tune retrieval as an engineering problem.", "Make retrieval|observable.", "1Uoyg8nb09nUiN6bbhLqsPLlP6l6wFPgH4fTC0T-L1fY", [
        ("Separate retrieval from model failures", "When an answer is wrong, first ask whether the correct passage was retrieved. Only then decide whether the model misunderstood it, ignored it or received a poor instruction.", "Evidence is the first diagnostic."),
        ("Chunk for the document shape", "Policy documents, code, tables and manuals have different semantic boundaries. Use headings and natural sections where possible, then validate chunks against the questions people truly ask.", "One size rarely fits all."),
        ("Combine lexical and semantic search", "Vector search finds related meaning. BM25-style lexical search protects precise terms, identifiers and product names. Hybrid retrieval often improves coverage where either signal alone misses important evidence.", "Meaning plus exactness."),
        ("Rerank within a context budget", "More retrieved text can lower answer quality by crowding the model's window. Retrieve candidates broadly, rerank carefully and pass only the strongest evidence that fits the available context.", "More is not always better."),
        ("Evaluate a corpus deliberately", "Maintain questions with known supporting passages, expected answers and difficulty labels. Track retrieval recall, citation quality, latency and regression after changing chunking, embeddings or a vector database.", "Measure before declaring success."),
    ], ["Debug a poor answer by layer.", "Explain why Top K is not simply a larger-is-better setting.", "Create one evaluation question with a known source passage."], ("Write a retrieval test", "Pick five questions, list the document passage expected for each and record whether the current setup retrieves it before judging the model's prose.")),

    chapter("08", "tools-functions", "Tools & Functions", "Python, APIs, OpenAPI, MCP and real actions.", "Extensibility", "A language model generates tokens. A tool gives it a constrained way to ask for a real action. Functions operate deeper in the application and therefore demand a stricter trust model.", "Move from answers to deliberate, reviewable actions.", "From chat|to action.", "1nMn7r83cP5dS9bl4lFU549049mAJ1RKlPTxtwMtl8tc", [
        ("A tool call is a contract", "The model receives a tool name, description and schema. It requests structured arguments; the system validates and executes the action; the result returns as new context. Clear schemas reduce ambiguous behaviour.", "Describe actions precisely."),
        ("Choose the right integration form", "Use a Workspace Tool for reviewed server-side Python, OpenAPI for a defined HTTP contract and MCP for an external tool server. The choice changes deployment, authentication and who owns the boundary.", "Integration is architecture."),
        ("Native tool calling is preferable", "Models with reliable native tool use can decide when and how to request actions. Legacy strategies can help compatibility, but should be tested carefully because prompt-based imitation is more brittle.", "Test the model, not the promise."),
        ("Valves keep configuration explicit", "A well-made tool exposes configuration through controlled fields rather than hidden constants. Separate user-facing input from administrator secrets, validate values and make failure messages useful.", "Configuration is part of safety."),
        ("Functions deserve elevated caution", "Filters, pipes and actions can alter platform behaviour or execute with broad backend access. Read code, understand dependencies and restrict who can install or edit them.", "Review before trust."),
    ], ["Trace the lifecycle of one tool call.", "Choose between an OpenAPI and MCP integration.", "Explain why a tool schema affects reliability."], ("Define one read-only tool", "Write the name, purpose, input schema, expected result and failure response for a harmless read-only action before connecting any real service.")),

    chapter("09", "mcp-connectors", "MCP & Connectors", "Building a connected Open WebUI.", "Extensibility", "MCP turns external capabilities into a discoverable tool surface. The connection is useful only when its scope, identity and network boundary are as clear as its tool descriptions.", "Connect services without losing control of what can happen.", "Connect systems|with care.", "18ZumUhGnWTnqdqKz7qlNYWlI5vmH59iADo3l6TVkPxg", [
        ("MCP separates client and tool server", "An MCP client discovers the tools, resources or prompts a server provides. The server owns the actual integration with a filesystem, SaaS product, database or internal API.", "Keep ownership visible."),
        ("Transport changes the risk", "Local process, HTTP and remote transports expose different operational surfaces. A remote server requires deliberate authentication, network reachability, logging and lifecycle management.", "A connection is a boundary."),
        ("Authenticate with least privilege", "Give each connector only the scopes it needs and keep tokens outside prompts or user-editable fields. Rotate credentials and ensure a tool cannot silently widen the authority of the connecting account.", "Identity must be scoped."),
        ("Design tools for human review", "Use verbs and descriptions that make side effects visible. Prefer read-only discovery first, then require clear arguments and confirmation patterns before an action can modify an external system.", "Make consequences legible."),
        ("Operate connectors as services", "Health checks, timeouts, audit logs and versioned configurations matter once a connector supports more than one person. Treat a useful integration as a small production service.", "Connected means operated."),
    ], ["Explain the client/server split in MCP.", "Identify where a connector credential should live.", "Describe a safe first integration."], ("Map one connector", "Choose one service and document its tool server, transport, auth scope, read-only action and one side effect you would keep disabled initially.")),

    chapter("10", "agents", "Agents", "Planning, tool use, loops, state and multi-step workflows.", "Agents", "An agent is not a model with a dramatic prompt. It is a loop that interprets a goal, plans, acts through tools, observes the result and stops under defined conditions.", "Build multi-step work that remains inspectable and bounded.", "Make a plan.|Then verify it.", "1mIVeGrgZqS8DJRZezd766_Z_T6zC089YHM0jvsbmh_s", [
        ("The agent loop", "Goal, plan, act, observe and repeat is a useful mental model. Each iteration should add evidence, update the state or move toward a verifiable completion condition.", "A loop needs an exit."),
        ("State is more than chat history", "An agent may need explicit task state, files, tool outputs or durable records. Decide what must persist between steps and what should remain temporary for privacy and clarity.", "Memory has a purpose."),
        ("Tools give an agent consequences", "Tool calling lets an agent inspect a repository, retrieve knowledge or request an external action. Restrict the surface and make tool results structured so the next decision rests on evidence.", "Actions need observations."),
        ("Planning should be visible", "Task lists and checkpoints help people see what the agent believes remains. Plans are hypotheses, so allow revision after new evidence but require a final verification step.", "Plans can change; evidence wins."),
        ("Guardrails define acceptable autonomy", "Set limits on retries, spending, time, destructive operations and escalation. The right autonomy level depends on the action; browsing a document and deleting a record are not equivalent.", "Stop conditions are features."),
    ], ["Draw an agent loop for a small task.", "Separate conversation history from durable state.", "Write a stop condition for an automated action."], ("Prototype a bounded agent", "Choose a read-only research task. Define its goal, two allowed tools, maximum iterations, evidence it must collect and the condition that ends the run.")),

    chapter("11", "coding-agents", "Coding Agents", "Repositories, terminals, tests, Git and safe software workflows.", "Agents", "Coding work is valuable because it changes files and environments. A reliable coding agent follows the same discipline as an experienced engineer: inspect, plan, isolate, edit, test and review.", "Give an agent a workspace without giving up engineering practice.", "Change code.|Keep evidence.", "1ndX0JEwn_CsNVFcj8-gH8TdfqnDG_wQswxoslqEXK-E", [
        ("A coding agent works against real state", "It needs repository files, commands, dependencies and test output rather than a prompt alone. That makes a clean working directory and a known baseline essential before any edit.", "Context lives in the repo."),
        ("Inspect before changing", "Read project instructions, dependency files and the relevant code path. Run the existing tests or build first so later failures can be attributed to the change rather than to a pre-existing issue.", "Establish the baseline."),
        ("Isolate changes with Git", "Branches and worktrees separate experiments from stable work. Review the diff before staging; a short, focused change is easier to verify, revert and explain.", "Isolation reduces blast radius."),
        ("Treat tools as privileged", "Terminal commands, environment variables and repository credentials expose real systems. Limit the workspace, avoid leaking secrets into prompts or logs and require review before external side effects.", "Code execution is trust."),
        ("Verification is part of completion", "Tests, linting, type checks, builds and manual acceptance each answer a different question. A good final report names what changed, why it works and what was actually checked.", "Done includes verification."),
    ], ["State the baseline command for a repository.", "Explain why a worktree can reduce risk.", "List the checks that would validate a small change."], ("Practice a no-op review", "Open a repository, read its instructions, run one existing check and write a one-paragraph plan without editing anything.")),

    chapter("12", "pipelines-automation", "Pipelines & Automation", "Schedules, webhooks, repeatable workflows and orchestration.", "Automation", "Automation is useful when a task can run predictably without a person waiting. It also raises the bar for visibility, idempotency, approvals and operational recovery.", "Turn repeatable work into a system you can trust.", "Repeat work.|Keep control.", "1cLlju2DnaMvlYqwp8w9kY58EkmlIShhqDnwECTCozXE", [
        ("Modern automation is a stack", "Native schedules, functions, tools, webhooks and external services each solve a different part of a workflow. Start with the smallest mechanism that can execute and observe the task.", "Use the minimum moving parts."),
        ("Schedules need a clear contract", "A scheduled prompt needs a title, instructions, model, cadence and destination for its result. Treat the schedule as code-like configuration: readable, reviewed and easy to disable.", "Time is an input."),
        ("Webhooks connect events", "Inbound webhooks receive a trigger; outbound webhooks notify another system. Verify payload signatures, retry behaviour and idempotency so one event does not create many unintended actions.", "Events can repeat."),
        ("Reliability comes from design", "Use timeouts, retries with limits, durable state where needed and observability for every run. A workflow that cannot explain a failure is difficult to operate unattended.", "Make failures visible."),
        ("Unattended actions change safety", "A human can notice ambiguity in a chat; an automation cannot. Keep side effects narrow, require approvals where appropriate and test with harmless destinations before production use.", "Autonomy needs guardrails."),
    ], ["Describe one schedule as a complete contract.", "Explain why webhook retries need idempotency.", "Choose a safe dry run for an automated workflow."], ("Design a daily briefing", "Define its input sources, scheduled time, model, delivery destination, retry policy and one condition that should prevent it from sending.")),

    chapter("13", "apis-applications", "APIs & Building Your Own Applications", "OpenAI-compatible endpoints, Python, JavaScript, Django and streaming.", "APIs", "Open WebUI can also be the platform behind another application. A durable integration keeps provider credentials server-side, understands streaming and makes identity part of the architecture.", "Build your own experience on a controlled AI backend.", "Build on|a real platform.", "13lvQNAk1843c-z6j2evvWsmyDKCq41OwSkJgB5HjEFw", [
        ("The API is a product surface", "List models and send a minimal chat request before building an interface. Confirm the account, model visibility and error response so the first integration rests on a known contract.", "Start with one useful request."),
        ("Identity and keys shape access", "An API key carries the authority of its owner. Do not embed administrative keys in browser code; use a backend proxy or user-specific flow that can enforce scope, auditing and revocation.", "The browser is not a secret store."),
        ("Streaming improves perceived speed", "Server-sent events deliver tokens as they arrive. The client needs to render partial output, handle disconnects and distinguish a completed stream from a failed request.", "First token matters."),
        ("Django makes a safe boundary", "A Django view can authenticate the user, validate input, call Open WebUI with protected credentials and stream an appropriate response. This keeps policy and secrets on the server side.", "Your backend owns trust."),
        ("Design for failures", "Handle timeouts, unavailable models, upstream rate limits and malformed tool results. A clear error message and retry policy are part of a credible application experience.", "Failure modes are requirements."),
    ], ["Make a minimal model-list request.", "Explain why API keys do not belong in client JavaScript.", "Describe the lifecycle of a streamed chat response."], ("Sketch a Django proxy", "Write the route, user authentication check, input validation, upstream call, timeout and error response for a single chat endpoint.")),

    chapter("14", "security-hardening", "Security Hardening", "Reverse proxy, HTTPS, secrets, network isolation and production boundaries.", "Security", "Hardening turns individual settings into a defensible deployment. Start with what needs protection, then make every route, secret and service boundary deliberate.", "Place the platform behind clear, tested protections.", "Protect the|whole path.", "1X9RNIebnnbZHlfZzUY1MFszqXNS_ZCYNJs7nqEkq2Z0", [
        ("Start with a threat model", "A private homelab and a public service face different risks. Identify identities, chats, documents, provider keys, compute, tools and backups before choosing controls.", "Protection follows assets."),
        ("HTTPS and reverse proxy placement", "A proxy terminates encrypted browser traffic and forwards it to the application on an internal route. Configure the public URL, cookies, WebSocket support and allowed origins as one coherent boundary.", "Browser to backend is a path."),
        ("Secrets must stay stable and private", "Protect the application secret key, provider credentials and OAuth tokens. Put them in controlled environment configuration, rotate when needed and never treat logs, prompts or screenshots as safe secret storage.", "Secrets outlive deployments."),
        ("Networks limit reachability", "Separate public exposure from internal services such as databases, Ollama and tool servers. Restrict outbound paths where possible and avoid mounts or ports that a component does not need.", "Reachability is permission."),
        ("Recovery proves the design", "A backup is useful only when it can be restored safely. Test a recovery path, include secrets-aware procedures and make updates, patches and monitoring part of the operational routine.", "Restore is the real test."),
    ], ["Name the assets in your threat model.", "Draw the HTTPS path to Open WebUI.", "Identify one network boundary around a sensitive service."], ("Create a hardening checklist", "List public ports, trusted origins, secret locations, backup location, update cadence and the one recovery test you will run.")),

    chapter("15", "observability-troubleshooting", "Observability & Troubleshooting", "Logs, health, GPU, model and RAG failures.", "Operations", "Troubleshooting is a method: reproduce, isolate, observe, change one thing and verify. A layered system becomes manageable when you can locate the first boundary that fails.", "Diagnose the stack without collecting random fixes.", "Observe first.|Then change.", "1fmgBxKwCoAiMYQR6JJ87WxIAeldRbSARABMi0UoPZJo", [
        ("Use a diagnostic ladder", "Move from browser to proxy, application, network, model runtime, GPU, RAG and tools. This sequence avoids changing a model setting when the real failure is a blocked request or unhealthy container.", "Find the first broken layer."),
        ("Health means usable, not merely running", "A process can be alive while a provider connection, model load or document pipeline is failing. Pair simple health checks with one meaningful end-to-end request.", "Probe the real path."),
        ("Logs are evidence", "Browser console output, container logs, provider logs and structured events each reveal a different part of the request. Correlate timestamps and request identifiers instead of relying on memory.", "Collect before changing."),
        ("Performance failures have a shape", "Slow first token, slow generation, out-of-memory errors and queueing point to different causes. Measure latency, tokens per second, context, VRAM use and concurrent load before tuning.", "Measure the symptom."),
        ("RAG and tool failures are layered", "Inspect extracted text, chunks, retrieval sources, credentials, network reachability and tool schemas. A polished response does not prove the system used the correct evidence or action.", "Trace inputs to outputs."),
    ], ["Use the diagnostic ladder on one failure.", "Distinguish a liveness check from a useful health check.", "Record the evidence needed to explain a slow response."], ("Build an incident note", "For a reproducible failure, write the time, request, expected result, observed result, failing layer, logs consulted and one single change to test.")),

    chapter("16", "performance-optimization", "Performance & Optimization", "VRAM, concurrency, context, loading and faster local inference.", "Operations", "Performance is a system property. The model, context, hardware, provider runtime, RAG pipeline and concurrent workload all contribute to the time a person experiences.", "Improve speed by measuring the right constraint first.", "Fit the model.|Respect the budget.", "1Iq0beiLBPOgxFPGTg-AVcLwd_2peD8GpVhw8oKRfL4E", [
        ("Measure what people feel", "Time to first token, generation speed, total latency, queue time and error rate reveal different bottlenecks. A fast token rate cannot compensate for a long cold start or overloaded queue.", "Metrics guide tuning."),
        ("VRAM is a shared budget", "Weights, KV cache, runtime overhead and other GPU processes compete for memory. Leave headroom; a setup that fits only on paper can become unstable under longer context or concurrent use.", "Budget before scaling."),
        ("Context changes throughput", "Longer prompts and larger context windows increase processing work and KV-cache use. Trim history, retrieve selectively and choose context targets that match the real task rather than a maximum label.", "Every token has a cost."),
        ("Loading and concurrency need policy", "Keep-alive reduces cold starts but ties up memory. Multiple loaded models and simultaneous users require queues or additional capacity. Pick an operating profile rather than letting defaults compete blindly.", "Warmth costs memory."),
        ("Benchmark with representative work", "Use the same prompts, model version, context and concurrency when comparing changes. Track regressions alongside gains so a faster response does not quietly lower answer quality.", "Repeatable beats anecdotal."),
    ], ["Name the metric that reveals a cold-start issue.", "Explain why a model can fit and still be too slow.", "Design a fair before/after benchmark."], ("Run a small benchmark", "Use one short prompt and one long-context prompt. Record first-token time, tokens per second, total time and any VRAM observation for each.")),

    chapter("17", "building-platform", "Building Our Open WebUI Platform", "Models, RAG, agents, tools, services and final architecture.", "Architecture", "The final platform is not one giant assistant. It is a set of specialised components with clear jobs, data ownership and boundaries that can grow without becoming mysterious.", "Assemble the system from deliberate, observable parts.", "Build the|whole platform.", "1AVdhW_HjEn7miOsMDAtniJY4MIf2kVYOLIt5RUw4A1Y", [
        ("Assign a job to every component", "Keep the interface, model portfolio, retrieval layer, tools, automation and API services separate enough that each can be inspected, changed and scaled independently.", "Separation enables reasoning."),
        ("Build a model portfolio", "A general assistant, coding model, fast task model and embedding model may each be the right size for their job. Workspace Models make that portfolio understandable to people using the platform.", "Specialise with intent."),
        ("Treat knowledge as a source-of-truth system", "Document ownership, update paths, indexing choices and citation expectations determine whether RAG remains credible. A vector index is not the source of truth; it is a retrieval aid.", "Evidence needs ownership."),
        ("Connect actions behind boundaries", "Tools, connectors and agent workspaces should expose only the authority they need. Give each integration an owner, a test path, monitoring and a simple way to disable it.", "Capability needs a steward."),
        ("Implement in a stable sequence", "Start with reliable chat and model access, add a small knowledge corpus, then a read-only tool, a bounded agent and only later automation or custom applications. Validate each layer before stacking another.", "Grow from known baselines."),
    ], ["Draw the components of your target platform.", "Assign a model family to each distinct job.", "Choose the next layer to implement and its success test."], ("Create your platform card", "For every planned component, record its owner, inputs, outputs, secrets, monitoring signal and the condition that would make you disable it.")),

    chapter("18", "cookbook", "Cookbook", "Practical recipes for models, RAG, agents, tools, automation and apps.", "Practice", "Use recipes as verified starting points, not as magic incantations. Build the smallest useful version, run a focused test and only then add more context, capabilities or automation.", "Turn the guide into practical, repeatable outcomes.", "Build small.|Verify early.", "1zc0gXC4-bZ121hEFC1WNWwXnj8RVpYfW8MVjUM6Ytf0", [
        ("Every recipe uses the same loop", "Define the goal, gather only the necessary ingredients, build a minimal working version, test it, verify the evidence and improve one dimension at a time.", "Goal → build → verify."),
        ("Start with a Daily Assistant", "Choose a known-good model, add a short instruction and leave advanced capabilities disconnected. This gives you a clean benchmark for later changes to knowledge, tools or memory.", "Establish a useful baseline."),
        ("Add RAG as a document analyst", "Create one knowledge collection, upload a small sample, inspect extraction and test questions with known supporting passages. Expand the corpus only after this path is reliable.", "Evidence before scale."),
        ("Connect a real service carefully", "Whether through OpenAPI or MCP, begin with a read-only action and a narrow credential. Test the complete request, authentication and error path before introducing a side effect.", "Read before write."),
        ("Ship a small application or automation", "A Django integration needs a server-side credential boundary and streaming-aware UI. A scheduled briefing needs a destination, retry policy and a safe failure mode. Both become reliable through explicit contracts.", "Production is a set of checks."),
    ], ["Choose a recipe that matches one real outcome.", "Run its verification step before customising it.", "Record the smallest next improvement."], ("Choose one recipe", "Pick Daily Assistant, Document Analyst, read-only connector, scheduled briefing or Django app. Write its goal, baseline test and one optional enhancement you will postpone.")),
)

SECTION_OVERRIDES = {
    "00": [
        ("architecture", "What Open WebUI is — and is not"), ("layers", "The platform layers"),
        ("request", "Follow a request"), ("building-blocks", "Core building blocks"),
        ("providers", "Ollama and model providers"), ("agents", "From chatbot to agent"),
        ("security", "Security boundaries"), ("learning-path", "The Zero to Hero path"),
        ("checkpoint", "Checkpoint"), ("glossary", "Essential vocabulary"),
    ],
    "01": [
        ("surfaces", "The four surfaces"), ("chat", "The Chat surface"),
        ("model-picker", "The model picker"), ("sidebar", "History and organisation"),
        ("workspace", "Reusable components"), ("settings", "Personal settings"),
        ("admin", "Instance administration"), ("interaction", "@, /, files and integrations"),
        ("walkthrough", "First-session walkthrough"), ("find-feature", "Find any feature"),
        ("checkpoint", "Checkpoint"), ("glossary", "Essential vocabulary"),
    ],
    "02": [
        ("docker", "Why Docker"), ("persistence", "Persistent data"),
        ("canonical", "Canonical Docker setup"), ("compose", "Maintainable Compose"),
        ("ollama", "Connect to Ollama"), ("networking", "Ports and networking"),
        ("images-gpu", "Images and GPU"), ("first-boot", "First boot"),
        ("logs", "Logs and troubleshooting"), ("backups", "Backups"),
        ("updates", "Safe updates"), ("https", "HTTPS and proxies"),
        ("standard", "Deployment standard"), ("checkpoint", "Checkpoint"),
        ("glossary", "Essential vocabulary"),
    ],
    "03": [
        ("inference", "What an LLM does"), ("tokens", "Tokens"),
        ("parameters", "Parameters"), ("training", "Training vs inference"),
        ("model-name", "Read a model name"), ("quantization", "Quantization"),
        ("formats", "GGUF, Safetensors and Modelfiles"), ("memory", "VRAM, RAM and disk"),
        ("context", "Context and KV cache"), ("offload", "GPU offload"),
        ("families", "Model families"), ("moe", "Dense vs MoE"),
        ("sampling", "Sampling"), ("twelve-gb", "A 12 GB GPU"),
        ("workflow", "Selection workflow"), ("checkpoint", "Checkpoint"),
        ("glossary", "Essential vocabulary"),
    ],
    "04": [
        ("task", "Choose for the task"), ("questions", "Five questions first"),
        ("scope", "Where settings live"), ("context", "Context length"),
        ("sampling", "Sampling controls"), ("prompts", "Useful system prompts"),
        ("presets", "Workspace Models"), ("task-models", "Task Models"),
        ("profiles", "12 GB profiles"), ("evaluation", "Fair comparison"),
        ("diagnosis", "Diagnose poor results"), ("workflow", "A scalable workflow"),
        ("checkpoint", "Checkpoint"), ("glossary", "Essential vocabulary"),
    ],
    "05": [
        ("administration", "What administration means"), ("roles", "System roles"),
        ("permissions", "Additive permissions"), ("groups", "Groups and grants"),
        ("resources", "Resource access"), ("visibility", "Defaults and visibility"),
        ("boundaries", "Security boundaries"), ("dangerous-permissions", "Tools and Functions"),
        ("hardening", "Safe defaults"), ("team-designs", "Team designs"),
        ("troubleshooting", "Access troubleshooting"), ("checklist", "Admin checklist"),
        ("checkpoint", "Checkpoint"), ("glossary", "Essential vocabulary"),
    ],
    "06": [
        ("rag-problem", "What problem RAG solves"), ("pipeline", "Upload-to-answer pipeline"),
        ("extraction", "Document extraction"), ("chunking", "Chunking"),
        ("embeddings", "Embeddings"), ("vector-db", "Vector databases"),
        ("retrieval", "Retrieval and context"), ("hybrid", "Hybrid Search and reranking"),
        ("retrieval-modes", "Focused vs Full Context"), ("knowledge", "Knowledge and chat files"),
        ("agentic", "Agentic retrieval"), ("configuration", "Starting configurations"),
        ("reindex", "Reindexing safely"), ("troubleshooting", "Troubleshooting"),
        ("lab", "Practical lab"), ("checkpoint", "Checkpoint"),
        ("glossary", "Essential vocabulary"),
    ],
    "07": [
        ("mindset", "The advanced-RAG mindset"), ("chunking", "Chunking strategy"),
        ("hybrid", "Hybrid Search"), ("reranking", "Reranking and Top K"),
        ("context", "Context budget"), ("embeddings", "Embeddings and reindexing"),
        ("agentic", "Agentic retrieval"), ("evaluation", "Evaluate RAG"),
        ("production", "Production architecture"), ("external", "External Knowledge"),
        ("playbook", "Tuning playbook"), ("troubleshooting", "Troubleshooting by layer"),
        ("checkpoint", "Checkpoint"), ("glossary", "Essential vocabulary"),
    ],
    "08": [
        ("action", "From answering to acting"), ("map", "The tooling map"),
        ("call-flow", "The tool-call loop"), ("native", "Native vs Legacy"),
        ("workspace-tools", "Workspace Tools"), ("anatomy", "Anatomy of a Tool"),
        ("configuration", "Valves and injected context"), ("openapi", "OpenAPI"),
        ("mcp", "MCP"), ("choosing", "Choose the integration"),
        ("functions", "Functions"), ("terminal", "Open Terminal"),
        ("security", "Security boundaries"), ("troubleshooting", "Tool troubleshooting"),
        ("project", "Support Assistant project"), ("glossary", "Essential vocabulary"),
    ],
    "09": [
        ("connector", "What a connector is"), ("mcp-model", "MCP mental model"),
        ("native", "Native MCP"), ("choices", "MCP, OpenAPI or Tools"),
        ("network", "Network origin"), ("authentication", "Authentication"),
        ("oauth", "Per-user OAuth"), ("identity", "Identity propagation"),
        ("mcpo", "MCPO bridge"), ("openapi-example", "Build an OpenAPI connector"),
        ("patterns", "Integration patterns"), ("security", "Least privilege"),
        ("troubleshooting", "Connection troubleshooting"), ("design", "Design a connected system"),
        ("checkpoint", "Checkpoint"), ("glossary", "Essential vocabulary"),
    ],
    "10": [
        ("agent", "What an agent is"), ("spectrum", "The agentic spectrum"),
        ("loop", "The agent loop"), ("planning", "Planning"),
        ("state", "State"), ("memory", "Memory and external state"),
        ("native", "Native tool calling"), ("tasks", "Task Management"),
        ("composition", "Skills, Knowledge and Tools"), ("delegation", "Sub-agents"),
        ("terminal", "Open Terminal"), ("automations", "Automations"),
        ("guardrails", "Guardrails and stopping"), ("building", "Build an agent"),
        ("external", "External agents"), ("evaluation", "Agent evaluation"),
        ("troubleshooting", "Troubleshooting"), ("stack", "The local agent stack"),
        ("checkpoint", "Checkpoint"), ("glossary", "Essential vocabulary"),
    ],
    "11": [
        ("difference", "What makes a coding agent"), ("surfaces", "Choose a coding surface"),
        ("workflow", "The safe workflow"), ("inspect", "Inspect the repository"),
        ("baseline", "Rules and baseline"), ("planning", "Planning"),
        ("isolation", "Branches and worktrees"), ("editing", "Safe editing"),
        ("environment", "Execution environment"), ("validation", "Tests and checks"),
        ("git", "Git review and commits"), ("approvals", "Approval modes"),
        ("computer", "Computer workspace"), ("backends", "Coding-agent backends"),
        ("gateway", "Computer in Open WebUI"), ("parallel", "Parallel agents"),
        ("security", "Security boundaries"), ("example", "Django bug example"),
        ("troubleshooting", "Troubleshooting"), ("checklist", "Completion checklist"),
        ("glossary", "Essential vocabulary"),
    ],
    "12": [
        ("meaning", "What automation means"), ("stack", "Modern automation stack"),
        ("native", "Native Automations"), ("schedule", "RRULE scheduling"),
        ("run", "Anatomy of a run"), ("functions", "Functions for orchestration"),
        ("events", "Events and Actions"), ("webhooks", "Webhooks and notifications"),
        ("computer", "Computer scheduled work"), ("safety", "Unattended safety"),
        ("reliability", "Reliability controls"), ("patterns", "Practical patterns"),
        ("troubleshooting", "Troubleshooting"), ("checkpoint", "Checkpoint"),
        ("glossary", "Essential vocabulary"),
    ],
    "13": [
        ("platform", "Open WebUI as a platform"), ("identity", "API identity"),
        ("minimum", "Minimum useful API"), ("python", "Python client"),
        ("browser", "Browser trust boundary"), ("django", "Django proxy"),
        ("streaming", "SSE streaming"), ("knowledge", "Files and Knowledge"),
        ("tools", "Tools and MCP"), ("state", "Conversation state"),
        ("failures", "Errors and retries"), ("security", "Defence in depth"),
        ("architecture", "Application architecture"), ("checkpoint", "Checkpoint"),
        ("glossary", "Essential vocabulary"),
    ],
    "14": [
        ("assets", "Assets and threat model"), ("path", "Secure deployment path"),
        ("proxy", "Proxy and HTTPS"), ("secrets", "Secrets"),
        ("networks", "Network isolation"), ("identity", "Authentication and RBAC"),
        ("capabilities", "Capability boundaries"), ("data", "Storage encryption"),
        ("egress", "Egress and SSRF"), ("recovery", "Backup and recovery"),
        ("operations", "Patching and monitoring"), ("design", "Hardened homelab"),
        ("checklist", "Production checklist"), ("troubleshooting", "Troubleshooting"),
        ("checkpoint", "Checkpoint"), ("glossary", "Essential vocabulary"),
    ],
    "15": [
        ("method", "Troubleshooting method"), ("ladder", "Diagnostic ladder"),
        ("health", "Health checks"), ("logs", "Logs"),
        ("runtime", "Container diagnosis"), ("ollama", "Ollama connectivity"),
        ("gpu", "GPU and VRAM"), ("context", "Context failures"),
        ("rag", "RAG diagnosis"), ("tools", "Tools and MCP"),
        ("web", "Browser and proxy"), ("storage", "Storage failures"),
        ("performance", "Performance symptoms"), ("monitoring", "Monitoring"),
        ("checklist", "Incident checklist"), ("examples", "Worked diagnoses"),
        ("checkpoint", "Checkpoint"), ("glossary", "Essential vocabulary"),
    ],
    "16": [
        ("system", "Performance as a system"), ("metrics", "Performance metrics"),
        ("vram", "VRAM budget"), ("context", "Context and KV cache"),
        ("offload", "CPU offload"), ("loading", "Cold starts and keep-alive"),
        ("concurrency", "Concurrency and queues"), ("models", "Multiple models"),
        ("overrides", "Configuration overrides"), ("rag", "RAG performance"),
        ("cache", "Caching"), ("scale-out", "Multiple Ollama servers"),
        ("application", "Application scaling"), ("profile", "12 GB profile"),
        ("benchmark", "Benchmarking"), ("antipatterns", "Anti-patterns"),
        ("checkpoint", "Checkpoint"), ("glossary", "Essential vocabulary"),
    ],
    "17": [
        ("mindset", "Platform mindset"), ("homelab", "12 GB starting point"),
        ("layers", "Target architecture"), ("portfolio", "Model portfolio"),
        ("presets", "Workspace Models"), ("knowledge", "Knowledge design"),
        ("memory", "Memory, Prompts and Skills"), ("connectors", "Tools and connectors"),
        ("agents", "Agents and coding"), ("automation", "Automation"),
        ("api", "Platform API"), ("trust", "Trust tiers"),
        ("operations", "Operations"), ("scaling", "Scaling"),
        ("sequence", "Implementation sequence"), ("assistants", "Example assistants"),
        ("checklist", "Architecture checklist"), ("checkpoint", "Checkpoint"),
        ("glossary", "Essential vocabulary"),
    ],
    "18": [
        ("method", "How the cookbook works"), ("daily", "Daily Assistant"),
        ("rag", "Document Analyst"), ("ba", "Business Analyst"),
        ("coding", "Coding Agent"), ("openapi", "OpenAPI service"),
        ("mcp", "MCP connector"), ("briefing", "Automated briefing"),
        ("django", "Django application"), ("memory", "Memory"),
        ("recovery", "Backup and recovery"), ("cheatsheet", "Component map"),
        ("layers", "Grow in layers"),
    ],
}

COVER_OVERRIDES = {
    "05": "imgs/05-image-6.webp", "06": "imgs/06-image-6.webp",
    "07": "imgs/07-image-6.webp", "08": "imgs/08-image-7.webp",
    "09": "imgs/09-image-2.webp", "10": "imgs/10-image-7.webp",
    "11": "imgs/11-image-9.webp", "12": "imgs/12-image-4.webp",
    "13": "imgs/13-image-8.webp", "14": "imgs/14-image-5.webp",
    "15": "imgs/15-image-9.webp", "16": "imgs/16-image-9.webp",
    "17": "imgs/17-image-10.webp", "18": "imgs/18-image-10.webp",
}

for item in CHAPTERS:
    if item["number"] in SECTION_OVERRIDES:
        item["sections"] = [
            {"id": section_id, "title": title}
            for section_id, title in SECTION_OVERRIDES[item["number"]]
        ]
    if item["number"] in COVER_OVERRIDES:
        item["cover"] = COVER_OVERRIDES[item["number"]]

BY_SLUG = {chapter["slug"]: chapter for chapter in CHAPTERS}
