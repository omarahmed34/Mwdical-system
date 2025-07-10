<?php
header('Content-Type: application/json');

// Enable error reporting for debugging
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Configure CORS
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Check if it's a POST request
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed']);
    exit();
}

try {
    // Validate input directly from $_POST
    if (empty($_POST['symptoms'])) {
        throw new Exception('Symptoms description is required');
    }

    // Sanitize input
    $symptoms = filter_var($_POST['symptoms'], FILTER_SANITIZE_STRING);
    $age = isset($_POST['age']) ? filter_var($_POST['age'], FILTER_SANITIZE_NUMBER_INT) : null;
    $gender = isset($_POST['gender']) ? filter_var($_POST['gender'], FILTER_SANITIZE_STRING) : null;

    // Process the symptoms using NLP (example implementation)
    $diagnosis = analyzeSymptomsWithNLP($symptoms, $age, $gender);

    // Store the diagnosis results
    $diagnosisId = storeDiagnosisResults($diagnosis);

    // Return success response
    echo json_encode([
        'success' => true,
        'diagnosisId' => $diagnosisId,
        'message' => 'Diagnosis completed successfully'
    ]);

} catch (Exception $e) {
    http_response_code(400);
    echo json_encode([
        'error' => $e->getMessage()
    ]);
}

function analyzeSymptomsWithNLP($symptoms, $age, $gender) {
    // This is where you would implement your NLP analysis
    // For now, we'll return a mock response
    return [
        'conditions' => [
            [
                'name' => 'Common Cold',
                'probability' => 0.85,
                'description' => 'A viral infection of the upper respiratory tract',
                'recommendations' => [
                    'Rest and stay hydrated',
                    'Take over-the-counter cold medications',
                    'Monitor symptoms for worsening'
                ]
            ],
            [
                'name' => 'Seasonal Allergies',
                'probability' => 0.65,
                'description' => 'An allergic response to environmental triggers',
                'recommendations' => [
                    'Avoid known allergens',
                    'Consider antihistamines',
                    'Use air purifiers'
                ]
            ]
        ],
        'severity' => 'mild',
        'urgent' => false,
        'timestamp' => date('Y-m-d H:i:s')
    ];
}

function storeDiagnosisResults($diagnosis) {
    // In a real application, you would store this in a database
    // For now, we'll generate a unique ID
    $diagnosisId = uniqid('DIAG_');
    
    // Store in a temporary file (for demonstration purposes only)
    $filename = "diagnoses/{$diagnosisId}.json";
    file_put_contents($filename, json_encode($diagnosis));
    
    return $diagnosisId;
}
?>