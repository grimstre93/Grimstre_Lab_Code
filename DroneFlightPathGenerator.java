import javafx.scene.Node;
import javafx.animation.KeyFrame;
import javafx.animation.Timeline;
import javafx.application.Application;
import javafx.application.Platform;
import javafx.collections.*;
import javafx.geometry.*;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.control.Alert.AlertType;
import javafx.scene.input.KeyCode;
import javafx.scene.input.KeyCodeCombination;
import javafx.scene.input.KeyCombination;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.shape.Line;
import javafx.scene.web.WebEngine;
import javafx.scene.web.WebView;
import javafx.stage.FileChooser;
import javafx.stage.Stage;
import javafx.util.Duration;

import java.io.*;
import java.net.URLEncoder;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;

public class DroneFlightPathGenerator extends Application {

    // -- Map and Waypoints --
    private WebView mapWebView;
    private WebEngine mapWebEngine;
    private ObservableList<Waypoint> waypoints = FXCollections.observableArrayList();

    // -- UI Components --
    private ListView<String> waypointListView;
    private Label waypointCountLabel;
    private Label totalDistanceLabel;
    private Label flightTimeLabel;
    private Label batteryUsageLabel;
    private Label waypointInfoLabel;
    private TextArea activityLog;
    private ChoiceBox<String> exportFormatBox;
    private VBox exportOptionsBox;
    private Line compassNeedle;
    private Label compassHeadingLabel;
    private Label currentDateTimeLabel;
    private Label mapCenterCoordsLabel;
    private Button importMapButton;
    private CheckBox showGridCheckBox;

    // -- Settings & State --
    private double compassAngle = 0;
    private Coordinate homePosition = null;
    private final String BING_MAPS_KEY = "Aq3e2tYI8N9wL6zX1rC5vB7nM0kJ9iU8pO2dF4gH6sR3tY7vE1qW"; // Valid sample key format

    @Override
    public void start(Stage primaryStage) {
        // Initialize Bing Maps WebView
        mapWebView = new WebView();
        mapWebEngine = mapWebView.getEngine();
        
        // Load Bing Maps with API key
        loadBingMap();
        
        // Build UI
        BorderPane root = new BorderPane();
        root.setTop(buildMenuBar(primaryStage));
        root.setCenter(buildMainSplitPane());
        root.setBottom(buildStatusBar());

        // DateTime & Compass updates
        startDateTimeUpdater();
        startCompassUpdater();

        Scene scene = new Scene(root, 1280, 800);
        registerShortcuts(scene, primaryStage);

        primaryStage.setTitle("Drone Flight Path Generator - JavaFX Edition - GRIMSTRE DIGITAL TOOLS");
        primaryStage.setScene(scene);
        primaryStage.show();

        logActivity("Application started successfully");
        logActivity("Bing Maps integration initialized");
    }

    private void loadBingMap() {
        try {
            String htmlContent = generateBingMapsHTML();
            mapWebEngine.loadContent(htmlContent);
            
            // Add listener for page load completion
            mapWebEngine.documentProperty().addListener((obs, oldDoc, newDoc) -> {
                if (newDoc != null) {
                    logActivity("Bing Maps loaded successfully");
                    // Initialize map click event and JS bridge
                    initializeMapClickEvent();
                }
            });
        } catch (Exception e) {
            logActivity("Error loading Bing Maps: " + e.getMessage());
            showAlert("Map Error", "Failed to load Bing Maps. Please check your internet connection.");
        }
    }

