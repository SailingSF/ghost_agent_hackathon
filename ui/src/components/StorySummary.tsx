import React from 'react'

type Props = {
    story: string,
    content: {
      title?: string,
      themes?: string[],
      characters?: string[],
      setting?: string,
      main_plot_point?: string
    }
}

const StorySummary = (props: Props) => {
  return (
    <div className="container w-full h-full p-10 bg-[#fffbf5]">
        <h2 className="text-lg font-medium mb-3 text-primary">
            { props.content.title || "Story" }
        </h2>
        <p className="text-sm text-slate-400">
            {props.story}
        </p>

        <h2 className="text-lg font-medium mb-1 text-primary mt-3">
            Themes
        </h2>

        <ul className="container-list">
          {props.content.themes?.map((theme, index) => (
            <li 
              key={index}
              className="container-list-item text-sm text-slate-400">
              {theme}
            </li>
          ))}
        </ul>

        <h2 className="text-lg font-medium mb-1 text-primary mt-3">
            Characters
        </h2>

        <ul className="container-list">
          {props.content.characters?.map((character, index) => (
            <li 
              key={index}
              className="container-list-item text-sm text-slate-400">
              {character}
            </li>
          ))}
        </ul>

        <h2 className="text-lg font-medium mb-1 text-primary mt-3">
            Setting
        </h2>

        <p className="text-sm text-slate-400">
            {props.content.setting}
        </p>


        <h2 className="text-lg font-medium mb-1 text-primary mt-3">
            Main Plot Point
        </h2>

        <p className="text-sm text-slate-400">
            {props.content.main_plot_point}
        </p>

    </div>
  )
}

export default StorySummary