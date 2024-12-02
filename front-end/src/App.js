import "./App.css";
import axios from "axios";
import React, { useRef, useState, useEffect } from "react";

const HandwritingApp = () => {
  const canvasRef = useRef(null);
  const contextRef = useRef(null);
  const [isDraw, setIsDraw] = useState(false);
  const [output, setOutput] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const canvas = canvasRef.current;
    canvas.width = 600;
    canvas.height = 600;

    const context = canvas.getContext("2d");
    context.lineCap = "round";
    context.strokeStyle = "black";
    context.lineWidth = 10;
    contextRef.current = context;
  }, []);

  const startDraw = (e) => {
    contextRef.current.beginPath();
    contextRef.current.moveTo(e.nativeEvent.offsetX, e.nativeEvent.offsetY);
    setIsDraw(true);
  };

  const finishDraw = () => {
    contextRef.current.closePath();
    setIsDraw(false);
  };

  const draw = (e) => {
    if (!isDraw) return;
    contextRef.current.lineTo(e.nativeEvent.offsetX, e.nativeEvent.offsetY);
    contextRef.current.stroke();
  };

  const clearCanvas = () => {
    const canvas = canvasRef.current;
    const context = canvas.getContext("2d");
    context.clearRect(0, 0, canvas.width, canvas.height);
  };

  const sendImage = () => {
    setIsLoading(true);
    const canvas = canvasRef.current;
    const imageData = canvas.toDataURL("image/png");
    axios
      .post("/upload", { image: imageData })
      .then((res) => {
        setOutput(res.data);
        setIsLoading(false);
      })
      .catch((error) => {
        console.error("Error sending image:", error);
        setIsLoading(false);
      });
  };

  const handleSendAndClear = () => {
    sendImage();
    clearCanvas();
  };

  return (
    <div>
      <canvas
        ref={canvasRef}
        onMouseDown={startDraw}
        onMouseUp={finishDraw}
        onMouseMove={draw}
        onMouseLeave={finishDraw}
        onTouchStart={(e) => startDraw(e.touches[0])}
        onTouchEnd={finishDraw}
        onTouchMove={(e) => draw(e.touches[0])}
        style={{
          border: "2px solid #000",
          cursor: "crosshair",
        }}
      />

      <button
        onClick={clearCanvas}
        style={{
          position: "absolute",
          top: "100px",
          left: "1100px",
          zIndex: 10,
          padding: "15px 30px",
          fontSize: "20px",
          backgroundColor: "#007BFF",
          color: "#FFF",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
        }}
      >
        Clear
      </button>

      <button
        onClick={sendImage}
        style={{
          position: "absolute",
          top: "200px",
          left: "1100px",
          zIndex: 10,
          padding: "15px 30px",
          fontSize: "20px",
          backgroundColor: "#28a745",
          color: "#FFF",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
        }}
      >
        Send Image
      </button>

      <h3>
        {isLoading ? (
          <span>Đang xử lý...</span>
        ) : Array.isArray(output) || output.length > 0 ? (
          <span>Kết quả của phép tính là: {output}</span>
        ) : (
          <span>Hãy vẽ</span>
        )}
      </h3>
    </div>
  );
};

export default HandwritingApp;