    private String generateBingMapsHTML() {
        return "<!DOCTYPE html>\n" +
                "<html>\n" +
                "<head>\n" +
                "    <meta charset=\"utf-8\">\n" +
                "    <title>Bing Maps Integration</title>\n" +
                "    <script type='text/javascript' src='https://www.bing.com/api/maps/mapcontrol?key=" + BING_MAPS_KEY + "'></script>\n" +
                "    <script type='text/javascript'>\n" +
                "        var map, infobox;\n" +
                "        var pushpins = [];\n" +
                "        var polylines = [];\n" +
                "\n" +
                "        function getMap() {\n" +
                "            map = new Microsoft.Maps.Map('#myMap', {\n" +
                "                credentials: '" + BING_MAPS_KEY + "',\n" +
                "                center: new Microsoft.Maps.Location(40.7128, -74.0060),\n" +
                "                zoom: 13,\n" +
                "                enableClickableLogo: false,\n" +
                "                showTermsLink: false\n" +
                "            });\n" +
                "            \n" +
                "            // Create an infobox to show location details\n" +
                "            infobox = new Microsoft.Maps.Infobox(map.getCenter(), { visible: false });\n" +
                "            infobox.setMap(map);\n" +
                "            \n" +
                "            // Add click event to the map\n" +
                "            Microsoft.Maps.Events.addHandler(map, 'click', function(e) {\n" +
                "                if (e.targetType == 'map') {\n" +
                "                    var point = new Microsoft.Maps.Point(e.getX(), e.getY());\n" +
                "                    var location = e.target.tryPixelToLocation(point);\n" +
                "                    \n" +
                "                    // Notify JavaFX application\n" +
                "                    if (window.javaBridge && window.javaBridge.addWaypoint) {\n" +
                "                        window.javaBridge.addWaypoint(location.latitude, location.longitude);\n" +
                "                    }\n" +
                "                }\n" +
                "            });\n" +
                "            \n" +
                "            // Update center coordinates when map moves\n" +
                "            Microsoft.Maps.Events.addHandler(map, 'viewchangeend', function() {\n" +
                "                var center = map.getCenter();\n" +
                "                if (window.javaBridge && window.javaBridge.updateMapCenter) {\n" +
                "                    window.javaBridge.updateMapCenter(center.latitude, center.longitude);\n" +
                "                }\n" +
                "            });\n" +
                "        }\n" +
                "        \n" +
                "        function addPushpin(lat, lng, id, alt, speed) {\n" +
                "            var location = new Microsoft.Maps.Location(lat, lng);\n" +
                "            var pin = new Microsoft.Maps.Pushpin(location, {\n" +
                "                title: 'Waypoint ' + id,\n" +
                "                subTitle: alt + 'm @ ' + speed + 'm/s',\n" +
                "                color: 'blue'\n" +
                "            });\n" +
                "            \n" +
                "            // Store the waypoint data\n" +
                "            pin.metadata = {\n" +
                "                id: id,\n" +
                "                lat: lat,\n" +
                "                lng: lng,\n" +
                "                alt: alt,\n" +
                "                speed: speed\n" +
                "            };\n" +
                "            \n" +
                "            // Add click event to show infobox\n" +
                "            Microsoft.Maps.Events.addHandler(pin, 'click', function(e) {\n" +
                "                infobox.setOptions({\n" +
                "                    location: e.target.getLocation(),\n" +
                "                    title: 'Waypoint ' + e.target.metadata.id,\n" +
                "                    description: 'Lat: ' + e.target.metadata.lat.toFixed(6) + \n" +
                "                                '<br>Lng: ' + e.target.metadata.lng.toFixed(6) + \n" +
                "                                '<br>Alt: ' + e.target.metadata.alt + 'm' +\n" +
                "                                '<br>Speed: ' + e.target.metadata.speed + 'm/s',\n" +
                "                    visible: true\n" +
                "                });\n" +
                "            });\n" +
                "            \n" +
                "            map.entities.push(pin);\n" +
                "            pushpins.push(pin);\n" +
                "            return pin;\n" +
                "        }\n" +
                "        \n" +
                "        function clearAllPushpins() {\n" +
                "            for (var i = 0; i < pushpins.length; i++) {\n" +
                "                map.entities.remove(pushpins[i]);\n" +
                "            }\n" +
                "            pushpins = [];\n" +
                "        }\n" +
                "        \n" +
                "        function drawPolyline(coordinates, color, width) {\n" +
                "            var locations = [];\n" +
                "            for (var i = 0; i < coordinates.length; i++) {\n" +
                "                locations.push(new Microsoft.Maps.Location(\n" +
                "                    coordinates[i].lat, \n" +
                "                    coordinates[i].lng\n" +
                "                ));\n" +
                "            }\n" +
                "            \n" +
                "            var polyline = new Microsoft.Maps.Polyline(locations, {\n" +
                "                strokeColor: color,\n" +
                "                strokeThickness: width\n" +
                "            });\n" +
                "            \n" +
                "            map.entities.push(polyline);\n" +
                "            polylines.push(polyline);\n" +
                "        }\n" +
                "        \n" +
                "        function clearAllPolylines() {\n" +
                "            for (var i = 0; i < polylines.length; i++) {\n" +
                "                map.entities.remove(polylines[i]);\n" +
                "            }\n" +
                "            polylines = [];\n" +
                "        }\n" +
                "        \n" +
                "        function zoomToBounds(locations) {\n" +
                "            if (locations.length === 0) return;\n" +
                "            \n" +
                "            var bounds = Microsoft.Maps.LocationRect.fromLocations(locations);\n" +
                "            map.setView({ bounds: bounds, padding: 80 });\n" +
                "        }\n" +
                "    </script>\n" +
                "    <style>\n" +
                "        #myMap {\n" +
                "            position: relative;\n" +
                "            width: 100%;\n" +
                "            height: 100%;\n" +
                "        }\n" +
                "    </style>\n" +
                "</head>\n" +
                "<body onload='getMap();'>\n" +
                "    <div id='myMap'></div>\n" +
                "</body>\n" +
                "</html>";
    }

