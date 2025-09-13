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
import java.net.HttpURLConnection;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.Timer;
import java.util.TimerTask;

public class DroneFlightPathGenerator extends JFrame {
    private List<Waypoint> waypoints = new ArrayList<>();
    private List<Waypoint> flightPath = new ArrayList<>();
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

    // Bing Maps API settings
    private String bingMapsKey = ""; // Add your Bing Maps key here
    private static final String BING_MAPS_URL = "https://t0.tiles.virtualearth.net/tiles/a{quadkey}.jpeg?g=1&n=z";

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

    // New UI components
    private JButton showFirmwareButton;
    private JButton downloadMapButton;
    private JDialog firmwareDialog;
    private JTextArea firmwareCodeArea;
    private JLabel gpsStatusLabel;

    // Activity log
    private List<String> activityLog = new ArrayList<>();

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
    private JMenuItem setBingKeyItem;
    private JMenuItem downloadMapItem;

    // GPS simulation
    private Timer gpsUpdateTimer;
    private boolean simulateGPS = true;

    // Waypoint class to store coordinates and altitude
    class Waypoint {
        double lat;
        double lon;
        int alt;

        Waypoint(double lat, double lon, int alt) {
            this.lat = lat;
            this.lon = lon;
            this.alt = alt;
        }
    }

