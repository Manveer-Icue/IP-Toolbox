import streamlit as st
from openpyxl import load_workbook
from io import BytesIO
from urllib.parse import quote
import re
import pandas as pd

from auth import require_password


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
    Normalize a patent number for country detection
    and URL construction.
    """

    value = clean_value(value)

    return re.sub(
        r"[\s,./-]+",
        "",
        value
    ).upper()


def get_country_code(patent_number):
    """Extract the two-letter country code."""

    normalized = normalize_patent_number(
        patent_number
    )

    match = re.match(
        r"^([A-Z]{2})",
        normalized
    )

    if match:
        return match.group(1)

    return ""


def google_patents_url(patent_number):
    """Create Google Patents URL."""

    patent = normalize_patent_number(
        patent_number
    )

    return (
        f"https://patents.google.com/patent/"
        f"{quote(patent, safe='')}/en"
    )


def espacenet_url(patent_number):
    """Create New Espacenet search URL."""

    patent = normalize_patent_number(
        patent_number
    )

    query = quote(
        f"pn={patent}",
        safe=""
    )

    return (
        f"https://worldwide.espacenet.com/patent/search"
        f"?q={query}"
    )


def get_orbit_hyperlink(cell):
    """
    Extract the actual hyperlink target from an Excel cell.

    The visible text is ignored.
    """

    if cell is None:
        return ""

    if cell.hyperlink is None:
        return ""

    target = cell.hyperlink.target

    if target:
        return target

    return ""


def create_target_url(
    patent_number,
    mode,
    orbit_link
):
    """
    Determine the destination URL.
    """

    patent = normalize_patent_number(
        patent_number
    )

    country = get_country_code(
        patent
    )


    # --------------------------------------------------------
    # GOOGLE PATENTS
    # --------------------------------------------------------

    if mode == "Google Patents":

        return (
            google_patents_url(patent),
            "Google Patents"
        )


    # --------------------------------------------------------
    # NEW ESPACENET
    # --------------------------------------------------------

    if mode == "New Espacenet":

        return (
            espacenet_url(patent),
            "New Espacenet"
        )


    # --------------------------------------------------------
    # DYNAMIC
    # --------------------------------------------------------

    if mode == "Dynamic":

        if country == "US":

            return (
                google_patents_url(patent),
                "Google Patents"
            )


        if country == "IN":

            if orbit_link:

                return (
                    orbit_link,
                    "Original Orbit Link"
                )

            return (
                "",
                "Missing Orbit Link"
            )


        return (
            espacenet_url(patent),
            "New Espacenet"
        )


    return (
        "",
        "No Link"
    )


def process_workbook(
    uploaded_file,
    patent_column,
    orbit_column,
    mode
):
    """
    Process uploaded workbook.

    Adds a NOT LINKED PATENTS column immediately next to
    PUBLICATION NUMBER.

    Only Indian patents that cannot be linked because an
    actual Orbit hyperlink is unavailable are marked
    NOT LINKED.
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

    for col in range(
        1,
        worksheet.max_column + 1
    ):

        value = clean_value(
            worksheet.cell(
                1,
                col
            ).value
        )

        if value:
            headers[value] = col


    if patent_column not in headers:
        raise ValueError(
            f'Publication number column "{patent_column}" was not found.'
        )


    patent_col_index = headers[
        patent_column
    ]


    # --------------------------------------------------------
    # ORBIT LINK is optional
    # --------------------------------------------------------

    if orbit_column and orbit_column != "None":

        orbit_col_index = headers.get(
            orbit_column
        )

    else:

        orbit_col_index = None


    # --------------------------------------------------------
    # Add NOT LINKED PATENTS column
    # immediately next to PUBLICATION NUMBER
    # --------------------------------------------------------

    existing_status_index = None

    for col in range(
        1,
        worksheet.max_column + 1
    ):

        header_value = clean_value(
            worksheet.cell(
                1,
                col
            ).value
        )

        if (
            header_value.casefold()
            == "not linked patents"
        ):

            existing_status_index = col

            break


    if existing_status_index is not None:

        # Use the existing status column if it is already
        # immediately next to the publication number.
        if existing_status_index == patent_col_index + 1:

            status_col_index = existing_status_index

        else:

            # Remove an existing status column elsewhere
            # so that the output always places it next to
            # PUBLICATION NUMBER.
            worksheet.delete_cols(
                existing_status_index,
                1
            )

            # If the deleted column was before the patent
            # column, its index has shifted left.
            if existing_status_index < patent_col_index:

                patent_col_index -= 1

            # Recalculate Orbit column after deletion.
            if orbit_col_index is not None:

                if existing_status_index < orbit_col_index:

                    orbit_col_index -= 1

                elif existing_status_index == orbit_col_index:

                    orbit_col_index = None

            worksheet.insert_cols(
                patent_col_index + 1,
                1
            )

            status_col_index = patent_col_index + 1

    else:

        worksheet.insert_cols(
            patent_col_index + 1,
            1
        )

        status_col_index = patent_col_index + 1


        # Inserting before the Orbit column shifts its index.
        if (
            orbit_col_index is not None
            and orbit_col_index > patent_col_index
        ):

            orbit_col_index += 1


    worksheet.cell(
        1,
        status_col_index
    ).value = "NOT LINKED PATENTS"


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

    for row in range(
        2,
        worksheet.max_row + 1
    ):

        patent_cell = worksheet.cell(
            row,
            patent_col_index
        )

        status_cell = worksheet.cell(
            row,
            status_col_index
        )

        # Keep the status column blank by default.
        status_cell.value = ""


        if orbit_col_index is not None:

            orbit_cell = worksheet.cell(
                row,
                orbit_col_index
            )

        else:

            orbit_cell = None


        patent_number = clean_value(
            patent_cell.value
        )


        if not patent_number:
            continue


        total_rows += 1


        # ----------------------------------------------------
        # Read actual Orbit hyperlink if available
        # ----------------------------------------------------

        orbit_link = get_orbit_hyperlink(
            orbit_cell
        )


        target_url, destination = create_target_url(
            patent_number,
            mode,
            orbit_link
        )


        # ----------------------------------------------------
        # Patent cannot be linked
        # ----------------------------------------------------

        if not target_url:

            skipped_rows += 1

            if destination == "Missing Orbit Link":

                missing_orbit_count += 1

                status_cell.value = "NOT LINKED"

            continue


        # ----------------------------------------------------
        # Remove existing hyperlink
        # ----------------------------------------------------

        patent_cell.hyperlink = None


        # ----------------------------------------------------
        # Add new hyperlink
        # ----------------------------------------------------

        patent_cell.hyperlink = target_url

        patent_cell.value = patent_number

        patent_cell.style = "Hyperlink"


        linked_rows += 1


        # ----------------------------------------------------
        # Statistics
        # ----------------------------------------------------

        if destination == "Google Patents":

            google_count += 1

        elif destination == "New Espacenet":

            espacenet_count += 1

        elif destination == "Original Orbit Link":

            orbit_count += 1


    # --------------------------------------------------------
    # Excel usability
    # --------------------------------------------------------

    worksheet.freeze_panes = "A2"

    if worksheet.max_row >= 1:

        worksheet.auto_filter.ref = (
            worksheet.dimensions
        )


    # --------------------------------------------------------
    # Save
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
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Patent Hyperlinker",
    page_icon="🔗",
    layout="wide"
)


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
<style>

