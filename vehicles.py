
import streamlit as st
import pandas as pd


def show_vehicles():

    # Page heading
    st.title("Vehicle Management")
    st.write("Register vehicles and manage vehicle information.")
    st.divider()

    # Initialize vehicle storage
    if "vehicles" not in st.session_state:
        st.session_state.vehicles = []

    # Vehicle registration section
    st.subheader("Register a Vehicle")

    with st.container(border=True):

        with st.form("vehicle_form"):

            license_plate = st.text_input(
                "License Plate Number",
                placeholder="Example: ABC123"
            )

            vehicle_name = st.text_input(
                "Vehicle Make or Model",
                placeholder="Example: Toyota Camry"
            )

            submitted = st.form_submit_button(
                "Register Vehicle",
                use_container_width=True
            )

            if submitted:

                if not license_plate.strip():
                    st.error("Please enter a license plate number.")

                elif not vehicle_name.strip():
                    st.error("Please enter the vehicle make or model.")

                else:

                    # Check for duplicate license plates
                    existing_plates = [
                        vehicle["License Plate"].upper()
                        for vehicle in st.session_state.vehicles
                    ]

                    if license_plate.strip().upper() in existing_plates:
                        st.error("This vehicle is already registered.")

                    else:

                        # Save vehicle information
                        new_vehicle = {
                            "License Plate": license_plate.strip().upper(),
                            "Vehicle": vehicle_name.strip(),
                            "Status": "Registered"
                        }

                        st.session_state.vehicles.append(new_vehicle)

                        st.success("Vehicle registered successfully!")

    st.write("")
    st.divider()

    # Registered vehicles section
    st.subheader("Registered Vehicles")

    # Display vehicle count
    total_vehicles = len(st.session_state.vehicles)

    st.metric("Total Registered Vehicles", total_vehicles)

    if st.session_state.vehicles:

        vehicle_data = pd.DataFrame(
            st.session_state.vehicles
        )

        st.dataframe(
            vehicle_data,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No vehicles have been registered yet.")

    st.caption("Smart Park Management System")
