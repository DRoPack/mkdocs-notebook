---
title: Section 4 - Building a Chatbot
---

<!-- markdownlint-disable MD046 -->
<!-- markdownlint-disable MD007 -->

!!! note "Fork in the Road"

    At this stage of the course, Mosh begins building the application using an OpenAI-hosted model.

    OpenAI does not provide a free developer tier for API usage. To follow along exactly as demonstrated,
    you will need an OpenAI account with billing enabled and available credit to consume the models.

    If you prefer not to incur API costs while completing the course, consider skipping ahead to
    [Section 7 – Building with Open Source Models](section7.md).

    In that section, you can adapt the code to use Hugging Face inference endpoints (or other
    open-source models) as an alternative to OpenAI.

## Video 2.1 - Building the Chat API

- Navigate to server folder and run add Hugging Face Inference

```cmd title="Terminal"
cd packages\server

// Install Hugging Face
bun add @huggingface/inference

```

- Set up Hugging Face client

```ts title="packages\server\index.ts"
import { InferenceClient } from '@huggingface/inference';

// Model token
const inferenceClient = new InferenceClient(process.env.HF_Token);
```

- Create chat endpoint

```ts title="packages\server\index.ts"
// Middleware
app.use(express.json()); // parses the req.body

app.post('/api/chat', async (req: Request, res: Response) => {
 const { prompt } = req.body;

 const response = await inferenceClient.chatCompletion({
  model: 'meta-llama/Llama-3.1-8B-Instruct:novita',
  messages: [
   {
    role: 'user',
    content: prompt,
   },
  ],
 });
 res.json({
  messages: response.choices[0]?.message || "ohh... It didn't work.",
 });
});
```

## Video 2.2 - Testing the API

- Install Postman Extension in :material-microsoft-visual-studio-code: VSCode

!!! tip "Open Postman in VS Code"

    1. Press `Ctrl + Shift + P`
    2. Type **Show Postman**
    3. Select **View: Show Postman**

- Create New HTTP Request

```httpCall

    method=POST

    path
    http://localhost:3000/api/chat

    body
    {
      "prompt": "What is the capital of France?"
    }
```

## Video 2.3 - Managing Conversation State

Phase 1 - Declare variable to hold last response

```ts title="packages/server/index.ts" hl_lines="1 4 6  8-11 15  18 20-22 24 26 29"
const conversations = new Map<string, any[]>();

app.post('/api/chat', async (req: Request, res: Response) => {
 const { prompt, id } = req.body;

 const history = conversations.get(id) || [];

 history.push({
  role: 'user',
  content: prompt,
 });

 const response = await inferenceClient.chatCompletion({
  model: 'meta-llama/Llama-3.1-8B-Instruct:novita',
  messages: history,
 });

 const assistantMessage = response.choices?.[0]?.message;

 if (!assistantMessage) {
  return res.status(500).json({ error: 'Invalid model response' });
 }

 history.push(assistantMessage);

 conversations.set(id, history);

 res.json({
  assistantMessage,
 });
});
```