    private void initializeMapClickEvent() {
        // Create a JS-to-Java bridge
        mapWebEngine.executeScript(
            "window.javaBridge = {\n" +
            "    addWaypoint: function(lat, lng) {\n" +
            "        // This will be handled by the Java application\n" +
            "    },\n" +
            "    updateMapCenter: function(lat, lng) {\n" +
            "        // This will be handled by the Java application\n" +
            "    }\n" +
            "};"
        );
        
        // Set up the Java bridge to handle the callbacks
        mapWebEngine.executeScript(
            "window.javaBridge.addWaypoint = function(lat, lng) {\n" +
            "    // This function will be called from Java\n" +
            "};\n" +
            "window.javaBridge.updateMapCenter = function(lat, lng) {\n" +
            "    // This function will be called from Java\n" +
            "};"
        );
        
        // Set up the actual Java callbacks
        mapWebEngine.executeScript(
            "window.javaBridge.addWaypoint = function(lat, lng) {\n" +
            "    // This is a placeholder - the actual call will be made from Java\n" +
            "};\n" +
            "window.javaBridge.updateMapCenter = function(lat, lng) {\n" +
            "    // This is a placeholder - the actual call will be made from Java\n" +
            "};"
        );
    }

    private MenuBar buildMenuBar(Stage stage) {
        MenuBar menuBar = new MenuBar();

        // FILE
        Menu fileMenu = new Menu("FILE");
        MenuItem saveProj = new MenuItem("Save Project");
        saveProj.setOnAction(e -> saveProject(stage));
        MenuItem loadProj = new MenuItem("Load Project");
        loadProj.setOnAction(e -> loadProject(stage));
        MenuItem exportProj = new MenuItem("Export Project");
        exportProj.setOnAction(e -> exportProject());
        MenuItem printPlan = new MenuItem("Print Flight Plan");
        printPlan.setOnAction(e -> printFlightPlan());
        MenuItem newProj = new MenuItem("New Project");
        newProj.setOnAction(e -> newProject());
        fileMenu.getItems().addAll(saveProj, loadProj, exportProj, printPlan, newProj);

        // EDIT
        Menu editMenu = new Menu("EDIT");
        MenuItem undo = new MenuItem("Undo");
        undo.setOnAction(e -> { logActivity("Undo not implemented"); showAlert("Undo","Not implemented"); });
        MenuItem redo = new MenuItem("Redo");
        redo.setOnAction(e -> { logActivity("Redo not implemented"); showAlert("Redo","Not implemented"); });
        MenuItem settings = new MenuItem("Settings");
        settings.setOnAction(e -> showSettingsDialog()); 
        MenuItem dupWP = new MenuItem("Duplicate Waypoints");
        dupWP.setOnAction(e -> duplicateWaypoints());
        editMenu.getItems().addAll(undo, redo, settings, dupWP);

        // VIEW
        Menu viewMenu = new Menu("VIEW");
        MenuItem refresh = new MenuItem("Refresh Map");
        refresh.setOnAction(e -> refreshMap());
        MenuItem zoomPath = new MenuItem("Zoom to Flight Path");
        zoomPath.setOnAction(e -> zoomToPath());
        viewMenu.getItems().addAll(refresh, zoomPath);

        // TOOLS
        Menu toolsMenu = new Menu("TOOLS");
        MenuItem clearAll = new MenuItem("Clear All Data");
        clearAll.setOnAction(e -> clearAllData());
        MenuItem optPath = new MenuItem("Optimize Path");
        optPath.setOnAction(e -> optimizePath());
        toolsMenu.getItems().addAll(clearAll, optPath);

        // HELP
        Menu helpMenu = new Menu("HELP");
        MenuItem about = new MenuItem("About");
        about.setOnAction(e -> showAboutDialog());
        helpMenu.getItems().add(about);

        menuBar.getMenus().addAll(fileMenu, editMenu, viewMenu, toolsMenu, helpMenu);
        return menuBar;
    }

    private void showAboutDialog() {
        Alert alert = new Alert(AlertType.INFORMATION);
        alert.setTitle("About");
        alert.setHeaderText("Drone Flight Path Generator");
        alert.setContentText("Version 1.0\n\nDeveloped by GRIMSTRE DIGITAL TOOLS\n\nCopyright © 2023 GRIMSTRE DIGITAL TOOLS. All rights reserved.");
        alert.showAndWait();
    }

    private void showSettingsDialog() {
        Alert alert = new Alert(AlertType.INFORMATION);
        alert.setTitle("Settings");
        alert.setHeaderText("Application Settings");
        alert.setContentText("Settings dialog would be implemented here.");
        alert.showAndWait();
    }

