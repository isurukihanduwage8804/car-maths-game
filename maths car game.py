import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="IsuruSoft Fast Racer", layout="centered")

st.markdown("""
    <h1 style='text-align: center; color: #ff4b4b; font-family: sans-serif; margin-bottom: 0;'>🏎️ IsuruSoft Fast Racer</h1>
    <p style='text-align: center; color: #cbd5e1; font-family: sans-serif;'>පාරේ දිග අඩු කළා - දැන් වේගයෙන් ප්‍රශ්න එනවා!</p>
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

        // පාරේ දිග (Height) සැලකිය යුතු ලෙස අඩු කළා
        canvas.width = 320; 
        canvas.height = 450; 

        let carX = 135;
        const carY = 340; // කාර් එකේ පිහිටීමත් උඩට ගත්තා
        let score = 0;
        let obsY = -50;
        let speed = 5; 
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
            let n1 = Math.floor(Math.random() * 12) + 1;
            let n2 = Math.floor(Math.random() * 12) + 1;
            correctAns = n1 + n2;
            question = n1 + " + " + n2 + " = ?";
            let wrongAns = correctAns + (Math.random() < 0.5 ? 2 : -2);
            options = [correctAns, wrongAns].sort(() => Math.random() - 0.5);
        }

        generateQuestion();

        function update() {
            if (leftPressed && carX > 5) carX -= 8;
            if (rightPressed && carX < 265) carX += 8;

            obsY += speed;
            if (obsY > canvas.height) {
                obsY = -40;
                generateQuestion();
                speed += 0.03;
            }

            if (obsY > carY - 25 && obsY < carY + 60) {
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

        function drawCar(x, y) {
            ctx.fillStyle = "#ff4b4b"; // Body
            ctx.fillRect(x, y, 50, 80);
            ctx.fillStyle = "#000"; // Wheels
            ctx.fillRect(x-4, y+10, 6, 15); ctx.fillRect(x+48, y+10, 6, 15);
            ctx.fillRect(x-4, y+55, 6, 15); ctx.fillRect(x+48, y+55, 6, 15);
            ctx.fillStyle = "#94a3b8"; // Window
            ctx.fillRect(x+10, y+15, 30, 15);
            ctx.fillStyle = "#fbbf24"; // Lights
            ctx.fillRect(x+5, y+2, 10, 4); ctx.fillRect(x+35, y+2, 10, 4);
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // Lane lines
            ctx.strokeStyle = "rgba(255,255,255,0.2)";
            ctx.setLineDash([15, 15]);
            ctx.beginPath(); ctx.moveTo(160, 0); ctx.lineTo(160, 450); ctx.stroke();

            drawCar(carX, carY);

            ctx.fillStyle = "#facc15";
            ctx.font = "bold 22px sans-serif";
            ctx.textAlign = "center";
            ctx.fillText(question, 160, 50);

            ctx.fillStyle = "white";
            ctx.font = "16px sans-serif";
            ctx.fillText("Score: " + score, 50, 25);

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
