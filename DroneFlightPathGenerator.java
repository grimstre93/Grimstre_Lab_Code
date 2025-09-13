import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.ArrayList;
import java.util.List;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.io.FileWriter;
import java.io.IOException;
import java.awt.image.BufferedImage;
import javax.imageio.ImageIO;
import java.io.File;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.net.HttpURLConnection;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.file.StandardCopyOption;
import java.util.Base64;

public class DroneFlightPathGenerator extends JFrame {
    private List<Point> waypoints = new ArrayList<>();
    private List<Point> flightPath = new ArrayList<>();
    private Point origin = new Point(400, 300); // Default origin point
    private boolean loopPath = false;
    
    // Current coordinates
    private double currentLatitude = 0.046757;
    private double currentLongitude = 37.654663;
    private int droneAltitude = 300; // Default altitude in meters
    
    // Map settings
    private int zoomLevel = 10;
    private static final int TILE_SIZE = 256;
    private boolean onlineMode = true;
    private File offlineMapDir = new File("offline_maps");
    
    // Azure Maps API settings (replacing Bing Maps)
    private String azureMapsKey = ""; // Add your Azure Maps key here
    private static final String AZURE_MAPS_URL = "https://atlas.microsoft.com/map/tile?api-version=2.1&tilesetId=microsoft.imagery&zoom={z}&x={x}&y={y}&tileSize=256&language=en-US&view=Auto&subscription-key=";
    
    // UI components
    private MapPanel mapPanel;
    private JCheckBox loopCheckBox;
    private JButton clearButton, generateButton, exportButton;
    private JButton zoomInButton, zoomOutButton, toggleOnlineButton;
    private JComboBox<String> exportMethodCombo;
    private JTextArea logArea;
    private CompassPanel compassPanel;
    private JLabel coordinatesLabel;
    private JLabel altitudeLabel;
    private JTextField altitudeField;
    
    // Activity log
    private List<String> activityLog = new ArrayList<>();
    
    // Map calibration points
    private Point calibrationPoint1 = null;
    private Point calibrationPoint2 = null;
    private double calibLat1, calibLon1, calibLat2, calibLon2;
    
    // Map center coordinates
    private double centerLat = 0.046757;
    private double centerLon = 37.654663;
    
    // Map viewport
    private int viewportX = 0;
    private int viewportY = 0;
    private Point dragStart;
    
    // Menu items
    private JMenuItem saveProjectItem, loadProjectItem, exitItem;
    private JMenuItem undoItem, redoItem, preferencesItem;
    private JMenuItem refreshMapItem;
    private JMenuItem clearAllDataItem;
    private JMenuItem aboutItem;
    private JMenuItem exportAllDataItem;
    private JMenuItem setAzureKeyItem;
    
    public DroneFlightPathGenerator() {
        setTitle("Drone Flight Path Generator with Azure Maps");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(1000, 700);
        setLayout(new BorderLayout());
        
        // Initialize UI components first
        initializeComponents();
        
        // Create menu bar
        createMenuBar();
        
        // Create offline maps directory if it doesn't exist
        if (!offlineMapDir.exists()) {
            offlineMapDir.mkdirs();
        }
        
        // Load Azure Maps key from file if exists
        loadAzureMapsKey();
        
        setVisible(true);
    }
    
    private void initializeComponents() {
        // Create main content panel with split pane
        JSplitPane mainSplitPane = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT);
        mainSplitPane.setDividerLocation(650);
        
        // Create left panel for map and controls
        JPanel leftPanel = new JPanel(new BorderLayout());
        