/* ============================================================
   SIDEBAR
   ============================================================ */

[data-testid="stSidebar"] {
    display: none;
}

[data-testid="collapsedControl"] {
    display: none;
}


/* ============================================================
   GLOBAL
   ============================================================ */

.stApp {
    background-color: var(--background-color);
    color: var(--text-color);
}

.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 3.5rem;
}


/* ============================================================
   HEADER
   ============================================================ */

.main-title {
    font-size: 2.35rem;
    font-weight: 700;
    color: #EE3C18;
    letter-spacing: -0.04em;
    line-height: 1.15;
    margin-top: 0;
    margin-bottom: 0.35rem;
}

.sub-title {
    font-size: 1.08rem;
    font-weight: 500;
    color: var(--text-color);
    margin-bottom: 1.05rem;
}

.block-container p {
    color: var(--text-color);
    opacity: 0.70;
    line-height: 1.65;
}


/* ============================================================
   BACK BUTTON
   ============================================================ */

.back-button-area {
    min-height: 48px;
    margin-bottom: 0.8rem;
}


/* ============================================================
   NATIVE STREAMLIT CONTAINERS
   ============================================================ */

[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 10px;
    border: 1px solid rgba(128,128,128,0.20);
    background-color: var(--background-color);
}


/* ============================================================
   PROCESSING INFORMATION
   ============================================================ */

