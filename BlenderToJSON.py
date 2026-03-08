import bpy
import bmesh
import json
import os

def export_mesh_to_json(filepath):
    # Get the active object
    obj = bpy.context.active_object

    if not obj or obj.type != 'MESH':
        print("Please select a mesh object.")
        return

    # Create a copy of the mesh to avoid destructive changes to your model
    mesh_data = obj.to_mesh()
    bm = bmesh.new()
    bm.from_mesh(mesh_data)

    # Triangulate all faces
    bmesh.ops.triangulate(bm, faces=bm.faces[:])

    # Prepare data structure
    data = {
        "object_name": obj.name,
        "vertices": [],
        "edges": [],
        "faces": []
    }

    # 1. Extract Vertices
    for v in bm.verts:
        data["vertices"].append({
            "index": v.index,
            "position": [round(c, 4) for c in v.co]
        })

    # 2. Extract Edges
    for e in bm.edges:
        data["edges"].append({
            "index": e.index,
            "vertices_indices": [v.index for v in e.verts]
        })

    # 3. Extract Faces (now all triangles)
    for f in bm.faces:
        data["faces"].append({
            "index": f.index,
            "vertices_indices": [v.index for v in f.verts]
        })

    # Write to file
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

    bm.free()
    print(f"Exported successfully to {filepath}")

# Change this path to where you want to save the file
output_path = os.path.join(os.getcwd(), 'C:\\Users\\name')
json_filename = "model_data.json"
output_filepath = os.path.join(output_path, json_filename)
export_mesh_to_json(output_filepath)