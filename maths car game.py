import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="IsuruSoft Taxi Racer", layout="centered")

st.markdown("""
    <h1 style='text-align: center; color: #facc15; font-family: sans-serif; margin-bottom: 0;'>🚕 IsuruSoft Taxi Racer</h1>
    <p style='text-align: center; color: #cbd5e1; font-family: sans-serif;'>ඔයා එවපු ටැක්සි කාර් එකත් සමඟ ගණිත ගැටලු විසඳමු!</p>
""", unsafe_allow_html=True)

game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; background: #0f172a; display: flex; justify-content: center; align-items: center; height: 100vh; }
        canvas { 
            display: block; 
            background: #1e293b; 
            border: 5px solid #475569; 
            box-shadow: 0 0 30px rgba(0,0,0,0.5);
        }
    </style>
</head>
<body>
    <canvas id="gameCanvas"></canvas>
    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        canvas.width = 320; 
        canvas.height = 450; 

        // ඔයා එවපු PNG කාර් රූපය ලෝඩ් කිරීම
        const carImg = new Image();
        carImg.src = "https://raw.githubusercontent.com/isurukihanduwage8804/isurusoft/main/car.png"; 

        let carX = 135;
        const carY = 340; 
        let score = 0;
        let obsY = -50;
        let speed = 2; // ඔයා ඉල්ලපු විදිහට වේගය අඩු කර ඇත
        let question = "";
        let options = [];
        let correctAns = 0;
        
        let leftPressed = false;
        let rightPressed = false;

        document.addEventListener("keydown", (e) => {
            if (e.key === "ArrowLeft") leftPressed = true;
            if (e.key === "ArrowRight") rightPressed = true;
        });

        document.addEventListener("keyup", (e) => {
            if (e.key === "ArrowLeft") leftPressed = false;
            if (e.key === "ArrowRight") rightPressed = false;
        });

        function generateQuestion() {
            let n1 = Math.floor(Math.random() * 10) + 1;
            let n2 = Math.floor(Math.random() * 10) + 1;
            correctAns = n1 + n2;
            question = n1 + " + " + n2 + " = ?";
            let wrongAns = correctAns + (Math.random() < 0.5 ? 2 : -2);
            options = [correctAns, wrongAns].sort(() => Math.random() - 0.5);
        }

        generateQuestion();

        function update() {
            if (leftPressed && carX > 5) carX -= 5;
            if (rightPressed && carX < 265) carX += 5;

            obsY += speed;
            if (obsY > canvas.height) {
                obsY = -40;
                generateQuestion();
                speed += 0.01; 
            }

            if (obsY > carY - 20 && obsY < carY + 80) {
                let hitSide = (carX < 130) ? 0 : (carX > 140 ? 1 : -1);
                if (hitSide !== -1) {
                    if (options[hitSide] === correctAns) {
                        score += 10;
                    } else {
                        score = Math.max(0, score - 5);
                    }
                    obsY = canvas.height + 50;
                }
            }
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // පාරේ ඉරි
            ctx.strokeStyle = "rgba(255,255,255,0.15)";
            ctx.setLineDash([15, 15]);
            ctx.beginPath(); ctx.moveTo(160, 0); ctx.lineTo(160, 450); ctx.stroke();

            // කාර් එක ඇඳීම (ටැක්සි කාර් එකේ රූපය)
            ctx.drawImage(carImg, carX, carY, 50, 95);

            // UI
            ctx.fillStyle = "#facc15";
            ctx.font = "bold 22px sans-serif";
            ctx.textAlign = "center";
            ctx.fillText(question, 160, 50);

            ctx.fillStyle = "white";
            ctx.font = "16px sans-serif";
            ctx.fillText("Score: " + score, 50, 25);

            // පිළිතුරු බෝල (Glowing Blue)
            ctx.fillStyle = "#38bdf8";
            ctx.beginPath(); ctx.arc(80, obsY, 28, 0, Math.PI * 2); ctx.fill();
            ctx.beginPath(); ctx.arc(240, obsY, 28, 0, Math.PI * 2); ctx.fill();

            ctx.fillStyle = "white";
            ctx.font = "bold 18px sans-serif";
            ctx.fillText(options[0], 80, obsY + 6);
            ctx.fillText(options[1], 240, obsY + 6);

            update();
            requestAnimationFrame(draw);
        }
        draw();
    </script>
</body>
</html>
"""

components.html(game_html, height=470)