    public DroneFlightPathGenerator() {
        setTitle("Drone Flight Path Generator with Bing Maps");
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

        // Load Bing Maps key from file if exists
        loadBingMapsKey();

        // Start GPS simulation
        startGPSSimulation();

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
                    int alt = Integer.parseInt(altitudeField.getText());
                    if (alt < 300) {
                        JOptionPane.showMessageDialog(DroneFlightPathGenerator.this,
                                "Altitude must be at least 300m for drone flight", "Invalid Altitude",
                                JOptionPane.WARNING_MESSAGE);
                        altitudeField.setText("300");
                        return;
                    }

                    // Convert pixel coordinates to GPS
                    double[] coords = pixelToGPS(e.getPoint().x, e.getPoint().y);
                    Waypoint wp = new Waypoint(coords[0], coords[1], alt);
                    waypoints.add(wp);

                    logActivity("Waypoint added at: Lat " + String.format("%.6f", coords[0]) +
                            ", Lon " + String.format("%.6f", coords[1]) +
                            ", Alt: " + alt + "m");
                    mapPanel.repaint();
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
        downloadMapButton = new JButton("Download Map");

        // Firmware button
        showFirmwareButton = new JButton("Firmware Code");

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
                logActivity("Zoom level increased to: " + zoomLevel);
                mapPanel.repaint();
            }
        });

        zoomOutButton.addActionListener(e -> {
            if (zoomLevel > 1) {
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

        // Download map button action
        downloadMapButton.addActionListener(e -> {
            showDownloadMapDialog();
        });

        // Firmware button action
        showFirmwareButton.addActionListener(e -> {
            showFirmwareDialog();
        });

        controlPanel.add(loopCheckBox);
        controlPanel.add(clearButton);
        controlPanel.add(generateButton);
        controlPanel.add(zoomInButton);
        controlPanel.add(zoomOutButton);
        controlPanel.add(toggleOnlineButton);
        controlPanel.add(downloadMapButton);
        controlPanel.add(altitudeLabel);
        controlPanel.add(altitudeField);
        controlPanel.add(exportMethodCombo);
        controlPanel.add(exportButton);
        controlPanel.add(showFirmwareButton);

        // Coordinates display
        coordinatesLabel = new JLabel("Lat: " + String.format("%.6f", currentLatitude) +
                ", Lon: " + String.format("%.6f", currentLongitude) +
                ", Alt: " + droneAltitude + "m");
        coordinatesLabel.setBorder(BorderFactory.createEmptyBorder(5, 10, 5, 10));

        // GPS status label
        gpsStatusLabel = new JLabel("GPS: Acquiring signal...");
        gpsStatusLabel.setBorder(BorderFactory.createEmptyBorder(5, 10, 5, 10));
        gpsStatusLabel.setForeground(Color.BLUE);

        JPanel northPanel = new JPanel(new BorderLayout());
        northPanel.add(coordinatesLabel, BorderLayout.NORTH);
        northPanel.add(gpsStatusLabel, BorderLayout.SOUTH);

        leftPanel.add(mapPanel, BorderLayout.CENTER);
        leftPanel.add(controlPanel, BorderLayout.SOUTH);
        leftPanel.add(northPanel, BorderLayout.NORTH);

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

        // VIEW menu
        JMenu viewMenu = new JMenu("VIEW");
        refreshMapItem = new JMenuItem("Refresh Map");

        refreshMapItem.addActionListener(e -> refreshMap());

        viewMenu.add(refreshMapItem);

        // DATA menu
        JMenu dataMenu = new JMenu("DATA");
        clearAllDataItem = new JMenuItem("Clear All Data");
        exportAllDataItem = new JMenuItem("Export All Data");

        clearAllDataItem.addActionListener(e -> clearAllData());
        exportAllDataItem.addActionListener(e -> exportAllData());

        dataMenu.add(clearAllDataItem);
        dataMenu.add(exportAllDataItem);

        // SETTINGS menu
        JMenu settingsMenu = new JMenu("SETTINGS");
        setBingKeyItem = new JMenuItem("Set Bing Maps Key");
        downloadMapItem = new JMenuItem("Download Map Area");

        setBingKeyItem.addActionListener(e -> setBingMapsKey());
        downloadMapItem.addActionListener(e -> showDownloadMapDialog());

        settingsMenu.add(setBingKeyItem);
        settingsMenu.add(downloadMapItem);

        // HELP menu
        JMenu helpMenu = new JMenu("HELP");
        aboutItem = new JMenuItem("About");

        aboutItem.addActionListener(e -> showAboutDialog());

        helpMenu.add(aboutItem);

        // Add all menus to the menu bar
        menuBar.add(fileMenu);
        menuBar.add(editMenu);
        menuBar.add(viewMenu);
        menuBar.add(dataMenu);
        menuBar.add(settingsMenu);
        menuBar.add(helpMenu);

        setJMenuBar(menuBar);
    }

    private void loadBingMapsKey() {
        File keyFile = new File("bing_key.txt");
        if (keyFile.exists()) {
            try {
                bingMapsKey = new String(Files.readAllBytes(keyFile.toPath())).trim();
                logActivity("Bing Maps key loaded from file");
            } catch (IOException e) {
                logActivity("Error loading Bing Maps key: " + e.getMessage());
            }
        }
    }

    private void saveBingMapsKey() {
        File keyFile = new File("bing_key.txt");
        try (FileWriter writer = new FileWriter(keyFile)) {
            writer.write(bingMapsKey);
            logActivity("Bing Maps key saved to file");
        } catch (IOException e) {
            logActivity("Error saving Bing Maps key: " + e.getMessage());
        }
    }

    private void startGPSSimulation() {
        gpsUpdateTimer = new Timer();
        gpsUpdateTimer.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
                if (simulateGPS) {
                    // Simulate small GPS position changes
                    currentLatitude += (Math.random() - 0.5) * 0.0001;
                    currentLongitude += (Math.random() - 0.5) * 0.0001;

                    // Update UI on the EDT
                    SwingUtilities.invokeLater(() -> {
                        coordinatesLabel.setText("Lat: " + String.format("%.6f", currentLatitude) +
                                ", Lon: " + String.format("%.6f", currentLongitude) +
                                ", Alt: " + droneAltitude + "m");

                        // Update GPS status
                        if (Math.random() > 0.1) { // 90% chance of good signal
                            gpsStatusLabel.setText("GPS: Good signal (12 satellites)");
                            gpsStatusLabel.setForeground(new Color(0, 128, 0)); // Dark green
                        } else {
                            gpsStatusLabel.setText("GPS: Weak signal (4 satellites)");
                            gpsStatusLabel.setForeground(Color.ORANGE);
                        }
                    });
                }
            }
        }, 1000, 2000); // Start after 1 second, update every 2 seconds
    }

    private void updateCoordinatesLabel(Point p) {
        double[] coords = pixelToGPS(p.x, p.y);
        coordinatesLabel.setText("Lat: " + String.format("%.6f", coords[0]) +
                ", Lon: " + String.format("%.6f", coords[1]) +
                ", Alt: " + droneAltitude + "m");
    }

    private double[] pixelToGPS(int x, int y) {
        // Convert pixel coordinates to GPS coordinates
        int centerX = mapPanel.getWidth() / 2;
        int centerY = mapPanel.getHeight() / 2;

        double lat = centerLat + (y - centerY - viewportY) / (Math.pow(2, zoomLevel) * TILE_SIZE);
        double lon = centerLon + (x - centerX - viewportX) / (Math.pow(2, zoomLevel) * TILE_SIZE);

        return new double[]{lat, lon};
    }

    private Point gpsToPixel(double lat, double lon) {
        // Convert GPS coordinates to pixel coordinates
        int centerX = mapPanel.getWidth() / 2;
        int centerY = mapPanel.getHeight() / 2;

        int x = centerX + (int) ((lon - centerLon) * Math.pow(2, zoomLevel) * TILE_SIZE) + viewportX;
        int y = centerY + (int) ((lat - centerLat) * Math.pow(2, zoomLevel) * TILE_SIZE) + viewportY;

        return new Point(x, y);
    }

    private void generateFlightPath() {
        flightPath.clear();
        if (waypoints.isEmpty()) {
            return;
        }

        // Add all waypoints to the flight path
        flightPath.addAll(waypoints);

        // If not looping, return to the starting point
        if (!loopPath && waypoints.size() > 1) {
            flightPath.add(waypoints.get(0));
        }
    }

    private void exportCoordinates() {
        String method = (String) exportMethodCombo.getSelectedItem();
        StringBuilder sb = new StringBuilder();

        // Create header with timestamp
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        String timestamp = sdf.format(new Date());
        sb.append("Drone Flight Path - Generated on ").append(timestamp).append("\n\n");

        // Add waypoints
        sb.append("WAYPOINTS:\n");
        for (int i = 0; i < waypoints.size(); i++) {
            Waypoint wp = waypoints.get(i);
            sb.append(i + 1).append(". Lat: ").append(String.format("%.6f", wp.lat))
                    .append(", Lon: ").append(String.format("%.6f", wp.lon))
                    .append(", Alt: ").append(wp.alt).append("m\n");
        }

        // Add flight path
        sb.append("\nFLIGHT PATH:\n");
        for (int i = 0; i < flightPath.size(); i++) {
            Waypoint wp = flightPath.get(i);
            sb.append(i + 1).append(". Lat: ").append(String.format("%.6f", wp.lat))
                    .append(", Lon: ").append(String.format("%.6f", wp.lon))
                    .append(", Alt: ").append(wp.alt).append("m\n");
        }

        // Handle different export methods
        switch (method) {
            case "Display Only":
                JTextArea textArea = new JTextArea(sb.toString(), 20, 50);
                JScrollPane scrollPane = new JScrollPane(textArea);
                textArea.setEditable(false);
                JOptionPane.showMessageDialog(this, scrollPane, "Flight Path Coordinates",
                        JOptionPane.INFORMATION_MESSAGE);
                logActivity("Coordinates displayed in dialog");
                break;

            case "Save to File":
                JFileChooser fileChooser = new JFileChooser();
                fileChooser.setDialogTitle("Save Flight Path");
                if (fileChooser.showSaveDialog(this) == JFileChooser.APPROVE_OPTION) {
                    File file = fileChooser.getSelectedFile();
                    try (FileWriter writer = new FileWriter(file)) {
                        writer.write(sb.toString());
                        logActivity("Coordinates saved to file: " + file.getName());
                        JOptionPane.showMessageDialog(this, "Coordinates saved successfully!",
                                "Success", JOptionPane.INFORMATION_MESSAGE);
                    } catch (IOException e) {
                        logActivity("Error saving file: " + e.getMessage());
                        JOptionPane.showMessageDialog(this, "Error saving file: " + e.getMessage(),
                                "Error", JOptionPane.ERROR_MESSAGE);
                    }
                }
                break;

            case "USB Transfer":
                logActivity("USB transfer simulation - coordinates ready for transfer");
                JOptionPane.showMessageDialog(this,
                        "Connect USB device to transfer coordinates", "USB Transfer",
                        JOptionPane.INFORMATION_MESSAGE);
                break;

            case "GPS Sync":
                logActivity("GPS synchronization simulation - coordinates synced with GPS device");
                JOptionPane.showMessageDialog(this,
                        "Coordinates synchronized with GPS device", "GPS Sync",
                        JOptionPane.INFORMATION_MESSAGE);
                break;

            case "Memory Card":
                logActivity("Memory card export simulation - coordinates saved to memory card");
                JOptionPane.showMessageDialog(this,
                        "Coordinates saved to memory card", "Memory Card",
                        JOptionPane.INFORMATION_MESSAGE);
                break;

            case "Drone Firmware":
                generateFirmwareCode();
                logActivity("Drone firmware code generated");
                break;
        }
    }

    private void generateFirmwareCode() {
        StringBuilder code = new StringBuilder();
        code.append("// Drone Flight Path Firmware Code\n");
        code.append("// Generated on ").append(new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date())).append("\n\n");
        code.append("#include <DroneNavigation.h>\n\n");
        code.append("Waypoint flightPath[] = {\n");

        for (Waypoint wp : flightPath) {
            code.append("  {").append(wp.lat).append("f, ").append(wp.lon).append("f, ").append(wp.alt).append("},\n");
        }

        code.append("};\n\n");
        code.append("void setup() {\n");
        code.append("  Drone.init();\n");
        code.append("  Drone.setFlightPath(flightPath, ").append(flightPath.size()).append(");\n");
        code.append("  Drone.setReturnToHome(").append(!loopPath).append(");\n");
        code.append("}\n\n");
        code.append("void loop() {\n");
        code.append("  Drone.flyPath();\n");
        code.append("}\n");

        // Show the code in a dialog
        JTextArea codeArea = new JTextArea(code.toString(), 20, 60);
        codeArea.setEditable(false);
        codeArea.setFont(new Font("Monospaced", Font.PLAIN, 12));
        JScrollPane scrollPane = new JScrollPane(codeArea);
        JOptionPane.showMessageDialog(this, scrollPane, "Drone Firmware Code",
                JOptionPane.INFORMATION_MESSAGE);
    }

    private void logActivity(String message) {
        String timestamp = new SimpleDateFormat("HH:mm:ss").format(new Date());
        activityLog.add(timestamp + " - " + message);
        updateLogDisplay();
    }

    private void updateLogDisplay() {
        StringBuilder sb = new StringBuilder();
        for (String entry : activityLog) {
            sb.append(entry).append("\n");
        }
        logArea.setText(sb.toString());
        logArea.setCaretPosition(logArea.getDocument().getLength());
    }

    private void showFirmwareDialog() {
        if (firmwareDialog == null) {
            firmwareDialog = new JDialog(this, "Drone Firmware Code", false);
            firmwareDialog.setSize(600, 500);
            firmwareDialog.setLayout(new BorderLayout());

            firmwareCodeArea = new JTextArea();
            firmwareCodeArea.setFont(new Font("Monospaced", Font.PLAIN, 12));
            JScrollPane scrollPane = new JScrollPane(firmwareCodeArea);
            firmwareDialog.add(scrollPane, BorderLayout.CENTER);

            JPanel buttonPanel = new JPanel();
            JButton closeButton = new JButton("Close");
            JButton copyButton = new JButton("Copy to Clipboard");
            JButton saveButton = new JButton("Save to File");

            closeButton.addActionListener(e -> firmwareDialog.setVisible(false));
            copyButton.addActionListener(e -> {
                firmwareCodeArea.selectAll();
                firmwareCodeArea.copy();
                logActivity("Firmware code copied to clipboard");
            });
            saveButton.addActionListener(e -> {
                JFileChooser fileChooser = new JFileChooser();
                fileChooser.setDialogTitle("Save Firmware Code");
                if (fileChooser.showSaveDialog(firmwareDialog) == JFileChooser.APPROVE_OPTION) {
                    File file = fileChooser.getSelectedFile();
                    try (FileWriter writer = new FileWriter(file)) {
                        writer.write(firmwareCodeArea.getText());
                        logActivity("Firmware code saved to file: " + file.getName());
                        JOptionPane.showMessageDialog(firmwareDialog, "Code saved successfully!",
                                "Success", JOptionPane.INFORMATION_MESSAGE);
                    } catch (IOException ex) {
                        logActivity("Error saving firmware code: " + ex.getMessage());
                        JOptionPane.showMessageDialog(firmwareDialog, "Error saving file: " + ex.getMessage(),
                                "Error", JOptionPane.ERROR_MESSAGE);
                    }
                }
            });

            buttonPanel.add(copyButton);
            buttonPanel.add(saveButton);
            buttonPanel.add(closeButton);
            firmwareDialog.add(buttonPanel, BorderLayout.SOUTH);
        }

        // Generate the code
        generateFirmwareCodeForDialog();
        firmwareDialog.setLocationRelativeTo(this);
        firmwareDialog.setVisible(true);
    }

    private void generateFirmwareCodeForDialog() {
        StringBuilder code = new StringBuilder();
        code.append("// Drone Flight Path Firmware Code\n");
        code.append("// Generated on ").append(new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date())).append("\n\n");
        code.append("#include <DroneNavigation.h>\n\n");
        code.append("// Waypoint structure definition\n");
        code.append("typedef struct {\n");
        code.append("    float latitude;\n");
        code.append("    float longitude;\n");
        code.append("    int altitude;\n");
        code.append("} Waypoint;\n\n");
        code.append("// Flight path waypoints\n");
        code.append("Waypoint flightPath[] = {\n");

        if (flightPath.isEmpty()) {
            code.append("  // No waypoints defined yet\n");
        } else {
            for (Waypoint wp : flightPath) {
                code.append("  {").append(String.format("%.6f", wp.lat)).append("f, ")
                        .append(String.format("%.6f", wp.lon)).append("f, ")
                        .append(wp.alt).append("},\n");
            }
        }

        code.append("};\n\n");
        code.append("void setup() {\n");
        code.append("  // Initialize drone systems\n");
        code.append("  DroneNavigation_init();\n");
        code.append("  \n");
        code.append("  // Set flight path parameters\n");
        code.append("  DroneNavigation_setFlightPath(flightPath, ").append(flightPath.size()).append(");\n");
        code.append("  DroneNavigation_setReturnToHome(").append(!loopPath).append(");\n");
        code.append("  \n");
        code.append("  // Calibrate sensors\n");
        code.append("  DroneNavigation_calibrateSensors();\n");
        code.append("}\n\n");
        code.append("void loop() {\n");
        code.append("  // Execute flight path\n");
        code.append("  if (DroneNavigation_isReady()) {\n");
        code.append("    DroneNavigation_flyPath();\n");
        code.append("  }\n");
        code.append("  \n");
        code.append("  // Monitor systems\n");
        code.append("  DroneNavigation_monitorSystems();\n");
        code.append("}\n");

        firmwareCodeArea.setText(code.toString());
    }

    private void showDownloadMapDialog() {
        JDialog dialog = new JDialog(this, "Download Map Area", true);
        dialog.setSize(400, 300);
        dialog.setLayout(new BorderLayout());

        JPanel contentPanel = new JPanel(new GridLayout(5, 2, 5, 5));
        contentPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        // Zoom level selection
        contentPanel.add(new JLabel("Zoom Level:"));
        JComboBox<Integer> zoomCombo = new JComboBox<>();
        for (int i = 1; i <= 19; i++) {
            zoomCombo.addItem(i);
        }
        zoomCombo.setSelectedItem(zoomLevel);
        contentPanel.add(zoomCombo);

        // Area size selection
        contentPanel.add(new JLabel("Area Size (tiles):"));
        JComboBox<String> sizeCombo = new JComboBox<>(new String[]{"3x3", "5x5", "7x7", "9x9"});
        sizeCombo.setSelectedIndex(1);
        contentPanel.add(sizeCombo);

        // Center coordinates
        contentPanel.add(new JLabel("Center Latitude:"));
        JTextField latField = new JTextField(String.valueOf(centerLat));
        contentPanel.add(latField);

        contentPanel.add(new JLabel("Center Longitude:"));
        JTextField lonField = new JTextField(String.valueOf(centerLon));
        contentPanel.add(lonField);

        dialog.add(contentPanel, BorderLayout.CENTER);

        JPanel buttonPanel = new JPanel();
        JButton downloadButton = new JButton("Download");
        JButton cancelButton = new JButton("Cancel");

        downloadButton.addActionListener(e -> {
            try {
                int selectedZoom = (Integer) zoomCombo.getSelectedItem();
                String sizeStr = (String) sizeCombo.getSelectedItem();
                int size = Integer.parseInt(sizeStr.substring(0, 1));
                double centerLat = Double.parseDouble(latField.getText());
                double centerLon = Double.parseDouble(lonField.getText());

                downloadMapArea(selectedZoom, centerLat, centerLon, size);
                dialog.dispose();
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(dialog, "Please enter valid coordinates",
                        "Error", JOptionPane.ERROR_MESSAGE);
            }
        });

        cancelButton.addActionListener(e -> dialog.dispose());

        buttonPanel.add(downloadButton);
        buttonPanel.add(cancelButton);
        dialog.add(buttonPanel, BorderLayout.SOUTH);

        dialog.setLocationRelativeTo(this);
        dialog.setVisible(true);
    }

    private void downloadMapArea(int zoom, double centerLat, double centerLon, int size) {
        logActivity("Starting map download for zoom level " + zoom + ", size " + size + "x" + size);

        // Create directory for this zoom level
        File zoomDir = new File(offlineMapDir, "z" + zoom);
        if (!zoomDir.exists()) {
            zoomDir.mkdirs();
        }

        // Calculate tile coordinates for the center
        int tileX = (int) Math.floor((centerLon + 180) / 360 * (1 << zoom));
        int tileY = (int) Math.floor((1 - Math.log(Math.tan(Math.toRadians(centerLat)) + 1 / Math.cos(Math.toRadians(centerLat))) / Math.PI) / 2 * (1 << zoom));

        int startX = tileX - size / 2;
        int startY = tileY - size / 2;
        int endX = tileX + size / 2;
        int endY = tileY + size / 2;

        int totalTiles = (endX - startX + 1) * (endY - startY + 1);
        int downloaded = 0;

        for (int x = startX; x <= endX; x++) {
            for (int y = startY; y <= endY; y++) {
                String quadKey = tileXYToQuadKey(x, y, zoom);
                String urlStr = BING_MAPS_URL.replace("{quadkey}", quadKey);

                if (bingMapsKey != null && !bingMapsKey.isEmpty()) {
                    urlStr += "&key=" + bingMapsKey;
                }

                try {
                    URL url = new URL(urlStr);
                    HttpURLConnection connection = (HttpURLConnection) url.openConnection();
                    connection.setRequestMethod("GET");

                    if (connection.getResponseCode() == HttpURLConnection.HTTP_OK) {
                        String filename = "tile_" + x + "_" + y + ".jpeg";
                        File outputFile = new File(zoomDir, filename);

                        try (InputStream in = connection.getInputStream();
                             OutputStream out = Files.newOutputStream(outputFile.toPath())) {
                            byte[] buffer = new byte[4096];
                            int bytesRead;
                            while ((bytesRead = in.read(buffer)) != -1) {
                                out.write(buffer, 0, bytesRead);
                            }
                        }

                        downloaded++;
                        logActivity("Downloaded tile " + downloaded + "/" + totalTiles + " (" + x + "," + y + ")");
                    }
                } catch (Exception e) {
                    logActivity("Error downloading tile (" + x + "," + y + "): " + e.getMessage());
                }
            }
        }

        logActivity("Map download completed. Downloaded " + downloaded + " of " + totalTiles + " tiles.");
        JOptionPane.showMessageDialog(this, "Map download completed!\nDownloaded " + downloaded + " of " + totalTiles + " tiles.",
                "Download Complete", JOptionPane.INFORMATION_MESSAGE);
    }

    private String tileXYToQuadKey(int tileX, int tileY, int levelOfDetail) {
        StringBuilder quadKey = new StringBuilder();
        for (int i = levelOfDetail; i > 0; i--) {
            char digit = '0';
            int mask = 1 << (i - 1);
            if ((tileX & mask) != 0) {
                digit++;
            }
            if ((tileY & mask) != 0) {
                digit += 2;
            }
            quadKey.append(digit);
        }
        return quadKey.toString();
    }

    // Menu action methods
    private void saveProject() {
        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setDialogTitle("Save Project");
        if (fileChooser.showSaveDialog(this) == JFileChooser.APPROVE_OPTION) {
            File file = fileChooser.getSelectedFile();
            try (FileWriter writer = new FileWriter(file)) {
                // Simple project format: waypoints only for this example
                for (Waypoint wp : waypoints) {
                    writer.write(wp.lat + "," + wp.lon + "," + wp.alt + "\n");
                }
                logActivity("Project saved to: " + file.getName());
                JOptionPane.showMessageDialog(this, "Project saved successfully!",
                        "Success", JOptionPane.INFORMATION_MESSAGE);
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
                for (String line : lines) {
                    String[] parts = line.split(",");
                    if (parts.length == 3) {
                        double lat = Double.parseDouble(parts[0]);
                        double lon = Double.parseDouble(parts[1]);
                        int alt = Integer.parseInt(parts[2]);
                        waypoints.add(new Waypoint(lat, lon, alt));
                    }
                }
                logActivity("Project loaded from: " + file.getName() + " (" + waypoints.size() + " waypoints)");
                mapPanel.repaint();
                JOptionPane.showMessageDialog(this, "Project loaded successfully!",
                        "Success", JOptionPane.INFORMATION_MESSAGE);
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
            Waypoint removed = waypoints.remove(waypoints.size() - 1);
            logActivity("Undo: Removed waypoint at Lat " + String.format("%.6f", removed.lat) +
                    ", Lon " + String.format("%.6f", removed.lon));
            mapPanel.repaint();
        } else {
            logActivity("Undo: No waypoints to remove");
        }
    }

    private void redoLastAction() {
        logActivity("Redo: Functionality not implemented in this version");
        JOptionPane.showMessageDialog(this, "Redo functionality not implemented in this version",
                "Info", JOptionPane.INFORMATION_MESSAGE);
    }

    private void showPreferences() {
        JDialog dialog = new JDialog(this, "Preferences", true);
        dialog.setSize(400, 300);
        dialog.setLayout(new BorderLayout());

        JPanel contentPanel = new JPanel(new GridLayout(4, 2, 5, 5));
        contentPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        // Bing Maps Key
        contentPanel.add(new JLabel("Bing Maps Key:"));
        JTextField keyField = new JTextField(bingMapsKey);
        contentPanel.add(keyField);

        // Default Altitude
        contentPanel.add(new JLabel("Default Altitude (m):"));
        JTextField altField = new JTextField(String.valueOf(droneAltitude));
        contentPanel.add(altField);

        // GPS Simulation
        contentPanel.add(new JLabel("Simulate GPS:"));
        JCheckBox gpsCheckbox = new JCheckBox("", simulateGPS);
        contentPanel.add(gpsCheckbox);

        dialog.add(contentPanel, BorderLayout.CENTER);

        JPanel buttonPanel = new JPanel();
        JButton saveButton = new JButton("Save");
        JButton cancelButton = new JButton("Cancel");

        saveButton.addActionListener(e -> {
            bingMapsKey = keyField.getText();
            saveBingMapsKey();

            try {
                int alt = Integer.parseInt(altField.getText());
                if (alt >= 300) {
                    droneAltitude = alt;
                    altitudeField.setText(String.valueOf(alt));
                } else {
                    JOptionPane.showMessageDialog(dialog, "Altitude must be at least 300m",
                            "Error", JOptionPane.ERROR_MESSAGE);
                    return;
                }
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(dialog, "Please enter a valid number for altitude",
                        "Error", JOptionPane.ERROR_MESSAGE);
                return;
            }

            simulateGPS = gpsCheckbox.isSelected();
            logActivity("Preferences saved");
            dialog.dispose();
        });

        cancelButton.addActionListener(e -> dialog.dispose());

        buttonPanel.add(saveButton);
        buttonPanel.add(cancelButton);
        dialog.add(buttonPanel, BorderLayout.SOUTH);

        dialog.setLocationRelativeTo(this);
        dialog.setVisible(true);
    }

    private void refreshMap() {
        logActivity("Map refreshed");
        mapPanel.repaint();
    }

    private void clearAllData() {
        int result = JOptionPane.showConfirmDialog(this,
                "Are you sure you want to clear all data? This cannot be undone.",
                "Confirm Clear All", JOptionPane.YES_NO_OPTION);
        if (result == JOptionPane.YES_OPTION) {
            waypoints.clear();
            flightPath.clear();
            activityLog.clear();
            updateLogDisplay();
            logActivity("All data cleared");
            mapPanel.repaint();
        }
    }

    private void exportAllData() {
        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setDialogTitle("Export All Data");
        if (fileChooser.showSaveDialog(this) == JFileChooser.APPROVE_OPTION) {
            File file = fileChooser.getSelectedFile();
            try (FileWriter writer = new FileWriter(file)) {
                // Write waypoints
                writer.write("WAYPOINTS:\n");
                for (int i = 0; i < waypoints.size(); i++) {
                    Waypoint wp = waypoints.get(i);
                    writer.write(i + 1 + ". Lat: " + String.format("%.6f", wp.lat) +
                            ", Lon: " + String.format("%.6f", wp.lon) +
                            ", Alt: " + wp.alt + "m\n");
                }

                // Write flight path
                writer.write("\nFLIGHT PATH:\n");
                for (int i = 0; i < flightPath.size(); i++) {
                    Waypoint wp = flightPath.get(i);
                    writer.write(i + 1 + ". Lat: " + String.format("%.6f", wp.lat) +
                            ", Lon: " + String.format("%.6f", wp.lon) +
                            ", Alt: " + wp.alt + "m\n");
                }

                // Write activity log
                writer.write("\nACTIVITY LOG:\n");
                for (String entry : activityLog) {
                    writer.write(entry + "\n");
                }

                logActivity("All data exported to: " + file.getName());
                JOptionPane.showMessageDialog(this, "All data exported successfully!",
                        "Success", JOptionPane.INFORMATION_MESSAGE);
            } catch (IOException e) {
                logActivity("Error exporting all data: " + e.getMessage());
                JOptionPane.showMessageDialog(this, "Error exporting data: " + e.getMessage(),
                        "Error", JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    private void setBingMapsKey() {
        String key = JOptionPane.showInputDialog(this,
                "Enter your Bing Maps Key:",
                bingMapsKey);
        if (key != null) {
            bingMapsKey = key.trim();
            saveBingMapsKey();
            logActivity("Bing Maps key updated");
        }
    }

    private void showAboutDialog() {
        String aboutMessage = "Drone Flight Path Generator\n" +
                "Version 1.0\n\n" +
                "A tool for planning and visualizing drone flight paths\n" +
                "with support for Bing Maps integration.\n\n" +
                "© 2023 Drone Flight Path Generator Team";
        JOptionPane.showMessageDialog(this, aboutMessage, "About", JOptionPane.INFORMATION_MESSAGE);
    }

    // Map panel for displaying the map and waypoints
    class MapPanel extends JPanel {
        public MapPanel() {
            setBackground(Color.LIGHT_GRAY);
            setPreferredSize(new Dimension(600, 500));
        }

        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);

            // Draw the map
            if (onlineMode) {
                drawOnlineMap(g);
            } else {
                drawOfflineMap(g);
            }

            // Draw waypoints and flight path
            drawWaypoints(g);
            drawFlightPath(g);

            // Draw current position
            drawCurrentPosition(g);
        }

        private void drawOnlineMap(Graphics g) {
            int width = getWidth();
            int height = getHeight();

            // Draw a simple grid as a placeholder for the map
            g.setColor(new Color(220, 230, 240));
            g.fillRect(0, 0, width, height);

            // Draw grid lines
            g.setColor(new Color(200, 210, 220));
            for (int x = 0; x < width; x += 20) {
                g.drawLine(x, 0, x, height);
            }
            for (int y = 0; y < height; y += 20) {
                g.drawLine(0, y, width, y);
            }

            // Draw a simple representation of the map
            g.setColor(new Color(100, 150, 200));
            g.drawString("Bing Maps Display (Online Mode)", 10, 20);
            g.drawString("Zoom Level: " + zoomLevel, 10, 40);
            g.drawString("Center: " + String.format("%.6f", centerLat) + ", " + 
                         String.format("%.6f", centerLon), 10, 60);
            
            // Draw some terrain features
            g.setColor(new Color(100, 180, 100));
            g.fillOval(width/4, height/4, width/2, height/2);
            
            g.setColor(new Color(100, 100, 200));
            g.fillOval(width/3, height/3, width/4, height/4);
        }

        private void drawOfflineMap(Graphics g) {
            int width = getWidth();
            int height = getHeight();

            // Draw a simple grid as a placeholder for the offline map
            g.setColor(new Color(240, 240, 220));
            g.fillRect(0, 0, width, height);

            // Draw grid lines
            g.setColor(new Color(220, 220, 200));
            for (int x = 0; x < width; x += 20) {
                g.drawLine(x, 0, x, height);
            }
            for (int y = 0; y < height; y += 20) {
                g.drawLine(0, y, width, y);
            }

            // Draw a simple representation of the map
            g.setColor(new Color(150, 100, 50));
            g.drawString("Offline Map Display", 10, 20);
            g.drawString("Zoom Level: " + zoomLevel, 10, 40);
            g.drawString("Center: " + String.format("%.6f", centerLat) + ", " + 
                         String.format("%.6f", centerLon), 10, 60);
            
            // Draw some terrain features
            g.setColor(new Color(150, 120, 100));
            g.fillRect(width/4, height/4, width/2, height/2);
            
            g.setColor(new Color(150, 150, 100));
            g.fillRect(width/3, height/3, width/4, height/4);
        }

        private void drawWaypoints(Graphics g) {
            for (Waypoint wp : waypoints) {
                Point p = gpsToPixel(wp.lat, wp.lon);
                int x = p.x;
                int y = p.y;

                // Draw waypoint circle
                g.setColor(new Color(0, 100, 0));
                g.fillOval(x - 5, y - 5, 10, 10);

                // Draw waypoint outline
                g.setColor(Color.WHITE);
                g.drawOval(x - 5, y - 5, 10, 10);

                // Draw altitude text
                g.setColor(Color.BLACK);
                g.drawString(wp.alt + "m", x + 8, y - 8);
            }
        }

        private void drawFlightPath(Graphics g) {
            if (flightPath.size() < 2) {
                return;
            }

            g.setColor(new Color(0, 0, 200, 150));
            ((Graphics2D) g).setStroke(new BasicStroke(2.0f));

            for (int i = 0; i < flightPath.size() - 1; i++) {
                Waypoint wp1 = flightPath.get(i);
                Waypoint wp2 = flightPath.get(i + 1);

                Point p1 = gpsToPixel(wp1.lat, wp1.lon);
                Point p2 = gpsToPixel(wp2.lat, wp2.lon);

                g.drawLine(p1.x, p1.y, p2.x, p2.y);
            }

            // Reset stroke
            ((Graphics2D) g).setStroke(new BasicStroke(1.0f));
        }

        private void drawCurrentPosition(Graphics g) {
            Point p = gpsToPixel(currentLatitude, currentLongitude);
            int x = p.x;
            int y = p.y;

            // Draw drone position
            g.setColor(Color.RED);
            g.fillOval(x - 6, y - 6, 12, 12);

            // Draw drone outline
            g.setColor(Color.WHITE);
            g.drawOval(x - 6, y - 6, 12, 12);

            // Draw direction indicator
            int dx = (int) (10 * Math.cos(Math.toRadians(compassPanel.getHeading())));
            int dy = (int) (10 * Math.sin(Math.toRadians(compassPanel.getHeading())));
            g.setColor(Color.YELLOW);
            g.drawLine(x, y, x + dx, y + dy);
        }
    }

    // Compass panel for displaying heading
    class CompassPanel extends JPanel {
        private int heading = 0;

        public CompassPanel() {
            setPreferredSize(new Dimension(300, 300));
            setBorder(BorderFactory.createTitledBorder("Drone Compass"));

            // Simulate compass changes
            Timer compassTimer = new Timer();
            compassTimer.scheduleAtFixedRate(new TimerTask() {
                @Override
                public void run() {
                    heading = (heading + 1) % 360;
                    repaint();
                }
            }, 1000, 100);
        }

        public int getHeading() {
            return heading;
        }

        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);

            int centerX = getWidth() / 2;
            int centerY = getHeight() / 2;
            int radius = Math.min(centerX, centerY) - 20;

            // Draw compass circle
            g.setColor(Color.WHITE);
            g.fillOval(centerX - radius, centerY - radius, radius * 2, radius * 2);

            g.setColor(Color.BLACK);
            g.drawOval(centerX - radius, centerY - radius, radius * 2, radius * 2);

            // Draw compass directions
            g.drawString("N", centerX - 5, centerY - radius + 15);
            g.drawString("S", centerX - 5, centerY + radius - 5);
            g.drawString("E", centerX + radius - 15, centerY + 5);
            g.drawString("W", centerX - radius + 5, centerY + 5);

            // Draw heading line
            int x2 = centerX + (int) (radius * 0.8 * Math.sin(Math.toRadians(heading)));
            int y2 = centerY - (int) (radius * 0.8 * Math.cos(Math.toRadians(heading)));

            g.setColor(Color.RED);
            ((Graphics2D) g).setStroke(new BasicStroke(3.0f));
            g.drawLine(centerX, centerY, x2, y2);

            // Draw current heading text
            g.setColor(Color.BLACK);
            g.drawString("Heading: " + heading + "°", centerX - 30, centerY + radius + 20);
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
            } catch (Exception e) {
                e.printStackTrace();
            }
            new DroneFlightPathGenerator();
        });
    }
}