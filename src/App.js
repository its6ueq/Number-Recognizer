import React, { useRef, useState, useEffect } from "react";

const HandwritingApp = () => {
  const canvasRef = useRef(null);
  const contextRef = useRef(null);
  const [isDraw, setIsDraw] = useState(false);

  useEffect(() => {
    const canvas = canvasRef.current;
    canvas.width = 600;
    canvas.height = 600;

    const context = canvas.getContext("2d");
    context.lineCap = "round";
    context.strokeStyle = "black";
    context.lineWidth = 5;
    contextRef.current = context;
  }, []);

  const startDraw = (e) => {
    contextRef.current.beginPath();
    contextRef.current.moveTo(
      e.nativeEvent.offsetX, 
      e.nativeEvent.offsetY);
    setIsDraw(true);
  };

  const finishDraw = () => {
    contextRef.current.closePath();
    setIsDraw(false);
  };

  const draw = (e) => {
    if (!isDraw) return;
    contextRef.current.lineTo(      
      e.nativeEvent.offsetX, 
      e.nativeEvent.offsetY
    );
    contextRef.current.stroke();
  };

  const clearCanvas = () => {
    const canvas = canvasRef.current;
    const context = canvas.getContext("2d");
    context.clearRect(0, 0, canvas.width, canvas.height);
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
          top: "300px",           
          left: "700px",          
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
    </div>
  );
};

export default HandwritingApp;
