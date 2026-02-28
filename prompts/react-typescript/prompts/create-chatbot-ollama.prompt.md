---
mode: 'agent'
description: 'Implement a new feature called Chat Ollama'
version: '1.0.0'
---

> **Learn why this works:** [Decomposition + Role-Playing](../../../learn/02-core-principles.md#22-principle-2-decomposition)

# Role

Act as a **Coding LLM** with the role of an **expert full-stack engineer** for building a **feature-based**, production-grade SaaS web application having React, TypeScript, and a Node.js as tech stack. Implement a new feature named **Chat Ollama** that integrates interaction with a locally running LLM served by **Ollama** into the existing app.

# Task

You are responsible for extending the existing SaaS application (frontend: React + TypeScript, backend: Node.js) without breaking current functionality. You must follow the established project architecture, module structure, and naming conventions.

## **Task**

1. Add a new sidebar navigation entry labeled **"Chat Ollama"**.

2. Route this entry to a new page at path **`/chat-ollama`**, using the same routing system already used in the app.

3. Implement a chat UI inspired by **ChatGPT**, including:

   * UI elements must use **shadcn/ui** components.
   * A scrollable message list showing both user and assistant messages.
   * A user input text area or input box.
   * A send action (button and “Enter to send” behavior if consistent with existing UX).
   * Visible loading state while waiting for LLM responses.
   * Error display for failed or timed-out requests.
     
4. Connect the chat UI to a backend API endpoint that:
  
   * Accepts user messages as input.
   * Forwards them to a locally running LLM served by **Ollama** (via `http://localhost:11434` or a configurable `OLLAMA_API_URL`).
   * Streams the LLM response back to the frontend in incremental chunks (e.g., using server-sent events or a streaming HTTP response consistent with the existing stack).
     
5. On the frontend, consume the streamed response and progressively append tokens/chunks to the assistant message in the message list.

6. Organize the code using a modular structure with clear separation of concerns:

   * Reusable presentational components (e.g., MessageList, MessageItem, ChatInput, LoadingIndicator, ErrorBanner).
   * Container/logic components or hooks for networking and state (e.g., `useChatOllama`).
   * A dedicated backend route/controller module for Chat Ollama integration.

## **Constraints**

* Do not introduce breaking changes to the existing SaaS scaffolding, routing, or build configuration.

* Follow existing project patterns for:

  * Folder structure (e.g., `pages`, `components`, `hooks`, `routes`, `controllers`, `services`).
  * Naming conventions and TypeScript typing conventions.
  * Error handling and logging.

* Ensure safe handling of input and output:

  * Sanitize and validate user input.
  * Enforce reasonable limits on message length and request frequency (if applicable).
  * Handle and surface network, timeout, and server errors gracefully.

* Keep the integration configurable:

  * Use environment variables or config constants for Ollama endpoint URLs and model names where appropriate.

* Use idiomatic, production-ready React and Node.js patterns (no experimental or deprecated APIs).

# Output Format

* Provide complete, ready-to-apply code with modern UI for:

  * New frontend page and components for **Chat Ollama**.
  * Any new hooks or utilities used for chat state management and streaming.
  * Backend route(s), controller(s), and service(s) that call the local Ollama instance and stream responses.
  * Any necessary configuration or environment variable additions.
     
* Output all files in a clean, structured format based on best practices defined in the copilot-instructions.md file.
