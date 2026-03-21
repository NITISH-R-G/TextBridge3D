require 'sketchup.rb'
require 'extensions.rb'

module TextToModeling
  EXTENSION = SketchupExtension.new(
    'Text To Modeling',
    'text_to_modeling/main'
  )
  EXTENSION.description = 'Prompt-driven modeling powered by a local FastAPI backend.'
  EXTENSION.version = '0.1.0'
  EXTENSION.creator = 'OpenAI'

  Sketchup.register_extension(EXTENSION, true)
end
