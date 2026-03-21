using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

namespace TextToModeling.Revit;

[Transaction(TransactionMode.Manual)]
public sealed class GenerateMeshCommand : IExternalCommand
{
    public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
    {
        var window = new PromptWindow();
        var confirmed = window.ShowDialog();
        if (confirmed != true || window.ResultMesh is null)
        {
            return Result.Cancelled;
        }

        RevitMeshBuilder.CreateDirectShape(
            commandData.Application.ActiveUIDocument.Document,
            window.ResultMesh);

        return Result.Succeeded;
    }
}
