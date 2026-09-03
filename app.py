import streamlit as st
import pandas as pd
from io import BytesIO

from generator import generate_test_cases
from email_sender import send_test_cases_email


st.set_page_config(
    page_title="AI Test Case Generator",
    page_icon="🧪",
    layout="wide"
)


st.title("🧪 AI Test Case Generator")

st.write(
    "Enter a software requirement and let AI generate structured test cases."
)


# Store generated test cases in session state
if "test_cases" not in st.session_state:
    st.session_state.test_cases = None


requirement = st.text_area(
    "Enter your software requirement:",
    placeholder="Example: Users should be able to reset their password using their registered email address.",
    height=150
)


# Generate test cases
if st.button("Generate Test Cases"):

    if requirement.strip():

        with st.spinner("Generating test cases..."):

            st.session_state.test_cases = generate_test_cases(requirement)

    else:

        st.warning("Please enter a software requirement.")


# Display generated test cases
if st.session_state.test_cases:

    test_cases = st.session_state.test_cases

    st.success(f"Generated {len(test_cases)} test cases.")

    st.subheader("Generated Test Cases")

    for test_case in test_cases:

        with st.expander(
            f"{test_case.id} — {test_case.title}",
            expanded=False
        ):

            st.write(f"**Test Type:** {test_case.test_type}")

            st.write(f"**Priority:** {test_case.priority}")

            st.write("**Preconditions:**")
            st.write(test_case.preconditions)

            st.write("**Test Steps:**")

            for i, step in enumerate(test_case.steps, start=1):
                st.write(f"{i}. {step}")

            st.write("**Expected Result:**")
            st.write(test_case.expected_result)


    # Convert test cases into a DataFrame

    data = []

    for test_case in test_cases:

        data.append({
            "ID": test_case.id,
            "Title": test_case.title,
            "Test Type": test_case.test_type,
            "Priority": test_case.priority,
            "Preconditions": test_case.preconditions,
            "Steps": "\n".join(
                f"{i}. {step}"
                for i, step in enumerate(test_case.steps, start=1)
            ),
            "Expected Result": test_case.expected_result
        })


    df = pd.DataFrame(data)


    # Create Excel file

    excel_file = BytesIO()

    with pd.ExcelWriter(
        excel_file,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Test Cases"
        )


    excel_file.seek(0)


    # Download Excel

    st.download_button(
        label="📥 Download Test Cases as Excel",
        data=excel_file,
        file_name="AI_Test_Cases.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


    # Email section

    st.subheader("📧 Email Test Cases")

    recipient_email = st.text_input(
        "Enter the email address to send the test cases to:"
    )


    if st.button("📤 Send Test Cases by Email"):

        if recipient_email.strip():

            try:

                excel_file.seek(0)

                excel_data = excel_file.getvalue()

                with st.spinner("Sending email..."):

                    send_test_cases_email(
                        recipient_email,
                        excel_data
                    )

                st.success(
                    f"Test cases successfully sent to {recipient_email}!"
                )

            except Exception as e:

                st.error(
                    f"Failed to send email: {e}"
                )

        else:

            st.warning(
                "Please enter an email address."
            )