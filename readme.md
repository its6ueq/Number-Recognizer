# Handwritten Math Expression Recognizer

[![Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://www.kaggle.com/code/banghai/number-recognition)
[![GitHub](https://img.shields.io/badge/GitHub-View%20on%20GitHub-blue?logo=github)](https://github.com/its6ueq/Number-Recognizer)

This project implements a handwritten mathematical expression recognizer capable of identifying digits (0-9) and basic mathematical operators (+, -, ×, ÷) from images and calculating the result. The system achieves an accuracy of **97.96%** on the test set. It uses a **Support Vector Machine (SVM)** model, combined with **Depth-First Search (DFS)** and **K-Means clustering** for image processing and character recognition. The user interface is built with **React**, and the backend logic and API are implemented using **FastAPI**.

## Key Features & Methodology

The system employs a multi-stage approach to recognize and calculate handwritten mathematical expressions:

1.  **Image Preprocessing:**
    *   **Input Acquisition:** The user draws the expression on a canvas in the React frontend. This drawing is converted to a base64 encoded image.
    *   **Segmentation (DFS):** Depth-First Search (DFS) is applied to the image to identify connected components. Each connected component represents a separate digit or operator. This separates the "2", "+", "3", etc., in an expression like "2 + 3".
    *   **Special Handling for Division (:):** The division symbol (":") presents a unique challenge because it consists of two separate dots. K-Means clustering is used to group these dots into a single logical character. The algorithm identifies two clusters, representing the two dots, and combines them.
    *   **Standardization:** Each segmented character (digit or operator) undergoes further preprocessing:
        *   Cropping and Squaring: The character is tightly cropped and resized to a square aspect ratio.
        *   Blurring: A blurring filter (e.g., Gaussian blur) is applied to reduce noise and improve generalization.
        *   Resizing: The character is resized to a standard 28x28 pixel resolution.
        *   Alpha Channel Extraction: The alpha channel (transparency) of the image is extracted and used as the feature vector.

2.  **Character Recognition (SVM):**
    *   A **Support Vector Machine (SVM)** model is the core of the recognition system. This model is trained on the MNIST dataset for digits (0-9) and a custom dataset for the mathematical operators (+, -, ×, ÷).
    *   **Training:** The SVM model is trained to find the optimal decision boundary that separates the different classes (digits and operators) in the feature space.
    *   **Prediction:** The preprocessed image of each character is input to the SVM, outputting the result of the prediction of operator or digit.
    *   **Accuracy:** The model achieved an accuracy of **97.96%** on the test set.

3.  **Expression Parsing and Calculation:**
    *   **Character Ordering:** The segmented characters, now recognized, need to be put in the correct order. This is done by:
        *   Calculating the centroid (center of mass) of each character.
        *   Grouping characters into rows based on their vertical position.
        *   Ordering characters within each row from left to right based on their horizontal position.
    *   **Two-Pass Calculation:** The ordered sequence of digits and operators is then evaluated using a two-pass algorithm to handle operator precedence:
        *   **Pass 1 (Multiplication and Division):** The expression is scanned from left to right. Multiplication (×) and division (:) operations are performed immediately as they are encountered. Intermediate results and the positions of addition/subtraction operators are stored.
        *   **Pass 2 (Addition and Subtraction):** The expression is processed again, performing addition (+) and subtraction (-) operations based on the stored positions and intermediate results from the first pass.

4.  **Frontend and Backend:**
    *   **React Frontend:** Provides the user interface, including the drawing canvas and the display of the result.
    *   **FastAPI Backend:** Handles image processing, character recognition, calculation, and provides an API endpoint (`/upload`) for the frontend to communicate with. The frontend sends the base64 image data to this endpoint via a POST request.

## Data

*   **MNIST Dataset:** Used for training the digit recognition model.
*   **Custom Operator Dataset:** Images of +, -, ×, and ÷ symbols.

## Demo

The user draws an expression on a canvas:


![Example](/img/nr1.png)
![Example](/img/nr2.png)
![Example](/img/nr3.png)
