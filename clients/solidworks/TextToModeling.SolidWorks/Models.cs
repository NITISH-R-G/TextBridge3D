using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace TextToModeling.SolidWorks;

public sealed class GenerateRequest
{
    [JsonPropertyName("prompt")]
    public string Prompt { get; set; } = string.Empty;
}

public sealed class GenerateResponse
{
    [JsonPropertyName("shape")]
    public string Shape { get; set; } = "cube";

    [JsonPropertyName("dimensions")]
    public DimensionsDto Dimensions { get; set; } = new();

    [JsonPropertyName("vertices")]
    public List<List<double>> Vertices { get; set; } = new();

    [JsonPropertyName("faces")]
    public List<List<int>> Faces { get; set; } = new();

    [JsonPropertyName("meta")]
    public MetaDto Meta { get; set; } = new();
}

public sealed class MetaDto
{
    [JsonPropertyName("object_name")]
    public string ObjectName { get; set; } = "generated-object";
}

public sealed class DimensionsDto
{
    [JsonPropertyName("width")]
    public double? Width { get; set; }

    [JsonPropertyName("height")]
    public double Height { get; set; }

    [JsonPropertyName("depth")]
    public double? Depth { get; set; }

    [JsonPropertyName("radius")]
    public double? Radius { get; set; }
}
