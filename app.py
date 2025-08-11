import streamlit as st

st.set_page_config(page_title="Combat Diet & Training Planner", layout="centered")

st.title("Combat Diet & Training Planner (MVP)")

col1, col2 = st.columns(2)
sex = col1.selectbox("Sex", ["Male","Female"])
age = col1.number_input("Age", 16, 65, 19)
height_cm = col1.number_input("Height (cm)", 140.0, 220.0, 178.0, step=0.5)
weight_kg = col1.number_input("Weight (kg)", 45.0, 160.0, 84.5, step=0.1)
goal = col2.selectbox("Goal", ["Cut","Recomp","Slow Bulk"])
bjj_days = col2.slider("BJJ days/week", 0, 7, 4)
strength_days = col2.slider("Strength days/week", 0, 7, 4)
cardio_days = col2.slider("Cardio days/week", 0, 7, 1)

def bmr_msj(sex, w, h, a):
    return 10*w + 6.25*h - 5*a + (5 if sex=="Male" else -161)

def tdee(bmr, bjj, strn, cardio):
    mult = 1.2 + 0.10*strn + 0.07*bjj + 0.05*cardio
    return min(mult, 1.85) * bmr

def target_calories(tdee, goal):
    return round(tdee * (0.82 if goal=="Cut" else 0.98 if goal=="Recomp" else 1.10))

def macros(weight_kg, cals, goal):
    p = 2.2*weight_kg if goal=="Cut" else (1.8*weight_kg if goal=="Slow Bulk" else 2.0*weight_kg)
    f = (0.6 if goal=="Cut" else 0.7)*weight_kg
    p_kcal, f_kcal = 4*p, 9*f
    c = max(cals - p_kcal - f_kcal, 0)/4
    return round(p), round(c), round(f)

if st.button("Create Plan"):
    bmr = bmr_msj(sex, weight_kg, height_cm, age)
    tdee_val = tdee(bmr, bjj_days, strength_days, cardio_days)
    cals = target_calories(tdee_val, goal)
    p, c, f = macros(weight_kg, cals, goal)

    st.subheader("Daily Targets")
    st.write(f"**Calories:** {cals} kcal  |  **Protein:** {p} g  |  **Carbs:** {c} g  |  **Fat:** {f} g")
    st.caption(f"BMR: {round(bmr)} kcal  |  TDEE: {round(tdee_val)} kcal")

    st.subheader("Meal Skeleton (4 meals)")
    splits = [0.30,0.30,0.25,0.15]
    for i, s in enumerate(splits, start=1):
        st.write(f"**Meal {i}** — Protein {round(p*s)} g, Carbs {round(c*[0.20,0.35,0.30,0.15][i-1])} g, Fat {round(f*[0.30,0.25,0.25,0.20][i-1])} g")

    st.subheader("4-Day Training Split")
    st.markdown("""
**Day 1 – Upper Push:** Bench/DB Press 4×6–8, OHP 3×6–8, Incline DB 3×8–10, Dips 3×AMRAP, Laterals 4×12–15, Triceps 3×10–12  
**Day 2 – Lower (hinge+quad):** RDL 4×6–8, Back/Hack Squat 4×6–10, Split Squat 3×8–10, Ham Curl 3×10–12, Calves 4×12–15  
**Day 3 – Upper Pull + Arms:** Pull-ups 4×AMRAP, Row 4×6–10, Pulldown 3×10–12, Face Pull 3×15, Hammer Curl 3×10–12, Cable Curl 3×12–15  
**Day 4 – Athletic/Conditioning:** Trap Bar Jumps 4×3, KB Swings 4×12, Sled Push 6×30m, Core 10–12 min  
*BJJ on Days 1/3/4; load carbs ~90–120 min pre-roll and post-roll.*
    """)
    st.success("Done. You can now record a quick demo.")
