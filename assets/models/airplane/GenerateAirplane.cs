#if UNITY_EDITOR
using UnityEditor;
using UnityEngine;

namespace Aircraft
{
    public static class AirplaneBuilder
    {
        [MenuItem("GameObject/3D Object/Procedural Airplane", false, 10)]
        [MenuItem("Tools/Generate 3D Airplane", false, 10)]
        public static void CreateAirplane()
        {
            // Root
            GameObject airplane = new GameObject("Airplane_3D");
            Undo.RegisterCreatedObjectUndo(airplane, "Create Procedural Airplane");

            // Materials
            Material bodyMat = CreateColorMaterial("Mat_Fuselage", new Color(0.92f, 0.92f, 0.94f), 0.2f);
            Material wingMat = CreateColorMaterial("Mat_Wings", new Color(0.15f, 0.25f, 0.45f), 0.5f);
            Material engineMat = CreateColorMaterial("Mat_Engines", new Color(0.25f, 0.25f, 0.28f), 0.8f);
            Material trimMat = CreateColorMaterial("Mat_Trim", new Color(0.95f, 0.40f, 0.08f), 0.4f);
            Material glassMat = CreateGlassMaterial("Mat_Glass", new Color(0.2f, 0.5f, 0.85f, 0.6f));

            // 1. Fuselage
            GameObject fuselage = GameObject.CreatePrimitive(PrimitiveType.Capsule);
            fuselage.name = "Fuselage";
            fuselage.transform.SetParent(airplane.transform, false);
            fuselage.transform.localPosition = new Vector3(0, 0, 0);
            fuselage.transform.localRotation = Quaternion.Euler(90f, 0, 0);
            fuselage.transform.localScale = new Vector3(1.2f, 3.2f, 1.2f);
            fuselage.GetComponent<Renderer>().sharedMaterial = bodyMat;

            // 2. Cockpit Canopy
            GameObject canopy = GameObject.CreatePrimitive(PrimitiveType.Capsule);
            canopy.name = "Canopy_Glass";
            canopy.transform.SetParent(airplane.transform, false);
            canopy.transform.localPosition = new Vector3(0, 0.6f, 1.2f);
            canopy.transform.localRotation = Quaternion.Euler(75f, 0, 0);
            canopy.transform.localScale = new Vector3(0.7f, 1.1f, 0.6f);
            canopy.GetComponent<Renderer>().sharedMaterial = glassMat;

            // 3. Main Wings (Left and Right)
            CreateWing(airplane.transform, "Wing_Left", new Vector3(-2.8f, 0, 0.2f), new Vector3(4.8f, 0.08f, 1.6f), new Vector3(0, -12f, 3f), wingMat);
            CreateWing(airplane.transform, "Wing_Right", new Vector3(2.8f, 0, 0.2f), new Vector3(4.8f, 0.08f, 1.6f), new Vector3(0, 12f, -3f), wingMat);

            // Winglets
            CreateWing(airplane.transform, "Winglet_Left", new Vector3(-5.2f, 0.4f, -0.2f), new Vector3(0.08f, 0.7f, 0.6f), new Vector3(0, -15f, 0), trimMat);
            CreateWing(airplane.transform, "Winglet_Right", new Vector3(5.2f, 0.4f, -0.2f), new Vector3(0.08f, 0.7f, 0.6f), new Vector3(0, 15f, 0), trimMat);

            // 4. Engines (Turbines under wings)
            CreateEngine(airplane.transform, "Engine_Left", new Vector3(-1.8f, -0.35f, 0.1f), engineMat);
            CreateEngine(airplane.transform, "Engine_Right", new Vector3(1.8f, -0.35f, 0.1f), engineMat);

            // 5. Tail Stabilizers
            // Horizontal Tail (Elevators)
            CreateWing(airplane.transform, "Tail_Left", new Vector3(-1.1f, 0.2f, -2.9f), new Vector3(1.8f, 0.06f, 0.9f), new Vector3(0, -15f, 0), wingMat);
            CreateWing(airplane.transform, "Tail_Right", new Vector3(1.1f, 0.2f, -2.9f), new Vector3(1.8f, 0.06f, 0.9f), new Vector3(0, 15f, 0), wingMat);

            // Vertical Stabilizer (Fin & Rudder)
            GameObject verticalFin = GameObject.CreatePrimitive(PrimitiveType.Cube);
            verticalFin.name = "Vertical_Fin";
            verticalFin.transform.SetParent(airplane.transform, false);
            verticalFin.transform.localPosition = new Vector3(0, 1.1f, -2.7f);
            verticalFin.transform.localRotation = Quaternion.Euler(20f, 0, 0);
            verticalFin.transform.localScale = new Vector3(0.1f, 1.6f, 1.1f);
            verticalFin.GetComponent<Renderer>().sharedMaterial = trimMat;

            // Select created object
            Selection.activeGameObject = airplane;
            SceneView.FrameLastActiveSceneView();
        }

        private static void CreateWing(Transform parent, string name, Vector3 pos, Vector3 scale, Vector3 rot, Material mat)
        {
            GameObject wing = GameObject.CreatePrimitive(PrimitiveType.Cube);
            wing.name = name;
            wing.transform.SetParent(parent, false);
            wing.transform.localPosition = pos;
            wing.transform.localRotation = Quaternion.Euler(rot);
            wing.transform.localScale = scale;
            wing.GetComponent<Renderer>().sharedMaterial = mat;
        }

        private static void CreateEngine(Transform parent, string name, Vector3 pos, Material mat)
        {
            GameObject engine = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
            engine.name = name;
            engine.transform.SetParent(parent, false);
            engine.transform.localPosition = pos;
            engine.transform.localRotation = Quaternion.Euler(90f, 0, 0);
            engine.transform.localScale = new Vector3(0.55f, 0.8f, 0.55f);
            engine.GetComponent<Renderer>().sharedMaterial = mat;
        }

        private static Material CreateColorMaterial(string name, Color color, float metallic = 0.1f)
        {
            Shader shader = Shader.Find("Universal Render Pipeline/Lit") ?? Shader.Find("Standard");
            Material mat = new Material(shader) { name = name };
            mat.color = color;
            mat.SetFloat("_Metallic", metallic);
            mat.SetFloat("_Smoothness", 0.7f);
            return mat;
        }

        private static Material CreateGlassMaterial(string name, Color color)
        {
            Shader shader = Shader.Find("Universal Render Pipeline/Lit") ?? Shader.Find("Standard");
            Material mat = new Material(shader) { name = name };
            mat.color = color;
            mat.SetFloat("_Metallic", 0.9f);
            mat.SetFloat("_Smoothness", 0.95f);
            return mat;
        }
    }
}
#endif