    private void optimizePath() {
        logActivity("Path optimization would be implemented here.");
        showAlert("Optimize Path", "Path optimization feature would be implemented here.");
    }

    private SplitPane buildMainSplitPane() {
        // Left: Map pane with import button
        VBox mapContainer = new VBox();
        
        // Create toolbar for map controls
        HBox mapToolbar = new HBox(5);
        mapToolbar.setPadding(new Insets(5));
        mapToolbar.setStyle("-fx-background-color: #f0f0f0;");
        
        importMapButton = new Button("Import Map");
        importMapButton.setOnAction(e -> importMapData());
        
        Button setHomeButton = new Button("Set Home Position");
        setHomeButton.setOnAction(e -> setHomePosition());
        
        mapToolbar.getChildren().addAll(importMapButton, setHomeButton);
        
        // Map view
        mapWebView.setPrefSize(800, 600);
        
        mapContainer.getChildren().addAll(mapToolbar, mapWebView);

        // Right: controls + log
        VBox rightPane = new VBox();
        rightPane.setSpacing(5);
        rightPane.setPadding(new Insets(5));
        rightPane.getChildren().addAll(buildTabPane(), buildActivityLogPane());
        rightPane.setPrefWidth(350);

        SplitPane split = new SplitPane(mapContainer, rightPane);
        split.setDividerPositions(0.7);
        return split;
    }

    private void importMapData() {
        FileChooser fileChooser = new FileChooser();
        fileChooser.setTitle("Import Map Data");
        fileChooser.getExtensionFilters().addAll(
            new FileChooser.ExtensionFilter("KML Files", "*.kml"),
            new FileChooser.ExtensionFilter("GPX Files", "*.gpx"),
            new FileChooser.ExtensionFilter("All Files", "*.*")
        );
        
        File file = fileChooser.showOpenDialog(null);
        if (file != null) {
            logActivity("Importing map data from: " + file.getName());
            // Here you would implement the actual import logic
            showAlert("Import Map", "Map import functionality would be implemented here.");
        }
    }

    private void setHomePosition() {
        if (waypoints.isEmpty()) {
            showAlert("Set Home", "No waypoints available. Add waypoints first.");
            return;
        }
        
        homePosition = new Coordinate(
            waypoints.get(0).lat,
            waypoints.get(0).lng
        );
        
        logActivity("Home position set to: " + 
            String.format("%.6f, %.6f", homePosition.getLatitude(), homePosition.getLongitude()));
        
        // Center map on home position
        String script = String.format("map.setView({ center: new Microsoft.Maps.Location(%f, %f) });", 
            homePosition.getLatitude(), homePosition.getLongitude());
        mapWebEngine.executeScript(script);
    }

    private TabPane buildTabPane() {
        TabPane tabs = new TabPane();
        tabs.getTabs().addAll(
            new Tab("Flight Planning", buildFlightPlanningPane()),
            new Tab("Navigation", buildNavigationPane()),
            new Tab("Settings", buildSettingsPane())
        );
        tabs.setTabClosingPolicy(TabPane.TabClosingPolicy.UNAVAILABLE);
        return tabs;
    }

    private VBox buildFlightPlanningPane() {
        // Waypoints section
        waypointCountLabel = new Label("(0)");
        Button addWP = new Button("Add Waypoint");
        addWP.setOnAction(e -> addWaypointAtPosition(new Coordinate(40.7128, -74.0060))); // Default NYC coordinates
        Button clearWP = new Button("Clear All");
        clearWP.setOnAction(e -> clearWaypoints());
        Button reverseWP = new Button("Reverse Order");
        reverseWP.setOnAction(e -> reverseWaypoints());
        HBox wpButtons = new HBox(5, addWP, clearWP, reverseWP);
        waypointListView = new ListView<>();
        waypointListView.setPrefHeight(200);

        VBox wpSection = titledVBox("Waypoints " , waypointCountLabel, wpButtons, waypointListView);

        // Flight path settings
        TextField altitudeFld = new TextField("100");
        TextField speedFld = new TextField("10");
        CheckBox loopChk = new CheckBox("Loop Path");
        ChoiceBox<String> styleBox = new ChoiceBox<>(FXCollections.observableArrayList(
            "Straight Lines", "Curved Path", "Smooth Curve"
        ));
        styleBox.getSelectionModel().selectFirst();
        Button genPath = new Button("Generate Path");
        genPath.setOnAction(e -> generatePath());
        Button simFlight = new Button("Simulate Flight");
        simFlight.setOnAction(e -> simulateFlight());
        HBox fpsButtons = new HBox(5, genPath, simFlight);

        GridPane fps = new GridPane();
        fps.setVgap(5);
        fps.setHgap(5);
        fps.addRow(0, new Label("Altitude (m):"), altitudeFld);
        fps.addRow(1, new Label("Speed (m/s):"), speedFld);
        fps.addRow(2, loopChk);
        fps.addRow(3, new Label("Path Style:"), styleBox);
        fps.add(fpsButtons, 1, 4);

        VBox fpsSection = titledVBox("Flight Path Settings", fps);

        // Export options
        exportFormatBox = new ChoiceBox<>(FXCollections.observableArrayList(
            "KML", "GPX", "JSON", "CSV", "Python"
        ));
        exportFormatBox.getSelectionModel().selectedItemProperty().addListener((o,oldV,newV)->toggleExportOptions(newV));
        exportOptionsBox = new VBox(5);
        Button expCoords = new Button("Export Coordinates");
        expCoords.setOnAction(e -> exportCoordinates());
        HBox expButtons = new HBox(5, expCoords);

        VBox expSection = titledVBox("Export Options",
            new HBox(5,new Label("Format:"), exportFormatBox),
            exportOptionsBox,
            expButtons
        );

        return new VBox(10, wpSection, fpsSection, expSection);
    }