.processing-heading {
    font-weight: 600;
    color: var(--text-color);
    margin-bottom: 0.45rem;
}

.processing-list {
    color: var(--text-color);
    opacity: 0.70;
    line-height: 1.65;
    margin: 0;
    padding-left: 1.35rem;
}

.processing-list li {
    margin-bottom: 0.45rem;
}

.processing-list li:last-child {
    margin-bottom: 0;
}


/* ============================================================
   INPUT FORMAT
   ============================================================ */

.input-format-heading {
    font-weight: 600;
    color: var(--text-color);
    margin-bottom: 0.75rem;
}

.input-format-note {
    font-size: 0.82rem;
    color: var(--text-color);
    opacity: 0.65;
    line-height: 1.55;
    margin-top: 0.75rem;
}


/* ============================================================
   INPUT TABLE
   ============================================================ */

.input-table-wrapper {
    border: 1px solid rgba(128,128,128,0.22);
    border-radius: 9px;
    overflow: hidden;
}


/* ============================================================
   BUTTONS
   ============================================================ */

div[data-testid="stButton"] button {
    border-radius: 7px;
    font-size: 0.82rem;
    font-weight: 500;
    border: 1px solid rgba(128,128,128,0.25);
    background-color: var(--secondary-background-color);
    color: var(--text-color);
    min-height: 36px;
}

div[data-testid="stButton"] button:hover {
    border-color: #EE3C18;
    color: #EE3C18;
}


/* ------------------------------------------------------------
   PRIMARY BUTTON
   ------------------------------------------------------------ */

div[data-testid="stButton"] button[kind="primary"] {
    background-color: #EE3C18 !important;
    border: 1px solid #EE3C18 !important;
    min-height: 42px;
    opacity: 1 !important;
}

div[data-testid="stButton"] button[kind="primary"] * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    opacity: 1 !important;
    font-weight: 700 !important;
    text-shadow: none !important;
}

div[data-testid="stButton"] button[kind="primary"] p,
div[data-testid="stButton"] button[kind="primary"] span,
div[data-testid="stButton"] button[kind="primary"] div {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    opacity: 1 !important;
    font-weight: 700 !important;
    text-shadow: none !important;
}

/* ------------------------------------------------------------
   DOWNLOAD BUTTON
   ------------------------------------------------------------ */

div[data-testid="stDownloadButton"] button {
    background-color: #EE3C18 !important;
    border: 1px solid #EE3C18 !important;
    color: #FFFFFF !important;
    border-radius: 8px;
    font-weight: 600 !important;
    min-height: 42px;
}

div[data-testid="stDownloadButton"] button *,
div[data-testid="stDownloadButton"] button p,
div[data-testid="stDownloadButton"] button span,
div[data-testid="stDownloadButton"] button div,
div[data-testid="stDownloadButton"] button svg {
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}


