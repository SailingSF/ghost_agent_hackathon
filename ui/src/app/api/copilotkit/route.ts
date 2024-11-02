import {
  CopilotRuntime,
  OpenAIAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import OpenAI from "openai";
import { NextRequest } from "next/server";

const openai = new OpenAI({ apiKey: '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' });
const llmAdapter = new OpenAIAdapter({ openai });

// const runtime = new CopilotRuntime({
//   remoteActions: [
//     {
//       url: process.env.REMOTE_ACTION_URL || "http://localhost:8000/copilotkit",
//     },
//   ],
// });
const runtime = new CopilotRuntime();

export const POST = async (req: NextRequest) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    serviceAdapter: llmAdapter,
    endpoint: "/api/copilotkit",
  });

  return handleRequest(req);
};
