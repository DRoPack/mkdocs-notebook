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
      "prompt": "What is the capital of France?",
      "id": "ab5a9ef4-c1b1-43ee-816a-53e66190945f"
    }

    response
    {
    "assistantMessage": {
        "id": "71b6bbf2d1a045998b2b09f87b5707d1",
        "object": "chat.completion",
        "created": 1771862809,
        "model": "meta-llama/llama-3.1-8b-instruct",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "Paris is the capital of France."
                },
                "finish_reason": "stop",
                "content_filter_results": {
                    "hate": {
                        "filtered": false
                    },
                    "self_harm": {
                        "filtered": false
                    },
                    "sexual": {
                        "filtered": false
                    },
                    "violence": {
                        "filtered": false
                    },
                    "jailbreak": {
                        "filtered": false,
                        "detected": false
                    },
                    "profanity": {
                        "filtered": false,
                        "detected": false
                    }
                }
            }
        ],
        "usage": {
            "prompt_tokens": 41,
            "completion_tokens": 34,
            "total_tokens": 75,
            "prompt_tokens_details": null,
            "completion_tokens_details": null
        },
        "system_fingerprint": ""
        }
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

## Video 2.4 - Input Validation

<!-- prettier-ignore-start -->
!!! Zod
  
    A TypeScript-first validation library used in React and Node.js
    for ensuring incoming data matches expected types.
<!-- prettier-ignore-end -->

- Navigate to server folder and run add Zod

```cmd title="Terminal"
  cd packages/server

  // Install Zod
  bun add zod
```

- Set up Zod in server/index.ts

```ts title="packages/server/index.ts" hl_lines="1 4-11 14-18"
  import z from 'zod';

  ....
  const chatSchema = z.object({
  prompt: z
    .string()
    .trim()
    .min(1, 'Prompt is required')
    .max(1000, 'Prompt is too long (max 1000 characters)'),
  conversationId: z.uuid(),  // expects a valid UUID
});

app.post('/api/chat', async (req: Request, res: Response) => {
  const parseResult = chatSchema.safeParse(req.body);
  if (!parseResult.success) {
    res.status(400).json(z.treeifyError(parseResult.error)); // treeifyError formats the error
    return;
  }
  ...
});
```

## Video 2.5 - Error Handling

- Add a try/catch block for proper error Handling

```ts title="packages/server/index.ts" hl_lines="6-7 13 21-28"
app.post('/api/chat', async (req: Request, res: Response) => {
 const parseResult = chatSchema.safeParse(req.body);

 // ... existing validation logic

 try {
  const { prompt, conversationId } = parseResult.data;
  const history = conversations.get(id) || [];

  // ... existing logic

  if (!assistantMessage) {
   return res.status(500).json({ error: 'Invalid model response' });
  }

  // ... existing logic

  res.json({
   assistantMessage,
  });
 } catch (error) {
  res.status(500).json({
   error:
    error instanceof Error ? error.message : 'Failed to generate a response.',
  });
 }
});
```

## Video 3 - Refactor the Chat API

!!! note

    Restructure the project into organized folders called **layers**. This improves readability, separation of concerns, and long-term scalability

    - Controllers - Handle HTTP requests and return HTTP responses
    - Services - Contain application/business logic
    - Repository - Store and retrieve data from a database or in-memory store

## Video 3.1 - Extracting Conversation Repository

- Create folder `repositories` within `server` folder

```bash title="packages/server"
    # Use command line or manually create folder in VSCode
    mkdir repositories
```

- Create file `conversation.repository.ts` within `repositories` folder

```bash title="packages/server"
    # Use command line or manually create foler in VSCode

    # Using the command line
    type nul > repositories/conversation.repository.ts   # CMD
    # or
    touch repositories/conversation.repository.ts       # Git Bash
    # or
    New-Item repositories/conversation.repository.ts    # PowerShell
```

```ts title="packages/server/repositories/conversation.repository.ts"
export interface IChatMessage {
 role: 'user' | 'assistant' | 'system' | 'tool' | 'function';
 content: string;
 [key: string]: unknown; // allows extra fields (Llama)
}

// Implementation detail
const conversations = new Map<string, IChatMessage[]>();

// Export object with two methods
export const conversationRepository = {
 getConversation(conversationId: string) {
  return conversations.get(conversationId) || [];
 },
 setConversation(conversationId: string, messages: IChatMessage[]): void {
  conversations.set(conversationId, messages);
 },
};
```