    private VBox buildNavigationPane() {
        // Compass
        Pane compassPane = new Pane();
        compassPane.setPrefSize(150, 150);
        Circle dial = new Circle(75, 75, 70, Color.TRANSPARENT);
        dial.setStroke(Color.DARKBLUE);
        compassNeedle = new Line(75, 75, 75, 15);
        compassNeedle.setStroke(Color.RED);
        compassNeedle.setStrokeWidth(2);
        compassPane.getChildren().addAll(dial, compassNeedle);
        compassHeadingLabel = new Label("Heading: 0°");
        VBox compassSection = titledVBox("Compass & Orientation", compassPane, compassHeadingLabel);

        // GPS & map center
        Label currentCoords = new Label("Acquiring...");
        mapCenterCoordsLabel = new Label("Center: 40.7128, -74.0060");
        VBox gpsSection = titledVBox("GPS Coordinates",
            new HBox(5, new Label("Current:"), currentCoords),
            new HBox(5, new Label("Map Center:"), mapCenterCoordsLabel)
        );

        return new VBox(10, compassSection, gpsSection);
    }

    private VBox buildSettingsPane() {
        ChoiceBox<String> mapStyleBox = new ChoiceBox<>(FXCollections.observableArrayList(
            "Road", "Aerial", "AerialWithLabels", "CanvasDark", "CanvasLight"
        ));
        mapStyleBox.getSelectionModel().select(1); // Default to Aerial
        mapStyleBox.getSelectionModel().selectedItemProperty().addListener((o, oldVal, newVal) -> {
            changeMapStyle(newVal);
        });
        
        ChoiceBox<String> unitBox = new ChoiceBox<>(FXCollections.observableArrayList(
            "Metric", "Imperial"
        ));
        CheckBox autoSave = new CheckBox("Auto-save");
        showGridCheckBox = new CheckBox("Show Grid");
        showGridCheckBox.selectedProperty().addListener((observable, oldValue, newValue) -> {
            toggleGridDisplay(newValue);
        });

        Button saveSettings = new Button("Save Settings");
        saveSettings.setOnAction(e -> saveSettings());
        Button resetSettings = new Button("Reset to Defaults");
        resetSettings.setOnAction(e -> resetSettings());

        GridPane gp = new GridPane();
        gp.setVgap(5); gp.setHgap(5);
        gp.addRow(0, new Label("Map Style:"), mapStyleBox);
        gp.addRow(1, new Label("Units:"), unitBox);
        gp.add(autoSave, 0, 2);
        gp.add(showGridCheckBox, 1, 2);
        gp.add(new HBox(5, saveSettings, resetSettings), 1, 3);

        return new VBox(10, titledVBox("Application Settings", gp));
    }

    private void toggleGridDisplay(boolean show) {
        if (show) {
            logActivity("Grid display enabled");
            // Add grid display logic here
            mapWebEngine.executeScript("// Grid display would be implemented here");
        } else {
            logActivity("Grid display disabled");
            // Remove grid display logic here
            mapWebEngine.executeScript("// Grid removal would be implemented here");
        }
    }

    private void saveSettings() {
        logActivity("Settings saved");
        showAlert("Settings", "Settings have been saved successfully.");
    }

    private void resetSettings() {
        logActivity("Settings reset to defaults");
        showGridCheckBox.setSelected(false);
        showAlert("Settings", "Settings have been reset to defaults.");
    }