/* ============================================================
   FILE UPLOADER
   ============================================================ */

[data-testid="stFileUploader"] {
    background-color: var(--secondary-background-color);
    border: 1px dashed rgba(128,128,128,0.30);
    border-radius: 10px;
    padding: 0.8rem 1rem;
}


/* ============================================================
   SUMMARY
   ============================================================ */

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


/* ============================================================
   DOWNLOAD BUTTON
   ============================================================ */

div[data-testid="stDownloadButton"] button {
    background-color: #EE3C18;
    border: 1px solid #EE3C18;
    color: #FFFFFF !important;
    border-radius: 8px;
    font-weight: 600;
    min-height: 42px;
}

div[data-testid="stDownloadButton"] button p,
div[data-testid="stDownloadButton"] button span,
div[data-testid="stDownloadButton"] button div {
    color: #FFFFFF !important;
}


/* ============================================================
   DIVIDERS
   ============================================================ */

hr {
    border-top: 1px solid rgba(128,128,128,0.22);
}


/* ============================================================
   RESPONSIVE
   ============================================================ */

@media (max-width: 800px) {

    .block-container {
        padding-top: 2rem;
    }

    .main-title {
        font-size: 2.1rem;
    }

    .back-button-area {
        min-height: 48px;
        margin-bottom: 0.8rem;
    }

}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# AUTHENTICATION
# ============================================================

require_password()


# ============================================================
# BACK TO HOME
# ============================================================

st.markdown(
    '<div class="back-button-area">',
    unsafe_allow_html=True
)

if st.button("← Back to Home"):
    st.switch_page("Home.py")

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# PAGE HEADER
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


# ============================================================
# PROCESSING INFORMATION
# ============================================================

