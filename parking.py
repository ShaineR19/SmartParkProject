
import streamlit as st


def show_parking():

    st.title("Parking Management")
    st.write("View parking space availability and status.")
    st.divider()

    # Sample parking space information
    total_spaces = 100
    available = 50
    assigned = 10
    occupied = 40

    # Summary cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Spaces", total_spaces)

    with col2:
        st.metric("Available", available)

    with col3:
        st.metric("Assigned", assigned)

    with col4:
        st.metric("Occupied", occupied)

    st.divider()

    # Parking lot legend
    st.subheader("Parking Lot Layout")

    legend1, legend2, legend3 = st.columns(3)

    with legend1:
        st.markdown("🟢 **Available**")

    with legend2:
        st.markdown("🟡 **Assigned**")

    with legend3:
        st.markdown("🔴 **Occupied**")

    st.write("")

    # Create 100 parking spaces
    rows = st.columns(10)

    letters = "ABCDEFGHIJ"

    for letter in letters:

        for number in range(1, 11):

            space_number = letters.index(letter) * 10 + number

            if space_number <= 50:
                status = "Available"
                color = "#DCFCE7"
                text_color = "#166534"

            elif space_number <= 60:
                status = "Assigned"
                color = "#FEF3C7"
                text_color = "#92400E"

            else:
                status = "Occupied"
                color = "#FEE2E2"
                text_color = "#991B1B"

            with rows[number - 1]:

                st.markdown(
                    f"""
                    <div style="
                        background-color: {color};
                        color: {text_color};
                        border-radius: 8px;
                        padding: 12px 2px;
                        text-align: center;
                        margin-bottom: 10px;
                        border: 1px solid #E2E8F0;
                    ">
                        <b>{letter}{number}</b>
                        <br>
                        <small>{status}</small>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        rows = st.columns(10)

    st.divider()

    st.caption("Smart Park Management System")
    