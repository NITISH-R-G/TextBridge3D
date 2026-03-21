using System;
using System;
using System.Collections.Generic;
using Autodesk.Revit.DB;

namespace TextToModeling.Revit;

public static class RevitMeshBuilder
{
    public static void CreateDirectShape(Document document, GenerateResponse mesh)
    {
        var materialId = ElementId.InvalidElementId;
        var builder = new TessellatedShapeBuilder
        {
            Target = TessellatedShapeBuilderTarget.AnyGeometry,
            Fallback = TessellatedShapeBuilderFallback.Mesh
        };

        builder.OpenConnectedFaceSet(false);

        foreach (var face in mesh.Faces)
        {
            if (face.Count < 3)
            {
                continue;
            }

            var loop = new List<XYZ>();
            foreach (var vertexIndex in face)
            {
                if (vertexIndex < 0 || vertexIndex >= mesh.Vertices.Count)
                {
                    throw new InvalidOperationException("FastAPI response contains an invalid face index.");
                }

                var vertex = mesh.Vertices[vertexIndex];
                loop.Add(new XYZ(vertex[0], vertex[1], vertex[2]));
            }

            builder.AddFace(new TessellatedFace(loop, materialId));
        }

        builder.CloseConnectedFaceSet();
        builder.Build();
        var result = builder.GetBuildResult();

        using var transaction = new Transaction(document, "Text to Modeling");
        transaction.Start();

        var directShape = DirectShape.CreateElement(
            document,
            new ElementId(BuiltInCategory.OST_GenericModel));
        directShape.ApplicationId = "TextToModeling.Revit";
        directShape.ApplicationDataId = mesh.Meta.ObjectName;
        directShape.Name = mesh.Meta.ObjectName;
        directShape.SetShape(result.GetGeometricalObjects());

        transaction.Commit();
    }
}
