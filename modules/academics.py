# modules/academics.py

import streamlit as st

# ---------- 1. Percentage Calculator (single Part/Year) ----------

def calculate_percentage(subjects: list[dict]) -> dict:
    """
    subjects: list of {"name": str, "max_marks": float, "obtained_marks": float}
    Returns total obtained, total max, and percentage.
    """
    total_max = sum(s["max_marks"] for s in subjects)
    total_obtained = sum(s["obtained_marks"] for s in subjects)

    if total_max == 0:
        return {"error": "Total max marks cannot be zero."}

    percentage = round((total_obtained / total_max) * 100, 2)
    return {
        "total_obtained": total_obtained,
        "total_max": total_max,
        "percentage": percentage,
    }


# ---------- 2. Official Syllabus links (verified from mmhapu.ac.in/syllabus) ----------

SYLLABUS_LINKS = {
        
    "BCA": "https://mmhapu.ac.in/uploads/syllabus/1727437777_Syllabus%20of%20BCA.pdf",
    "BBA": "https://mmhapu.ac.in/uploads/syllabus/1727437749_Syllabus%20of%20BBA.pdf",
    "BJMC": "https://mmhapu.ac.in/uploads/syllabus/1727689616_Syllabus%20of%20BJMC.pdf",
    # BLIS aur honours subjects (Arabic, Botany, Chemistry, etc.) ke liye
    # mmhapu.ac.in/syllabus page pe list hai, lekin unke exact PDF link
    # mujhe search me nahi mile — verify na hone tak add nahi kar raha

    # Baaki courses ke exact PDF links mmhapu.ac.in/syllabus page se
    # verify karke yahan add karte jaana — sirf verified links hi daalna
}


def get_syllabus_link(course: str) -> str | None:
    return SYLLABUS_LINKS.get(course.upper().strip())


# ---------- 3. Streamlit UI (app.py me import karke call karna) ----------

def cgpa_calculator_tab():
    st.header("📊 Percentage Calculator")
    st.caption("Apne Part (I/II/III) ka result nikaalo — yearly exam system ke hisaab se")

    num_subjects = st.number_input("Kitne subjects hain is Part me?", min_value=1, max_value=15, value=5, step=1)

    subjects = []
    for i in range(int(num_subjects)):
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            name = st.text_input(f"Subject {i+1} ka naam", key=f"name_{i}")
        with col2:
            max_marks = st.number_input(f"Max Marks", min_value=1.0, value=100.0, key=f"max_{i}")
        with col3:
            obtained = st.number_input(f"Obtained Marks", min_value=0.0, value=0.0, key=f"obt_{i}")
        subjects.append({"name": name or f"Subject {i+1}", "max_marks": max_marks, "obtained_marks": obtained})

    if st.button("Calculate Percentage"):
        result = calculate_percentage(subjects)
        if "error" in result:
            st.error(result["error"])
        else:
            st.success(f"✅ Total: {result['total_obtained']} / {result['total_max']}")
            st.metric("Percentage", f"{result['percentage']}%")


def syllabus_tab():
    st.header("📚 Syllabus")
    st.caption("Official MMHAPU syllabus PDFs")

    course = st.selectbox("Course chuno", list(SYLLABUS_LINKS.keys()))
    link = get_syllabus_link(course)
    if link:
        st.markdown(f"[📄 {course} Syllabus PDF kholo]({link})")
    else:
        st.warning("Is course ka syllabus abhi verified/available nahi hai.")