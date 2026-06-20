import streamlit as st
import sqlite3

def shipment_booking_ui():

    # =====================================
    # SESSION STATE
    # =====================================

    if "rate_calculated" not in st.session_state:
        st.session_state.rate_calculated = False

    st.title("📦 Shipment Booking")

    st.markdown("---")

    # =====================================
    # SENDER INFORMATION
    # =====================================

    st.subheader("Sender Information")

    col1, col2 = st.columns(2)

    with col1:
        sender_name = st.text_input(
            "Sender Name"
        )

    with col2:
        sender_phone = st.text_input(
            "Sender Phone"
        )

    sender_address = st.text_area(
        "Sender Address"
    )

    sender_zip = st.text_input(
        "Sender ZIP Code"
    )

    st.markdown("---")

    # =====================================
    # RECEIVER INFORMATION
    # =====================================

    st.subheader("Receiver Information")

    col1, col2 = st.columns(2)

    with col1:
        receiver_name = st.text_input(
            "Receiver Name"
        )

    with col2:
        receiver_phone = st.text_input(
            "Receiver Phone"
        )

    receiver_address = st.text_area(
        "Receiver Address"
    )

    receiver_zip = st.text_input(
        "Receiver ZIP Code"
    )

    st.markdown("---")

    # =====================================
    # PACKAGE INFORMATION
    # =====================================

    st.subheader("Package Information")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        weight = st.number_input(
            "Weight (lbs)",
            min_value=0.1,
            value=1.0
        )

    with col2:
        length = st.number_input(
            "Length (inches)",
            min_value=1.0,
            value=10.0
        )

    with col3:
        width = st.number_input(
            "Width (inches)",
            min_value=1.0,
            value=10.0
        )

    with col4:
        height = st.number_input(
            "Height (inches)",
            min_value=1.0,
            value=10.0
        )

    package_type = st.selectbox(
        "Package Type",
        [
            "Document",
            "Parcel",
            "Freight"
        ]
    )

    service_type = st.selectbox(
        "Service Type",
        [
            "FedEx Ground",
            "FedEx Economy",
            "FedEx Standard Overnight",
            "FedEx Priority Overnight",
            "FedEx International Economy",
            "FedEx International Priority",
            "FedEx International First"
        ]
    )

    shipment_type = st.selectbox(
        "Shipment Type",
        [
            "Domestic",
            "International"
        ]
    )

    st.markdown("---")

    calculate_btn = st.button(
        "Calculate Rate",
        use_container_width=True
    )
        # =====================================
    # CALCULATION LOGIC
    # =====================================

    if calculate_btn:

        st.session_state.rate_calculated = True

        # =====================================
        # DIMENSIONAL WEIGHT
        # =====================================

        if shipment_type == "Domestic":
            divisor = 139
        else:
            divisor = 166

        volume = (
            length *
            width *
            height
        )

        dim_weight = (
            volume /
            divisor
        )

        billed_weight = max(
            weight,
            dim_weight
        )

        # =====================================
        # SERVICE RATE TABLE
        # =====================================

        service_details = {

            "FedEx Ground": {
                "base_rate": 100,
                "rate_per_lb": 20,
                "transit_time": "3-5 Business Days",
                "mbg": "No",
                "best_for": "Budget Shipments"
            },

            "FedEx Economy": {
                "base_rate": 120,
                "rate_per_lb": 25,
                "transit_time": "2-4 Business Days",
                "mbg": "No",
                "best_for": "Cost Effective Shipping"
            },

            "FedEx Standard Overnight": {
                "base_rate": 250,
                "rate_per_lb": 40,
                "transit_time": "Next Business Day",
                "mbg": "Yes",
                "best_for": "Time Sensitive Deliveries"
            },

            "FedEx Priority Overnight": {
                "base_rate": 400,
                "rate_per_lb": 60,
                "transit_time": "Next Business Day Morning",
                "mbg": "Yes",
                "best_for": "Urgent Deliveries"
            },

            "FedEx International Economy": {
                "base_rate": 500,
                "rate_per_lb": 70,
                "transit_time": "4-6 Business Days",
                "mbg": "Limited",
                "best_for": "Affordable International Shipping"
            },

            "FedEx International Priority": {
                "base_rate": 700,
                "rate_per_lb": 90,
                "transit_time": "1-3 Business Days",
                "mbg": "Limited",
                "best_for": "Fast International Shipping"
            },

            "FedEx International First": {
                "base_rate": 1000,
                "rate_per_lb": 120,
                "transit_time": "Early Morning Delivery",
                "mbg": "Limited",
                "best_for": "Critical International Shipments"
            }
        }

        selected_service = service_details[
            service_type
        ]

        base_rate = selected_service[
            "base_rate"
        ]

        rate_per_lb = selected_service[
            "rate_per_lb"
        ]

        transit_time = selected_service[
            "transit_time"
        ]

        mbg = selected_service[
            "mbg"
        ]

        best_for = selected_service[
            "best_for"
        ]

        estimated_rate = (
            base_rate +
            (
                billed_weight *
                rate_per_lb
            )
        )

        # Save values for booking step

        st.session_state.estimated_rate = estimated_rate
        st.session_state.billed_weight = billed_weight
        st.session_state.transit_time = transit_time
        st.session_state.mbg = mbg
        st.session_state.best_for = best_for
        st.session_state.dim_weight = dim_weight
        st.session_state.weight = weight

    # =====================================
    # SHOW RESULTS AFTER CALCULATION
    # =====================================

    if st.session_state.rate_calculated:

        estimated_rate = st.session_state.estimated_rate
        billed_weight = st.session_state.billed_weight
        transit_time = st.session_state.transit_time
        mbg = st.session_state.mbg
        best_for = st.session_state.best_for
        dim_weight = st.session_state.dim_weight

        st.success(
            "✅ Shipment Details Captured"
        )

        st.markdown("---")

        st.subheader(
            "📦 Shipment Summary"
        )

        st.write(
            f"**Package Type:** {package_type}"
        )

        st.write(
            f"**Shipment Type:** {shipment_type}"
        )

        st.write(
            f"**Service Type:** {service_type}"
        )

        st.write(
            f"**Estimated Transit Time:** {transit_time}"
        )

        st.write(
            f"**MBG Eligibility:** {mbg}"
        )

        st.write(
            f"**Recommended For:** {best_for}"
        )

        st.markdown("---")

        st.subheader(
            "📏 Dimensional Weight Transparency"
        )

        st.write(
            f"Dimensional Weight = {dim_weight:.2f} lbs"
        )

        st.write(
            f"Actual Weight = {weight:.2f} lbs"
        )

        st.write(
            f"Billed Weight = {billed_weight:.2f} lbs"
        )

        if dim_weight > weight:

            st.warning(
                "Dimensional Weight is greater than "
                "Actual Weight. FedEx will bill "
                "the Dimensional Weight."
            )

        else:

            st.success(
                "Actual Weight is greater than "
                "Dimensional Weight. FedEx will bill "
                "the Actual Weight."
            )

        st.markdown("---")

        st.subheader(
            "💰 Rate Estimate"
        )

        st.metric(
            label="Estimated Shipping Cost",
            value=f"₹ {estimated_rate:.2f}"
        )

        # =====================================
        # BOOK SHIPMENT
        # =====================================

        book_btn = st.button(
            "📦 Book Shipment",
            use_container_width=True
        )

        if book_btn:

            # =====================================
            # VALIDATION
            # =====================================

            missing_fields = []

            if sender_name.strip() == "":
                missing_fields.append("Sender Name")

            if sender_phone.strip() == "":
                missing_fields.append("Sender Phone")

            if sender_address.strip() == "":
                missing_fields.append("Sender Address")

            if sender_zip.strip() == "":
                missing_fields.append("Sender ZIP Code")

            if receiver_name.strip() == "":
                missing_fields.append("Receiver Name")

            if receiver_phone.strip() == "":
                missing_fields.append("Receiver Phone")

            if receiver_address.strip() == "":
                missing_fields.append("Receiver Address")

            if receiver_zip.strip() == "":
                missing_fields.append("Receiver ZIP Code")

            if missing_fields:

                st.error(
                    "Please fill the following fields:\n\n• "
                    + "\n• ".join(missing_fields)
                )

                st.stop()

            # =====================================
            # SAVE TO DATABASE
            # =====================================

            try:

                conn = sqlite3.connect("fedex.db")

                cursor = conn.cursor()

                cursor.execute("""
                INSERT INTO shipments(

                    sender_name,
                    sender_phone,
                    sender_address,
                    sender_zip,

                    receiver_name,
                    receiver_phone,
                    receiver_address,
                    receiver_zip,

                    package_type,
                    service_type,
                    shipment_type,

                    weight,
                    length,
                    width,
                    height,

                    billed_weight,
                    estimated_rate

                )
                VALUES(
                    ?, ?, ?, ?,
                    ?, ?, ?, ?,
                    ?, ?, ?,
                    ?, ?, ?, ?,
                    ?, ?
                )
                """,
                (

                    sender_name,
                    sender_phone,
                    sender_address,
                    sender_zip,

                    receiver_name,
                    receiver_phone,
                    receiver_address,
                    receiver_zip,

                    package_type,
                    service_type,
                    shipment_type,

                    weight,
                    length,
                    width,
                    height,

                    billed_weight,
                    estimated_rate
                ))

                shipment_id = cursor.lastrowid

                tracking_number = f"FDX{shipment_id:06d}"

                conn.commit()

                conn.close()

                st.success(
                    "🎉 Shipment Booked Successfully!"
                )

                st.info(
                    f"Tracking Number: {tracking_number}"
                )

                st.session_state.rate_calculated = False

            except Exception as e:

                st.error(
                    f"Database Error: {e}"
                )

        st.markdown("---")

        st.subheader(
            "✅ Billing Decision"
        )

        if billed_weight == dim_weight:

            st.error(
                f"FedEx will bill "
                f"{dim_weight:.2f} lbs "
                f"because Dimensional Weight "
                f"is greater than Actual Weight "
                f"({weight:.2f} lbs)."
            )

        else:

            st.success(
                f"FedEx will bill "
                f"{weight:.2f} lbs "
                f"because Actual Weight "
                f"is greater than Dimensional Weight "
                f"({dim_weight:.2f} lbs)."
            )
