using System;
using System.Drawing;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace TextToModeling.SolidWorks;

public sealed class TaskpaneControl : UserControl
{
    private readonly TextBox _promptTextBox;
    private readonly Button _generateButton;
    private readonly FastApiClient _client = new();

    public event EventHandler<GenerateResponse>? MeshGenerated;

    public TaskpaneControl()
    {
        BackColor = Color.WhiteSmoke;
        Dock = DockStyle.Fill;

        var title = new Label
        {
            Text = "Text To Modeling",
            Dock = DockStyle.Top,
            Height = 28,
            Font = new Font("Segoe UI", 12, FontStyle.Bold)
        };

        _promptTextBox = new TextBox
        {
            Multiline = true,
            Dock = DockStyle.Top,
            Height = 160,
            Font = new Font("Segoe UI", 10)
        };

        _generateButton = new Button
        {
            Text = "Generate",
            Dock = DockStyle.Top,
            Height = 36
        };
        _generateButton.Click += async (_, _) => await GenerateAsync();

        Controls.Add(_generateButton);
        Controls.Add(_promptTextBox);
        Controls.Add(title);
    }

    private async Task GenerateAsync()
    {
        var prompt = _promptTextBox.Text.Trim();
        if (string.IsNullOrWhiteSpace(prompt))
        {
            MessageBox.Show("Enter a prompt before generating.", "Text To Modeling");
            return;
        }

        _generateButton.Enabled = false;
        try
        {
            var mesh = await _client.GenerateAsync(prompt);
            MeshGenerated?.Invoke(this, mesh);
        }
        catch (Exception ex)
        {
            MessageBox.Show(ex.Message, "Generation Failed");
        }
        finally
        {
            _generateButton.Enabled = true;
        }
    }
}