```ts title="packages/server/index.ts" hl_lines="1-3 12-13 17"
import { conversationRepository } from './repositories/conversation.repository';

app.post('/api/chat', async (req: Request, res: Response) => {
 // existing validation logic

 try {
  const { prompt, conversationId } = parseResult.data;

  // Get conversation from repository
  const history = conversationRepository.getConversation(id);

  // existing logic: push user prompt, HTTP Model call, validate, push response message

  conversationRepository.setConversation(id, history);

  res.json({
   assistantMessage,
  });
 } catch (error) {
  res.status(500).json({
   error:
    error instanceof Error ? error.message : 'Failed to generate a response.',
  });
 }
});
```

!!! tip "Exporting an object with Methods"

    Instead of exporting multiple standalone functions, you can export a single object that contains all related methods. This pattern makes it clear which file each method comes from keeping internal state shared and encapsulated.

## Video 3.2 - Extracting Chat Service

- Create folder `service` within `server` folder

- Create file `conversation.repository.ts` within `service` folder

```ts title="packages/server/services/chat.service.ts"
// server/services/chat.service.ts
import { InferenceClient } from '@huggingface/inference';
import { conversationRepository } from '../repositories/conversation.repository';

// Implemenation detail
const inferenceClient = new InferenceClient(process.env.HF_Token);

type ChatResponse = {
 id: string;
 message: string;
};

// Public interface
export const chatService = {
 async sendMessage(
  prompt: string,
  conversationId: string
 ): Promise<ChatResponse> {
  // Get conversation from repository
  const history = conversationRepository.getConversation(conversationId);

  // Add user message
  history.push({
   role: 'user',
   content: prompt,
  });

  const response = await inferenceClient.chatCompletion({
   model: 'meta-llama/Llama-3.1-8B-Instruct:novita',
   messages: history,
  });

  const assistantMessage = response.choices?.[0]?.message;

  if (!assistantMessage?.content) {
   throw new Error('Chat Service: Invalid model response');
  }

  // Add assistant messge
  history.push({
   role: 'assistant',
   content: assistantMessage?.content || '',
  });

  conversationRepository.setConversation(conversationId, history);

  return {
   id: response.id,
   message: assistantMessage?.content || '',
  };
 },
};
```

```ts title="packages/server/index.ts"
// server/index.ts
import express from 'express';
import type { Request, Response } from 'express';
import dotenv from 'dotenv';
import { z } from 'Zod';
import { chatService } from './services/chat.service';

dotenv.config();

const app = express();

// Middleware
app.use(express.json()); // parses the req.body

const port = process.env.PORT || 3000;

app.get('/', (req: Request, res: Response) => {
 res.send('Hello World!');
});

app.get('/api/hello', (req: Request, res: Response) => {
 res.json({ message: 'Hello World!' });
});

// Zod validation
const chatSchema = z.object({
 prompt: z
  .string()
  .trim()
  .min(1, 'Prompt is required')
  .max(1000, 'Prompt is too long (max 1000 characters)'),
 conversationId: z.uuid(), // expects a valid UUID
});

app.post('/api/chat', async (req: Request, res: Response) => {
 const parseResult = chatSchema.safeParse(req.body);
 if (!parseResult.success) {
  res.status(400).json(z.treeifyError(parseResult.error)); // treeifyError formats the error
  return;
 }

 try {
  const { prompt, conversationId } = parseResult.data;
  const response = await chatService.sendMessage(prompt, conversationId);

  res.json({
   message: response.message,
  });
 } catch (error) {
  res.status(500).json({
   error:
    error instanceof Error ? error.message : 'Failed to generate a response.',
  });
 }
});

app.listen(port, () => {
 console.log(`Server is running on http://localhost:${port}`);
});
```

## Video 3.3 - Extacting Chat Controllers

- Create folder `controllers` within `server` folder

- Create file `chat.controller.ts` within `controllers` folder

```ts title="packages/server/controllers/chat.controller.ts"
import type { Request, Response } from 'express';
import { chatService } from '../services/chat.service';
import z from 'zod';

// Zod validation
const chatSchema = z.object({
 prompt: z
  .string()
  .trim()
  .min(1, 'Prompt is required')
  .max(1000, 'Prompt is too long (max 1000 characters)'),
 conversationId: z.uuid(), // expects a valid UUID
});

// Public interface
export const chatController = {
 async sendMessage(req: Request, res: Response) {
  const parseResult = chatSchema.safeParse(req.body);
  if (!parseResult.success) {
   res.status(400).json(z.treeifyError(parseResult.error)); // treeifyError formats the error
   return;
  }

  try {
   const { prompt, id: conversationId } = parseResult.data;
   const response = await chatService.sendMessage(prompt, conversationId);

   res.json({
    message: response.message,
   });
  } catch (error) {
   res.status(500).json({
    error:
     error instanceof Error ? error.message : 'Failed to generate a response.',
   });
  }
 },
};
```

```ts title="packages/server/index.ts"
// server/index.ts
import express from 'express';
import type { Request, Response } from 'express';
import dotenv from 'dotenv';
import { chatController } from './controllers/chat.controller';