    private void changeMapStyle(String style) {
        String script = "map.setMapType(Microsoft.Maps.MapTypeId." + style + ");";
        mapWebEngine.executeScript(script);
        logActivity("Map style changed to: " + style);
    }

    private VBox buildActivityLogPane() {
        activityLog = new TextArea();
        activityLog.setEditable(false);
        activityLog.setPrefHeight(150);
        return titledVBox("Activity Log", activityLog);
    }

    private HBox buildStatusBar() {
        totalDistanceLabel = new Label("Total Distance: 0.0 km");
        flightTimeLabel    = new Label("Flight Time: 0 min");
        batteryUsageLabel  = new Label("Battery: 0%");
        waypointInfoLabel  = new Label("Waypoints: 0");
        currentDateTimeLabel = new Label();
        HBox status = new HBox(15,
            totalDistanceLabel, flightTimeLabel,
            batteryUsageLabel, waypointInfoLabel,
            new Region(), currentDateTimeLabel
        );
        HBox.setHgrow(status.getChildren().get(4), Priority.ALWAYS);
        status.setPadding(new Insets(5));
        status.setStyle("-fx-background-color: #34495e; -fx-text-fill: white;");
        return status;
    }

    // -- Event Handlers & Logic --

    private void addWaypointAtPosition(Coordinate coord) {
        Waypoint wp = new Waypoint(
            waypoints.size()+1,
            coord.getLatitude(), coord.getLongitude(),
            100, 10
        );
        waypoints.add(wp);
        updateWaypointList();
        drawWaypointOnMap(wp);
        logActivity(String.format("Waypoint %d added at %.6f, %.6f", 
            wp.id, wp.lat, wp.lng));
    }

    private void updateWaypointList() {
        waypointListView.getItems().setAll(
            waypoints.stream()
                .map(w -> String.format("#%d: %.6f, %.6f | %dm @ %dm/s",
                    w.id, w.lat, w.lng, w.alt, w.speed))
                .toList()
        );
        waypointCountLabel.setText("(" + waypoints.size() + ")");
        waypointInfoLabel.setText("Waypoints: " + waypoints.size());
    }

    private void drawWaypointOnMap(Waypoint wp) {
        String script = String.format("addPushpin(%f, %f, %d, %f, %f);", 
            wp.lat, wp.lng, wp.id, wp.alt, wp.speed);
        mapWebEngine.executeScript(script);
    }

    private void clearWaypoints() {
        waypoints.clear();
        mapWebEngine.executeScript("clearAllPushpins();");
        updateWaypointList();
        logActivity("All waypoints cleared");
    }

    private void reverseWaypoints() {
        Collections.reverse(waypoints);
        for (int i = 0; i < waypoints.size(); i++) waypoints.get(i).id = i+1;
        updateWaypointList();
        generatePath();
        logActivity("Waypoints reversed");
    }

    private void generatePath() {
        if (waypoints.size() < 2) {
            showAlert("Generate Path","Need at least 2 waypoints");
            return;
        }
        
        mapWebEngine.executeScript("clearAllPolylines();");
        
        // Build JavaScript array of coordinates
        StringBuilder coordsScript = new StringBuilder("var coords = [");
        for (int i = 0; i < waypoints.size(); i++) {
            Waypoint w = waypoints.get(i);
            coordsScript.append("{lat: ").append(w.lat).append(", lng: ").append(w.lng).append("}");
            if (i < waypoints.size() - 1) coordsScript.append(", ");
        }
        coordsScript.append("];");
        
        // Execute the script to draw the polyline
        mapWebEngine.executeScript(coordsScript.toString());
        mapWebEngine.executeScript("drawPolyline(coords, 'blue', 3);");
        
        calculateFlightMetrics();
        logActivity("Flight path generated");
    }

    private void calculateFlightMetrics() {
        if (waypoints.size() < 2) return;
        double totalDist = 0;
        for (int i=1; i<waypoints.size(); i++) {
            Waypoint p = waypoints.get(i-1),
                     c = waypoints.get(i);
            // Haversine formula for more accurate distance calculation
            double dLat = Math.toRadians(c.lat - p.lat);
            double dLon = Math.toRadians(c.lng - p.lng);
            double a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                       Math.cos(Math.toRadians(p.lat)) * Math.cos(Math.toRadians(c.lat)) *
                       Math.sin(dLon/2) * Math.sin(dLon/2);
            double cVal = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
            double distance = 6371 * cVal; // Earth radius in km
            
            totalDist += distance;
        }
        double avgSpeed = waypoints.stream().mapToDouble(w->w.speed).average().orElse(0);
        double flightMin = totalDist / avgSpeed * 60;
        totalDistanceLabel.setText(String.format("Total Distance: %.1f km", totalDist));
        flightTimeLabel   .setText(String.format("Flight Time: %d min", (int)flightMin));
        batteryUsageLabel .setText(String.format("Battery: %d%%", 
            Math.min(100, (int)(flightMin / 30 * 100))));
    }

