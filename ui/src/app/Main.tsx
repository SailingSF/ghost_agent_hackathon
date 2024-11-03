import { ResearchCanvas } from "@/components/ResearchCanvas";
import StorySummary from '@/components/StorySummary';
import { useModelSelectorContext } from "@/lib/model-selector-provider";
import { AgentState } from "@/lib/types";
import { useCoAgent, useCopilotAction, useCopilotMessagesContext, useCopilotReadable } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
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
    handler: ({story}) => handleAddStory(story as string)
  })

  const handleAddStory = (story: string) => {
    setStory(story);
    setTimeout(async () => {
      const request  = requestMaker()
      await storySummaryMock(request)
    }, 1000);
  }

  const delay = (ms: number) => {
    return new Promise(resolve => setTimeout(resolve, ms))
  }

  const storySummaryMock = async (request: any ) => {
    await delay(1000);
    setContent({
      title: "Javascript halloween stories",
      themes: ["Javascript", "Halloween", "AI", "PHP", "Typescript"],
      characters: ["Frameworks", "Libraries", "Tools", "Languages"],
      setting: "Text editors like VSCode, Cursor, Atom, etc.",
      main_plot_point: "Javascript is the best language for Halloween stories"
    })
  }

  const requestMaker = () => ({ conversation_context: messages.map((m: any) => ({role: m.role, content: m.content})), summary: story })    

  return (
    <>
      <h1 className="flex h-[60px] bg-[#ff7919] text-white items-center px-10 text-2xl font-bold">
        Ghost agent
      </h1>

      <div
        className="flex flex-1 border"
        style={{ height: "calc(100vh - 60px)" }}
      >
        {/* <div className="flex-1 overflow-hidden">
          <ResearchCanvas />
        </div> */}
        <div className="flex-1 overflow-hidden">
          <StorySummary story={story} content={content}/>
        </div>
        <div
          className="w-[500px] h-full flex-shrink-0"
          style={
            {
              "--copilot-kit-background-color": "#fdf5e0",
              "--copilot-kit-secondary-color": "#f79316",
              "--copilot-kit-secondary-contrast-color": "#FFFFFF",
              "--copilot-kit-primary-color": "#FFFFFF",
              "--copilot-kit-contrast-color": "#000000",
            } as any
          }
        >
          
          <CopilotChat
            className="h-full"
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