dotenv.config();

const app = express();

// Middleware
app.use(express.json()); // parses the req.body

const port = process.env.PORT || 3000;

app.get('/', (req: Request, res: Response) => {
 res.send('Hello World!');
});

app.get('/api/hello', (req: Request, res: Response) => {
 res.json({ message: 'Hello World!' });
});

app.post('/api/chat', chatController.sendMessage);

app.listen(port, () => {
 console.log(`Server is running on http://localhost:${port}`);
});
```

## Video 3.4 - Extracting Routes

- Create file `routes.ts` within `server` folder

```ts title="server/routes.ts"
import express from 'express';
import type { Request, Response } from 'express';
import { chatController } from './controllers/chat.controller';

const router = express.Router();

router.get('/', (req: Request, res: Response) => {
 res.send('Hello World!');
});

router.get('/api/hello', (req: Request, res: Response) => {
 res.json({ message: 'Hello World!' });
});

router.post('/api/chat', chatController.sendMessage);

export default router;
```

```ts title="packages/server/index.ts"
// server/index.ts
import express from 'express';
import dotenv from 'dotenv';
import router from './routes';

dotenv.config();

const app = express();
app.use(express.json()); // Middleware - parses the req.body
app.use(router);

const port = process.env.PORT || 3000;

app.listen(port, () => {
 console.log(`Server is running on http://localhost:${port}`);
});
```

## Video 4.1 - Building the ChatBot Component

- Create file `ChatBot.tsx` within `packages/client/src/components`

- Install `ES7+ React/Redux/React-Native snippets` extension in :material-microsoft-visual-studio-code: VSCode

!!! tip "Using ES7+ React Extension"

    Creating a React component by typing `rafce`

    Shorthand for React Arrow Function Export Component

- Install `React-Icons`

- [x] [https://react-icons.github.io/react-icons](https://react-icons.github.io/react-icons/)

```cmd title="Terminal"
cd packages\client

// Install React Icons
bun add react-icons
```

```tsx title="client/src/App.tsx"
import ChatBot from './components/ChatBot';

function App() {
 return (
  <div className="p-4">
   <ChatBot />
  </div>
 );
}
```

```tsx title="client/src/ChatBot.tsx"
import { Button } from './ui/button';
import { FaArrowUp } from 'react-icons/fa';

const ChatBot = () => {
 return (
  <div className="flex flex-col gap-2 items-end border-2 p-4 rounded-3xl">
   <textarea
    className="w-full border-0 focus:outline-0 resize-none"
    placeholder="Ask anything..."
    maxLength={1000}
   />
   <Button className="rounded-full w-9 h-9">
    <FaArrowUp />
   </Button>
  </div>
 );
};

export default ChatBot;
```

## Video 4.2 - Handling Form Submission

- Install `React-Hook-Form`

- [x] [https://react-hook-form.com](https://react-hook-form.com/)

```cmd title="Terminal"
cd packages\client

// Install React Icons
bun add react-hook-form
```

```tsx title="client/src/ChatBot.tsx"
import { useForm } from 'react-hook-form';
import { Button } from './ui/button';
import { FaArrowUp } from 'react-icons/fa';
import type { KeyboardEvent } from 'react';

type FormData = {
 prompt: string;
};

const ChatBot = () => {
 const { register, handleSubmit, reset, formState } = useForm<FormData>();

 const onSubmit = (data: FormData) => {
  console.log(data);
  reset();
 };

 const onKeyDown = (e: KeyboardEvent<HTMLFormElement>) => {
  if (e.key === 'Enter' && !e.shiftKey) {
   e.preventDefault();
   handleSubmit(onSubmit)();
  }
 };
 return (
  <form
   onSubmit={handleSubmit(onSubmit)}
   onKeyDown={onKeyDown}
   className="flex flex-col gap-2 items-end border-2 p-4 rounded-3xl"
  >
   <textarea
    {...register('prompt', {
     required: true,
     validate: (data) => data.trim().length > 0,
    })}
    className="w-full border-0 focus:outline-0 resize-none"
    placeholder="Ask anything..."
    maxLength={1000}
   />
   <Button disabled={!formState.isValid} className="rounded-full w-9 h-9">
    <FaArrowUp />
   </Button>
  </form>
 );
};

export default ChatBot;
```

## Video 4.3 - Calling the Backend

- Install `Axios`

- [x] [https://axios-http.com](https://axios-http.com)

```cmd title="Terminal"
cd packages\client

// Install Axios
bun add axios
```

!!! tip "Tip for :material-microsoft-visual-studio-code: VS Code"

    To navigate back to your previous cursor location

    On Windows:

    __Alt + ←__ - Go Back

    __Alt + →__ -  Go Forward
