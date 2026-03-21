using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace TextToModeling.Revit;

public sealed class GenerateRequest
{
    [JsonPropertyName("prompt")]
    public string Prompt { get; set; } = string.Empty;
}

public sealed class GenerateResponse
{
    [JsonPropertyName("shape")]
    public string Shape { get; set; } = "cube";

    [JsonPropertyName("vertices")]
    public List<List<double>> Vertices { get; set; } = new();

    [JsonPropertyName("faces")]
    public List<List<int>> Faces { get; set; } = new();

    [JsonPropertyName("material")]
    public MaterialDto Material { get; set; } = new();

    [JsonPropertyName("meta")]
    public MetaDto Meta { get; set; } = new();
}

public sealed class MaterialDto
{
    [JsonPropertyName("name")]
    public string Name { get; set; } = "default-concrete";

    [JsonPropertyName("color")]
    public string Color { get; set; } = "#c7c9cc";
}

public sealed class MetaDto
{
    [JsonPropertyName("object_name")]
    public string ObjectName { get; set; } = "generated-object";
}
