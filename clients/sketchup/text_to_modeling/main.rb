require 'json'
require 'net/http'
require 'uri'
require 'sketchup.rb'

module TextToModeling
  extend self

  DIALOG_WIDTH = 420
  DIALOG_HEIGHT = 320
  API_URL = 'http://127.0.0.1:8000/generate'.freeze

  def show_dialog
    @dialog ||= build_dialog
    @dialog.show
  end

  def build_dialog
    dialog = UI::HtmlDialog.new(
      dialog_title: 'Text To Modeling',
      width: DIALOG_WIDTH,
      height: DIALOG_HEIGHT,
      style: UI::HtmlDialog::STYLE_DIALOG
    )

    dialog.set_html(dialog_html)
    dialog.add_action_callback('generateMesh') do |_context, prompt|
      handle_prompt(prompt)
    end

    dialog
  end

  def handle_prompt(prompt)
    cleaned_prompt = prompt.to_s.strip
    if cleaned_prompt.empty?
      UI.messagebox('Enter a prompt before generating.')
      return
    end

    response = request_mesh(cleaned_prompt)
    draw_mesh(response)
  rescue StandardError => e
    UI.messagebox("Generation failed: #{e.message}")
  end

  def request_mesh(prompt)
    uri = URI.parse(API_URL)
    request = Net::HTTP::Post.new(uri.request_uri, 'Content-Type' => 'application/json')
    request.body = JSON.generate({ prompt: prompt })

    response = Net::HTTP.start(uri.host, uri.port) do |http|
      http.request(request)
    end

    unless response.is_a?(Net::HTTPSuccess)
      raise "FastAPI server returned #{response.code}"
    end

    JSON.parse(response.body)
  end

  def draw_mesh(response)
    model = Sketchup.active_model
    entities = model.active_entities
    mesh = Geom::PolygonMesh.new

    response.fetch('vertices').each do |vertex|
      mesh.add_point(Geom::Point3d.new(vertex[0], vertex[1], vertex[2]))
    end

    response.fetch('faces').each do |face|
      polygon = face.map { |index| index + 1 }
      mesh.add_polygon(polygon)
    end

    material_name = ensure_material(response.fetch('material'))

    model.start_operation('Text To Modeling', true)
    entities.add_faces_from_mesh(
      mesh,
      Geom::PolygonMesh::AUTO_SOFTEN | Geom::PolygonMesh::SMOOTH_SOFT_EDGES,
      material_name,
      material_name
    )
    model.commit_operation
  end

  def ensure_material(material_hash)
    model = Sketchup.active_model
    materials = model.materials
    material_name = material_hash.fetch('name')
    material = materials[material_name] || materials.add(material_name)
    material.color = hex_to_color(material_hash.fetch('color'))
    material_name
  end

  def hex_to_color(value)
    hex = value.delete('#')
    red = hex[0..1].to_i(16)
    green = hex[2..3].to_i(16)
    blue = hex[4..5].to_i(16)
    Sketchup::Color.new(red, green, blue)
  end

  def dialog_html
    <<~HTML
      <!DOCTYPE html>
      <html lang="en">
      <head>
        <meta charset="UTF-8">
        <title>Text To Modeling</title>
        <style>
          body {
            font-family: Segoe UI, sans-serif;
            margin: 0;
            padding: 18px;
            background: linear-gradient(180deg, #f7f8fa 0%, #e9edf3 100%);
            color: #20232a;
          }
          textarea {
            width: 100%;
            height: 150px;
            margin-top: 10px;
            padding: 12px;
            border-radius: 12px;
            border: 1px solid #c8cfdb;
            resize: none;
            box-sizing: border-box;
            font-size: 14px;
          }
          button {
            margin-top: 14px;
            padding: 10px 16px;
            border: none;
            border-radius: 999px;
            background: #1b5cff;
            color: white;
            font-weight: 600;
            cursor: pointer;
          }
        </style>
      </head>
      <body>
        <h2>Text To Modeling</h2>
        <p>Describe a cube or cylinder, then send it to the local generator.</p>
        <textarea id="prompt" placeholder="Example: blue cylinder height 12 radius 3"></textarea>
        <button onclick="window.sketchup.generateMesh(document.getElementById('prompt').value)">Generate</button>
      </body>
      </html>
    HTML
  end

  unless file_loaded?(__FILE__)
    UI.menu('Plugins').add_item('Text To Modeling') do
      show_dialog
    end
    file_loaded(__FILE__)
  end
end