        // Create map panel
        mapPanel = new MapPanel();
        mapPanel.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                if (e.getButton() == MouseEvent.BUTTON1) {
                    // Left click adds waypoint
                    waypoints.add(e.getPoint());
                    double[] coords = pixelToGPS(e.getPoint().x, e.getPoint().y);
                    logActivity("Waypoint added at: Lat " + String.format("%.6f", coords[0]) + 
                               ", Lon " + String.format("%.6f", coords[1]) + 
                               ", Alt: " + droneAltitude + "m");
                    mapPanel.repaint();
                } else if (e.getButton() == MouseEvent.BUTTON3) {
                    // Right click for calibration
                    handleMapCalibrationClick(e.getPoint());
                }
            }
            
            @Override
            public void mousePressed(MouseEvent e) {
                dragStart = e.getPoint();
            }
        });
        
        mapPanel.addMouseMotionListener(new MouseMotionAdapter() {
            @Override
            public void mouseDragged(MouseEvent e) {
                if (dragStart != null) {
                    int dx = e.getX() - dragStart.x;
                    int dy = e.getY() - dragStart.y;
                    viewportX -= dx;
                    viewportY -= dy;
                    dragStart = e.getPoint();
                    mapPanel.repaint();
                }
            }
            
            @Override
            public void mouseMoved(MouseEvent e) {
                updateCoordinatesLabel(e.getPoint());
            }
        });
        
        // Create control panel
        JPanel controlPanel = new JPanel(new FlowLayout());
        loopCheckBox = new JCheckBox("Loop Path (don't return to origin)");
        clearButton = new JButton("Clear Waypoints");
        generateButton = new JButton("Generate Flight Path");
        exportButton = new JButton("Export Coordinates");
        zoomInButton = new JButton("Zoom In");
        zoomOutButton = new JButton("Zoom Out");
        toggleOnlineButton = new JButton("Go Offline");
        
        // Altitude input
        altitudeLabel = new JLabel("Altitude (m):");
        altitudeField = new JTextField(String.valueOf(droneAltitude), 5);
        altitudeField.addActionListener(e -> {
            try {
                int alt = Integer.parseInt(altitudeField.getText());
                if (alt >= 300) {
                    droneAltitude = alt;
                    logActivity("Drone altitude set to: " + droneAltitude + "m");
                } else {
                    JOptionPane.showMessageDialog(DroneFlightPathGenerator.this, 
                        "Altitude must be at least 300m for drone flight", "Invalid Altitude", 
                        JOptionPane.WARNING_MESSAGE);
                    altitudeField.setText(String.valueOf(droneAltitude));
                }
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(DroneFlightPathGenerator.this, 
                    "Please enter a valid number for altitude", "Invalid Input", 
                    JOptionPane.ERROR_MESSAGE);
                altitudeField.setText(String.valueOf(droneAltitude));
            }
        });
        
        // Export method selection
        String[] exportMethods = {"Display Only", "Save to File", "USB Transfer", "GPS Sync", 
                                 "Memory Card", "Drone Firmware"};
        exportMethodCombo = new JComboBox<>(exportMethods);
        
        clearButton.addActionListener(e -> {
            waypoints.clear();
            flightPath.clear();
            logActivity("All waypoints cleared");
            mapPanel.repaint();
        });
        
        generateButton.addActionListener(e -> {
            loopPath = loopCheckBox.isSelected();
            generateFlightPath();
            logActivity("Flight path generated with " + flightPath.size() + " points");
            mapPanel.repaint();
        });
        
        exportButton.addActionListener(e -> {
            exportCoordinates();
        });
        
        zoomInButton.addActionListener(e -> {
            if (zoomLevel < 19) {
                zoomLevel++;
                // Adjust viewport to zoom toward center
                viewportX = viewportX * 2 + mapPanel.getWidth() / 2;
                viewportY = viewportY * 2 + mapPanel.getHeight() / 2;
                logActivity("Zoom level increased to: " + zoomLevel);
                mapPanel.repaint();
            }
        });
        
        zoomOutButton.addActionListener(e -> {
            if (zoomLevel > 1) {
                // Adjust viewport to zoom out from center
                viewportX = (viewportX - mapPanel.getWidth() / 2) / 2;
                viewportY = (viewportY - mapPanel.getHeight() / 2) / 2;
                zoomLevel--;
                logActivity("Zoom level decreased to: " + zoomLevel);
                mapPanel.repaint();
            }
        });
        
        toggleOnlineButton.addActionListener(e -> {
            onlineMode = !onlineMode;
            toggleOnlineButton.setText(onlineMode ? "Go Offline" : "Go Online");
            logActivity("Switched to " + (onlineMode ? "online" : "offline") + " mode");
            mapPanel.repaint();
        });
        
        controlPanel.add(loopCheckBox);
        controlPanel.add(clearButton);
        controlPanel.add(generateButton);
        controlPanel.add(zoomInButton);
        controlPanel.add(zoomOutButton);
        controlPanel.add(toggleOnlineButton);
        controlPanel.add(altitudeLabel);
        controlPanel.add(altitudeField);
        controlPanel.add(exportMethodCombo);
        controlPanel.add(exportButton);
        
        // Coordinates display
        coordinatesLabel = new JLabel("Lat: " + String.format("%.6f", currentLatitude) + 
                                     ", Lon: " + String.format("%.6f", currentLongitude) +
                                     ", Alt: " + droneAltitude + "m");
        coordinatesLabel.setBorder(BorderFactory.createEmptyBorder(5, 10, 5, 10));
        
        leftPanel.add(mapPanel, BorderLayout.CENTER);
        leftPanel.add(controlPanel, BorderLayout.SOUTH);
        leftPanel.add(coordinatesLabel, BorderLayout.NORTH);
        
        // Create right panel for compass and log
        JPanel rightPanel = new JPanel(new BorderLayout());
        
        // Create compass panel
        compassPanel = new CompassPanel();
        rightPanel.add(compassPanel, BorderLayout.NORTH);
        
        // Create log panel
        JPanel logPanel = new JPanel(new BorderLayout());
        logPanel.setBorder(BorderFactory.createTitledBorder("Activity Log"));
        logArea = new JTextArea(10, 30);
        logArea.setEditable(false);
        JScrollPane logScrollPane = new JScrollPane(logArea);
        logPanel.add(logScrollPane, BorderLayout.CENTER);
        
        JButton clearLogButton = new JButton("Clear Log");
        clearLogButton.addActionListener(e -> {
            activityLog.clear();
            updateLogDisplay();
        });
        logPanel.add(clearLogButton, BorderLayout.SOUTH);
        
        rightPanel.add(logPanel, BorderLayout.CENTER);
        
        mainSplitPane.setLeftComponent(leftPanel);
        mainSplitPane.setRightComponent(rightPanel);
        
        add(mainSplitPane, BorderLayout.CENTER);
        
        // Add initial log entry
        logActivity("Application started");
        logActivity("Current position: Lat " + currentLatitude + ", Lon " + currentLongitude);
        logActivity("Drone altitude set to: " + droneAltitude + "m");
        logActivity("Right-click on map to set calibration points for accurate GPS mapping");
    }
    
    private void createMenuBar() {
        JMenuBar menuBar = new JMenuBar();
        
        // FILE menu
        JMenu fileMenu = new JMenu("FILE");
        saveProjectItem = new JMenuItem("Save Project");
        loadProjectItem = new JMenuItem("Load Project");
        exitItem = new JMenuItem("Exit");
        
        saveProjectItem.addActionListener(e -> saveProject());
        loadProjectItem.addActionListener(e -> loadProject());
        exitItem.addActionListener(e -> System.exit(0));
        
        fileMenu.add(saveProjectItem);
        fileMenu.add(loadProjectItem);
        fileMenu.addSeparator();
        fileMenu.add(exitItem);
        
        // EDIT menu
        JMenu editMenu = new JMenu("EDIT");
        undoItem = new JMenuItem("Undo");
        redoItem = new JMenuItem("Redo");
        preferencesItem = new JMenuItem("Settings");
        
        undoItem.addActionListener(e -> undoLastAction());
        redoItem.addActionListener(e -> redoLastAction());
        preferencesItem.addActionListener(e -> showPreferences());
        
        editMenu.add(undoItem);
        editMenu.add(redoItem);
        editMenu.addSeparator();
        editMenu.add(preferencesItem);
        
        // REFRESH menu
        JMenu refreshMenu = new JMenu("REFRESH");
        refreshMapItem = new JMenuItem("Refresh Map");
        
        refreshMapItem.addActionListener(e -> refreshMap());
        
        refreshMenu.add(refreshMapItem);
        
        // CLEAR ALL DATA menu
        JMenu clearMenu = new JMenu("CLEAR ALL DATA");
        clearAllDataItem = new JMenuItem("Clear All Data");
        
        clearAllDataItem.addActionListener(e -> clearAllData());
        
        clearMenu.add(clearAllDataItem);
        
        // ABOUT menu
        JMenu aboutMenu = new JMenu("ABOUT");
        aboutItem = new JMenuItem("About");
        
        aboutItem.addActionListener(e -> showAboutDialog());
        
        aboutMenu.add(aboutItem);
        
        // EXPORT menu
        JMenu exportMenu = new JMenu("EXPORT");
        exportAllDataItem = new JMenuItem("Export All Data");
        
        exportAllDataItem.addActionListener(e -> exportAllData());
        
        exportMenu.add(exportAllDataItem);
        
        // SETTINGS menu
        JMenu settingsMenu = new JMenu("SETTINGS");
        setAzureKeyItem = new JMenuItem("Set Azure Maps Key");
        
        setAzureKeyItem.addActionListener(e -> setAzureMapsKey());
        
        settingsMenu.add(setAzureKeyItem);
        
        // Add all menus to the menu bar
        menuBar.add(fileMenu);
        menuBar.add(editMenu);
        menuBar.add(refreshMenu);
        menuBar.add(clearMenu);
        menuBar.add(aboutMenu);
        menuBar.add(exportMenu);
        menuBar.add(settingsMenu);
        
        setJMenuBar(menuBar);
    }
    
    private void loadAzureMapsKey() {
        File keyFile = new File("azure_key.txt");
        if (keyFile.exists()) {
            try {
                azureMapsKey = new String(Files.readAllBytes(keyFile.toPath())).trim();
                logActivity("Azure Maps key loaded from file");
            } catch (IOException e) {
                logActivity("Error loading Azure Maps key: " + e.getMessage());
            }
        }
    }
    
    private void saveAzureMapsKey() {
        File keyFile = new File("azure_key.txt");
        try (FileWriter writer = new FileWriter(keyFile)) {
            writer.write(azureMapsKey);
            logActivity("Azure Maps key saved to file");
        } catch (IOException e) {
            logActivity("Error saving Azure Maps key: " + e.getMessage());
        }
    }
    
    private void setAzureMapsKey() {
        String key = JOptionPane.showInputDialog(this, 
            "Enter your Azure Maps API Key:", azureMapsKey);
        if (key != null && !key.trim().isEmpty()) {
            azureMapsKey = key.trim();
            saveAzureMapsKey();
            logActivity("Azure Maps key updated");
            mapPanel.repaint(); // Refresh map with new key
            JOptionPane.showMessageDialog(this, "Azure Maps key saved successfully!");
        }
    }
    
    // Custom JSON-like data structure for project saving/loading
    private static class ProjectData {
        public List<Point> waypoints = new ArrayList<>();
        public List<Point> flightPath = new ArrayList<>();
        public boolean loopPath = false;
        public double currentLatitude = 0.0;
        public double currentLongitude = 0.0;
        public int droneAltitude = 300;
        public int zoomLevel = 10;
        public boolean onlineMode = true;
        public double centerLat = 0.0;
        public double centerLon = 0.0;
        public Point calibrationPoint1 = null;
        public Point calibrationPoint2 = null;
        public double calibLat1 = 0.0;
        public double calibLon1 = 0.0;
        public double calibLat2 = 0.0;
        public double calibLon2 = 0.0;
        public List<String> activityLog = new ArrayList<>();
    }
    
    private void saveProject() {
        ProjectData project = new ProjectData();
        
        // Add waypoints
        project.waypoints = new ArrayList<>(waypoints);
        
        // Add flight path
        project.flightPath = new ArrayList<>(flightPath);
        
        // Add settings
        project.loopPath = loopPath;
        project.currentLatitude = currentLatitude;
        project.currentLongitude = currentLongitude;
        project.droneAltitude = droneAltitude;
        project.zoomLevel = zoomLevel;
        project.onlineMode = onlineMode;
        project.centerLat = centerLat;
        project.centerLon = centerLon;
        
        // Add calibration data if available
        if (calibrationPoint1 != null) {
            project.calibrationPoint1 = new Point(calibrationPoint1.x, calibrationPoint1.y);
            project.calibLat1 = calibLat1;
            project.calibLon1 = calibLon1;
        }
        
        if (calibrationPoint2 != null) {
            project.calibrationPoint2 = new Point(calibrationPoint2.x, calibrationPoint2.y);
            project.calibLat2 = calibLat2;
            project.calibLon2 = calibLon2;
        }
        
        // Add activity log
        project.activityLog = new ArrayList<>(activityLog);
        
        // Save to file
        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setDialogTitle("Save Project");
        if (fileChooser.showSaveDialog(this) == JFileChooser.APPROVE_OPTION) {
            File file = fileChooser.getSelectedFile();
            if (!file.getName().toLowerCase().endsWith(".drone")) {
                file = new File(file.getAbsolutePath() + ".drone");
            }
            
            try (FileWriter writer = new FileWriter(file)) {
                // Write waypoints
                writer.write("WAYPOINTS:\n");
                for (Point p : waypoints) {
                    writer.write(p.x + "," + p.y + "\n");
                }
                
                // Write flight path
                writer.write("FLIGHT_PATH:\n");
                for (Point p : flightPath) {
                    writer.write(p.x + "," + p.y + "\n");
                }
                
                // Write settings
                writer.write("SETTINGS:\n");
                writer.write("loopPath=" + loopPath + "\n");
                writer.write("currentLatitude=" + currentLatitude + "\n");
                writer.write("currentLongitude=" + currentLongitude + "\n");
                writer.write("droneAltitude=" + droneAltitude + "\n");
                writer.write("zoomLevel=" + zoomLevel + "\n");
                writer.write("onlineMode=" + onlineMode + "\n");
                writer.write("centerLat=" + centerLat + "\n");
                writer.write("centerLon=" + centerLon + "\n");
                
                // Write calibration data if available
                if (calibrationPoint1 != null) {
                    writer.write("calibrationPoint1=" + calibrationPoint1.x + "," + calibrationPoint1.y + "\n");
                    writer.write("calibLat1=" + calibLat1 + "\n");
                    writer.write("calibLon1=" + calibLon1 + "\n");
                }
                
                if (calibrationPoint2 != null) {
                    writer.write("calibrationPoint2=" + calibrationPoint2.x + "," + calibrationPoint2.y + "\n");
                    writer.write("calibLat2=" + calibLat2 + "\n");
                    writer.write("calibLon2=" + calibLon2 + "\n");
                }
                
                // Write activity log
                writer.write("ACTIVITY_LOG:\n");
                for (String entry : activityLog) {
                    writer.write(entry + "\n");
                }
                
                logActivity("Project saved to: " + file.getName());
                JOptionPane.showMessageDialog(this, "Project saved successfully!");
            } catch (IOException e) {
                logActivity("Error saving project: " + e.getMessage());
                JOptionPane.showMessageDialog(this, "Error saving project: " + e.getMessage(), 
                    "Error", JOptionPane.ERROR_MESSAGE);
            }
        }
    }
    
    private void loadProject() {
        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setDialogTitle("Load Project");
        if (fileChooser.showOpenDialog(this) == JFileChooser.APPROVE_OPTION) {
            File file = fileChooser.getSelectedFile();
            
            try {
                List<String> lines = Files.readAllLines(file.toPath());
                waypoints.clear();
                flightPath.clear();
                
                String section = "";
                for (String line : lines) {
                    if (line.equals("WAYPOINTS:")) {
                        section = "WAYPOINTS";
                    } else if (line.equals("FLIGHT_PATH:")) {
                        section = "FLIGHT_PATH";
                    } else if (line.equals("SETTINGS:")) {
                        section = "SETTINGS";
                    } else if (line.equals("ACTIVITY_LOG:")) {
                        section = "ACTIVITY_LOG";
                    } else if (!line.isEmpty()) {
                        switch (section) {
                            case "WAYPOINTS":
                                String[] wpCoords = line.split(",");
                                if (wpCoords.length == 2) {
                                    waypoints.add(new Point(
                                        Integer.parseInt(wpCoords[0]),
                                        Integer.parseInt(wpCoords[1])
                                    ));
                                }
                                break;
                            case "FLIGHT_PATH":
                                String[] fpCoords = line.split(",");
                                if (fpCoords.length == 2) {
                                    flightPath.add(new Point(
                                        Integer.parseInt(fpCoords[0]),
                                        Integer.parseInt(fpCoords[1])
                                    ));
                                }
                                break;
                            case "SETTINGS":
                                String[] setting = line.split("=", 2);
                                if (setting.length == 2) {
                                    switch (setting[0]) {
                                        case "loopPath":
                                            loopPath = Boolean.parseBoolean(setting[1]);
                                            loopCheckBox.setSelected(loopPath);
                                            break;
                                        case "currentLatitude":
                                            currentLatitude = Double.parseDouble(setting[1]);
                                            break;
                                        case "currentLongitude":
                                            currentLongitude = Double.parseDouble(setting[1]);
                                            break;
                                        case "droneAltitude":
                                            droneAltitude = Integer.parseInt(setting[1]);
                                            altitudeField.setText(String.valueOf(droneAltitude));
                                            break;
                                        case "zoomLevel":
                                            zoomLevel = Integer.parseInt(setting[1]);
                                            break;
                                        case "onlineMode":
                                            onlineMode = Boolean.parseBoolean(setting[1]);
                                            toggleOnlineButton.setText(onlineMode ? "Go Offline" : "Go Online");
                                            break;
                                        case "centerLat":
                                            centerLat = Double.parseDouble(setting[1]);
                                            break;
                                        case "centerLon":
                                            centerLon = Double.parseDouble(setting[1]);
                                            break;
                                        case "calibrationPoint1":
                                            String[] calib1 = setting[1].split(",");
                                            if (calib1.length == 2) {
                                                calibrationPoint1 = new Point(
                                                    Integer.parseInt(calib1[0]),
                                                    Integer.parseInt(calib1[1])
                                                );
                                            }
                                            break;
                                        case "calibLat1":
                                            calibLat1 = Double.parseDouble(setting[1]);
                                            break;
                                        case "calibLon1":
                                            calibLon1 = Double.parseDouble(setting[1]);
                                            break;
                                        case "calibrationPoint2":
                                            String[] calib2 = setting[1].split(",");
                                            if (calib2.length == 2) {
                                                calibrationPoint2 = new Point(
                                                    Integer.parseInt(calib2[0]),
                                                    Integer.parseInt(calib2[1])
                                                );
                                            }
                                            break;
                                        case "calibLat2":
                                            calibLat2 = Double.parseDouble(setting[1]);
                                            break;
                                        case "calibLon2":
                                            calibLon2 = Double.parseDouble(setting[1]);
                                            break;
                                    }
                                }
                                break;
                            case "ACTIVITY_LOG":
                                activityLog.add(line);
                                break;
                        }
                    }
                }
                
                updateLogDisplay();
                mapPanel.repaint();
                logActivity("Project loaded from: " + file.getName());
                JOptionPane.showMessageDialog(this, "Project loaded successfully!");
            } catch (IOException e) {
                logActivity("Error loading project: " + e.getMessage());
                JOptionPane.showMessageDialog(this, "Error loading project: " + e.getMessage(), 
                    "Error", JOptionPane.ERROR_MESSAGE);
            } catch (NumberFormatException e) {
                logActivity("Error parsing project file: " + e.getMessage());
                JOptionPane.showMessageDialog(this, "Error parsing project file: " + e.getMessage(), 
                    "Error", JOptionPane.ERROR_MESSAGE);
            }
        }
    }
    
    private void undoLastAction() {
        if (!waypoints.isEmpty()) {
            Point removed = waypoints.remove(waypoints.size() - 1);
            logActivity("Undo: Removed waypoint at (" + removed.x + ", " + removed.y + ")");
            mapPanel.repaint();
        } else {
            logActivity("Nothing to undo");
        }
    }
    
    private void redoLastAction() {
        logActivity("Redo functionality not implemented yet");
    }
    
    private void showPreferences() {
        JPanel panel = new JPanel(new GridLayout(0, 2, 5, 5));
        
        panel.add(new JLabel("Default Altitude (m):"));
        JTextField altField = new JTextField(String.valueOf(droneAltitude));
        panel.add(altField);
        
        panel.add(new JLabel("Online Mode:"));
        JCheckBox onlineCheckbox = new JCheckBox("", onlineMode);
        panel.add(onlineCheckbox);
        
        panel.add(new JLabel("Azure Maps Key:"));
        JButton keyButton = new JButton("Set API Key");
        keyButton.addActionListener(e -> setAzureMapsKey());
        panel.add(keyButton);
        
        int result = JOptionPane.showConfirmDialog(this, panel, "Settings", 
            JOptionPane.OK_CANCEL_OPTION, JOptionPane.PLAIN_MESSAGE);
        
        if (result == JOptionPane.OK_OPTION) {
            try {
                int newAlt = Integer.parseInt(altField.getText());
                if (newAlt >= 300) {
                    droneAltitude = newAlt;
                    altitudeField.setText(String.valueOf(droneAltitude));
                    logActivity("Default altitude changed to: " + droneAltitude + "m");
                } else {
                    JOptionPane.showMessageDialog(this, 
                        "Altitude must be at least 300m for drone flight", "Invalid Altitude", 
                        JOptionPane.WARNING_MESSAGE);
                }
            } catch (NumberFormatException e) {
                JOptionPane.showMessageDialog(this, 
                    "Please enter a valid number for altitude", "Invalid Input", 
                    JOptionPane.ERROR_MESSAGE);
            }
            
            onlineMode = onlineCheckbox.isSelected();
            toggleOnlineButton.setText(onlineMode ? "Go Offline" : "Go Online");
            logActivity("Online mode set to: " + onlineMode);
        }
    }
    
    private void refreshMap() {
        // Clear cached map tiles
        File[] tileFiles = offlineMapDir.listFiles();
        if (tileFiles != null) {
            for (File file : tileFiles) {
                file.delete();
            }
        }
        
        logActivity("Map cache cleared, refreshing map");
        mapPanel.repaint();
    }
    
    private void clearAllData() {
        int result = JOptionPane.showConfirmDialog(this, 
            "Are you sure you want to clear all data?", "Confirm Clear", 
            JOptionPane.YES_NO_OPTION, JOptionPane.WARNING_MESSAGE);
        
        if (result == JOptionPane.YES_OPTION) {
            waypoints.clear();
            flightPath.clear();
            activityLog.clear();
            calibrationPoint1 = null;
            calibrationPoint2 = null;
            logActivity("All data cleared");
            mapPanel.repaint();
        }
    }
    
    private void showAboutDialog() {
        String aboutText = "<html><div style='text-align: center;'>" +
            "<h2>Drone Flight Path Generator</h2>" +
            "<p>Version 2.0</p>" +
            "<p>Copyright © 2023 GRIMSTRE DIGITAL TOOLS</p>" +
            "<p>This software is designed for generating and managing" +
            " drone flight paths with altitude control and map integration.</p>" +
            "<p>Features include:</p>" +
            "<ul style='text-align: left;'>" +
            "<li>Interactive map with Azure Maps integration</li>" +
            "<li>Waypoint-based flight path generation</li>" +
            "<li>Altitude control (minimum 300m)</li>" +
            "<li>Multiple export options</li>" +
            "<li>Project saving and loading</li>" +
            "</ul>" +
            "</div></html>";
        
        JOptionPane.showMessageDialog(this, aboutText, "About", JOptionPane.INFORMATION_MESSAGE);
    }
    
    private void exportAllData() {
        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setDialogTitle("Export All Data");
        if (fileChooser.showSaveDialog(this) == JFileChooser.APPROVE_OPTION) {
            File file = fileChooser.getSelectedFile();
            if (!file.getName().toLowerCase().endsWith(".txt")) {
                file = new File(file.getAbsolutePath() + ".txt");
            }
            
            try (FileWriter writer = new FileWriter(file)) {
                // Write waypoints
                writer.write("WAYPOINTS (Latitude, Longitude, Altitude):\n");
                for (Point p : waypoints) {
                    double[] coords = pixelToGPS(p.x, p.y);
                    writer.write(String.format("%.6f, %.6f, %dm\n", 
                        coords[0], coords[1], droneAltitude));
                }
                
                // Write flight path
                writer.write("\nFLIGHT PATH (Latitude, Longitude, Altitude):\n");
                for (Point p : flightPath) {
                    double[] coords = pixelToGPS(p.x, p.y);
                    writer.write(String.format("%.6f, %.6f, %dm\n", 
                        coords[0], coords[1], droneAltitude));
                }
                
                // Write activity log
                writer.write("\nACTIVITY LOG:\n");
                for (String entry : activityLog) {
                    writer.write(entry + "\n");
                }
                
                logActivity("All data exported to: " + file.getName());
                JOptionPane.showMessageDialog(this, "All data exported successfully!");
            } catch (IOException e) {
                logActivity("Error exporting data: " + e.getMessage());
                JOptionPane.showMessageDialog(this, "Error exporting data: " + e.getMessage(), 
                    "Error", JOptionPane.ERROR_MESSAGE);
            }
        }
    }
    
    private void handleMapCalibrationClick(Point point) {
        if (calibrationPoint1 == null) {
            calibrationPoint1 = point;
            String input = JOptionPane.showInputDialog(this, 
                "Enter latitude for calibration point 1:", currentLatitude);
            if (input != null) {
                try {
                    calibLat1 = Double.parseDouble(input);
                    input = JOptionPane.showInputDialog(this, 
                        "Enter longitude for calibration point 1:", currentLongitude);
                    if (input != null) {
                        calibLon1 = Double.parseDouble(input);
                        logActivity("Calibration point 1 set at: Lat " + calibLat1 + ", Lon " + calibLon1);
                    } else {
                        calibrationPoint1 = null;
                    }
                } catch (NumberFormatException e) {
                    JOptionPane.showMessageDialog(this, "Invalid number format", "Error", JOptionPane.ERROR_MESSAGE);
                    calibrationPoint1 = null;
                }
            } else {
                calibrationPoint1 = null;
            }
        } else if (calibrationPoint2 == null) {
            calibrationPoint2 = point;
            String input = JOptionPane.showInputDialog(this, 
                "Enter latitude for calibration point 2:", currentLatitude);
            if (input != null) {
                try {
                    calibLat2 = Double.parseDouble(input);
                    input = JOptionPane.showInputDialog(this, 
                        "Enter longitude for calibration point 2:", currentLongitude);
                    if (input != null) {
                        calibLon2 = Double.parseDouble(input);
                        logActivity("Calibration point 2 set at: Lat " + calibLat2 + ", Lon " + calibLon2);
                    } else {
                        calibrationPoint2 = null;
                    }
                } catch (NumberFormatException e) {
                    JOptionPane.showMessageDialog(this, "Invalid number format", "Error", JOptionPane.ERROR_MESSAGE);
                    calibrationPoint2 = null;
                }
            } else {
                calibrationPoint2 = null;
            }
        } else {
            // Reset calibration
            calibrationPoint1 = null;
            calibrationPoint2 = null;
            logActivity("Calibration points cleared");
        }
        
        mapPanel.repaint();
    }
    
    private void updateCoordinatesLabel(Point mousePoint) {
        double[] coords = pixelToGPS(mousePoint.x, mousePoint.y);
        coordinatesLabel.setText("Lat: " + String.format("%.6f", coords[0]) + 
                                ", Lon: " + String.format("%.6f", coords[1]) +
                                ", Alt: " + droneAltitude + "m");
    }
    
    private void logActivity(String message) {
        String timestamp = new SimpleDateFormat("HH:mm:ss").format(new Date());
        String logEntry = "[" + timestamp + "] " + message;
        activityLog.add(logEntry);
        updateLogDisplay();
    }
    
    private void updateLogDisplay() {
        StringBuilder logText = new StringBuilder();
        for (String entry : activityLog) {
            logText.append(entry).append("\n");
        }
        logArea.setText(logText.toString());
        logArea.setCaretPosition(logArea.getDocument().getLength());
    }
    
    private void generateFlightPath() {
        flightPath.clear();
        
        if (waypoints.isEmpty()) {
            logActivity("No waypoints to generate flight path");
            return;
        }
        
        // Start from origin if not looping
        if (!loopPath) {
            flightPath.add(origin);
        }
        
        // Add all waypoints
        flightPath.addAll(waypoints);
        
        // Return to origin if not looping
        if (!loopPath) {
            flightPath.add(origin);
        }
        
        logActivity("Generated flight path with " + flightPath.size() + " points");
    }
    
    private void exportCoordinates() {
        String method = (String) exportMethodCombo.getSelectedItem();
        
        if (flightPath.isEmpty()) {
            JOptionPane.showMessageDialog(this, "No flight path to export. Generate a flight path first.", 
                "No Data", JOptionPane.WARNING_MESSAGE);
            return;
        }
        
        StringBuilder sb = new StringBuilder();
        sb.append("Drone Flight Path Coordinates\n");
        sb.append("Generated: ").append(new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date())).append("\n");
        sb.append("Altitude: ").append(droneAltitude).append("m\n");
        sb.append("Loop Path: ").append(loopPath).append("\n\n");
        sb.append("Latitude, Longitude, Altitude (m)\n");
        
        for (Point p : flightPath) {
            double[] coords = pixelToGPS(p.x, p.y);
            sb.append(String.format("%.6f, %.6f, %d\n", coords[0], coords[1], droneAltitude));
        }
        
        if ("Display Only".equals(method)) {
            // Show in a dialog
            JTextArea textArea = new JTextArea(sb.toString(), 20, 50);
            textArea.setEditable(false);
            JScrollPane scrollPane = new JScrollPane(textArea);
            JOptionPane.showMessageDialog(this, scrollPane, "Flight Path Coordinates", 
                JOptionPane.INFORMATION_MESSAGE);
        } else if ("Save to File".equals(method)) {
            // Save to file
            JFileChooser fileChooser = new JFileChooser();
            fileChooser.setDialogTitle("Save Coordinates");
            if (fileChooser.showSaveDialog(this) == JFileChooser.APPROVE_OPTION) {
                File file = fileChooser.getSelectedFile();
                if (!file.getName().toLowerCase().endsWith(".txt")) {
                    file = new File(file.getAbsolutePath() + ".txt");
                }
                
                try (FileWriter writer = new FileWriter(file)) {
                    writer.write(sb.toString());
                    logActivity("Coordinates saved to: " + file.getName());
                    JOptionPane.showMessageDialog(this, "Coordinates saved successfully!");
                } catch (IOException e) {
                    logActivity("Error saving coordinates: " + e.getMessage());
                    JOptionPane.showMessageDialog(this, "Error saving coordinates: " + e.getMessage(), 
                        "Error", JOptionPane.ERROR_MESSAGE);
                }
            }
        } else {
            // Other methods (simulated)
            logActivity("Coordinates prepared for " + method);
            JOptionPane.showMessageDialog(this, 
                "Coordinates prepared for " + method + ".\nThis functionality would be implemented with hardware integration.", 
                "Export Method", JOptionPane.INFORMATION_MESSAGE);
        }
    }
    
    private double[] pixelToGPS(int x, int y) {
        // If we have two calibration points, use affine transformation
        if (calibrationPoint1 != null && calibrationPoint2 != null) {
            // Calculate scale factors
            double latScale = (calibLat2 - calibLat1) / (calibrationPoint2.y - calibrationPoint1.y);
            double lonScale = (calibLon2 - calibLon1) / (calibrationPoint2.x - calibrationPoint1.x);
            
            // Calculate GPS coordinates
            double lat = calibLat1 + (y - calibrationPoint1.y) * latScale;
            double lon = calibLon1 + (x - calibrationPoint1.x) * lonScale;
            
            return new double[]{lat, lon};
        }
        
        // Default conversion (approximate)
        int centerX = mapPanel.getWidth() / 2;
        int centerY = mapPanel.getHeight() / 2;
        
        // Adjust for viewport
        int adjX = x - viewportX;
        int adjY = y - viewportY;
        
        // Convert to relative coordinates
        double relX = (adjX - centerX) / (double) centerX;
        double relY = (adjY - centerY) / (double) centerY;
        
        // Convert to GPS (approximate)
        double lat = centerLat - relY * (0.5 / Math.pow(2, 20 - zoomLevel));
        double lon = centerLon + relX * (0.5 / Math.pow(2, 20 - zoomLevel));
        
        return new double[]{lat, lon};
    }
    
    private Point gpsToPixel(double lat, double lon) {
        // If we have two calibration points, use affine transformation
        if (calibrationPoint1 != null && calibrationPoint2 != null) {
            // Calculate scale factors
            double yScale = (calibrationPoint2.y - calibrationPoint1.y) / (calibLat2 - calibLat1);
            double xScale = (calibrationPoint2.x - calibrationPoint1.x) / (calibLon2 - calibLon1);
            
            // Calculate pixel coordinates
            int x = calibrationPoint1.x + (int) ((lon - calibLon1) * xScale);
            int y = calibrationPoint1.y + (int) ((lat - calibLat1) * yScale);
            
            return new Point(x, y);
        }
        
        // Default conversion (approximate)
        int centerX = mapPanel.getWidth() / 2;
        int centerY = mapPanel.getHeight() / 2;
        
        // Convert to relative coordinates
        double relX = (lon - centerLon) * Math.pow(2, 20 - zoomLevel) / 0.5;
        double relY = (centerLat - lat) * Math.pow(2, 20 - zoomLevel) / 0.5;
        
        // Convert to pixel coordinates
        int x = centerX + (int) (relX * centerX) - viewportX;
        int y = centerY + (int) (relY * centerY) - viewportY;
        
        return new Point(x, y);
    }
    
    // Map panel class
    class MapPanel extends JPanel {
        public MapPanel() {
            setPreferredSize(new Dimension(600, 500));
            setBackground(Color.LIGHT_GRAY);
        }
        
        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            
            // Draw map background
            drawMapTiles(g);
            
            // Draw grid with kilometer measurements
            drawGrid(g);
            
            // Draw waypoints and flight path
            drawWaypoints(g);
            drawFlightPath(g);
            
            // Draw calibration points if set
            drawCalibrationPoints(g);
            
            // Draw scale
            drawScale(g);
        }
        
        private void drawMapTiles(Graphics g) {
            if (azureMapsKey.isEmpty()) {
                // Draw placeholder if no API key
                g.setColor(Color.LIGHT_GRAY);
                g.fillRect(0, 0, getWidth(), getHeight());
                g.setColor(Color.DARK_GRAY);
                g.drawString("Azure Maps API key not configured. Go to Settings > Set Azure Maps Key", 10, 20);
                g.drawString("Or right-click to set calibration points for coordinate mapping", 10, 40);
                return;
            }
            
            // Calculate tile coordinates for current view
            int[] centerTile = latLonToTile(centerLat, centerLon, zoomLevel);
            int tileX = centerTile[0];
            int tileY = centerTile[1];
            
            // Calculate offset
            Point centerPixel = latLonToPixel(centerLat, centerLon, zoomLevel);
            int offsetX = getWidth() / 2 - centerPixel.x % TILE_SIZE;
            int offsetY = getHeight() / 2 - centerPixel.y % TILE_SIZE;
            
            // Adjust for viewport
            offsetX += viewportX;
            offsetY += viewportY;
            
            // Calculate visible tile range
            int startX = (int) Math.floor((-offsetX) / (double) TILE_SIZE);
            int endX = (int) Math.ceil((getWidth() - offsetX) / (double) TILE_SIZE);
            int startY = (int) Math.floor((-offsetY) / (double) TILE_SIZE);
            int endY = (int) Math.ceil((getHeight() - offsetY) / (double) TILE_SIZE);
            
            // Draw tiles
            for (int x = startX; x <= endX; x++) {
                for (int y = startY; y <= endY; y++) {
                    int drawX = offsetX + x * TILE_SIZE;
                    int drawY = offsetY + y * TILE_SIZE;
                    
                    // Get tile image
                    Image tileImage = getTileImage(tileX + x, tileY + y, zoomLevel);
                    if (tileImage != null) {
                        g.drawImage(tileImage, drawX, drawY, TILE_SIZE, TILE_SIZE, this);
                    }
                }
            }
        }
        
        private Image getTileImage(int x, int y, int zoom) {
            String filename = "tile_" + zoom + "_" + x + "_" + y + ".jpg";
            File tileFile = new File(offlineMapDir, filename);
            
            // Check if we have the tile cached
            if (tileFile.exists()) {
                try {
                    return ImageIO.read(tileFile);
                } catch (IOException e) {
                    // If there's an error reading the cached file, we'll download it again
                }
            }
            
            // If we're offline and don't have the tile, skip it
            if (!onlineMode) {
                return null;
            }
            
            // Download the tile
            try {
                String urlStr = AZURE_MAPS_URL.replace("{z}", String.valueOf(zoom))
                                             .replace("{x}", String.valueOf(x))
                                             .replace("{y}", String.valueOf(y)) + azureMapsKey;
                
                URL url = new URL(urlStr);
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("GET");
                
                if (conn.getResponseCode() == 200) {
                    try (InputStream in = conn.getInputStream();
                         OutputStream out = Files.newOutputStream(tileFile.toPath())) {
                        
                        byte[] buffer = new byte[1024];
                        int bytesRead;
                        while ((bytesRead = in.read(buffer)) != -1) {
                            out.write(buffer, 0, bytesRead);
                        }
                    }
                    
                    return ImageIO.read(tileFile);
                }
            } catch (IOException e) {
                // If there's an error downloading the tile, we'll just skip it
            }
            
            return null;
        }
        
        private void drawGrid(Graphics g) {
            int width = getWidth();
            int height = getHeight();
            
            // Calculate grid spacing based on zoom level (more zoomed in = smaller grid)
            int gridSpacing = 50 * (int)Math.pow(2, 19 - zoomLevel);
            
            // Draw vertical grid lines
            g.setColor(new Color(0, 0, 0, 50)); // Semi-transparent black
            for (int x = viewportX % gridSpacing; x < width; x += gridSpacing) {
                g.drawLine(x, 0, x, height);
                
                // Add kilometer measurement
                if (x > 0 && x < width) {
                    int km = Math.abs((x - viewportX) / gridSpacing);
                    g.setColor(Color.BLACK);
                    g.drawString(km + "km", x + 5, 15);
                    g.setColor(new Color(0, 0, 0, 50));
                }
            }
            
            // Draw horizontal grid lines
            for (int y = viewportY % gridSpacing; y < height; y += gridSpacing) {
                g.drawLine(0, y, width, y);
                
                // Add kilometer measurement
                if (y > 0 && y < height) {
                    int km = Math.abs((y - viewportY) / gridSpacing);
                    g.setColor(Color.BLACK);
                    g.drawString(km + "km", 5, y - 5);
                    g.setColor(new Color(0, 0, 0, 50));
                }
            }
        }
        
        private void drawWaypoints(Graphics g) {
            // Draw waypoints
            for (Point wp : waypoints) {
                // Adjust for viewport
                int x = wp.x - viewportX;
                int y = wp.y - viewportY;
                
                if (x >= 0 && x < getWidth() && y >= 0 && y < getHeight()) {
                    g.setColor(Color.RED);
                    g.fillOval(x - 5, y - 5, 10, 10);
                    g.setColor(Color.BLACK);
                    g.drawOval(x - 5, y - 5, 10, 10);
                }
            }
        }
        
        private void drawFlightPath(Graphics g) {
            // Draw flight path
            if (flightPath.size() > 1) {
                Graphics2D g2d = (Graphics2D) g;
                g2d.setColor(new Color(0, 255, 0, 128)); // Semi-transparent green
                g2d.setStroke(new BasicStroke(2.0f, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND));
                
                for (int i = 0; i < flightPath.size() - 1; i++) {
                    Point p1 = flightPath.get(i);
                    Point p2 = flightPath.get(i + 1);
                    
                    // Adjust for viewport
                    int x1 = p1.x - viewportX;
                    int y1 = p1.y - viewportY;
                    int x2 = p2.x - viewportX;
                    int y2 = p2.y - viewportY;
                    
                    // Only draw if both points are in view or close to it
                    if ((x1 >= -100 && x1 < getWidth() + 100 && y1 >= -100 && y1 < getHeight() + 100) ||
                        (x2 >= -100 && x2 < getWidth() + 100 && y2 >= -100 && y2 < getHeight() + 100)) {
                        g2d.drawLine(x1, y1, x2, y2);
                    }
                }
            }
        }
        
        private void drawCalibrationPoints(Graphics g) {
            // Draw calibration points if set
            if (calibrationPoint1 != null) {
                int x = calibrationPoint1.x - viewportX;
                int y = calibrationPoint1.y - viewportY;
                
                if (x >= 0 && x < getWidth() && y >= 0 && y < getHeight()) {
                    g.setColor(Color.BLUE);
                    g.fillRect(x - 5, y - 5, 10, 10);
                    g.setColor(Color.WHITE);
                    g.drawString("1", x - 3, y + 5);
                }
            }
            
            if (calibrationPoint2 != null) {
                int x = calibrationPoint2.x - viewportX;
                int y = calibrationPoint2.y - viewportY;
                
                if (x >= 0 && x < getWidth() && y >= 0 && y < getHeight()) {
                    g.setColor(Color.BLUE);
                    g.fillRect(x - 5, y - 5, 10, 10);
                    g.setColor(Color.WHITE);
                    g.drawString("2", x - 3, y + 5);
                }
            }
        }
        
        private void drawScale(Graphics g) {
            // Draw scale indicator
            int scaleWidth = 100; // pixels
            double metersPerPixel = 156543.03392 * Math.cos(centerLat * Math.PI / 180) / Math.pow(2, zoomLevel);
            int meters = (int) (scaleWidth * metersPerPixel);
            
            // Convert to km if over 1000m
            String scaleText;
            if (meters >= 1000) {
                scaleText = String.format("%d km", meters / 1000);
            } else {
                scaleText = String.format("%d m", meters);
            }
            
            int scaleX = getWidth() - scaleWidth - 20;
            int scaleY = getHeight() - 30;
            
            g.setColor(Color.BLACK);
            g.drawLine(scaleX, scaleY, scaleX + scaleWidth, scaleY);
            g.drawLine(scaleX, scaleY - 5, scaleX, scaleY + 5);
            g.drawLine(scaleX + scaleWidth, scaleY - 5, scaleX + scaleWidth, scaleY + 5);
            g.drawString(scaleText, scaleX + scaleWidth / 2 - 20, scaleY + 20);
        }
        
        private int[] latLonToTile(double lat, double lon, int zoom) {
            double x = (lon + 180) / 360 * (1 << zoom);
            double y = (1 - Math.log(Math.tan(Math.toRadians(lat)) + 1 / Math.cos(Math.toRadians(lat))) / Math.PI) / 2 * (1 << zoom);
            
            return new int[]{(int) x, (int) y};
        }
        
        private Point latLonToPixel(double lat, double lon, int zoom) {
            double x = (lon + 180) / 360 * (1 << zoom) * TILE_SIZE;
            double y = (1 - Math.log(Math.tan(Math.toRadians(lat)) + 1 / Math.cos(Math.toRadians(lat))) / Math.PI) / 2 * (1 << zoom) * TILE_SIZE;
            
            return new Point((int) x, (int) y);
        }
    }
    
    // Compass panel class
    class CompassPanel extends JPanel {
        public CompassPanel() {
            setPreferredSize(new Dimension(150, 150));
            setBorder(BorderFactory.createTitledBorder("Compass"));
        }
        
        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            
            int centerX = getWidth() / 2;
            int centerY = getHeight() / 2;
            int radius = Math.min(centerX, centerY) - 10;
            
            // Draw compass circle
            g.setColor(Color.WHITE);
            g.fillOval(centerX - radius, centerY - radius, radius * 2, radius * 2);
            g.setColor(Color.BLACK);
            g.drawOval(centerX - radius, centerY - radius, radius * 2, radius * 2);
            
            // Draw north indicator only
            g.setColor(Color.RED);
            int northX = centerX;
            int northY = centerY - radius + 15;
            g.fillPolygon(
                new int[]{northX, northX - 10, northX + 10},
                new int[]{northY, northY + 20, northY + 20},
                3
            );
            
            // Draw "N" for North
            g.setColor(Color.BLACK);
            g.setFont(new Font("Arial", Font.BOLD, 16));
            g.drawString("N", centerX - 5, centerY - radius + 15);
        }
    }
    
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            new DroneFlightPathGenerator();
        });
    }
}