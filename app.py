import streamlit as st
from datetime import date

# ---------- Page Setup ----------
st.set_page_config(page_title="Combat Diet & Training Planner", page_icon="🥋", layout="centered")
import os
from PIL import Image

logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, width=120)
else:
    st.sidebar.write("")  # no crash if missing


# ---------- Header ----------
st.title("Combat Diet & Training Planner")
st.caption("Built by an aspiring MBZUAI student — blending medicine, BJJ, and AI for real-world sports performance.")

# ---------- Inputs ----------
with st.form("inputs"):
    col1, col2 = st.columns(2)
    sex = col1.selectbox("Sex", ["Male","Female"])
    age = col1.number_input("Age", 16, 65, 19)
    height_cm = col1.number_input("Height (cm)", 140.0, 220.0, 178.0, step=0.5)
    weight_kg = col1.number_input("Weight (kg)", 45.0, 160.0, 84.5, step=0.1)
    bodyfat_pct = col1.slider("Body fat % (estimate)", 5, 40, 22)
    goal = col2.selectbox("Goal", ["Cut","Recomp","Slow Bulk"])
    bjj_days = col2.slider("BJJ days/week", 0, 7, 4)
    strength_days = col2.slider("Strength days/week", 0, 7, 4)
    cardio_days = col2.slider("Cardio days/week", 0, 7, 1)
    weeks_to_event = col2.slider("Weeks to fight/event", 0, 24, 8)
    submitted = st.form_submit_button("Create Plan")

# ---------- Core Functions ----------
def bmr_msj(sex, w, h, a):
    return 10*w + 6.25*h - 5*a + (5 if sex=="Male" else -161)

def tdee(bmr, bjj, strn, cardio):
    mult = 1.2 + 0.10*strn + 0.07*bjj + 0.05*cardio
    return min(mult, 1.85) * bmr

def target_calories(tdee, goal):
    if goal == "Cut": return round(tdee * 0.82)
    if goal == "Recomp": return round(tdee * 0.98)
    if goal == "Slow Bulk": return round(tdee * 1.10)
    return round(tdee)

def macros(weight_kg, cals, goal):
    if goal == "Cut": p = 2.2*weight_kg
    elif goal == "Slow Bulk": p = 1.8*weight_kg
    else: p = 2.0*weight_kg
    f = (0.6 if goal=="Cut" else 0.7)*weight_kg
    p_kcal, f_kcal = 4*p, 9*f
    c = max(cals - p_kcal - f_kcal, 0)/4
    return round(p), round(c), round(f)

def meal_splits(p, c, f):
    p_split = [0.30,0.30,0.25,0.15]
    c_split = [0.20,0.35,0.30,0.15]
    f_split = [0.30,0.25,0.25,0.20]
    rows = []
    for i in range(4):
        rows.append((f"Meal {i+1}", round(p*p_split[i]), round(c*c_split[i]), round(f*f_split[i])))
    return rows

# ---------- Output ----------
# ---------- Output ----------
if submitted:
    bmr = bmr_msj(sex, weight_kg, height_cm, age)
    tdee_val = tdee(bmr, bjj_days, strength_days, cardio_days)
    cals = target_calories(tdee_val, goal)
    p, c, f = macros(weight_kg, cals, goal)

    st.subheader("Daily Targets")
    st.metric("Calories", f"{cals} kcal")
    st.metric("Protein", f"{p} g/day")
    st.metric("Carbs / Fat", f"{c} g / {f} g")

    st.subheader("Meal Skeleton (4 meals)")
    for name, p_g, c_g, f_g in meal_splits(p, c, f):
        st.write(f"**{name}** — Protein {p_g} g, Carbs {c_g} g, Fat {f_g} g")
    st.caption("BJJ days: load carbs in Meal 2/3 before training + post-roll.")

    st.subheader("4-Day Training Split")
    st.markdown("""
**Day 1 – Upper Push:** Bench/DB Press, OHP, Incline DB, Dips, Laterals, Triceps  
**Day 2 – Lower:** RDL, Squat, Split Squat, Ham Curl, Calves  
**Day 3 – Upper Pull + Arms:** Pull-ups, Row, Pulldown, Face Pull, Hammer Curl, Cable Curl  
**Day 4 – Athletic:** Trap Bar Jumps, KB Swings, Sled Push, Core Circuit
    """)

    if weeks_to_event <= 7:
        st.warning("Fight week: Avoid aggressive dehydration. Focus on sodium/carb timing, rest, and reduced training volume.")

    plan_txt = f"""Combat Diet & Training Plan — {date.today()}

Sex: {sex} | Age: {age}
Height: {height_cm} cm | Weight: {weight_kg} kg | BF%: {bodyfat_pct}
BJJ: {bjj_days} days/week | Strength: {strength_days} | Cardio: {cardio_days}
Weeks to event: {weeks_to_event} | Goal: {goal}

Calories: {cals} kcal/day
Protein: {p} g | Carbs: {c} g | Fat: {f} g

Meal Plan: 4 meals/day with carb loading on BJJ days.
Training: 4-day split with strength + conditioning for combat athletes.
"""

    st.download_button("Download Plan (.txt)", plan_txt, file_name="combat_plan.txt")

    st.caption("Inspired by MBZUAI’s vision to harness AI for transformative real-world impact.")
