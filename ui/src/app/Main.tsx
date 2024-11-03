import StorySummary from '@/components/StorySummary';
import { useModelSelectorContext } from "@/lib/model-selector-provider";
import { AgentState } from "@/lib/types";
import { useCoAgent, useCopilotAction, useCopilotMessagesContext, useCopilotReadable } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
import Image from 'next/image';
import logo from '../public/assets/logoHG.png';
import { useState } from 'react';


export default function Main() {
  const { model, agent } = useModelSelectorContext();
  const { state, setState } = useCoAgent<AgentState>({
    name: agent,
    initialState: {
      model,
      research_question: "",
      resources: [],
      report: "",
      logs: [],
    },
  });

  const [story, setStory] = useState("");
  const [content, setContent] = useState<any>({});

  const { messages } = useCopilotMessagesContext()

  useCopilotReadable({
    description: "The story of the research",
    value: story
  })

  useCopilotAction({
    name: "add_story",
    description: "Add a story to the research",
    parameters: [{
      name: "story",
      type: "string",
      description: "The story of the research",
      required: true,
    }],
    handler: ({ story }) => handleAddStory(story as string),
  })

  const handleAddStory = async (story: string) => {
    setStory(story);
    await delay(2000);
    const request = requestMaker(story)
    await storySummaryMock(request)
  }

  const delay = (ms: number) => {
    return new Promise(resolve => setTimeout(resolve, ms))
  }

  const storySummaryMock = async (request: any) => {
    await delay(1000);
    const summaryRequest = await fetch("http://localhost:8000/create_story_outline", {
      method: "POST",
      body: JSON.stringify(request),
      headers: {
        "Content-Type": "application/json",
      }
    })

    const summary = await summaryRequest.json();
    setContent(summary.outline)
  }

  const requestMaker = (created_story: string) => ({ conversation: JSON.stringify(messages.map((m: any) => ({role: m.role, content: m.content}))), previous_outline: created_story })

  return (
    <>
      <h1 className="flex h-[60px] bg-[#050e1c] backdrop-blur-[12px] backdrop-filter text-primary items-center pl-5 pr-10 text-2xl font-bold">
        <Image
          src={logo}
          alt="Ghost agent"
          width={56}
          height={56}
        />
        <span>Ghost agent</span>
      </h1>

      <div
        className="flex flex-1 border"
        style={{ height: "calc(100vh - 60px)" }}
      >
        {/* <div className="flex-1 overflow-hidden">
          <ResearchCanvas />
        </div> */}
        <div className="flex-1 overflow-hidden">
          <StorySummary story={story} outline={content} />
        </div>
        <div
          className="w-[500px] h-full flex-shrink-0"
          style={
            {
              "--copilot-kit-background-color": "#1f2937",
              "--copilot-kit-secondary-color": "#6b7280",
              "--copilot-kit-secondary-contrast-color": "#FFFFFF",
              "--copilot-kit-primary-color": "#FFFFFF",
              "--copilot-kit-contrast-color": "#000000",
              "--copilot-kit-muted-color": "#c2c4c7",
            } as any
          }
        >

          <CopilotChat
            className="h-[calc(100vh-100px)] mr-5 ml-2.5 my-5 rounded-lg"
            onSubmitMessage={async (message) => {
              setState({ ...state, logs: [] });
              await new Promise((resolve) => setTimeout(resolve, 30));
            }}
            labels={{
              initial: "Hi! How can I assist you with your research today?",
            }}
          />
        </div>
      </div>
    </>
  );
}