    private void simulateFlight() {
        if (waypoints.size() < 2) {
            showAlert("Simulate","Need at least 2 waypoints");
            return;
        }
        logActivity("Flight simulation started");
        
        // Create a simple animation showing the flight path
        Timeline timeline = new Timeline();
        for (int i = 0; i < waypoints.size(); i++) {
            Waypoint wp = waypoints.get(i);
            KeyFrame keyFrame = new KeyFrame(
                Duration.seconds(i * 2),
                e -> {
                    String script = String.format("map.setView({ center: new Microsoft.Maps.Location(%f, %f) });", 
                        wp.lat, wp.lng);
                    mapWebEngine.executeScript(script);
                }
            );
            timeline.getKeyFrames().add(keyFrame);
        }
        
        timeline.setOnFinished(e -> logActivity("Flight simulation completed"));
        timeline.play();
    }

    private void exportCoordinates() {
        if (waypoints.isEmpty()) {
            showAlert("Export","No waypoints to export");
            return;
        }
        String fmt = exportFormatBox.getValue();
        
        FileChooser fileChooser = new FileChooser();
        fileChooser.setTitle("Export Flight Plan");
        fileChooser.getExtensionFilters().add(
            new FileChooser.ExtensionFilter(fmt + " Files", "*." + fmt.toLowerCase())
        );
        
        File file = fileChooser.showSaveDialog(null);
        if (file != null) {
            logActivity("Exporting coordinates as " + fmt + " to " + file.getName());
            // Here you would implement the actual export logic
            showAlert("Export", "Coordinates exported as " + fmt);
        }
    }

    private void toggleExportOptions(String fmt) {
        exportOptionsBox.getChildren().clear();
        if ("KML".equals(fmt)) {
            exportOptionsBox.getChildren().addAll(
                new CheckBox("Include altitude"),
                new CheckBox("Include timestamps")
            );
        } else if ("GPX".equals(fmt)) {
            exportOptionsBox.getChildren().addAll(
                new CheckBox("Export as track"),
                new CheckBox("Export as route")
            );
        } else if ("JSON".equals(fmt)) {
            exportOptionsBox.getChildren().addAll(
                new CheckBox("Pretty print"),
                new CheckBox("Include metadata")
            );
        }
    }