with st.container(border=True):

    st.markdown(
        '<div class="processing-heading">Processing includes:</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
<ul class="processing-list">
<li>Uses the <b>PUBLICATION NUMBER</b> cell as the hyperlink target.</li>
<li>Reads the actual hyperlink behind the <b>ORBIT LINK</b> cell, regardless of whether it displays <b>"Open"</b> or a patent number.</li>
<li>Dynamic mode sends <b>US patents to Google Patents</b>, <b>Indian patents to their original Orbit link</b>, and <b>all other patents to New Espacenet</b>.</li>
<li>Adds a <b>NOT LINKED PATENTS</b> column immediately next to <b>PUBLICATION NUMBER</b>.</li>
<li>Indian patents without an available actual Orbit hyperlink are marked <b>NOT LINKED</b>.</li>
<li>Preserves the existing workbook data and columns.</li>
<li>Only the <b>PUBLICATION NUMBER</b> cells are updated with hyperlinks.</li>
</ul>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# INPUT FORMAT
# ============================================================

with st.container(border=True):

    st.markdown(
        '<div class="input-format-heading">Input file format</div>',
        unsafe_allow_html=True
    )


    input_example = pd.DataFrame(
        {
            "PUBLICATION NUMBER": [
                "US12345678B2",
                "IN123456A",
                "EP1234567B1"
            ],
            "ORBIT LINK": [
                "Open",
                "Open",
                "EP1234567B1"
            ]
        }
    )


    # --------------------------------------------------------
    # Styled Example Table
    # --------------------------------------------------------

    styled_table = (
        input_example.style
        .set_table_styles(
            [
                {
                    "selector": "table",
                    "props": [
                        ("width", "100%"),
                        ("border-collapse", "separate"),
                        ("border-spacing", "0"),
                        ("border", "1px solid #D9DEE5"),
                        ("border-radius", "8px"),
                        ("overflow", "hidden"),
                        ("font-size", "0.84rem")
                    ]
                },
                {
                    "selector": "thead th",
                    "props": [
                        ("background-color", "#F3F5F7"),
                        ("color", "#263238"),
                        ("font-weight", "600"),
                        ("text-align", "left"),
                        ("padding", "10px 12px"),
                        ("border-bottom", "1px solid #D9DEE5")
                    ]
                },
                {
                    "selector": "tbody td",
                    "props": [
                        ("padding", "10px 12px"),
                        ("color", "#4F5B66"),
                        ("border-bottom", "1px solid #E6E9ED")
                    ]
                },
                {
                    "selector": "tbody tr:nth-child(even) td",
                    "props": [
                        ("background-color", "#FAFBFC")
                    ]
                },
                {
                    "selector": "tbody tr:nth-child(odd) td",
                    "props": [
                        ("background-color", "#FFFFFF")
                    ]
                },
                {
                    "selector": "tbody tr:last-child td",
                    "props": [
                        ("border-bottom", "none")
                    ]
                }
            ]
        )
        .hide(axis="index")
    )


    st.table(
        styled_table
    )


    st.markdown(
        """
<div class="input-format-note">
<b>PUBLICATION NUMBER</b> is required.
<b>ORBIT LINK</b> is optional and is only required when the workbook
contains Indian patents that need to retain their original Orbit document link.
The visible text in the ORBIT LINK column may be <b>"Open"</b> or the
patent publication number, but the cell must contain the actual Excel hyperlink.
</div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FILE UPLOAD
# ============================================================

st.markdown(
    "### Upload Excel File"
)

uploaded_file = st.file_uploader(
    "Upload your Excel workbook",
    type=["xlsx"],
    label_visibility="collapsed",
    help=(
        "Upload an Excel workbook containing a "
        "PUBLICATION NUMBER column. "
        "ORBIT LINK is optional."
    )
)


# ============================================================
# INPUT OPTIONS
# ============================================================

if uploaded_file is not None:

    try:

        preview_bytes = uploaded_file.getvalue()

        preview_workbook = load_workbook(
            BytesIO(preview_bytes),
            read_only=False,
            keep_links=True
        )

        preview_sheet = preview_workbook.active

        available_columns = []


        for col in range(
            1,
            preview_sheet.max_column + 1
        ):

            value = clean_value(
                preview_sheet.cell(
                    1,
                    col
                ).value
            )

            if value:
                available_columns.append(value)


        preview_workbook.close()


        if not available_columns:

            st.error(
                "No column headers were found in Row 1."
            )

            st.stop()


        # ====================================================
        # COLUMN SELECTION
        # ====================================================

        st.markdown(
            "### Column Selection"
        )

        col1, col2 = st.columns(2)


        # ----------------------------------------------------
        # PUBLICATION NUMBER COLUMN
        # ----------------------------------------------------

        with col1:

            default_patent_index = 0


            for idx, name in enumerate(
                available_columns
            ):

                if normalize_patent_number(
                    name
                ) in [
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


        # ----------------------------------------------------
        # ORBIT LINK COLUMN
        # ----------------------------------------------------

        with col2:

            orbit_options = [
                "None"
            ] + available_columns


            default_orbit_index = 0


            for idx, name in enumerate(
                available_columns,
                start=1
            ):

                normalized_name = (
                    normalize_patent_number(
                        name
                    )
                )


                if normalized_name in [
                    "ORBITLINK",
                    "DOCUMENTLINK",
                    "ORBIT"
                ]:

                    default_orbit_index = idx

                    break


            orbit_column = st.selectbox(
                "Orbit Link Column",
                orbit_options,
                index=default_orbit_index
            )


        # ====================================================
        # ORBIT LINK INFORMATION
        # ====================================================

        if orbit_column == "None":

            st.info(
                "No ORBIT LINK column selected. "
                "This is suitable for lists that do not contain "
                "Indian patents or when Orbit links are not required."
            )


        # ====================================================
        # LINKING MODE
        # ====================================================

        st.markdown(
            "### Linking Mode"
        )


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

            if orbit_column == "None":

                st.info(
                    "Dynamic mode: US → Google Patents | "
                    "IN → Original Orbit Link when available; "
                    "if unavailable → NOT LINKED | "
                    "All other patents → New Espacenet"
                )

            else:

                st.info(
                    "Dynamic mode: US → Google Patents | "
                    "IN → Original Orbit Link | "
                    "if unavailable → NOT LINKED | "
                    "All other patents → New Espacenet"
                )


        elif mode == "Google Patents":

            st.info(
                "All publication numbers will be linked "
                "to Google Patents. No ORBIT LINK column is required."
            )


        else:

            st.info(
                "All publication numbers will be linked "
                "to New Espacenet. No ORBIT LINK column is required."
            )


    except Exception as e:

        st.error(
            f"Unable to read the uploaded Excel file: {e}"
        )

        st.stop()


# ============================================================
# RUN BUTTON
# ============================================================

run_button = st.button(
    "CREATE PATENT HYPERLINKS",
    type="primary",
    use_container_width=True
)


# ============================================================
# RUN
# ============================================================

if run_button:

    if uploaded_file is None:

        st.error(
            "Please upload an Excel workbook first."
        )

        st.stop()


    try:

        with st.spinner(
            "Creating patent hyperlinks..."
        ):

            output_file, stats = process_workbook(
                uploaded_file,
                patent_column,
                orbit_column,
                mode
            )


        st.success(
            f"Completed. "
            f"{stats['linked_rows']:,} patent numbers "
            f"were hyperlinked."
        )


        # ====================================================
        # PROCESSING SUMMARY
        # ====================================================

        st.markdown(
            "### Processing Summary"
        )


        st1, st2, st3, st4 = st.columns(4)


        with st1:

            st.markdown(
                f'<div class="summary-number">'
                f'{stats["total_rows"]:,}'
                f'</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="summary-label">'
                'Patent rows'
                '</div>',
                unsafe_allow_html=True
            )


        with st2:

            st.markdown(
                f'<div class="summary-number">'
                f'{stats["google_count"]:,}'
                f'</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="summary-label">'
                'Google Patents'
                '</div>',
                unsafe_allow_html=True
            )


        with st3:

            st.markdown(
                f'<div class="summary-number">'
                f'{stats["espacenet_count"]:,}'
                f'</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="summary-label">'
                'New Espacenet'
                '</div>',
                unsafe_allow_html=True
            )


        with st4:

            st.markdown(
                f'<div class="summary-number">'
                f'{stats["orbit_count"]:,}'
                f'</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="summary-label">'
                'Original Orbit Links'
                '</div>',
                unsafe_allow_html=True
            )


        # ====================================================
        # WARNINGS
        # ====================================================

        if stats["missing_orbit_count"] > 0:

            st.warning(
                f'{stats["missing_orbit_count"]:,} Indian patent(s) '
                f'could not be hyperlinked because no actual '
                f'ORBIT LINK was available. These are marked '
                f'"NOT LINKED" in the NOT LINKED PATENTS column.'
            )


        if stats["skipped_rows"] > 0:

            st.warning(
                f'{stats["skipped_rows"]:,} row(s) were skipped.'
            )


        # ====================================================
        # DOWNLOAD
        # ====================================================

        st.markdown("---")

        st.markdown(
            "### Download Result"
        )


        original_name = uploaded_file.name


        if original_name.lower().endswith(".xlsx"):

            download_name = (
                original_name[:-5]
                + "_HYPERLINKED.xlsx"
            )

        else:

            download_name = (
                original_name
                + "_HYPERLINKED.xlsx"
            )


        st.download_button(
            label="DOWNLOAD HYPERLINKED EXCEL",
            data=output_file,
            file_name=download_name,
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            ),
            type="primary",
            use_container_width=True
        )


    except Exception as e:

        st.error(
            f"An error occurred while processing "
            f"the workbook: {e}"
        )

        st.exception(e)
