import streamlit as st
from openpyxl import load_workbook
from io import BytesIO
from urllib.parse import quote
import re


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Patent Hyperlinker",
    page_icon="🔗",
    layout="wide"
)


# ============================================================
# STYLING
# ============================================================

st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.15rem;
        font-weight: 700;
        color: #EE3C18;
        margin-bottom: 0.15rem;
    }

    .sub-title {
        font-size: 1.35rem;
        font-weight: 600;
        color: var(--text-color);
        margin-bottom: 0.55rem;
    }

    .processing-box {
        margin-top: 1.25rem;
        margin-bottom: 2.2rem;
        padding: 1.15rem 1.5rem;
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(128,128,128,0.20);
        border-radius: 10px;
    }

    .processing-title {
        font-weight: 600;
        margin-bottom: 0.65rem;
        color: var(--text-color);
    }

    .processing-list {
        margin: 0;
        padding-left: 1.35rem;
        color: var(--text-color);
        opacity: 0.70;
        line-height: 1.65;
    }

    .stButton > button {
        background-color: #EE3C18;
        color: white;
        border: none;
        border-radius: 7px;
        font-weight: 600;
    }

    .stButton > button:hover {
        background-color: #D83212;
        color: white;
    }

    .summary-box {
        padding: 1rem 1.25rem;
        border: 1px solid rgba(128,128,128,0.20);
        border-radius: 10px;
        background-color: var(--secondary-background-color);
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    .summary-number {
        font-size: 1.35rem;
        font-weight: 700;
        color: #EE3C18;
    }

    .summary-label {
        font-size: 0.88rem;
        color: var(--text-color);
        opacity: 0.70;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">Patent Research</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Patent Hyperlinker</div>',
    unsafe_allow_html=True
)

st.write(
    """
    Creates clickable hyperlinks for patent publication numbers using
    Google Patents, New Espacenet, or the original Orbit document link.
    """
)

st.markdown(
    """
    <div class="processing-box">
        <div class="processing-title">Processing includes:</div>
        <ul class="processing-list">
            <li>Uses the publication number as the hyperlink target cell.</li>
            <li>Reads the actual hyperlink behind the ORBIT LINK cell, regardless of whether it displays "Open" or a patent number.</li>
            <li>Dynamic mode sends US patents to Google Patents, Indian patents to their original Orbit link, and all other patents to New Espacenet.</li>
            <li>Preserves the existing workbook data and columns.</li>
            <li>Only the PUBLICATION NUMBER cells are updated with hyperlinks.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FUNCTIONS
# ============================================================

def clean_value(value):
    """Return a clean string representation of an Excel cell."""
    if value is None:
        return ""

    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))

    return str(value).strip()


def normalize_patent_number(value):
    """
    Normalize a patent number sufficiently for country detection
    and URL construction.

    Examples:
        US12369069B2 -> US12369069B2
        US 12,369,069 B2 -> US12369069B2
        IN 123456 A -> IN123456A
    """
    value = clean_value(value)

    return re.sub(r"[\s,./-]+", "", value).upper()


def get_country_code(patent_number):
    """Extract the two-letter country code from a publication number."""
    normalized = normalize_patent_number(patent_number)

    match = re.match(r"^([A-Z]{2})", normalized)

    if match:
        return match.group(1)

    return ""


def google_patents_url(patent_number):
    """
    Create a Google Patents URL.
    """
    patent = normalize_patent_number(patent_number)

    return f"https://patents.google.com/patent/{quote(patent, safe='')}/en"


def espacenet_url(patent_number):
    """
    Create a New Espacenet search URL using the publication number.
    """
    patent = normalize_patent_number(patent_number)

    query = quote(f"pn={patent}", safe="")

    return f"https://worldwide.espacenet.com/patent/search?q={query}"


def get_orbit_hyperlink(cell):
    """
    Extract the actual hyperlink target from an Excel cell.

    This deliberately uses the hyperlink attached to the cell,
    not the visible text.

    Therefore it works for:
        Open -> [Orbit URL]
        US1234567B2 -> [Orbit URL]
    """
    if cell.hyperlink is None:
        return ""

    target = cell.hyperlink.target

    if target:
        return target

    return ""


def create_target_url(patent_number, mode, orbit_link):
    """
    Determine the destination URL based on the selected mode.
    """

    patent = normalize_patent_number(patent_number)
    country = get_country_code(patent)

    # --------------------------------------------------------
    # GOOGLE PATENTS
    # --------------------------------------------------------
    if mode == "Google Patents":
        return google_patents_url(patent), "Google Patents"

    # --------------------------------------------------------
    # NEW ESPACENET
    # --------------------------------------------------------
    if mode == "New Espacenet":
        return espacenet_url(patent), "New Espacenet"

    # --------------------------------------------------------
    # DYNAMIC
    # --------------------------------------------------------
    if mode == "Dynamic":

        # US -> Google Patents
        if country == "US":
            return google_patents_url(patent), "Google Patents"

        # IN -> Original Orbit link
        if country == "IN":
            if orbit_link:
                return orbit_link, "Original Orbit Link"

            return "", "Missing Orbit Link"

        # Everything else -> New Espacenet
        return espacenet_url(patent), "New Espacenet"

    return "", "No Link"


def process_workbook(
    uploaded_file,
    patent_column,
    orbit_column,
    mode
):
    """
    Process the uploaded workbook and return:
        output BytesIO
        statistics dictionary
    """

    uploaded_file.seek(0)

    workbook = load_workbook(
        uploaded_file,
        keep_links=True
    )

    worksheet = workbook.active

    # --------------------------------------------------------
    # Find headers
    # --------------------------------------------------------

    headers = {}

    for col in range(1, worksheet.max_column + 1):
        value = clean_value(worksheet.cell(1, col).value)

        if value:
            headers[value] = col

    patent_col_index = headers[patent_column]
    orbit_col_index = headers[orbit_column]

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    total_rows = 0
    linked_rows = 0
    skipped_rows = 0

    google_count = 0
    espacenet_count = 0
    orbit_count = 0
    missing_orbit_count = 0

    # --------------------------------------------------------
    # Process rows
    # --------------------------------------------------------

    for row in range(2, worksheet.max_row + 1):

        patent_cell = worksheet.cell(row, patent_col_index)
        orbit_cell = worksheet.cell(row, orbit_col_index)

        patent_number = clean_value(patent_cell.value)

        if not patent_number:
            continue

        total_rows += 1

        # Read actual hyperlink from Orbit cell.
        orbit_link = get_orbit_hyperlink(orbit_cell)

        target_url, destination = create_target_url(
            patent_number,
            mode,
            orbit_link
        )

        # No destination available.
        if not target_url:
            skipped_rows += 1

            if destination == "Missing Orbit Link":
                missing_orbit_count += 1

            continue

        # ----------------------------------------------------
        # Remove any previous hyperlink from publication cell
        # ----------------------------------------------------

        patent_cell.hyperlink = None

        # ----------------------------------------------------
        # Add new hyperlink
        # ----------------------------------------------------

        patent_cell.hyperlink = target_url

        # Keep the existing displayed patent number.
        patent_cell.value = patent_number

        # Excel hyperlink appearance.
        patent_cell.style = "Hyperlink"

        linked_rows += 1

        if destination == "Google Patents":
            google_count += 1

        elif destination == "New Espacenet":
            espacenet_count += 1

        elif destination == "Original Orbit Link":
            orbit_count += 1

    # --------------------------------------------------------
    # Preserve useful Excel usability features
    # --------------------------------------------------------

    worksheet.freeze_panes = "A2"

    # Only add autofilter if there are headers.
    if worksheet.max_row >= 1:
        worksheet.auto_filter.ref = worksheet.dimensions

    # --------------------------------------------------------
    # Save workbook
    # --------------------------------------------------------

    output = BytesIO()

    workbook.save(output)

    output.seek(0)

    statistics = {
        "total_rows": total_rows,
        "linked_rows": linked_rows,
        "skipped_rows": skipped_rows,
        "google_count": google_count,
        "espacenet_count": espacenet_count,
        "orbit_count": orbit_count,
        "missing_orbit_count": missing_orbit_count,
    }

    return output, statistics


# ============================================================
# FILE UPLOAD
# ============================================================

uploaded_file = st.file_uploader(
    "Upload Excel file",
    type=["xlsx"],
    help="Upload an Excel workbook containing PUBLICATION NUMBER and ORBIT LINK columns."
)


# ============================================================
# MAIN TOOL
# ============================================================

if uploaded_file is not None:

    # --------------------------------------------------------
    # Read workbook for header selection
    # --------------------------------------------------------

    try:
        uploaded_file.seek(0)

        preview_workbook = load_workbook(
            uploaded_file,
            read_only=False,
            keep_links=True
        )

        preview_sheet = preview_workbook.active

        available_columns = []

        for col in range(1, preview_sheet.max_column + 1):
            value = clean_value(preview_sheet.cell(1, col).value)

            if value:
                available_columns.append(value)

        if not available_columns:
            st.error("No column headers were found in Row 1.")
            st.stop()

        # ----------------------------------------------------
        # Column selection
        # ----------------------------------------------------

        st.subheader("Column Selection")

        col1, col2 = st.columns(2)

        with col1:

            default_patent_index = 0

            for idx, name in enumerate(available_columns):
                if normalize_patent_number(name) in [
                    "PUBLICATIONNUMBER",
                    "PATENTNUMBER",
                    "PUBLICATIONNO",
                    "PATENTNO"
                ]:
                    default_patent_index = idx
                    break

            patent_column = st.selectbox(
                "Publication Number Column",
                available_columns,
                index=default_patent_index
            )

        with col2:

            default_orbit_index = 0

            for idx, name in enumerate(available_columns):
                normalized_name = normalize_patent_number(name)

                if normalized_name in [
                    "ORBITLINK",
                    "DOCUMENTLINK",
                    "ORBIT"
                ]:
                    default_orbit_index = idx
                    break

            orbit_column = st.selectbox(
                "Orbit Link Column",
                available_columns,
                index=default_orbit_index
            )

        # ----------------------------------------------------
        # Linking mode
        # ----------------------------------------------------

        st.subheader("Linking Mode")

        mode = st.selectbox(
            "Select hyperlinking mode",
            [
                "Dynamic",
                "Google Patents",
                "New Espacenet"
            ],
            index=0
        )

        if mode == "Dynamic":
            st.info(
                "Dynamic mode: US → Google Patents | "
                "IN → Original Orbit Link | "
                "All other patents → New Espacenet"
            )

        elif mode == "Google Patents":
            st.info(
                "All publication numbers will be linked to Google Patents."
            )

        else:
            st.info(
                "All publication numbers will be linked to New Espacenet."
            )

        # ----------------------------------------------------
        # Run button
        # ----------------------------------------------------

        st.markdown("")

        if st.button(
            "Create Patent Hyperlinks",
            use_container_width=True
        ):

            try:

                with st.spinner("Creating patent hyperlinks..."):

                    uploaded_file.seek(0)

                    output_file, stats = process_workbook(
                        uploaded_file,
                        patent_column,
                        orbit_column,
                        mode
                    )

                st.success(
                    f"Completed. {stats['linked_rows']:,} patent numbers were hyperlinked."
                )

                # ------------------------------------------------
                # Summary
                # ------------------------------------------------

                st.markdown(
                    '<div class="summary-box">',
                    unsafe_allow_html=True
                )

                s1, s2, s3, s4 = st.columns(4)

                with s1:
                    st.markdown(
                        f'<div class="summary-number">{stats["total_rows"]:,}</div>',
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        '<div class="summary-label">Patent rows</div>',
                        unsafe_allow_html=True
                    )

                with s2:
                    st.markdown(
                        f'<div class="summary-number">{stats["google_count"]:,}</div>',
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        '<div class="summary-label">Google Patents</div>',
                        unsafe_allow_html=True
                    )

                with s3:
                    st.markdown(
                        f'<div class="summary-number">{stats["espacenet_count"]:,}</div>',
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        '<div class="summary-label">New Espacenet</div>',
                        unsafe_allow_html=True
                    )

                with s4:
                    st.markdown(
                        f'<div class="summary-number">{stats["orbit_count"]:,}</div>',
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        '<div class="summary-label">Original Orbit Links</div>',
                        unsafe_allow_html=True
                    )

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

                # ------------------------------------------------
                # Warning for missing Indian Orbit links
                # ------------------------------------------------

                if stats["missing_orbit_count"] > 0:

                    st.warning(
                        f'{stats["missing_orbit_count"]:,} Indian patent(s) '
                        f'could not be hyperlinked because the ORBIT LINK '
                        f'cell did not contain an actual hyperlink.'
                    )

                if stats["skipped_rows"] > 0:

                    st.warning(
                        f'{stats["skipped_rows"]:,} row(s) were skipped.'
                    )

                # ------------------------------------------------
                # Download
                # ------------------------------------------------

                st.download_button(
                    label="Download Hyperlinked Excel",
                    data=output_file,
                    file_name="Patent_Hyperlinked.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

            except Exception as e:

                st.error(
                    f"An error occurred while processing the workbook: {e}"
                )

    except Exception as e:

        st.error(
            f"Unable to read the uploaded Excel file: {e}"
        )


# ============================================================
# BACK TO HOME
# ============================================================

st.markdown("")

if st.button("← Back to Home"):
    st.switch_page("Home.py")
