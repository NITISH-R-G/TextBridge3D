using System;
using System.Threading.Tasks;
using System.Windows;

namespace TextToModeling.Revit;

public partial class PromptWindow : Window
{
    private readonly FastApiClient _client = new();

    public GenerateResponse? ResultMesh { get; private set; }

    public PromptWindow()
    {
        InitializeComponent();
    }

    private async void GenerateButton_OnClick(object sender, RoutedEventArgs e)
    {
        await GenerateAsync();
    }

    private async Task GenerateAsync()
    {
        var prompt = PromptTextBox.Text.Trim();
        if (string.IsNullOrWhiteSpace(prompt))
        {
            MessageBox.Show(this, "Enter a prompt before generating.", "Text To Modeling");
            return;
        }

        GenerateButton.IsEnabled = false;
        try
        {
            ResultMesh = await _client.GenerateAsync(prompt);
            DialogResult = true;
            Close();
        }
        catch (Exception ex)
        {
            MessageBox.Show(this, ex.Message, "Generation Failed");
        }
        finally
        {
            GenerateButton.IsEnabled = true;
        }
    }
}
