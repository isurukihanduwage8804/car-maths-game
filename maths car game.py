import streamlit as st
import streamlit.components.v1 as components

# පිටුවේ සැකසුම්
st.set_page_config(page_title="IsuruSoft Math Car Race", layout="centered")

st.markdown("""
    <h1 style='text-align: center; color: #ff4b4b; font-family: sans-serif;'>🏎️ IsuruSoft Math Car Race</h1>
    <p style='text-align: center; color: #cbd5e1; font-family: sans-serif;'>Keyboard එකේ <b>Left/Right Arrows</b> පාවිච්චි කර නිවැරදි පිළිතුර තෝරන්න!</p>
""", unsafe_allow_html=True)

# HTML/JavaScript කොටස
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; background: #0f172a; }
        canvas { display: block; background: #1e293b; margin: auto; border: 5px solid #334155; border-radius: 15px; }
    </style>
</head>
<body>
    <canvas id="gameCanvas"></canvas>
    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        canvas.width = 400;
        canvas.height = 600;

        let carX = 175;
        const carY = 480;
        let score = 0;
        let obsY = -100;
        let speed = 4;
        let question = "";
        let options = [];
        let correctAns = 0;
        
        // යතුරු පුවරුව පාලනය (Keyboard control)
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
            let wrongAns = correctAns + (Math.random() < 0.5 ? 2 : -1);
            options = [correctAns, wrongAns].sort(() => Math.random() - 0.5);
        }

        generateQuestion();

        function update() {
            // කාර් එක එහා මෙහා කිරීම
            if (leftPressed && carX > 10) carX -= 7;
            if (rightPressed && carX < 340) carX += 7;

            // බාධක පල්ලෙහාට ඒම
            obsY += speed;
            if (obsY > 600) {
                obsY = -100;
                generateQuestion();
                speed += 0.1;
            }

            // හැප්පීම පරීක්ෂා කිරීම (Collision)
            if (obsY > carY - 30 && obsY < carY + 80) {
                let hitSide = (carX < 150) ? 0 : (carX > 200 ? 1 : -1);
                if (hitSide !== -1) {
                    if (options[hitSide] === correctAns) {
                        score += 10;
                    } else {
                        score = Math.max(0, score - 5);
                    }
                    obsY = 650; // ඊළඟ ප්‍රශ්නයට යෑමට
                }
            }
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // පාරේ මැද ඉරි
            ctx.strokeStyle = "#475569";
            ctx.setLineDash([30, 30]);
            ctx.lineWidth = 4;
            ctx.beginPath();
            ctx.moveTo(200, 0); ctx.lineTo(200, 600);
            ctx.stroke();

            // කාර් එක (IsuruSoft Red)
            ctx.fillStyle = "#ff4b4b";
            ctx.shadowBlur = 10; ctx.shadowColor = "black";
            ctx.fillRect(carX, carY, 50, 90);
            ctx.shadowBlur = 0; 
            
            // කාර් එකේ වීදුරු සහ ලාම්පු
            ctx.fillStyle = "#94a3b8";
            ctx.fillRect(carX+5, carY+15, 40, 25); // වීදුරුව
            ctx.fillStyle = "#fbbf24";
            ctx.fillRect(carX+5, carY, 10, 5); // ලාම්පු
            ctx.fillRect(carX+35, carY, 10, 5);

            // ප්‍රශ්නය පෙන්වන කොටස
            ctx.fillStyle = "#facc15";
            ctx.font = "bold 28px sans-serif";
            ctx.textAlign = "center";
            ctx.fillText(question, 200, 60);

            // ලකුණු පෙන්වන කොටස
            ctx.fillStyle = "white";
            ctx.font = "20px sans-serif";
            ctx.fillText("Score: " + score, 60, 40);

            // පිළිතුරු බෝල (Answers)
            ctx.fillStyle = "#38bdf8"; // ලස්සන නිල් පාටක්
            ctx.beginPath(); ctx.arc(100, obsY, 35, 0, Math.PI * 2); ctx.fill();
            ctx.beginPath(); ctx.arc(300, obsY, 35, 0, Math.PI * 2); ctx.fill();
            
            ctx.fillStyle = "white";
            ctx.font = "bold 22px sans-serif";
            ctx.fillText(options[0], 100, obsY + 8);
            ctx.fillText(options[1], 300, obsY + 8);

            update();
            requestAnimationFrame(draw);
        }

        draw();
    </script>
</body>
</html>
"""

components.html(game_html, height=650)

st.sidebar.title("🎮 පාලනය (Controls)")
st.sidebar.info("ඔබේ පරිගණකයේ Keyboard එකේ ⬅️ සහ ➡️ ඊතල යතුරු (Arrow Keys) භාවිතයෙන් කාර් එක පාලනය කරන්න.")
