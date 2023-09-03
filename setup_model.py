# setup the initial model and prepare the analysis

# import genie python package (IMPORTANT, otherwise this does not work)

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

    # Include material
        #This can be another parameter for GaFra but fro simplicity lets keep S355 steel for now
    S355 = MaterialLinear(355000, 7.85 tonne/m^3, 210000000 kPa, 0.3, 1.2e-05 delC^-1, 3e-05 kN*s/m);
    S355.damping = 3e-05
    S275 = MaterialLinear(275000, 7.85 tonne/m^3, 210000000 kPa, 0.3, 1.2e-05 delC^-1, 3e-05 kN*s/m);
    S275.damping = 3e-05

    # Create loads and loadcombinations
        # GaFra shall only use this as input
    Gravity = LoadCase();
    Gravity.setAcceleration(Vector3d(0 m/s^2, 0 m/s^2, -9.80665 m/s^2));
    Gravity.includeSelfWeight();
    Gravity.includeStructureMassWithRotationField();
    Load = LoadCase();
    LC1 = LoadCombination();
    LC1.addCase(Gravity, 1);
    LC1.addCase(Load, 1.3);
    LC1.convertLoadToMass = false;
    LC1.EquipmentRep = EquipmentAsLineLoads;   
    
    # Create simple structure
        # GaFra shall only use this as input
    UB_127x76x13.setDefault();
    S355.setDefault();
    Bm1 = StraightBeam(Point(0 m,0 m,5 m), Point(5 m,0 m,5 m));
    Bm2 = StraightBeam(Point(5 m,0 m,5 m), Point(5 m,5 m,5 m));
    Bm3 = StraightBeam(Point(5 m,5 m,5 m), Point(0 m,5 m,5 m));
    Bm4 = StraightBeam(Point(0 m,5 m,5 m), Point(0 m,0 m,5 m));
    UC_152x152x23.setDefault();
    Bm5 = StraightBeam(Point(0 m,0 m,5 m), Point(0 m,0 m,0 m));
    Bm6 = StraightBeam(Point(5 m,0 m,5 m), Point(5 m,0 m,0 m));
    Bm7 = StraightBeam(Point(5 m,5 m,5 m), Point(5 m,5 m,0 m));
    Bm8 = StraightBeam(Point(0 m,5 m,5 m), Point(0 m,5 m,0 m));
    UB_152x89x16.setDefault();
    UB_127x76x13.setDefault();
    Bm9 = StraightBeam(Point(0 m,0 m,5 m), Point(5 m,0 m,0 m));
    Bm10 = StraightBeam(Point(5 m,0 m,5 m), Point(0 m,0 m,0 m));
    Bm11 = StraightBeam(Point(0 m,5 m,5 m), Point(5 m,5 m,0 m));
    Bm12 = StraightBeam(Point(5 m,5 m,5 m), Point(0 m,5 m,0 m));
    Bm13 = StraightBeam(Point(0 m,0 m,5 m), Point(5 m,5 m,5 m));
    Bm14 = StraightBeam(Point(5 m,0 m,5 m), Point(0 m,5 m,5 m));
    Create fixed support points at base
    Sp1 = SupportPoint(Point(5 m,0 m,0 m));
    Sp2 = SupportPoint(Point(0 m,0 m,0 m));
    Sp3 = SupportPoint(Point(5 m,5 m,0 m));
    Sp4 = SupportPoint(Point(0 m,5 m,0 m));

    # Include load at loadcase ‘Load’
    Load.setActive();
    PLoad1 = PointLoad(Load, FootprintPoint(Point(2.5 m,2.5 m,5 m)), PointForceMoment(Vector3d(0 kN, 0 kN, -10 kN), Vector3d(0 kN*m, 0 kN*m, 0 kN*m)));
    Create and run analysis
    Analysis1 = Analysis(true);
    Analysis1.add(MeshActivity());
    Analysis1.add(LinearAnalysis());
    Analysis1.step(2).useSestra10(true);
    Analysis1.add(LoadResultsActivity());
    Analysis1.setActive();
    Analysis1.step(1).step(1).execute();
    Analysis1.step(1).step(2).execute();
    SimplifyTopology();
    Analysis1.step(1).step(4).execute();
    Analysis1.step(2).execute();
    Analysis1.step(3).execute();

    # Create member check as per AISC
    AISC_Member_check = CapacityManager(Analysis1);
    AISC_Member_check.defaultRunType = "AISC ASD 9th edition";
    MemberCreationOpts = MemberCreationOption();
    MemberCreationOpts.splitAtJoint = false;
    MemberCreationOpts.splitAtIncomingBeam = true;
    MemberCreationOpts.splitAtBeamEnd = true;
    MemberCreationOpts.considerBeamOffset = true;
    AISC_Member_check.createMembers(MemberCreationOpts);
    AISC_Member_check.useFromStructureMemberOptions = false;
    AISC_Member_check.AddRun(AiscAsd9thRun());
    AISC_Member_check.run(1).generateListingFile = false;
    AISC_Member_check.run(1).addLoadCase(LC1);
    AISC_Member_check.run(1).generalOptions.computeLoadsAsNeeded = true;
    
    # Run code checks
    AISC_Member_check.updateStructureFromMembers();
    Analysis1.step(2).execute();
    Analysis1.step(3).execute();
    AISC_Member_check.executeCodeChecks();
    Analysis1.setActive();
    LC1.setActive();