import React from 'react'

type Props = {
  story: string,
    outline: {
      title?: string,
      themes?: string[],
      characters?: string[],
      setting?: string,
      plot_points?: string[]
    }
}

const StorySummary = (props: Props) => {
  return (
    <section className="flex-grow bg-gray-800 rounded-lg shadow-md p-6 h-[calc(100vh-100px)] ml-5 mr-2.5 my-5">
      <div className="overflow-y-auto h-full max-h-[calc(100vh-150px)] pr-4">
        {
          props.outline.title ?
            (
              <div className="p-4 bg-gray-700 rounded-md">
                <h3 className="text-lg font-semibold mb-2">{props.outline.title || "Story"}</h3>
                <p className="text-slate-300">{props.story}</p>
              </div>
            ) :
            (
              <>
                <h2 className="text-lg font-semibold mb-3 text-primary">
                  {"👋 Once you've requested your story, I'll summarize it for you."}
                </h2>
                <p className="text-sm text-slate-400">{props.story}</p>
              </>
            )
        }


        {props.outline.themes?.length && (
          <>
            <h2 className="text-lg font-medium mb-1 text-primary mt-3">📝 Themes</h2>
            <ul className="container-list">
              {props.outline.themes?.map((theme, index) => (
                <li key={index} className="container-list-item text-sm text-slate-400">
                  {theme}
                </li>
              ))}
            </ul>
          </>
        )}

        {props.outline.characters?.length && (
          <>
            <h2 className="text-lg font-medium mb-1 text-primary mt-3">🧙‍♂️ Characters</h2>
            <ul className="container-list">
              {props.outline.characters?.map((character, index) => (
                <li key={index} className="container-list-item text-sm text-slate-400">
                  {character}
                </li>
              ))}
            </ul>
          </>
        )}

        {props.outline.setting && (
          <>
            <h2 className="text-lg font-medium mb-1 text-primary mt-3">🌁Setting</h2>
            <p className="text-sm text-slate-400">{props.outline.setting}</p>
          </>
        )}

        {props.outline.plot_points?.length && (
          <>
            <h2 className="text-lg font-medium mb-1 text-primary mt-3">💥 Main Plot Point</h2>
            <ul className="container-list">
              {props.outline.plot_points?.map((point, index) => (
                <li key={index} className="container-list-item text-sm text-slate-400">
                  {point}
                </li>
              ))}
            </ul>
          </>
        )}
      </div>
    </section>
  )
}

export default StorySummary