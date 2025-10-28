import streamlit as st
import uuid

st.set_page_config(page_title="Court Case + Section Table", page_icon="⚖️")

st.title("⚖️ Court Case + Section Table")

# Initialize session state
if "cases" not in st.session_state:
    st.session_state.cases = [{
        "id": str(uuid.uuid4()),
        "court": "",
        "case_no": "",
        "section": "",
        "status": "Pending"
    }]

def add_case():
    st.session_state.cases.append({
        "id": str(uuid.uuid4()),
        "court": "",
        "case_no": "",
        "section": "",
        "status": "Pending"
    })
    st.rerun()

def delete_case(case_id):
    st.session_state.cases = [c for c in st.session_state.cases if c["id"] != case_id]
    st.rerun()

st.markdown("### 🧾 Enter Case Details")

# Table headers (single header row)
head_cols = st.columns([3, 2, 2, 2, 1])
head_cols[0].markdown("**Court Name**")
head_cols[1].markdown("**Case No.**")
head_cols[2].markdown("**Section**")
head_cols[3].markdown("**Status**")
head_cols[4].markdown("")  # spacer for delete column

# Rows (collapsed labels for compact alignment)
for case in list(st.session_state.cases):  # list() to allow safe mutation
    i = case["id"]
    cols = st.columns([3, 2, 2, 2, 1])
    case["court"] = cols[0].text_input("", value=case["court"], key=f"court_{i}", label_visibility="collapsed")
    case["case_no"] = cols[1].text_input("", value=case["case_no"], key=f"case_{i}", label_visibility="collapsed")
    case["section"] = cols[2].text_input("", value=case["section"], key=f"section_{i}", label_visibility="collapsed")
    case["status"] = cols[3].selectbox("", ["Pending", "None"],
                                       index=0 if case["status"] == "Pending" else 1,
                                       key=f"status_{i}", label_visibility="collapsed")
    if cols[4].button("🗑️", key=f"delete_{i}"):
        delete_case(i)

st.button("➕ Add One More Case", on_click=add_case)

# Build outputs
output_full = []
output_sections = []
for idx, case in enumerate(st.session_state.cases, start=1):
    if len(st.session_state.cases)==1:
            output_full.append(f"{case['court']}, {case['case_no']} & {case['status']}")
            output_sections.append(f"{case['section']}")
    else:
        if case["court"] or case["case_no"]:
            output_full.append(f"{idx}.{case['court']}, {case['case_no']} & {case['status']}")
        if case["section"]:
            output_sections.append(f"{idx}.{case['section']}")

result_full = "\n".join(output_full)
result_sections = "\n".join(output_sections)

# Display outputs as read-only code blocks (these show Streamlit's copy icon)
st.markdown("### 🧩 Full Case Details")
if result_full:
    st.code(result_full, language=None)
else:
    st.info("Enter at least one case above to see output.")

st.markdown("### 📘 Section-wise Summary")
if result_sections:
    st.code(result_sections, language=None)
else:
    st.info("Enter sections above to see summary.")
