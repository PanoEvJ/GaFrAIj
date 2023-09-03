def setup_model():
    
    # Open GeniE and create a workspace
    GenieRules.Compatibility.version = "V8.4-06";
    GenieRules.Tolerances.useTolerantModelling = true;
    GenieRules.Tolerances.angleTolerance = 2 deg;
    GenieRules.Meshing.autoSimplifyTopology = true;
    GenieRules.Meshing.eliminateInternalEdges = true;
    GenieRules.BeamCreation.DefaultCurveOffset = ReparameterizedBeamCurveOffset();
    GenieRules.Transformation.DefaultConnectedCopy = false;
    GenieRules.Units.setOutputUnits("m", "kN", "delC");
    GenieRules.Units.setInputUnit(Length, "m");
    GenieRules.Units.setInputUnit(Force, "kN");
    GenieRules.Units.setInputUnit(TempDiff, "delC");
    
    # Creating guiding points (user input)  
    Point1 = Point(0, 0, 0);
    Point2 = Point(0, 0, 5);
    Point3 = Point1.copyTranslate(Vector3d(0, 5, 0));
    Point4 = Point2.copyTranslate(Vector3d(0, 5, 0));
    Point5 = Point1.copyTranslate(Vector3d(5, 0, 0));
    Point6 = Point2.copyTranslate(Vector3d(5, 0, 0));
    Point7 = Point3.copyTranslate(Vector3d(5, 0, 0));
    Point8 = Point4.copyTranslate(Vector3d(5, 0, 0));

    # Importing section sizes from library
        # The input of members and section sizes here can be huge. GeniE has its own library of sections based on standard sizes
        # User can also create their own sections
    

    
    