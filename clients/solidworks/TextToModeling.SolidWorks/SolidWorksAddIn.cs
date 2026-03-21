using System;
using System.Runtime.InteropServices;
using System.Windows.Forms;
using SolidWorks.Interop.sldworks;
using SolidWorks.Interop.swconst;

namespace TextToModeling.SolidWorks;

[ComVisible(true)]
[Guid("4E4C7D73-7744-4F8A-AE34-0D821F8492A9")]
public sealed class SolidWorksAddIn : ISwAddin
{
    private ISldWorks? _app;
    private int _cookie;
    private ITaskpaneView? _taskpaneView;
    private TaskpaneControl? _taskpaneControl;

    public bool ConnectToSW(object ThisSW, int Cookie)
    {
        _app = (ISldWorks)ThisSW;
        _cookie = Cookie;
        _app.SetAddinCallbackInfo2(0, this, Cookie);

        _taskpaneView = _app.CreateTaskpaneView2(string.Empty, "Text To Modeling");
        _taskpaneControl = new TaskpaneControl();
        _taskpaneControl.CreateControl();
        _taskpaneControl.MeshGenerated += HandleMeshGenerated;
        _taskpaneView.DisplayWindowFromHandlex64(_taskpaneControl.Handle.ToInt64());

        return true;
    }

    public bool DisconnectFromSW()
    {
        if (_taskpaneControl is not null)
        {
            _taskpaneControl.MeshGenerated -= HandleMeshGenerated;
            _taskpaneControl.Dispose();
        }

        _taskpaneView = null;
        _app = null;
        return true;
    }

    private void HandleMeshGenerated(object? sender, GenerateResponse mesh)
    {
        if (_app?.ActiveDoc is not IModelDoc2 model)
        {
            MessageBox.Show("Open a part document before generating geometry.", "Text To Modeling");
            return;
        }

        try
        {
            CreateExtrusion(model, mesh);
        }
        catch (Exception ex)
        {
            MessageBox.Show(ex.Message, "Text To Modeling");
        }
    }

    private static void CreateExtrusion(IModelDoc2 model, GenerateResponse mesh)
    {
        var extension = model.Extension;
        var sketchManager = model.SketchManager;
        var featureManager = model.FeatureManager;

        model.ClearSelection2(true);
        var selected = extension.SelectByID2("Front Plane", "PLANE", 0, 0, 0, false, 0, null, 0);
        if (!selected)
        {
            throw new InvalidOperationException("Could not select the Front Plane.");
        }

        sketchManager.InsertSketch(true);

        if (string.Equals(mesh.Shape, "cylinder", StringComparison.OrdinalIgnoreCase))
        {
            var radius = ToMeters(mesh.Dimensions.Radius ?? 1.0);
            sketchManager.CreateCircleByRadius(0, 0, 0, radius);
        }
        else
        {
            var width = ToMeters(mesh.Dimensions.Width ?? 1.0);
            var depth = ToMeters(mesh.Dimensions.Depth ?? mesh.Dimensions.Width ?? 1.0);
            sketchManager.CreateCornerRectangle(-width / 2.0, -depth / 2.0, 0, width / 2.0, depth / 2.0, 0);
        }

        sketchManager.InsertSketch(true);
        model.ClearSelection2(true);
        extension.SelectByID2("Sketch1", "SKETCH", 0, 0, 0, false, 0, null, 0);

        var height = ToMeters(mesh.Dimensions.Height);
        var feature = featureManager.FeatureExtrusion3(
            true,
            false,
            false,
            0,
            0,
            height,
            0,
            false,
            false,
            false,
            false,
            0,
            0,
            false,
            false,
            false,
            false,
            true,
            true,
            true,
            0,
            0,
            false);

        if (feature is null)
        {
            throw new InvalidOperationException($"SolidWorks could not create the feature for '{mesh.Meta.ObjectName}'.");
        }
    }

    private static double ToMeters(double value)
    {
        return Math.Max(value * 0.1, 0.001);
    }
}
