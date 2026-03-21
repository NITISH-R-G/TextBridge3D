using System;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

namespace TextToModeling.Revit;

public sealed class FastApiClient
{
    private static readonly HttpClient HttpClient = new()
    {
        BaseAddress = new Uri("http://127.0.0.1:8000/")
    };

    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNameCaseInsensitive = true
    };

    public async Task<GenerateResponse> GenerateAsync(string prompt)
    {
        var payload = JsonSerializer.Serialize(new GenerateRequest { Prompt = prompt }, JsonOptions);
        using var response = await HttpClient.PostAsync(
            "generate",
            new StringContent(payload, Encoding.UTF8, "application/json"));

        response.EnsureSuccessStatusCode();
        var json = await response.Content.ReadAsStringAsync();
        var model = JsonSerializer.Deserialize<GenerateResponse>(json, JsonOptions);
        if (model is null)
        {
            throw new InvalidOperationException("FastAPI response could not be parsed.");
        }

        return model;
    }
}
