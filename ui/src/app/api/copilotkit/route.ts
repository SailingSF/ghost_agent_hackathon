import {
  CopilotRuntime,
  OpenAIAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import OpenAI from "openai";
import { NextRequest } from "next/server";

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