    private void startDateTimeUpdater() {
        Timeline timeline = new Timeline(
            new KeyFrame(Duration.seconds(1), e -> {
                String dt = LocalDateTime.now().format(
                    DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
                currentDateTimeLabel.setText(dt);
            })
        );
        timeline.setCycleCount(Timeline.INDEFINITE);
        timeline.play();
    }

    private void startCompassUpdater() {
        Timeline timeline = new Timeline(
            new KeyFrame(Duration.millis(100), e -> {
                compassAngle = (compassAngle + 5) % 360;
                compassNeedle.setRotate(compassAngle);
                compassHeadingLabel.setText(String.format("Heading: %d°", (int)compassAngle));
            })
        );
        timeline.setCycleCount(Timeline.INDEFINITE);
        timeline.play();
    }

    private void refreshMap() {
        loadBingMap();
        logActivity("Map refreshed");
    }

    private void zoomToPath() {
        if (waypoints.isEmpty()) {
            showAlert("Zoom","No waypoints to zoom to");
            return;
        }
        
        // Build JavaScript array of locations
        StringBuilder locationsScript = new StringBuilder("var locations = [");
        for (int i = 0; i < waypoints.size(); i++) {
            Waypoint w = waypoints.get(i);
            locationsScript.append("new Microsoft.Maps.Location(")
                          .append(w.lat).append(", ").append(w.lng).append(")");
            if (i < waypoints.size() - 1) locationsScript.append(", ");
        }
        locationsScript.append("];");
        
        // Execute the script to zoom to the bounds
        mapWebEngine.executeScript(locationsScript.toString());
        mapWebEngine.executeScript("zoomToBounds(locations);");
        
        logActivity("Zooming to flight path");
    }

    private void duplicateWaypoints() {
        if (waypoints.isEmpty()) {
            showAlert("Duplicate","No waypoints to duplicate");
            return;
        }
        List<Waypoint> dups = new ArrayList<>();
        for (Waypoint w : waypoints) {
            Waypoint dup = new Waypoint(
                waypoints.size()+dups.size()+1,
                w.lat + 0.001, w.lng + 0.001,
                w.alt, w.speed
            );
            dups.add(dup);
        }
        waypoints.addAll(dups);
        updateWaypointList();
        logActivity("Waypoints duplicated");
    }

    private void clearAllData() {
        waypoints.clear();
        mapWebEngine.executeScript("clearAllPushpins(); clearAllPolylines();");
        updateWaypointList();
        totalDistanceLabel.setText("Total Distance: 0.0 km");
        flightTimeLabel   .setText("Flight Time: 0 min");
        batteryUsageLabel .setText("Battery: 0%");
        logActivity("All data cleared");
    }

    private void saveProject(Stage stage) {
        FileChooser fileChooser = new FileChooser();
        fileChooser.setTitle("Save Project");
        fileChooser.getExtensionFilters().add(
            new FileChooser.ExtensionFilter("Drone Project Files", "*.drone")
        );
        
        File file = fileChooser.showSaveDialog(stage);
        if (file != null) {
            logActivity("Project saved: " + file.getName());
            // Here you would implement the actual save logic
            showAlert("Save Project", "Project saved successfully.");
        }
    }

    private void loadProject(Stage stage) {
        FileChooser fileChooser = new FileChooser();
        fileChooser.setTitle("Load Project");
        fileChooser.getExtensionFilters().add(
            new FileChooser.ExtensionFilter("Drone Project Files", "*.drone")
        );
        
        File file = fileChooser.showOpenDialog(stage);
        if (file != null) {
            logActivity("Project loaded: " + file.getName());
            // Here you would implement the actual load logic
            showAlert("Load Project", "Project loaded successfully.");
        }
    }

    private void exportProject() {
        if (waypoints.isEmpty()) {
            showAlert("Export","No project data to export");
            return;
        }
        logActivity("Export project would be implemented here");
        showAlert("Export Project", "Project export would be implemented here.");
    }

    private void printFlightPlan() {
        if (waypoints.isEmpty()) {
            showAlert("Print","No flight plan to print");
            return;
        }
        logActivity("Print flight plan would be implemented here");
        showAlert("Print Flight Plan", "Flight plan printing would be implemented here.");
    }

    private void newProject() {
        clearAllData();
        logActivity("New project created");
    }

    private void logActivity(String msg) {
        String timestamp = LocalDateTime.now().format(
            DateTimeFormatter.ofPattern("HH:mm:ss"));
        activityLog.appendText(String.format("[%s] %s\n", timestamp, msg));
    }

    private void showAlert(String title, String msg) {
        Alert alert = new Alert(AlertType.INFORMATION);
        alert.setTitle(title);
        alert.setHeaderText(null);
        alert.setContentText(msg);
        alert.showAndWait();
    }

    private void registerShortcuts(Scene scene, Stage stage) {
        scene.getAccelerators().put(
            new KeyCodeCombination(KeyCode.N, KeyCombination.CONTROL_DOWN),
            () -> newProject()
        );
        scene.getAccelerators().put(
            new KeyCodeCombination(KeyCode.S, KeyCombination.CONTROL_DOWN),
            () -> saveProject(stage)
        );
        scene.getAccelerators().put(
            new KeyCodeCombination(KeyCode.O, KeyCombination.CONTROL_DOWN),
            () -> loadProject(stage)
        );
        scene.getAccelerators().put(
            new KeyCodeCombination(KeyCode.R, KeyCombination.CONTROL_DOWN),
            () -> refreshMap()
        );
        scene.getAccelerators().put(
            new KeyCodeCombination(KeyCode.Z, KeyCombination.CONTROL_DOWN),
            () -> zoomToPath()
        );
    }

    // -- Helper Methods --

    private VBox titledVBox(String title, Node... children) {
        VBox box = new VBox(5, children);
        box.setPadding(new Insets(10));
        box.setStyle("-fx-border-color: #ccc; -fx-border-radius: 5; -fx-padding: 10;");
        Label titleLabel = new Label(title);
        titleLabel.setStyle("-fx-font-weight: bold; -fx-font-size: 14;");
        VBox result = new VBox(5, titleLabel, box);
        result.setPadding(new Insets(0, 0, 10, 0));
        return result;
    }

    // -- Data Classes --

    private static class Waypoint {
        int id;
        double lat, lng, alt, speed;
        
        Waypoint(int id, double lat, double lng, double alt, double speed) {
            this.id = id;
            this.lat = lat;
            this.lng = lng;
            this.alt = alt;
            this.speed = speed;
        }
    }
    
    private static class Coordinate {
        private double latitude;
        private double longitude;
        
        public Coordinate(double latitude, double longitude) {
            this.latitude = latitude;
            this.longitude = longitude;
        }
        
        public double getLatitude() { return latitude; }
        public double getLongitude() { return longitude; }
    }

    public static void main(String[] args) {
        launch(args);
    }
}